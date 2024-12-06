import pytest
import numpy as np
import xarray as xr
import os
import shutil
from coreframe import CoreArray, cache_result

@pytest.fixture(scope="session")
def cache_dir():
    """Create and manage a temporary cache directory."""
    dir_path = "test_cache"
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)
    yield dir_path
    shutil.rmtree(dir_path)

@pytest.fixture(scope="session")
def example_arrays():
    """Generate different array shapes and time ranges for testing."""
    test_cases = []
    
    # Case 1: Standard 3D array (500x100x100)
    data1 = np.random.rand(500, 100, 100)
    base1 = np.datetime64("2001-03-21", 'D')
    time1 = np.asarray([base1 + np.timedelta64(x, 'D') for x in range(500)])
    lat1 = np.linspace(-90, 90, 100)
    lon1 = np.linspace(-180, 180, 100)
    test_cases.append((data1, time1, lat1, lon1, "standard"))

    # Case 2: Small array (20x10x10)
    data2 = np.random.rand(20, 10, 10)
    base2 = np.datetime64("2020-01-01", 'D')
    time2 = np.asarray([base2 + np.timedelta64(x, 'D') for x in range(20)])
    lat2 = np.linspace(-45, 45, 10)
    lon2 = np.linspace(-90, 90, 10)
    test_cases.append((data2, time2, lat2, lon2, "small"))

    # Case 3: Large patches (100x40x40)
    data3 = np.random.rand(100, 40, 40)
    base3 = np.datetime64("2015-06-15", 'D')
    time3 = np.asarray([base3 + np.timedelta64(x, 'D') for x in range(100)])
    lat3 = np.linspace(-60, 60, 40)
    lon3 = np.linspace(-120, 120, 40)
    test_cases.append((data3, time3, lat3, lon3, "large_patches"))

    return test_cases

def convert_freq(freq):
    """Convert CoreArray frequency format to xarray format."""
    unit_mapping = {'Y': 'YS', 'M': 'MS', 'D': 'D', 'h': 'H', 'm': 'T', 's': 'S'}
    number = ''.join(c for c in freq if c.isdigit())
    unit = freq[len(number):]
    return number + unit_mapping.get(unit, unit)

# Custom functions that handle the axis parameter
def percentile_90(x, axis=0):
    return np.percentile(x, 90, axis=axis)

def nanmean_custom(x, axis=0):
    return np.nanmean(x, axis=axis)

@pytest.mark.parametrize("freq", [
    '1D', '3D', '7D',  # Daily aggregations
    '1M', '2M', '3M', '6M',  # Monthly aggregations
    '1Y'  # Yearly aggregation
])
@pytest.mark.parametrize("func", [
    (np.mean, "mean"),
    (np.sum, "sum"),
    (np.std, "std"),
    (np.min, "min"),
    (np.max, "max"),
    (percentile_90, "percentile_90"),
    (nanmean_custom, "nanmean")
])
def test_apply_by_time(example_arrays, freq, func):
    """Test apply_by_time with various frequencies and functions."""
    function, func_name = func
    for data, time, lat, lon, case_name in example_arrays:
        coords = {'time': time, 'lat': lat, 'lon': lon}
        
        # Create arrays
        core_arr = CoreArray(data, coords)
        xr_da = xr.DataArray(data, coords=coords, dims=['time', 'lat', 'lon'])
        
        # Apply operations
        core_result = core_arr.apply_by_time("time", freq, function, 1, axis=0)
        
        # For xarray, handle percentile and custom functions separately
        if func_name == "percentile_90":
            def percentile_reducer(x, axis=None, **kwargs):
                return np.percentile(x, 90, axis=axis)
            xr_result = xr_da.resample(time=convert_freq(freq)).reduce(percentile_reducer)
        else:
            xr_result = xr_da.resample(time=convert_freq(freq)).reduce(function)
        
        # Compare results with tolerance for floating point differences
        np.testing.assert_allclose(
            core_result.__array__(), 
            xr_result.values,
            rtol=1e-10, 
            atol=1e-10,
            err_msg=f"Failed for case {case_name} with freq={freq} and func={func_name}"
        )
        
        # Verify coordinates
        np.testing.assert_array_equal(
            core_result.coords['time'],
            xr_result.time.values,
            err_msg=f"Time coordinates don't match for case {case_name}"
        )

