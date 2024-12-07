#include <vector>
#include <cmath>
#include <numeric>
#include <Python.h>
#include <numpy/arrayobject.h>

// Modify function definition to support keyword arguments
static char seasonal_decompose_doc[] = 
    "seasonal_decompose(x, period=12)\n\n"
    "Decompose time series into trend, seasonal, and residual components.\n"
    "\nParameters:\n"
    "    x : array_like\n"
    "        The time series data\n"
    "    period : int, optional (default=12)\n"
    "        The period of the seasonal component\n"
    "\nReturns:\n"
    "    dict\n"
    "        Dictionary containing trend, seasonal, and residual components";

static PyObject* seasonal_decompose(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyArrayObject *input_array;
    int period = 12;  // Default value
    
    // Define keyword argument list
    static char* kwlist[] = {"x", "period", NULL};
    
    // Use PyArg_ParseTupleAndKeywords to parse arguments
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|i", kwlist,
                                    &PyArray_Type, &input_array, &period)) {
        return NULL;
    }

    // Get dimensions and data pointer
    npy_intp n = PyArray_DIM(input_array, 0);
    double *ts = (double*)PyArray_DATA(input_array);
    
    // Allocate arrays for results
    npy_intp dims[1] = {n};
    PyArrayObject *trend_array = (PyArrayObject*)PyArray_SimpleNew(1, dims, NPY_DOUBLE);
    PyArrayObject *seasonal_array = (PyArrayObject*)PyArray_SimpleNew(1, dims, NPY_DOUBLE);
    PyArrayObject *resid_array = (PyArrayObject*)PyArray_SimpleNew(1, dims, NPY_DOUBLE);
    
    double *trend = (double*)PyArray_DATA(trend_array);
    double *seasonal = (double*)PyArray_DATA(seasonal_array);
    double *resid = (double*)PyArray_DATA(resid_array);

    // Initialize arrays
    for (npy_intp i = 0; i < n; i++) {
        trend[i] = 0.0;
        seasonal[i] = 0.0;
        resid[i] = 0.0;
    }

    // Calculate trend using centered moving average
    int half_window = period / 2;
    for (npy_intp i = half_window; i < n - half_window; i++) {
        double sum = 0.0;
        if (period % 2 == 0) {
            for (npy_intp j = -half_window; j < half_window; j++) {
                sum += ts[i + j];
            }
            trend[i] = sum / period;
        } else {
            for (npy_intp j = -half_window; j <= half_window; j++) {
                sum += ts[i + j];
            }
            trend[i] = sum / period;
        }
    }

    // Calculate detrended series and seasonal component
    std::vector<double> detrended(n);
    std::vector<double> seasonal_avg(period, 0.0);
    std::vector<int> count(period, 0);
    
    for (npy_intp i = half_window; i < n - half_window; i++) {
        detrended[i] = ts[i] - trend[i];
        int season_idx = i % period;
        seasonal_avg[season_idx] += detrended[i];
        count[season_idx]++;
    }

    // Calculate average seasonal pattern
    for (int i = 0; i < period; i++) {
        if (count[i] > 0) {
            seasonal_avg[i] /= count[i];
        }
    }

    // Replicate seasonal pattern
    for (npy_intp i = 0; i < n; i++) {
        seasonal[i] = seasonal_avg[i % period];
    }

    // Calculate residuals
    for (npy_intp i = half_window; i < n - half_window; i++) {
        resid[i] = ts[i] - trend[i] - seasonal[i];
    }

    // Create return dictionary
    PyObject *result_dict = PyDict_New();
    PyDict_SetItemString(result_dict, "trend", (PyObject*)trend_array);
    PyDict_SetItemString(result_dict, "seasonal", (PyObject*)seasonal_array);
    PyDict_SetItemString(result_dict, "resid", (PyObject*)resid_array);
    
    Py_DECREF(trend_array);
    Py_DECREF(seasonal_array);
    Py_DECREF(resid_array);
    
    return result_dict;
}

// Modify method table to support keyword arguments
static PyMethodDef TrendMethods[] = {
    {"decompose", (PyCFunction)seasonal_decompose, 
     METH_VARARGS | METH_KEYWORDS,  // Add METH_KEYWORDS flag
     seasonal_decompose_doc},  // Add documentation string
    {NULL, NULL, 0, NULL}
};

// Module structure definition remains unchanged
static struct PyModuleDef trendmodule = {
    PyModuleDef_HEAD_INIT,
    "trend",
    NULL,
    -1,
    TrendMethods
};

// Initialization function remains unchanged
PyMODINIT_FUNC PyInit_trend(void) {
    import_array();
    return PyModule_Create(&trendmodule);
}


