#include <Python.h>
#include <numpy/arrayobject.h>
#include <vector>
#include <cmath>

// Function to calculate autocorrelation
std::vector<double> acf(const std::vector<double>& ts, int nlags) {
    int n = ts.size();
    std::vector<double> acf_values(nlags + 1, 0.0);
    double mean = 0.0;
    for (int i = 0; i < n; ++i) {
        mean += ts[i];
    }
    mean /= n;

    double c0 = 0.0;
    for (int i = 0; i < n; ++i) {
        c0 += (ts[i] - mean) * (ts[i] - mean);
    }

    for (int lag = 0; lag <= nlags; ++lag) {
        double c = 0.0;
        for (int i = 0; i < n - lag; ++i) {
            c += (ts[i] - mean) * (ts[i + lag] - mean);
        }
        acf_values[lag] = c / c0;
    }

    return acf_values;
}

static PyObject* wrap_acf(PyObject* self, PyObject* args) {
    PyObject* input_array;
    int nlags;

    if (!PyArg_ParseTuple(args, "Oi", &input_array, &nlags)) {
        return NULL;
    }

    PyArrayObject* arr = (PyArrayObject*)PyArray_FROM_OTF(input_array, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (arr == NULL) {
        return NULL;
    }

    npy_intp n = PyArray_SIZE(arr);
    double* data = (double*)PyArray_DATA(arr);

    std::vector<double> ts(data, data + n);
    std::vector<double> acf_result = acf(ts, nlags);

    PyObject* result_list = PyList_New(nlags + 1);
    for (int i = 0; i <= nlags; ++i) {
        PyList_SetItem(result_list, i, PyFloat_FromDouble(acf_result[i]));
    }

    Py_DECREF(arr);
    return result_list;
}

static PyMethodDef AcfMethods[] = {
    {"acf", wrap_acf, METH_VARARGS, "Calculate autocorrelation function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef acfmodule = {
    PyModuleDef_HEAD_INIT,
    "acf",
    NULL,
    -1,
    AcfMethods
};

PyMODINIT_FUNC PyInit_acf(void) {
    import_array();
    return PyModule_Create(&acfmodule);
}


