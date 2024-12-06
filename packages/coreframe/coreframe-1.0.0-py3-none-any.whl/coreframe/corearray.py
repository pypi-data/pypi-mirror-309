import numpy as np
from ._utils.apply_by_time import _apply_by_time
from ._utils.apply_by_area import _apply_by_area

class CoreArray(np.ndarray):
    def __new__(cls, input_array, coords) :
        # coords is a dictionary with keys as the names of the coordinates and values as the coordinate values 
        obj = np.asarray(input_array).view(cls)
        obj.coords = coords


        for i, key in enumerate(coords):
            assert len(coords[key]) == obj.shape[i], f"Length of coordinate '{key}' does not match the shape of the array."

        return obj
    
    def __getitem__(self, key):
        '''
        Returns selected elements from CoreArray object.

        Args:
            key (int, slice, tuple, str): Index or slice or dimension name.

        Returns:
            result (CoreFrame or ndarray): Result of indexing or slicing.
        '''
        # if dimension is accessed
        if isinstance(key, str):
            return self.coords[key]

        result = super().__getitem__(key)
    
        # if the result is an array, update the coordinates
        if isinstance(result, np.ndarray):

            if isinstance(key, tuple):
                slices = key
            else:
                slices = (key,)

            coords_items = list(self.coords.items())

            result.coords = self.coords.copy()
            for i, slice in enumerate(slices):
                result.coords[coords_items[i][0]] = coords_items[i][1][slice]

        return result.view(CoreArray)

    def __array_finalize__(self, obj):
        if obj is None: return
        self.coords = getattr(obj, 'coords', {})

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """
        Handle NumPy universal functions (ufuncs) for CoreArray.
        """
        # Convert CoreArray inputs to regular numpy arrays
        new_inputs = [obj.__array__() if isinstance(obj, CoreArray) else obj for obj in inputs]

        # Apply the ufunc
        out = super().__array_ufunc__(ufunc, method, *new_inputs, **kwargs)

        # Only wrap the output in CoreArray if it's an ndarray
        if isinstance(out, np.ndarray):
            out = out.view(type(self))
            out.coords = self.coords
            return out
        
        # Return plain output for non-array results (like comparison results)
        return out
  

    def __array_function__(self, func, types, args, kwargs):
        """
        Handle NumPy array functions for CoreArray.
        """
        # Convert CoreArray arguments to regular numpy arrays
        new_args = [
            arg.__array__() if isinstance(arg, CoreArray) 
            else [item.__array__() if isinstance(item, CoreArray) else item for item in arg] if isinstance(arg, list)
            else arg 
            for arg in args
        ]

        # Apply the numpy function
        out = func(*new_args, **kwargs)
        
        # Only wrap the output in CoreArray if it's an ndarray
        if not isinstance(out, np.ndarray):
            return out
            
        out = out.view(type(self))

        # Handle coordinate updates based on axis reduction
        axis = kwargs.get('axis', None)
        if axis is not None:
            keys = list(self.coords.keys())
            if isinstance(axis, (tuple, list)):
                # Sort axes in descending order to remove from highest to lowest
                axes = sorted(axis, reverse=True)
                out.coords = self.coords.copy()
                for ax in axes:
                    if ax < len(keys):
                        del out.coords[keys[ax]]
            else:
                if axis < len(keys):
                    out.coords = {k: self.coords[k] for k in keys if k != keys[axis]}
        else:
            out.coords = self.coords

        return out


    def apply_by_time(self, time_dim, itert, fun, res_len = None, **kwargs):
        '''
        Apply a function along the time dimension.

        Args:
            time_dim (str): Name of the time axis.
            itert (int): Number of iterations.
            res_length_per_itert (int): Length of the result per iteration.
            fun (callable): Function to apply along the time dimension.
            args (tuple): Arguments to pass to the function.
            kwargs (dict): Keyword arguments to pass to the function.

        Returns:
            result (CoreArray): Result of applying the function along the time dimension.
        '''

        return _apply_by_time(self, time_dim, itert, fun, res_len, **kwargs)

        
       
    def apply_by_area(self, dim1, dim2, func, patch_size, **kwargs):
        return _apply_by_area(self, dim1, dim2, func, patch_size, **kwargs)


    def __repr__(self):
        repr_str = f"CoreArray(\n  shape={self.shape},\n  coords={{\n"
        for coord_name, coord_values in self.coords.items():
            repr_str += f"    '{coord_name}': {coord_values},\n"
        repr_str += "  }\n)"
        return repr_str

    def __str__(self):
        str_str = f"CoreArray {self.shape} \n"
        str_str += "Coordinates:\n"
        for coord_name, coord_values in self.coords.items():
            if isinstance(coord_values, np.ndarray):
                if len(coord_values) > 4:
                    coord_str = f"[{coord_values[0]}, {coord_values[1]} ... {coord_values[-2]}, {coord_values[-1]}]"
                else:
                    coord_str = ", ".join(str(val) for val in coord_values)
                str_str += f"  {coord_name}: {coord_str}\n"
            else:
                str_str += f"  {coord_name}: {coord_values}\n"
        return str_str
    


if __name__ == "__main__":
    # Example usage

    data = np.random.rand(500, 100, 100)
    base = np.datetime64("2001-03-21", 'D')
    time = np.asarray([base + np.timedelta64(x, 'D') for x in range(500)])
    lat = np.linspace(-90, 90, 100)
    lon = np.linspace(-180, 180, 100)

    coords = {
        'time': time,
        'lat': lat,
        'lon': lon
    }

    arr = CoreArray(data, coords)

    a = arr[:250]
    b = arr[250:]


    res = np.concatenate([a, b], axis=0)
    # print(a)
    # print(b)
    # print(res["time"].shape)


    res1 = res.apply_by_time("time", "1M", np.max, 1, axis=0)

    print(res1.__array__())

    # res = np.max(a, 0)
    # res = np.sum(arr, axis=0)
    # res = arr["time"]

