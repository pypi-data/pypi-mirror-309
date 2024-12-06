import os
import functools
import pickle
import gzip
import hashlib
import numpy as np
from .corearray import CoreArray

class CoreArrayPickler:
    """
    Helper class for serializing and deserializing CoreArray objects.
    
    This class provides static methods to properly handle the pickling and unpickling
    of CoreArray objects while preserving both their numerical data and coordinate metadata.
    """   
    @staticmethod
    def dump(obj, file):
        """
        Serialize a CoreArray object or regular Python object to a file.

        Args:
            obj (CoreArray or any): Object to be serialized. Special handling is provided
                for CoreArray objects to preserve their metadata.
            file (file object): A file-like object opened in binary write mode.

        Note:
            For CoreArray objects, both the underlying array data and coordinates are saved.
            For other objects, standard pickle serialization is used.
        """
        if isinstance(obj, CoreArray):
            # Save both the array data and metadata
            pickle.dump({
                'array': obj.__array__(),
                'coords': obj.coords,
                'is_corearray': True
            }, file)
        else:
            pickle.dump({'is_corearray': False, 'data': obj}, file)
    
    @staticmethod
    def load(file):
        """
        Deserialize an object from a file, with special handling for CoreArray objects.

        Args:
            file (file object): A file-like object opened in binary read mode.

        Returns:
            CoreArray or any: The deserialized object. If the original object was a CoreArray,
                returns a reconstructed CoreArray with preserved data and coordinates.
        """
        data = pickle.load(file)
        if data.get('is_corearray', False):
            # Reconstruct CoreArray object
            arr = CoreArray(data['array'], data['coords'])
            return arr
        return data['data']

def array_to_string(arr, hash_length):
    """
    Convert an array or value to a string representation for cache key generation.

    This function creates a unique string identifier for different types of inputs,
    with special handling for numpy arrays and CoreArray objects.

    Args:
        arr (numpy.ndarray, CoreArray, or any): The input to convert to a string.
            Special handling is provided for numpy arrays and CoreArray objects.
        hash_length (int): Number of characters to use from the MD5 hash for array inputs.

    Returns:
        str: A string representation of the input, suitable for use in cache keys.
            - For CoreArray: "CoreArray_<truncated_md5>"
            - For numpy.ndarray: "nparray_<truncated_md5>"
            - For other types: str(value)
    """
    if isinstance(arr, np.ndarray):
        if isinstance(arr, CoreArray):
            array_bytes = pickle.dumps((arr.__array__(), arr.coords))
            md5_hash = hashlib.md5(array_bytes).hexdigest()
            return f"CoreArray_{md5_hash[:hash_length]}"
        else:
            array_bytes = pickle.dumps(arr)
            md5_hash = hashlib.md5(array_bytes).hexdigest()
            return f"nparray_{md5_hash[:hash_length]}"
    return str(arr)

def cache_result(cache_folder, compress=True, hash_length=8):
    """
    Decorator for caching function results with special handling for CoreArray objects.

    This decorator caches function results to disk, with intelligent handling of
    CoreArray objects and numpy arrays. It generates cache keys based on function
    name, arguments, and their contents.

    Args:
        cache_folder (str): Directory path where cached results will be stored.
        compress (bool, optional): Whether to compress cached files using gzip.
            Defaults to True.
        hash_length (int, optional): Length of hash to use in cache keys for array
            inputs. Defaults to 8.

    Returns:
        callable: A decorated function that implements caching behavior.

    Example:
        >>> @cache_result("./cache")
        ... def expensive_computation(data):
        ...     # Complex calculations here
        ...     return result

    Notes:
        - Cache keys are generated based on:
            * Function name
            * String representations of all arguments
            * For arrays, a truncated MD5 hash of their contents
        - Files are saved as .pkl or .pkl.gz (if compressed)
        - CoreArray objects are properly serialized with their coordinates
        - Cache hits and misses are logged to stdout
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key_parts = [func.__name__]
            for arg in args:
                cache_key_parts.append(array_to_string(arg, hash_length))
            for k, v in sorted(kwargs.items()):
                cache_key_parts.append(f"{k}_{array_to_string(v, hash_length)}")
            
            cache_key = "_".join(cache_key_parts)
            cache_filename = f"{cache_key}.pkl"
            if compress:
                cache_filename += ".gz"
            cache_path = os.path.join(cache_folder, cache_filename)

            # Check if cached result exists
            if os.path.exists(cache_path):
                open_func = gzip.open if compress else open
                with open_func(cache_path, 'rb') as f:
                    result = CoreArrayPickler.load(f)
                print(f"Loaded from cache: {cache_path}")
            else:
                # Compute result
                result = func(*args, **kwargs)
                
                # Cache result
                os.makedirs(cache_folder, exist_ok=True)
                open_func = gzip.open if compress else open
                with open_func(cache_path, 'wb') as f:
                    CoreArrayPickler.dump(result, f)
                print(f"Computed and saved to cache: {cache_path}")

            return result
        return wrapper
    return decorator