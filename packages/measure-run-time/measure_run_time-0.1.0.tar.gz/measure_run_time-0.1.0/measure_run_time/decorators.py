import time


def measure_run_time(func):
    """
    The measure_run_time function is a Python decorator that measures the execution time of a given
    function.
    
    :param func: The func parameter in the measure_run_time function is a function that you want to
    measure the execution time of. The measure_run_time function is a decorator that calculates the
    time taken for the provided function to execute and prints out the duration in seconds after the
    function has completed its
    :return: The measure_run_time function is returning the wrap function, which is a wrapper
    function that measures the execution time of the input function func.
    """
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'\t>>> La función {func.__name__}() tardó {end_time - start_time} segundos en ejecución')
        return result
    return wrap