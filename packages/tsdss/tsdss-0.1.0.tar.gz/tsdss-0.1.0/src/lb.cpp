#include <vector>
#include <cmath>
#include <numeric>
#include <Python.h>
#include <numpy/arrayobject.h>

// Calculate Ljung-Box test statistic and p-value
static PyObject* calculate_lb(PyObject* self, PyObject* args) {
    PyArrayObject *input_array;
    int max_lag = 10;
    
    if (!PyArg_ParseTuple(args, "O!|i", &PyArray_Type, &input_array, &max_lag)) {
        return NULL;
    }

    npy_intp n = PyArray_DIM(input_array, 0);
    
    // Input validation
    if (max_lag <= 0) {
        PyErr_SetString(PyExc_ValueError, "max_lag must be positive");
        return NULL;
    }
    if (max_lag >= n) {
        PyErr_SetString(PyExc_ValueError, "max_lag must be less than series length");
        return NULL;
    }
    if (n < 3) {
        PyErr_SetString(PyExc_ValueError, "Series length must be at least 3");
        return NULL;
    }

    double *data = (double*)PyArray_DATA(input_array);

    // Calculate mean
    double mean = 0.0;
    for (npy_intp i = 0; i < n; i++) {
        mean += data[i];
    }
    mean /= n;

    // Calculate variance
    double variance = 0.0;
    for (npy_intp i = 0; i < n; i++) {
        double dev = data[i] - mean;
        variance += dev * dev;
    }
    variance /= n;  // Note: Calculate actual variance

    // Check for zero variance
    if (variance < 1e-10) {
        PyErr_SetString(PyExc_ValueError, "Series has zero variance");
        return NULL;
    }

    // Calculate autocorrelations
    std::vector<double> acf(max_lag + 1);
    for (int k = 1; k <= max_lag; k++) {
        double numerator = 0.0;
        double denominator = 0.0;
        
        // Note: Calculate numerator and denominator separately
        for (npy_intp i = k; i < n; i++) {
            double dev_t = data[i] - mean;
            double dev_tk = data[i-k] - mean;
            numerator += dev_t * dev_tk;
        }
        
        // Note: Calculate autocorrelation coefficient
        for (npy_intp i = 0; i < n; i++) {
            double dev = data[i] - mean;
            denominator += dev * dev;
        }
        
        acf[k] = numerator / denominator;  // Note: Use sum of squares directly as denominator
    }

    // Calculate Ljung-Box statistic
    double lb_stat = 0.0;
    for (int k = 1; k <= max_lag; k++) {
        lb_stat += (acf[k] * acf[k]) / (n - k);
    }
    lb_stat = n * (n + 2) * lb_stat;

    // Calculate p-value (rest of the code remains the same)
    double p;
    if (lb_stat < 0) {
        p = 1.0;
    } else {
        double x = lb_stat;
        double df = max_lag;
        
        // Use more stable numerical computation method
        double a = df / 2.0;
        double y = x / 2.0;
        
        if (y <= a + 1) {
            // Use series expansion
            double term = exp(a * log(y) - y - lgamma(a + 1));
            double sum = term;
            for (int i = 1; i < 1000; i++) {
                term *= y / (a + i);
                sum += term;
                if (term < 1e-10 * sum) break;
            }
            p = 1.0 - sum;
        } else {
            // Use Continued Fraction expansion
            double an, b, c, d, del;
            b = y + 1 - a;
            c = 1.0 / 1e-30;
            d = 1.0 / b;
            p = d;
            
            for (int i = 1; i <= 100; i++) {
                an = -i * (i - a);
                b += 2.0;
                d = b + an * d;
                if (fabs(d) < 1e-30) d = 1e-30;
                c = b + an / c;
                if (fabs(c) < 1e-30) c = 1e-30;
                d = 1.0 / d;
                del = d * c;
                p *= del;
                if (fabs(del - 1.0) < 1e-8) break;
            }
            
            p = exp(a * log(y) - y - lgamma(a)) * p;
        }
        
        // Ensure p-value is within valid range
        if (p > 1.0) p = 1.0;
        if (p < 0.0) p = 0.0;
    }

    // Create and return tuple with (statistic, p-value)
    PyObject* result = PyTuple_New(2);
    PyTuple_SetItem(result, 0, PyFloat_FromDouble(lb_stat));
    PyTuple_SetItem(result, 1, PyFloat_FromDouble(p));
    
    return result;
}

static PyMethodDef LBMethods[] = {
    {"lb", calculate_lb, METH_VARARGS, "Calculate Ljung-Box test statistic and p-value. Args: array, max_lag=10"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef lbmodule = {
    PyModuleDef_HEAD_INIT,
    "lb",
    NULL,
    -1,
    LBMethods
};

PyMODINIT_FUNC PyInit_lb(void) {
    import_array();
    return PyModule_Create(&lbmodule);
}
