import multiprocessing

_config = {
    'parallel': False,
    'num_workers': 0,
    'scheduler': 'static',
    'res_shape': None, # "same" or int
}

def enable_parallel(num_workers =  multiprocessing.cpu_count(), res_shape = None):
    """
    Enable parallel computations and set the number of workers.

    Parameters:
    - num_workers (int, optional): The number of worker threads/processes to use.
      Defaults to the number of available CPU cores.
    """
    _config["parallel"] = True
    _config["num_workers"] = num_workers
    _config["res_shape"] = res_shape

def disable_parallel():
    """Disable parallel computations."""
    _config["parallel"] = False
    _config["num_workers"] = 0
    _config["res_shape"] = None

def is_parallel_enabled():
    return _config['parallel']

def get_num_workers():
    return _config['num_workers']

def get_res_shape():
    return _config['res_shape']

def set_num_workers(num_workers):
    _config['num_workers'] = num_workers

def set_res_shape(res_shape):
    _config['res_shape'] = res_shape

def set_scheduler(scheduler):
    _config['scheduler'] = scheduler

def get_scheduler():
    return _config['scheduler']