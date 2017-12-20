
#include <Python.h>
#include <vector>
#include <SiftGPU.hpp>
#include <stdio.h>
#include <stdlib.h>

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


static PyObject * sift_RunSIFT(PyObject *self, PyObject *args) {
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


static PyObject * sift_SaveSIFT(PyObject *self, PyObject *args) {
	const char *filename;

	if (!PyArg_ParseTuple(args, "s", &filename)) {
		return NULL;
	}

	_global_sift.SaveSIFT(filename);

	return Py_None;
}



static PyObject * sift_GetFeatureVector(PyObject *self, PyObject *args) {

	unsigned int i, j;
	unsigned int offset;

	double value;

	int numFeatures;
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
	PyObject* py_keyList = PyList_New(numFeatures * 4);
	if (!py_keyList) {
		PyErr_SetString(SiftError, "Failed to allocate memory for Python list");
		return NULL;
	}

	PyObject* py_descList = PyList_New(numFeatures * 128);
	if (!py_descList) {
		PyErr_SetString(SiftError, "Failed to allocate memory for Python list");
		return NULL;
	}


	for (i = 0; i<numFeatures; ++i) {
		offset = 4 * i;
		PyList_SET_ITEM(py_keyList, offset, PyFloat_FromDouble((double) keys[i].x));
		PyList_SET_ITEM(py_keyList, offset+1, PyFloat_FromDouble((double) keys[i].y));
		PyList_SET_ITEM(py_keyList, offset+2, PyFloat_FromDouble((double) keys[i].s));
		PyList_SET_ITEM(py_keyList, offset+3, PyFloat_FromDouble((double) keys[i].o));

		offset = 128 * i;
		for (j=0; j<128; ++j) {
			value = (double) (descriptors[i*128 + j] * 512.0 + 0.5);

			PyList_SET_ITEM(py_descList, offset+j, PyFloat_FromDouble(value));
		}
	}

	return Py_BuildValue("OO", py_keyList, py_descList);
}


static PyMethodDef SiftMethods[] = {
	{"init", sift_init, METH_VARARGS, "Create a SiftGPU instance"},
	{"RunSIFT", sift_RunSIFT, METH_VARARGS, "Run the SIFT feature detector"},
	{"SaveSIFT", sift_SaveSIFT, METH_VARARGS, "Save the SIFT features as an ascii file"},
	{"GetFeatureVector", sift_GetFeatureVector, METH_VARARGS, "Get the SIFT features as binary vector"},
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

	SiftError = PyErr_NewException("sift.error", NULL, NULL);
	Py_INCREF(SiftError);
	PyModule_AddObject(m, "error", SiftError);

	return m;
}

