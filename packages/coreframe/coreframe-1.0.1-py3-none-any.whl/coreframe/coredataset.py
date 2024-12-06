from coreframe import CoreArray
import h5py
import numpy as np
import tempfile
import os

def open_dataset(file_path):
    """
    Open an HDF5 file as a CoreDataset.

    Args:
        file_path (str): Path to the HDF5 file.

    Returns:
        CoreDataset: A dataset object providing access to the file's variables and metadata.
    """
    return CoreDataset(file_path)

def decode_if_bytes(value):
    """
    Decode byte strings to UTF-8 and clean up path-like strings.

    Args:
        value (bytes or str): Value to decode. If bytes, decodes to UTF-8.
            If string starting with '/', removes leading slash.

    Returns:
        str: Decoded and cleaned string value.
    """
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    if isinstance(value, str) and value.startswith('/'):
        value = value.lstrip('/')
    return value

def num2date(times, units, calendar='standard'):
    """
    Convert numerical time values to numpy datetime64 objects.

    Args:
        times (numpy.ndarray): Array of numerical time values.
        units (str): String specifying the time units and reference date,
            e.g., "days since 1970-01-01 00:00:00".
        calendar (str, optional): Calendar system used. Defaults to 'standard'.

    Returns:
        numpy.ndarray: Array of numpy.datetime64 objects.

    Raises:
        ValueError: If the units string format is invalid or time unit is unsupported.

    Note:
        Supported time units are: days, hours, minutes, seconds.
    """
    # Decode units if it's bytes
    units = decode_if_bytes(units)
    calendar = decode_if_bytes(calendar)
    
    # Parse the units string
    unit_parts = units.split()
    if len(unit_parts) != 4 or unit_parts[1] != 'since':
        raise ValueError(f"Invalid units string: {units}")

    time_unit, _, base_date_str, base_time_str = unit_parts

    # Parse the base date and time
    base_datetime = np.datetime64(f"{base_date_str}T{base_time_str}")

    # Convert times to timedelta objects
    if time_unit == 'days':
        deltas = times.astype('timedelta64[D]')
    elif time_unit == 'hours':
        deltas = times.astype('timedelta64[h]')
    elif time_unit == 'minutes':
        deltas = times.astype('timedelta64[m]')
    elif time_unit == 'seconds':
        deltas = times.astype('timedelta64[s]')
    else:
        raise ValueError(f"Unsupported time unit: {time_unit}")

    # Add the deltas to the base date
    dates = base_datetime + deltas

    return dates

class CoreVariable:
    """
    A wrapper class for HDF5 dataset variables providing enhanced functionality.

    This class provides a high-level interface to access and manipulate variables
    within an HDF5 dataset, including coordinate handling and dimension management.

    Attributes:
        variable (h5py.Dataset): The underlying HDF5 dataset.
        dataset (h5py.File): The parent HDF5 file object.
        dims (list): List of dimension names for the variable.
        coords (dict): Dictionary mapping dimension names to coordinate arrays.
    """
    def __init__(self, variable, dataset):
        """
        Initialize a CoreVariable instance.

        Args:
            variable (h5py.Dataset): The HDF5 dataset to wrap.
            dataset (h5py.File): The parent HDF5 file object.
        """
        self.variable = variable
        self.dataset = dataset
        self.dims = self._get_dimensions()
        self.coords = {}

    def _get_dimensions(self):
        """
        Extract dimension information from the variable.

        Returns:
            list: List of dimension names. If dimensions are not explicitly named,
                generates names in the format 'dim_0', 'dim_1', etc.
        """
        dims = []
        if hasattr(self.variable, 'dims'):
            for i, dim in enumerate(self.variable.dims):
                if isinstance(dim, str):
                    dims.append(dim)
                elif hasattr(dim, 'keys') and len(dim.keys()) > 0:
                    dims.append(list(dim.keys())[0])
                else:
                    dims.append(f'dim_{i}')
        else:
            # If the variable doesn't have dims attribute, use generic dimension names
            dims = [f'dim_{i}' for i in range(len(self.variable.shape))]
        return dims

    def __getitem__(self, key):
        """
        Get data from the variable using array-like indexing.

        Args:
            key (int, slice, tuple): Index or slice specifying the data to retrieve.

        Returns:
            CoreArray: A CoreArray containing the requested data and associated coordinates.
        """
        if not self.dims:
            # If there are no dimensions, just return the data as a CoreArray
            return CoreArray(self.variable[key], coords={})

        coords = {}
        for i, dim_name in enumerate(self.dims):
            if dim_name in self.coords and self.coords[dim_name] is not None:
                if isinstance(key, (slice, int)):
                    coord_key = key if i == 0 else slice(None)
                elif isinstance(key, tuple):
                    coord_key = key[i] if i < len(key) else slice(None)
                else:
                    coord_key = slice(None)
                coords[dim_name] = self.coords[dim_name][coord_key]

        data = self.variable[key]
        result = CoreArray(data, coords=coords)
        return result

    def __repr__(self):
        return f"<CoreVariable: name='{decode_if_bytes(self.variable.name)}', shape={self.variable.shape}, dtype={self.variable.dtype}, dims={self.dims}, coords={list(self.coords.keys())}>"

    def __str__(self):
        var_info = f"CoreVariable: {decode_if_bytes(self.variable.name)}\n"
        var_info += f"  shape: {self.variable.shape}\n"
        var_info += f"  dtype: {self.variable.dtype}\n"
        var_info += f"  dimensions: {self.dims}\n"
        var_info += f"  coordinates: {list(self.coords.keys())}\n"

        var_info += "  attributes:\n"
        for attr, value in self.variable.attrs.items():
            var_info += f"    {decode_if_bytes(attr)}: {decode_if_bytes(value)}\n"

        return var_info

