from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools
import numpy as np
from setuptools import setup, find_packages

cpp_extension = [
    Extension(
        "utils.trend", 
        sources=["src/trend.cpp"],
        include_dirs=[np.get_include()],
        language="c++",
        extra_compile_args=["-std=c++11"], 
    ),
    Extension(
        "utils.skew", 
        sources=["src/skew.cpp"],
        include_dirs=[np.get_include()],
        language="c++",
        extra_compile_args=["-std=c++11"], 
    ),
    Extension(
        "utils.kurtosis", 
        sources=["src/kurtosis.cpp"],
        include_dirs=[np.get_include()],
        language="c++",
        extra_compile_args=["-std=c++11"], 
    ),
    Extension(
        "utils.lb", 
        sources=["src/lb.cpp"],
        include_dirs=[np.get_include()],
        language="c++",
        extra_compile_args=["-std=c++11"], 
    ),
    Extension(
        "utils.acf", 
        sources=["src/acf.cpp"],
        include_dirs=[np.get_include()],
        language="c++",
        extra_compile_args=["-std=c++11"], 
    ),
]

# Setup function configuration
setup(
    name="tsdss",
    version="0.1.0",
    author="Hui Wang",
    author_email="huiw1128@gmail.com",
    description="Time Series Description",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wanghui5801/tsdss",
    packages=setuptools.find_packages(),
    ext_modules=cpp_extension,
    cmdclass={"build_ext": build_ext},
    install_requires=[
        'numpy>=1.19.0',
        'pandas>=1.0.0',
        'statsmodels>=0.13.0',
        'matplotlib>=3.0.0',
        'scipy>=1.6.0',
        'scikit-learn>=0.24.0',
    ],
    extras_require={
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'numpy>=1.19.0',
            'pandas>=1.0.0',
            'scipy>=1.6.0',
            'statsmodels>=0.13.0',
            'matplotlib>=3.0.0',
            'scikit-learn>=0.24.0',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
