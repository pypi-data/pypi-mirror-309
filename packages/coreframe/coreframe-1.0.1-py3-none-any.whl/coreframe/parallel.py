import time
import numpy as np
import ctypes
import multiprocessing as mp
from typing import Callable, List, Tuple, Union

def shmem_as_ndarray(raw_array: mp.RawArray) -> np.ndarray:
    """Convert a multiprocessing.RawArray to a NumPy ndarray."""
    ctypes_to_numpy = {
        ctypes.c_char: np.int8,
        ctypes.c_wchar: np.int16,
        ctypes.c_byte: np.int8,
        ctypes.c_ubyte: np.uint8,
        ctypes.c_short: np.int16,
        ctypes.c_ushort: np.uint16,
        ctypes.c_int: np.int32,
        ctypes.c_uint: np.uint32,
        ctypes.c_long: np.int32,
        ctypes.c_ulong: np.uint32,
        ctypes.c_longlong: np.int64,
        ctypes.c_float: np.float32,
        ctypes.c_double: np.float64,
    }
    numpy_dtype = ctypes_to_numpy[raw_array._type_]
    count = ctypes.sizeof(raw_array) // numpy_dtype().itemsize
    return np.frombuffer(raw_array, dtype=numpy_dtype, count=count)

class Scheduler:
    def __init__(self, src_shape: Tuple[int, ...], axis: int, nprocs: int, guided: bool = False, chunk=None, out_slice=None):
        self.n_tot = src_shape[axis]
        self.n_data = src_shape[axis]
        self.guided = guided
        self.slice = [slice(None)] * len(src_shape)
        self.out_slice = out_slice
        self.axis = axis
        self.n_cnt = mp.RawValue(ctypes.c_int, -1)
        self.n_data_value = mp.RawValue(ctypes.c_int, self.n_data)
        self.start = mp.RawValue(ctypes.c_int, 0)
        self.lock = mp.Lock()
        self.nprocs = nprocs
        self.chunk = self._set_chunk(chunk, nprocs)

    def _set_chunk(self, chunk, nprocs):
        if hasattr(chunk, '__iter__'):
            return chunk
        min_chunk = max(self.n_data // nprocs, 1)
        return chunk if chunk and chunk > min_chunk else min_chunk

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            if hasattr(self.chunk, '__iter__'):
                return self._next_iterable_chunk()
            return self._next_single_chunk()

    def _next_iterable_chunk(self):
        if self.guided:
            return self._next_guided_iterable_chunk()
        return self._next_unguided_iterable_chunk()

    def _next_guided_iterable_chunk(self):
        if self.n_cnt.value == -1:
            self.n_cnt.value = 0
        n_slices_to_process = max((len(self.chunk) - self.n_cnt.value) // self.nprocs, 1)
        
        if self.n_cnt.value < len(self.chunk):
            old_n_cnt = self.n_cnt.value
            self.n_cnt.value += n_slices_to_process
            current_n_cnt = min(self.n_cnt.value, len(self.chunk) - 1)
            self.n_cnt.value += 1
            _slice = self.slice.copy()
            _slice[self.axis] = slice(self.chunk[old_n_cnt].start, self.chunk[current_n_cnt].stop)
            
            if self.out_slice is None:
                _out_slice = None
            else:
                _out_slice = slice(self.out_slice[self.axis][old_n_cnt].start, self.out_slice[self.axis][current_n_cnt].stop)
            
            return _slice, _out_slice, self.chunk[old_n_cnt:current_n_cnt + 1]
        raise StopIteration

    def _next_unguided_iterable_chunk(self):
        if self.n_cnt.value < len(self.chunk) - 1:
            self.n_cnt.value += 1
            current_n_cnt = self.n_cnt.value
            _slice = self.slice.copy()
            _slice[self.axis] = self.chunk[current_n_cnt]
            _out_slice = None if self.out_slice is None else self.out_slice[self.axis][current_n_cnt]
            return _slice, _out_slice, None
        raise StopIteration

    def _next_single_chunk(self):
        if self.n_data_value.value:
            if self.chunk > self.n_data_value.value:
                s0, s1 = self.start.value, self.start.value + self.n_data_value.value
                self.n_data_value.value = 0
            else:
                s0, s1 = self.start.value, self.start.value + self.chunk
                self.n_data_value.value -= self.chunk
                self.start.value += self.chunk
            
            _slice = self.slice.copy()
            _slice[self.axis] = slice(s0, s1)
            _out_slice = None if self.out_slice is None else self.out_slice[self.axis][_slice[self.axis]]
            return _slice, _out_slice, None
        raise StopIteration

def parallel(nproc: int, guided: bool = False, shm_idx: List[int] = [0], out_shp=None, out_type=None, axis: int = 0, chunk=None):
    def wrapper(func: Callable):
        def inner(*args, **kwargs):
            if not all(hasattr(args[i], 'shape') for i in shm_idx):
                if out_shp is None:
                    raise ValueError("outShp must be provided when args are not numpy arrays")
            
            if nproc > 1:
                return mp_func(func, args, shm_idx, out_shp, out_type, axis, nproc, guided, chunk)
            return func(*args, **kwargs)
        return inner
    return wrapper

def mp_func(func: Callable, args: Tuple, shm_idx: List[int], out_shp, out_type, axis: int, nproc: int, guided: bool, chunk):
    def go_parallel(scheduler: Scheduler, func: Callable, args: Tuple, shm_out: mp.RawArray, shm_idx: List[int], dtimes_array: np.ndarray):
        for slc, out_slc, inner_slc in scheduler:
            slc = slc[0]
            _args = [arg if i not in shm_idx else arg[slc] for i, arg in enumerate(args)]

            if scheduler.guided:
                sub_out, timestamp_array = func(*_args, inner_slc)
            else:
                sub_out = func(*_args)

            dtimes_array[out_slc] = timestamp_array

            if out_slc is None:
                shm_out[slc] = sub_out
            else:
                if shm_out[out_slc].shape != sub_out.shape:
                    print(f'\t\t!! WARNING !! **SHAPE MISMATCH** outShp {shm_out[out_slc].shape} : subOut {sub_out.shape}')
                shm_out[out_slc] = sub_out

    args = list(args)
    nproc = nproc or mp.cpu_count()
    out_type = out_type or args[shm_idx[0]].dtype.char

    if out_shp is None:
        out_shp = args[shm_idx[0]].shape
        out_slice = None
    elif hasattr(out_shp[axis], '__iter__'):
        out_slice = [slice(None)] * len(out_shp)
        out_slice[axis] = out_shp[axis]
        out_shp[axis] = int(np.sum([np.ceil((sl.stop - sl.start) / float(sl.step or 1)) for sl in out_shp[axis]]))
    else:
        out_slice = None

    shm_out = mp.RawArray(out_type if isinstance(out_type, str) else out_type.dtype.char, int(np.prod(out_shp)))
    a_out = shmem_as_ndarray(shm_out).reshape(out_shp)

    dtimes_shm = mp.RawArray(ctypes.c_double, out_shp[0])
    dtimes_array = shmem_as_ndarray(dtimes_shm)

    scheduler = Scheduler(args[shm_idx[0]].shape, axis, nproc, guided, chunk, out_slice)
    query_args = (scheduler, func, args, a_out, shm_idx, dtimes_shm)

    pool = [mp.Process(target=go_parallel, args=query_args) for _ in range(nproc)]

    for p in pool:
        p.start()
    for p in pool:
        p.join()

    return a_out, dtimes_array