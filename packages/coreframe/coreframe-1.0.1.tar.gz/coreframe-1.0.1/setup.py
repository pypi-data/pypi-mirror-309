from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.1'
DESCRIPTION = 'COmmon REsearch FRAMEwork'
LONG_DESCRIPTION = '''COREFRAME (COmmon REsearch FRAMEwork) is a powerful Python framework designed specifically for Earth science research and data analysis. It provides a robust foundation for handling complex multidimensional datasets commonly encountered in atmospheric, oceanic, and climate sciences.

Core Features:
- CoreArray: A NumPy-based array implementation with coordinate-aware operations, intelligent dimension handling, and seamless integration with NumPy's universal functions
- HDF5 Integration: High-level interface for HDF5 files with automatic coordinate system management and time dimension handling
- Performance Optimization: Intelligent result caching and parallel processing capabilities
- Advanced Data Analysis: Efficient time-series analysis and spatial calculations

Key Advantages:
- Earth Science Focus: Native support for common data formats and conventions
- Performance: Optimized for large dataset operations with parallel processing and caching
- Usability: Intuitive NumPy-like interface with comprehensive coordinate system support
- Flexibility: Extensible architecture compatible with common scientific Python libraries

Ideal for climate data analysis, atmospheric science research, oceanographic studies, Earth system modeling, and geospatial data processing. Built on NumPy and HDF5, COREFRAME requires Python 3.6+ and provides researchers with a powerful tool for Earth science data analysis and research.

Developed and maintained by the MetaEarth Lab.'''

# Get the absolute path of the directory containing setup.py
here = os.path.abspath(os.path.dirname(__file__))

# Read long description from README.md if it exists
try:
    with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
        LONG_DESCRIPTION = fh.read()
except FileNotFoundError:
    LONG_DESCRIPTION = 'long_description to be written'

setup(
    name='coreframe',
    version=VERSION,
    author="MetaEarth Lab",
    author_email="hyungjun@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['coreframe', 'coreframe.*']),  # This will include all subpackages
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'h5py',
    ],
    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Atmospheric Science"
    ],
    include_package_data=True,
    zip_safe=False,
)