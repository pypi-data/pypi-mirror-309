![test results](https://github.com/kimlab/cf/actions/workflows/test.yml/badge.svg)

# COREFRAME

**COmmon REsearch FRAMEwork** - A Python framework for Earth science research and data analysis.

## Overview

COREFRAME is a specialized Python framework designed for Earth science research, providing robust tools for handling complex multidimensional datasets in atmospheric, oceanic, and climate sciences.

## Features

### CoreArray
- Coordinate-aware array operations based on NumPy
- Intelligent dimension handling
- Seamless integration with NumPy's universal functions
- Support for labeled dimensions and metadata

### HDF5 Integration
- High-level interface for HDF5 files
- Automatic coordinate system management
- Advanced time dimension handling with calendar support
- Comprehensive metadata preservation

### Performance Optimization
- Result caching system for computationally intensive operations
- Parallel processing capabilities with configurable worker pools
- Compressed storage options
- Hash-based cache management

### Data Analysis Tools
- Efficient time-series operations
- Support for various calendar systems
- Area-based spatial calculations
- Geographical coordinate support
- Gridded data handling

## Installation

```bash
pip install coreframe
```

### Requirements
- Python 3.6 or higher
- NumPy
- h5py

## Quick Start

```python
import numpy as np
from coreframe import CoreArray

# Create a sample dataset
data = np.random.rand(500, 100, 100)
time = np.arange('2001-01-01', '2002-05-15', dtype='datetime64[D]')
lat = np.linspace(-90, 90, 100)
lon = np.linspace(-180, 180, 100)

# Create CoreArray with coordinates
coords = {
    'time': time,
    'lat': lat,
    'lon': lon
}
arr = CoreArray(data, coords)

# Perform operations
result = arr.apply_by_time("time", "1M", np.max, axis=0)
```

## Key Use Cases
- Climate data analysis
- Atmospheric science research
- Oceanographic studies
- Earth system modeling
- Geospatial data processing
- Environmental time series analysis

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository.

## Authors

Developed and maintained by the MetaEarth Lab.

---

For more information, please contact: hyungjun@gmail.com