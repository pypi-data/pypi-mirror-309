#include <vector>
#include <cmath>
#include <numeric>
#include <Python.h>
#include <numpy/arrayobject.h>

// Calculate kurtosis of a time series
static PyObject* calculate_kurtosis(PyObject* self, PyObject* args) {
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

    // Calculate second and fourth moments
    double m2 = 0.0;
    double m4 = 0.0;
    for (npy_intp i = 0; i < n; i++) {
        double dev = data[i] - mean;
        double dev2 = dev * dev;
        m2 += dev2;
        m4 += dev2 * dev2;
    }
    m2 /= n;
    m4 /= n;

    // Calculate kurtosis (using Fisher's definition: normal = 0.0)
    double kurtosis = (m4 / (m2 * m2)) - 3.0;

    return PyFloat_FromDouble(kurtosis);
}

static PyMethodDef KurtosisMethods[] = {
    {"kurtosis", calculate_kurtosis, METH_VARARGS, "Calculate kurtosis of a time series"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef kurtosismodule = {
    PyModuleDef_HEAD_INIT,
    "kurtosis",
    NULL,
    -1,
    KurtosisMethods
};

PyMODINIT_FUNC PyInit_kurtosis(void) {
    import_array();
    return PyModule_Create(&kurtosismodule);
}
