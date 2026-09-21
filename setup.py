#!/usr/bin/env python
from setuptools import setup, Extension, find_namespace_packages

define_macros = [("CYTHON_FREETHREADING_COMPATIBLE", "1")]

try:
    from Cython.Build import cythonize
    from Cython.Compiler import Options

    directives = {}
    if getattr(Options, "directive_types", None) and "freethreading_compatible" in Options.directive_types:
        directives["freethreading_compatible"] = True

    extensions = cythonize(
        [
            Extension(name="pyteomics.cparser", sources=["pyteomics/cparser.pyx"], define_macros=define_macros),
            Extension(name="pyteomics.cmass", sources=["pyteomics/cmass.pyx"], define_macros=define_macros),
        ],
        compiler_directives=directives,
    )
except ImportError:
    extensions = [
        Extension(name="pyteomics.cparser", sources=["pyteomics/cparser.c"], define_macros=define_macros),
        Extension(name="pyteomics.cmass", sources=["pyteomics/cmass.c"], define_macros=define_macros),
    ]


setup(
    name="pyteomics.cythonize",
    description="An Cython-accelerated version of common pyteomics functions",
    long_description=open("README.rst").read(),
    version="0.2.10",
    packages=find_namespace_packages(include=["pyteomics*"]),
    zip_safe=False,
    install_requires=["pyteomics"],
    include_package_data=True,
    ext_modules=extensions,
    maintainer="Joshua Klein",
    maintainer_email="jaklein@bu.edu",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries",
    ],
    license="License :: OSI Approved :: Apache Software License",
    url="https://github.com/mobiusklein/pyteomics.cythonize",
)
