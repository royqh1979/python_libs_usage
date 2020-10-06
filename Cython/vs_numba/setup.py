from distutils.core import Extension,setup
from Cython.Build import cythonize
import numpy
ext_modules = [
    Extension(
        "julia",
        ["julia.pyx"],
        include_dirs=[numpy.get_include()],
    )
]

setup(
    ext_modules=cythonize(ext_modules)
)