class CoreDataset:
    """
    A high-level interface for working with HDF5 datasets.

    This class provides a convenient way to access and manipulate HDF5 files,
    handling coordinate systems, time dimensions, and metadata.

    Attributes:
        file_path (str): Path to the HDF5 file.
        is_virtual (bool): Whether the file is a temporary virtual file.
        variables (dict): Dictionary of CoreVariable objects.
        attributes (dict): Dataset-level attributes.
        coords (dict): Dictionary of coordinate arrays.

    Note:
        Time dimensions are automatically converted to numpy.datetime64 objects
        if the appropriate units and calendar attributes are present.
    """
    def __init__(self, file_path, is_virtual=False):
        """
        Initialize a CoreDataset instance.

        Args:
            file_path (str): Path to the HDF5 file.
            is_virtual (bool, optional): Whether the file is temporary. Defaults to False.

        Note:
            During initialization, the following operations are performed:
            1. Opens the HDF5 file in read-only mode
            2. Creates CoreVariable objects for each dataset
            3. Extracts coordinate variables
            4. Converts time dimensions if present
            5. Assigns coordinates to variables
        """
        self.file_path = file_path
        self.is_virtual = is_virtual
        self._dataset = h5py.File(self.file_path, 'r')
        self.variables = {}
        self.attributes = {decode_if_bytes(k): decode_if_bytes(v) for k, v in self._dataset.attrs.items()}
        self.coords = {}

        for var_name, var in self._dataset.items():
            if isinstance(var, h5py.Dataset):
                var_name = decode_if_bytes(var_name)
                core_var = CoreVariable(var, self._dataset)
                self.variables[var_name] = core_var
                if len(core_var.dims) == 1:
                    self.coords[var_name] = var[:]

        # Convert time dimension if present
        self._convert_time_dimension()

        # Assign coordinates to variables
        for var_name, var in self.variables.items():
            var.coords = {dim: self.coords.get(dim, None) for dim in var.dims}

    def _convert_time_dimension(self):
        """
        Convert time dimension to numpy.datetime64 objects if present.

        This method looks for variables with 'units' and 'calendar' attributes,
        and converts their values from numerical representations to datetime objects.

        Note:
            The conversion is done in-place, modifying both the coordinate dictionary
            and the corresponding variable's coordinates.
        """
        time_dim = None
        time_units = None
        time_calendar = None

        # Find the time dimension
        for var_name, var in self.variables.items():
            if 'units' in var.variable.attrs and 'calendar' in var.variable.attrs:
                time_dim = var_name
                time_units = decode_if_bytes(var.variable.attrs['units'])
                time_calendar = decode_if_bytes(var.variable.attrs['calendar'])
                break

        # Convert time dimension if present
        if time_dim is not None and time_dim in self.coords:
            converted_time = num2date(self.coords[time_dim], time_units, time_calendar)
            self.coords[time_dim] = converted_time
            self.variables[time_dim].coords[time_dim] = converted_time

    def __getitem__(self, variable_name):
        """
        Get a variable from the dataset by name.

        Args:
            variable_name (str): Name of the variable to retrieve.

        Returns:
            CoreVariable: The requested variable.

        Raises:
            KeyError: If the variable name is not found in the dataset.
        """
        if variable_name not in self.variables:
            raise KeyError(f"Variable '{variable_name}' not found in the dataset.")
        return self.variables[variable_name]

    def close(self):
        """
        Close the dataset and clean up resources.

        If the dataset is virtual (temporary), the file is also deleted.
        """
        self._dataset.close()
        if self.is_virtual:
            os.unlink(self.file_path)  # Remove the temporary virtual file

    def __repr__(self):
        return f"<CoreDataset: file_path='{self.file_path}', is_virtual={self.is_virtual}>"

    def __str__(self):
        dataset_info = f"CoreDataset: {self.file_path}\n"
        dataset_info += f"  variables:\n"
        for var_name, var in self.variables.items():
            dataset_info += f"    {var_name}: {var.dims}\n"
        dataset_info += "  coordinates:\n"
        for coord_name, coord in self.coords.items():
            dataset_info += f"    {coord_name}: {coord.shape}\n"
        dataset_info += "  attributes:\n"
        for attr, value in self.attributes.items():
            dataset_info += f"    {attr}: {value}\n"
        return dataset_info