import numpy as np

def _create_slices(arr, time_dim, time_axis, itert):
    # TODO: I think that weeks don't work so remove them
    # Determine the unit and quantity from the resample string
    quantity = int(itert[:-1])
    unit = itert[-1]

    # Extract the time coordinate from the xarray DataArray
    time_coord = arr[time_dim]
    
    # Initialize an empty list to store the slices
    slices = []
    
    # Define a dictionary mapping resample strings to their respective pd.DateOffset or pd.Timedelta calculations
    offset_mapping = {
        'Y': lambda q: np.timedelta64(q, 'Y'),
        'M': lambda q: np.timedelta64(q, 'M'),
        'W': lambda q: np.timedelta64(q, 'W'),
        'D': lambda q: np.timedelta64(q, 'D'),
        'h': lambda q: np.timedelta64(q, 'h'),
        'm': lambda q: np.timedelta64(q, 'm'),
        's': lambda q: np.timedelta64(q, 's'),
    }

    if unit == "W":
        time_coord = time_coord.astype(f"datetime64[D]")

        days_until_sunday = (7 - (time_coord[0].astype('datetime64[D]').view('int64') + 4) % 7) % 7    
        # Add the number of days to the original date to get the next Sunday
        next_sunday = time_coord[0] + np.timedelta64(days_until_sunday, 'D')
        next_sunday_idx = np.searchsorted(time_coord, next_sunday, side='left')

        slices.append(slice(0, next_sunday_idx+1))

        start_date = next_sunday + np.timedelta64(1, 'D')
        prev_end_idx = next_sunday_idx+1
    else:
        time_coord = time_coord.astype(f"datetime64[{unit}]")
        start_date = time_coord[0]
        prev_end_idx = 0


    # Check if the unit is in the dictionary to avoid KeyError
    if unit in offset_mapping:
        while start_date <= time_coord[-1]:
            # Use the function from the dictionary to calculate the next date
            next_date = start_date + offset_mapping[unit](quantity)
            
            # Use prev_end_idx as the start_idx for this slice
            start_idx = prev_end_idx
            # Find the end index for the current slice, adjusting if next_date is beyond the last date
            end_idx = np.searchsorted(time_coord, next_date, side='left')
            
            # Ensure the slice includes the last element if next_date is beyond the last date
            if start_date >= time_coord[-1] or end_idx >= len(time_coord):
                end_idx = len(time_coord)
            
            # Append the slice (start_idx, end_idx) to the list
            slices.append(slice(start_idx, end_idx))
            
            # Update prev_end_idx and start_date for the next iteration
            prev_end_idx = end_idx  # Next slice starts from the next index
            start_date = next_date
            
            # Break the loop if we've reached or surpassed the last date
            if start_date > time_coord[-1]:
                break
    else:
        raise ValueError("Unsupported resample string. Use 'Y', 'M', 'W', 'D', 'h', 'm', or 's'.")


    result_slices = [[slice(None, None) for _ in range(len(arr.shape)) ] for _ in slices]
    for i, s in enumerate(slices):
        result_slices[i][time_axis] = s

    return result_slices

def _apply_by_time(self, time_dim, itert, fun, res_len, **kwargs):
    """
    Apply a function along the time dimension with proper time-based chunking.
    
    Args:
        time_dim (str): Name of the time dimension
        itert (str): Time interval (e.g., '1M' for 1 month)
        fun (callable): Function to apply to each chunk
        res_len (int, optional): Expected length of result per iteration
        **kwargs: Additional arguments passed to fun
    """
    time_axis = list(self.coords.keys()).index(time_dim)
    
    def wrapper(x):
        return fun(x, **kwargs)
    
    data_array = self.__array__()
    chunk_slices = _create_slices(self, time_dim, time_axis, itert)
    
    if res_len is None:
        res_len = _guess_res_len(data_array, time_axis, chunk_slices, wrapper)
    
    # Initialize result array
    result, result_time = _init_res_arr(data_array, time_axis, chunk_slices, res_len)
    
    # Apply function to each chunk
    for i, chunk_slice in enumerate(chunk_slices):
        chunk_data = data_array[tuple(chunk_slice)]
        chunk_result = wrapper(chunk_data)
        
        # Handle the case where the function changes the time dimension length
        if res_len == "same":
            res_slice = chunk_slice
        else:
            res_slice = [slice(None) for _ in range(len(data_array.shape))]
            res_slice[time_axis] = slice(i*res_len, (i+1)*res_len)
        
        # Ensure proper assignment of results
        result[tuple(res_slice)] = chunk_result
        
        # Store the time value for this chunk (using first timestamp of chunk)
        chunk_time_slice = chunk_slice[time_axis]
        time_value = self.coords[time_dim][chunk_time_slice].flat[0]
        result_time[res_slice[time_axis]] = time_value
    
    # Convert time array to proper units
    result_time = result_time.astype('datetime64[ns]')
    result_time = result_time.astype(f'datetime64[{itert[-1]}]')
    
    # Create new CoreArray with updated coordinates
    result = result.view(type(self))
    result.coords = self.coords.copy()
    result.coords[time_dim] = result_time
    
    return result

def _guess_res_len(data_array, time_axis, slices, wrapper):
    """
    Determine the length of results from the function application.
    """
    test_slice = tuple(slices[0])
    first_chunk = data_array[test_slice]
    first_result = wrapper(first_chunk)
    
    # Check if the function preserves time dimension length
    if first_result.shape[time_axis] == first_chunk.shape[time_axis]:
        return "same"
    return first_result.shape[time_axis]

def _init_res_arr(data_array, time_axis, slices, res_len):
    """
    Initialize the result array and time array based on expected results.
    """
    if res_len == "same":
        result = np.empty(data_array.shape)
        result_time = np.empty(data_array.shape[time_axis], dtype='datetime64[ns]')
    else:
        new_shape = list(data_array.shape)
        new_shape[time_axis] = len(slices) * res_len
        result = np.empty(new_shape)
        result_time = np.empty(new_shape[time_axis], dtype='datetime64[ns]')
    
    return result, result_time