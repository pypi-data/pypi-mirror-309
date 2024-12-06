import datetime as dt
import inspect
from functools import partial, wraps

from moonspark.types import SparkDataFrame


def _get_shape_delta(old_shape, new_shape):
    """Returns a string with the difference in shape between old and new."""
    diffs = [
        ("+" if new > old else "") + str(new - old)
        for new, old in zip(new_shape, old_shape)
    ]

    return f"delta=({', '.join(diffs)})"


def log_step(
    func=None,
    *,
    time_taken=True,
    shape=True,
    shape_delta=False,
    names=False,
    dtypes=False,
    print_fn=print,
    display_args=True,
    log_error=True,
):
    """Decorates a function that transforms a PySpark dataframe to add automated logging statements.

    Parameters
    ----------
    func : Callable | None, default=None
        The function to decorate with logs. If None, returns a partial function with the given arguments.
    time_taken : bool, default=True
        Whether or not to log the time it took to run a function.
    shape : bool, default=True
        Whether or not to log the shape of the output result.
    shape_delta : bool, default=False
        Whether or not to log the difference in shape of input and output.
    names : bool, default=False
        Whether or not to log the names of the columns of the result.
    dtypes : bool, default=False
        Whether or not to log the dtypes of the result.
    print_fn : Callable, default=print
        Print function to use (e.g. `print` or `logger.info`)
    display_args : bool, default=True
        Whether or not to display the arguments given to the function.
    log_error : bool, default=True
        Whether or not to add the Exception message to the log if the function fails.

    Returns
    -------
    Callable
        The decorated function.

    Examples
    --------
    ```py
    @log_step
    def remove_outliers(df, min_obs=5):
        pass

    @log_step(print_fn=logging.info, shape_delta=True)
    def remove_outliers(df, min_obs=5):
        pass
    ```
    """

    if func is None:
        return partial(
            log_step,
            time_taken=time_taken,
            shape=shape,
            shape_delta=shape_delta,
            names=names,
            dtypes=dtypes,
            print_fn=print_fn,
            display_args=display_args,
            log_error=log_error,
        )

    names = False if dtypes else names

    @wraps(func)
    def wrapper(*args, **kwargs):
        if shape_delta:
            old_shape = args[0].shape
        tic = dt.datetime.now()

        optional_strings = []
        try:
            result = func(*args, **kwargs)
            optional_strings = [
                f"time={dt.datetime.now() - tic}" if time_taken else None,
                f"n_obs={result.shape[0]}, n_col={result.shape[1]}" if shape else None,
                _get_shape_delta(old_shape, result.shape) if shape_delta else None,
                f"names={result.columns}" if names else None,
                f"dtypes={dict(result.dtypes)}" if dtypes else None,
            ]
            return result
        except Exception as exc:
            optional_strings = [
                f"time={dt.datetime.now() - tic}" if time_taken else None,
                "FAILED" + (f" with error: {exc}" if log_error else ""),
            ]
            raise
        finally:
            combined = " ".join([s for s in optional_strings if s])

            if display_args:
                func_args = inspect.signature(func).bind(*args, **kwargs).arguments
                func_args_str = "".join(
                    ", {} = {!r}".format(*item) for item in list(func_args.items())[1:]
                )
                print_fn(
                    f"[{func.__name__}(df{func_args_str})] " + combined,
                )
            else:
                print_fn(
                    f"[{func.__name__}]" + combined,
                )

    return wrapper


def log_step_extra(
    *log_functions,
    print_fn=print,
    **log_func_kwargs,
):
    """Decorates a function that transforms a PySpark dataframe to add automated logging statements.

    Parameters
    ----------
    *log_functions : List[Callable]
        Functions that take the output of the decorated function and turn it into a log.
        Note that the output of each log_function is casted to string using `str()`.
    print_fn: Callable, default=print
        Print function (e.g. `print` or `logger.info`).
    **log_func_kwargs: dict
        Keyword arguments to be passed to `log_functions`

    Returns
    -------
    Callable
        The decorated function.

    Examples
    --------
    ```py
    @log_step_extra(lambda d: d["some_column"].value_counts())
    def remove_outliers(df, min_obs=5):
        pass
    ```
    """
    if not log_functions:
        raise ValueError("Supply at least one log_function for log_step_extra")

    def _log_step_extra(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            func_args_str = "".join(
                ", {} = {!r}".format(*item) for item in list(func_args.items())[1:]
            )

            try:
                extra_logs = " ".join(
                    [str(log_f(result, **log_func_kwargs)) for log_f in log_functions]
                )
            except TypeError:
                raise ValueError(
                    f"All log functions should be callable, got {[type(log_f) for log_f in log_functions]}"
                )

            print_fn(
                f"[{func.__name__}(df{func_args_str})] " + extra_logs,
            )

            return result

        return wrapper

    return _log_step_extra
