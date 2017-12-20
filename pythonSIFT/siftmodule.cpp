
#include <Python.h>
#include <vector>
#include <SiftGPU.hpp>
#include <stdio.h>
#include <stdlib.h>

static PyObject *SiftError;

SiftGPU _global_sift;


static PyObject * sift_init(PyObject *self, PyObject *args) {

	const char * s_argv[] = {"-v", "1",  "-fo", "0", "-da", "-tc2", "7680", "-nomc"};
	int s_argc = sizeof(s_argv)/sizeof(char*);

	printf("Hello from sift_create!\n");

	_global_sift.ParseParam(s_argc, (char **)s_argv);

	int support = _global_sift.CreateContextGL();

	if (support != SiftGPU::SIFTGPU_FULL_SUPPORTED) {
		printf("support: %d\n", support);
		return PyLong_FromLong(-1);
	}

	return PyLong_FromLong(123456);
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

	return PyLong_FromLong(retval);
}


static PyObject * sift_SaveSIFT(PyObject *self, PyObject *args) {
	const char *filename;

	if (!PyArg_ParseTuple(args, "s", &filename)) {
		return NULL;
	}

	_global_sift.SaveSIFT(filename);

	return PyLong_FromLong(0);
}


static PyMethodDef SiftMethods[] = {
	{"create", sift_create, METH_VARARGS, "Create a SiftGPU instance"},
	{"RunSIFT", sift_RunSIFT, METH_VARARGS, "Run the SIFT feature detector"},
	{"SaveSIFT", sift_SaveSIFT, METH_VARARGS, "Save the SIFT features"},
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

