
#include <Python.h>
#include <numpy/arrayobject.h>
#include <vector>
#include <SiftGPU.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <GL/glew.h>

using std::vector;

static PyObject *SiftError;

SiftGPU _global_sift;


static PyObject * sift_init(PyObject *self, PyObject *args) {

	const char * s_argv[] = {"-v", "1",  "-fo", "0", "-da", "-tc2", "7680", "-nomc"};
	//const char * s_argv[] = {"-v", "1",  "-fo", "0", "-tc2", "7680", "-nomc"};
	int s_argc = sizeof(s_argv)/sizeof(char*);

	//printf("Hello from sift_init!\n");

	_global_sift.ParseParam(s_argc, (char **)s_argv);

	int support = _global_sift.CreateContextGL();

	if (support != SiftGPU::SIFTGPU_FULL_SUPPORTED) {
		printf("support: %d\n", support);
		return PyLong_FromLong(-1);
	}

	return Py_None;
}


static PyObject * sift_RunSIFT_on_file(PyObject *self, PyObject *args) {
	int retval;
	const char *filename;

	if (!PyArg_ParseTuple(args, "s", &filename)) {
		return NULL;
	}

	retval = _global_sift.RunSIFT(filename);
	if (!retval) {
		PyErr_SetString(SiftError, "RunSIFT() failed.");
		return NULL;
	}

	return Py_None;
}


static PyObject * sift_RunSIFT(PyObject *self, PyObject *args) {
	int width;
	int height;
	const char *data;
	int data_len;
	int retval;

	if (!PyArg_ParseTuple(args, "iiy#", &width, &height, &data, &data_len)) {
		return NULL;
	}

	// Internally, the SiftGPU library only works on grayscale images (no alpha).
	// So I will leave it to Python to provide a simple grayscale.  (The original
	// sensor data is in YUYV format, so it's trivial to pull the grayscale.)

	if (data_len != (width * height)) {
		PyErr_SetString(SiftError, "Data length doesn't match image dimensions");
		return NULL;
	}

	// defines are in GL/glew.h
	retval = _global_sift.RunSIFT(width, height, data, GL_LUMINANCE, GL_UNSIGNED_BYTE);

	if (!retval) {
		PyErr_SetString(SiftError, "RunSIFT() failed.");
		return NULL;
	}

	return Py_None;
}

PyDoc_STRVAR (
	RunSIFT__doc__,
	"RunSIFT(width, height, image_pixel_data) -> None\n"
	"\n"
	"Parameters\n"
	"----------\n"
	"width : int\n"
	"height : int\n"
	"image_pixel_data : bytes\n"
	"    The image is 8-bit grayscale (unsigned char[] in C)\n"
	"\n"
	"Returns\n"
	"-------\n"
	"None.  Results are stored in the global sift object.  Use\n"
	"    sift.GetFeatureVector() or sift.SaveSIFT() to get the results.\n"
);


static PyObject * sift_SaveSIFT(PyObject *self, PyObject *args) {
	const char *filename;

	if (!PyArg_ParseTuple(args, "s", &filename)) {
		return NULL;
	}

	_global_sift.SaveSIFT(filename);

	return Py_None;
}



static PyObject * sift_GetFeatureVector(PyObject *self, PyObject *args) {

	int i, j;
	int numFeatures;

	double value;

	if (!PyArg_ParseTuple(args, "")) {
		return NULL;
	}

	vector<float> descriptors(1);
	// reminder:
	// a SiftKeypoint is:  struct {float x,y,s,o;};
	//    for x, y, scale, orientation
	vector<SiftGPU::SiftKeypoint> keys(1);

	printf("sizeof(float): %lu\n", sizeof(float));

	numFeatures = _global_sift.GetFeatureNum();
	printf("numFeatures: %d\n", numFeatures);


	// Allocate memory
	keys.resize(numFeatures);
	descriptors.resize(128 * numFeatures);

	_global_sift.GetFeatureVector(&keys[0], &descriptors[0]);

	// Convert keys and descriptors into something useful we can give back to Python

	npy_intp dims[2] = {numFeatures, 4};
	PyObject *np_keys = PyArray_SimpleNew(2, dims, NPY_FLOAT);

	dims[1] = 128;
	PyObject *np_descriptors = PyArray_SimpleNew(2, dims, NPY_UINT8);

	for (i = 0; i<numFeatures; ++i) {

		void* itemptr;

		itemptr = PyArray_GETPTR2(np_keys, i, 0);
		PyArray_SETITEM(np_keys, itemptr, PyFloat_FromDouble((double) keys[i].x));
		itemptr = PyArray_GETPTR2(np_keys, i, 1);
		PyArray_SETITEM(np_keys, itemptr, PyFloat_FromDouble((double) keys[i].y));
		itemptr = PyArray_GETPTR2(np_keys, i, 2);
		PyArray_SETITEM(np_keys, itemptr, PyFloat_FromDouble((double) keys[i].s));
		itemptr = PyArray_GETPTR2(np_keys, i, 3);
		PyArray_SETITEM(np_keys, itemptr, PyFloat_FromDouble((double) keys[i].o));

		for (j=0; j<128; ++j) {
			value = (double) (descriptors[i*128 + j] * 512.0 + 0.5);

			itemptr = PyArray_GETPTR2(np_descriptors, i, j);
			PyArray_SETITEM(np_descriptors, itemptr, PyLong_FromDouble(value));
		}
	}

	return Py_BuildValue("OO", np_keys, np_descriptors);
}

PyDoc_STRVAR (
	GetFeatureVector__doc__,
	"GetFeatureFector() -> keys, descriptors\n"
	"\n"
	"Parameters\n"
	"----------\n"
	"None\n"
	"\n"
	"Returns\n"
	"-------\n"
	"keys, descriptors : ndarray, ndarray\n"
	"    keys: 2-D array (floats), shape:  (number_of_features, 4)\n"
	"    descriptors: 2-D array (uint8), shape:  (number_of_features, 128)\n"
	"        a key is:  x, y, scale, orientation\n"
	"        each descriptor is a SIFT descriptor times 512, plus 0.5, cast to uint8\n"
	"          ie:  desc = int(desc * 512 + 0.5)\n"
);


static PyMethodDef SiftMethods[] = {
	{"init", sift_init, METH_VARARGS, "Create a SiftGPU instance"},
	{"RunSIFT_on_file", sift_RunSIFT_on_file, METH_VARARGS, "Run the SIFT feature detector"},
	{"RunSIFT", sift_RunSIFT, METH_VARARGS, RunSIFT__doc__},
	{"SaveSIFT", sift_SaveSIFT, METH_VARARGS, "Save the SIFT features as an ascii file"},
	{"GetFeatureVector", sift_GetFeatureVector, METH_VARARGS, GetFeatureVector__doc__},
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef siftmodule = {
	PyModuleDef_HEAD_INIT,
	"sift",
	NULL,  // TODO:  put docs here
	-1,
	SiftMethods
};


PyMODINIT_FUNC PyInit_sift(void) {
	PyObject *m;

	m = PyModule_Create(&siftmodule);
	if (m == NULL) {
		return NULL;
	}

	import_array();  // TODO:  Is this where this is supposed to go??  It solves a segfault...

	SiftError = PyErr_NewException("sift.error", NULL, NULL);
	Py_INCREF(SiftError);
	PyModule_AddObject(m, "error", SiftError);

	return m;
}

