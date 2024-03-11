import logging
import functools


LOG_FORMAT = "%(asctime)s:%(name)s:%(funcName)s:%(message)s"
GLOBAL_LOG_LEVEL = logging.DEBUG
GLOBAL_LOG_FILE = "aus_weather_data.log"
GLOBAL_LOG_STREAM = True


def log(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def FUNCTION_CALL(func_name, args, kwargs):
                logger.debug(f"CALL   {func_name}")
                logger.debug(f"ARGS   {args}")
                logger.debug(f"KWARGS {kwargs}")

            def FUNCTION_EXIT(func_name, func_result):
                logger.debug(f"END    {func_name}")
                logger.debug(f"RESULT {func_result}")

            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            FUNCTION_CALL(func.__name__, args_repr, kwargs_repr)

            try:
                result = func(*args, **kwargs)
                FUNCTION_EXIT(func.__name__, result)
                return result
            except Exception as e:
                logger.exception(f"Exception raised in {func.__name__}")
                raise e

        wrapper.__name__ += f"{func.__name__}"

        return wrapper

    return decorator
