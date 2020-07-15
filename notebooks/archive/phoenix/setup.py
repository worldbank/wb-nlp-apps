import os

from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    # Extension(
    #     "phoenix.cythonized.cython_skipgrams",
    #     ["phoenix/cythonized/cython_skipgrams.pyx"],
    #     include_dirs=[np.get_include()]
    # ),
]

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md"), encoding="utf-8").read()

requires = []

setup(
    name="phoenix",
    version="0.0",
    description="phoenix",
    long_description=README,
    classifiers=["Programming Language :: Python"],
    author="Aivin V. Solatorio",
    author_email="asolatorio@worldbank.org",
    url="",
    keywords="NLP data mining modelling word2vec",
    packages=find_packages(),
    include_package_data=True,
    package_data={"phoenix": ["standard_logging.ini"]},
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    ext_modules = cythonize(extensions)
)