@pytest.mark.parametrize("patch_size", [2, 4, 5, 8, 10])
@pytest.mark.parametrize("func", [
    (np.mean, "mean"),
    (np.sum, "sum"),
    (np.std, "std"),
    (np.min, "min"),
    (np.max, "max"),
    (percentile_90, "percentile_90"),
    (nanmean_custom, "nanmean")
])
def test_apply_by_area(example_arrays, patch_size, func):
    """Test apply_by_area with various patch sizes and functions."""
    function, func_name = func
    for data, time, lat, lon, case_name in example_arrays:
        # Skip if dimensions aren't compatible with patch_size
        if any(dim % patch_size != 0 for dim in data.shape[1:]):
            continue
            
        coords = {'time': time, 'lat': lat, 'lon': lon}
        arr = CoreArray(data, coords)
        
        try:
            result = arr.apply_by_area('lat', 'lon', function, patch_size)
            
            # Verify shape
            expected_spatial_shape = (data.shape[1] // patch_size, data.shape[2] // patch_size)
            assert result.shape[1:] == expected_spatial_shape, \
                f"Wrong shape for case {case_name}, patch_size={patch_size}"
            
            # Verify coordinates
            expected_lat = np.array([
                np.mean(lat[i:i+patch_size])
                for i in range(0, len(lat), patch_size)
            ])
            expected_lon = np.array([
                np.mean(lon[i:i+patch_size])
                for i in range(0, len(lon), patch_size)
            ])
            
            np.testing.assert_allclose(
                result.coords['lat'],
                expected_lat,
                rtol=1e-10,
                err_msg=f"Latitude coordinates wrong for case {case_name}"
            )
            np.testing.assert_allclose(
                result.coords['lon'],
                expected_lon,
                rtol=1e-10,
                err_msg=f"Longitude coordinates wrong for case {case_name}"
            )
            
            # Verify time dimension unchanged
            np.testing.assert_array_equal(
                result.coords['time'],
                time,
                err_msg=f"Time coordinates changed for case {case_name}"
            )
            
        except Exception as e:
            pytest.fail(f"Failed for case {case_name} with patch_size={patch_size}: {str(e)}")

def test_apply_combinations(example_arrays):
    """Test combinations of apply_by_time and apply_by_area."""
    for data, time, lat, lon, case_name in example_arrays:
        coords = {'time': time, 'lat': lat, 'lon': lon}
        arr = CoreArray(data, coords)
        
        try:
            area_first = arr.apply_by_area('lat', 'lon', np.mean, patch_size=2)
            result1 = area_first.apply_by_time('time', '1M', np.mean, 1, axis=0)
            
            time_first = arr.apply_by_time('time', '1M', np.mean, 1, axis=0)
            result2 = time_first.apply_by_area('lat', 'lon', np.mean, patch_size=2)
            
            np.testing.assert_allclose(
                result1.__array__(), 
                result2.__array__(),
                rtol=1e-5, 
                atol=1e-5,
                err_msg=f"Different results for different operation order in case {case_name}"
            )
        except Exception as e:
            pytest.fail(f"Failed combination test for case {case_name}: {str(e)}")

@pytest.mark.parametrize("func", [
    (np.mean, "mean"),
    (np.sum, "sum"),
    (np.max, "max")
])
def test_cache_basic(example_arrays, cache_dir, func):
    """Test basic caching functionality with different functions."""
    function, func_name = func
    
    @cache_result(cache_dir)
    def cached_operation(array):
        result = function(array, axis=0)
        if isinstance(array, CoreArray):
            new_coords = {k: v for k, v in array.coords.items() if k != 'time'}
            return CoreArray(result, new_coords)
        return result

    for data, time, lat, lon, case_name in example_arrays:
        coords = {'time': time, 'lat': lat, 'lon': lon}
        arr = CoreArray(data, coords)
        
        # First call - should compute
        result1 = cached_operation(arr)
        
        # Second call - should load from cache
        result2 = cached_operation(arr)
        
        # Verify results are identical
        np.testing.assert_array_almost_equal(
            result1.__array__(), 
            result2.__array__(),
            err_msg=f"Cached result differs for {func_name} in case {case_name}"
        )
        
        # Verify coordinates are preserved
        assert result1.coords.keys() == result2.coords.keys(), \
            f"Coordinate keys don't match for {func_name} in case {case_name}"
        
        for key in result1.coords:
            np.testing.assert_array_equal(
                result1.coords[key],
                result2.coords[key],
                err_msg=f"Coordinates differ for {func_name} in case {case_name}, key: {key}"
            )

@pytest.mark.parametrize("scale_factor", [0.5, 1.0, 2.0])
def test_cache_with_parameters(example_arrays, cache_dir, scale_factor):
    """Test caching with different function parameters."""
    @cache_result(cache_dir)
    def scaled_operation(array, scale):
        result = array * scale
        if isinstance(array, CoreArray):
            return CoreArray(result, array.coords.copy())
        return result
    
    for data, time, lat, lon, case_name in example_arrays:
        coords = {'time': time, 'lat': lat, 'lon': lon}
        arr = CoreArray(data, coords)
        
        # First call with specific scale
        result1 = scaled_operation(arr, scale_factor)
        
        # Second call with same scale - should use cache
        result2 = scaled_operation(arr, scale_factor)
        
        # Different scale - should not use cache
        result3 = scaled_operation(arr, scale_factor + 1.0)
        
        # Verify cache hit results match
        np.testing.assert_array_almost_equal(
            result1.__array__(),
            result2.__array__(),
            err_msg=f"Cached results differ for scale={scale_factor} in case {case_name}"
        )
        
        # Verify different parameters produce different results
        assert not np.array_equal(result1.__array__(), result3.__array__()), \
            f"Different parameters produced same result in case {case_name}"

def test_cache_coordinate_sensitivity(example_arrays, cache_dir):
    """Test that cache properly handles arrays with different coordinates."""
    @cache_result(cache_dir)
    def simple_operation(array):
        result = array * 2
        if isinstance(array, CoreArray):
            return CoreArray(result, array.coords.copy())
        return result
    
    for data, time, lat, lon, case_name in example_arrays:
        coords1 = {'time': time, 'lat': lat, 'lon': lon}
        coords2 = {
            'time': time + np.timedelta64(1, 'D'),  # Shift time by one day
            'lat': lat,
            'lon': lon
        }
        
        arr1 = CoreArray(data, coords1)
        arr2 = CoreArray(data.copy(), coords2)  # Same data, different coordinates
        
        result1 = simple_operation(arr1)
        result2 = simple_operation(arr2)
        
        # Verify coordinates are different
        assert not np.array_equal(result1.coords['time'], result2.coords['time']), \
            f"Arrays with different coordinates produced same cache result in case {case_name}"
        
        # Verify data operations were still performed correctly
        np.testing.assert_array_almost_equal(
            result1.__array__(),
            result2.__array__(),
            err_msg=f"Operation results differ for same data in case {case_name}"
        )

def test_cache_with_apply_methods(example_arrays, cache_dir):
    """Test caching with apply_by_time and apply_by_area methods."""
    @cache_result(cache_dir)
    def cached_time_operation(array, freq):
        return array.apply_by_time("time", freq, np.mean, 1, axis=0)
    
    @cache_result(cache_dir)
    def cached_area_operation(array, patch_size):
        return array.apply_by_area('lat', 'lon', np.mean, patch_size)
    
    for data, time, lat, lon, case_name in example_arrays:
        coords = {'time': time, 'lat': lat, 'lon': lon}
        arr = CoreArray(data, coords)
        
        # Test apply_by_time caching
        result1 = cached_time_operation(arr, '1M')
        result2 = cached_time_operation(arr, '1M')  # Should use cache
        
        np.testing.assert_array_almost_equal(
            result1.__array__(),
            result2.__array__(),
            err_msg=f"Cached apply_by_time results differ in case {case_name}"
        )
        
        # Test apply_by_area caching
        if data.shape[1] % 2 == 0 and data.shape[2] % 2 == 0:  # Only test if dimensions are even
            result3 = cached_area_operation(arr, 2)
            result4 = cached_area_operation(arr, 2)  # Should use cache
            
            np.testing.assert_array_almost_equal(
                result3.__array__(),
                result4.__array__(),
                err_msg=f"Cached apply_by_area results differ in case {case_name}"
            )
