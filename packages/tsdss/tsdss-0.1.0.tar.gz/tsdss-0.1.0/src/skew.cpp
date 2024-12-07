#include <vector>
#include <cmath>
#include <numeric>
#include <Python.h>
#include <numpy/arrayobject.h>

// Calculate skewness of a time series
static PyObject* calculate_skewness(PyObject* self, PyObject* args) {
    PyArrayObject *input_array;
    
    if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &input_array)) {
        return NULL;
    }

    npy_intp n = PyArray_DIM(input_array, 0);
    double *data = (double*)PyArray_DATA(input_array);

    // Calculate mean
    double mean = 0.0;
    for (npy_intp i = 0; i < n; i++) {
        mean += data[i];
    }
    mean /= n;

    // Calculate second and third moments
    double m2 = 0.0;
    double m3 = 0.0;
    for (npy_intp i = 0; i < n; i++) {
        double dev = data[i] - mean;
        m2 += dev * dev;
        m3 += dev * dev * dev;
    }
    m2 /= n;
    m3 /= n;

    // Calculate skewness
    double skewness = m3 / pow(m2, 1.5);

    return PyFloat_FromDouble(skewness);
}

static PyMethodDef SkewMethods[] = {
    {"skew", calculate_skewness, METH_VARARGS, "Calculate skewness of a time series"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef skewmodule = {
    PyModuleDef_HEAD_INIT,
    "skew",
    NULL,
    -1,
    SkewMethods
};

PyMODINIT_FUNC PyInit_skew(void) {
    import_array();
    return PyModule_Create(&skewmodule);
}

