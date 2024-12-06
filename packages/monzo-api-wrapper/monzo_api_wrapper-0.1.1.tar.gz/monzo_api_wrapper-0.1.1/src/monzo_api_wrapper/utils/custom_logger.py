from __future__ import annotations

import functools
import inspect
import json
import os
import sys
import time
from typing import Any, Callable

import loguru
from loguru import logger as loguru_base_logger


class CustomLogger:
    """Class to create custom loggers using the Loguru package.

    This class should not be instantiated directly. Use the `get_logger` class method
    to retrieve the logger instance.

    Raises:
        RuntimeError: Raised if the class constructor is called directly.

    """

    logger = None

    def __init__(self) -> None:
        """Initialize the custom logger instance.

        Raises:
            RuntimeError: Raised if the class constructor is called directly.

        """
        raise RuntimeError

    @classmethod
    def get_logger(cls) -> loguru.Logger:
        """Retrieve an instance of the logger with customised settings.

        The logger is configured to output logs to stderr with a specified format and
        log level set by the environment variable `LOG_LEVEL`, defaults to INFO.

        Returns:
            Logger: An instance of the customised Loguru logger.

        """
        if not cls.logger:
            cls.logger = loguru_base_logger
            cls.logger.remove()
            cls.logger = cls.logger.patch(cls.logger_patch)
            cls.logger.add(
                sys.stderr, format="{extra[serialized]}", level=os.getenv("LOG_LEVEL", "INFO")
            )

        return cls.logger

    @classmethod
    def logger_patch(cls, record: loguru.Record) -> None:
        """Customises the log record format for the Loguru logger.

        This method is used to patch the logger and serialize the log record data into JSON format.

        Args:
            record (dict[str, Any]): Dictionary containing log record data.

        """
        record["extra"]["serialized"] = json.dumps({
            "timestamp": str(record["time"]),
            "module": record["name"],
            "function": record["function"],
            "line_number": record["line"],
            "level": record["level"].name,
            "message": record["message"],
            "extra": record["extra"],
        })


def suppress_args_to_mask(
    list_of_args: list[tuple[str, Any]], params_to_mask: list[str]
) -> list[tuple[str, Any]]:
    """Filter out arguments to be masked, replacing them with 'suppressed'.

    Args:
        list_of_args (list[tuple[str, Any]]): list of function arguments.
        params_to_mask (list[str]): List of string representations of params to mask.

    Returns:
        list[tuple[str, Any]]: List of arguments with non-primitives suppressed.

    """
    return [x if x[0] not in params_to_mask else (x[0], "suppressed") for x in list_of_args]


def suppress_non_primitive_args(list_of_args: list[tuple[str, Any]]) -> list[tuple[str, Any]]:
    """Filter out non-primitive arguments, replacing them with 'suppressed'.

    Args:
        list_of_args (list[tuple[str, Any]]): List of function arguments.

    Returns:
        list[tuple[str, Any]]: List of arguments with non-primitives suppressed.

    """
    return [x if is_primitive(x[1]) else (x[0], "suppressed") for x in list_of_args]


def is_primitive(obj: object) -> bool:
    """Check if an object is an instance of a primitive type.

    Args:
        obj (Any): Standard Python object.

    Returns:
        bool: True if the object is a primitive type, False otherwise.

    """
    primitives = (bool, str, int, float, type(None))
    return isinstance(obj, primitives)


def get_aws_context_value(list_of_args: list[tuple[str, Any]], key: str) -> str | None:
    """Retrieve a specific value from the AWS context argument based on the provided
    key.

    Args:
        list_of_args (list[tuple[str, Any]]): List of arguments from the function.
        key (str): The key to retrieve from the context argument.

    Returns:
        Optional[str]: The value associated with the key in the AWS context, or None if not found.

    """
    for arg_tuple in list_of_args:
        if "context" in arg_tuple:
            context_arg = arg_tuple[1]
            value = getattr(context_arg, key, None)
            return value if isinstance(value, str) else str(value) if value is not None else None
    return None


def get_func_signature(list_of_args: list[tuple[str, Any]]) -> str:
    """Generate a string representation of the function's signature, with parameters
    filtered and masked as needed.

    Args:
        list_of_args (list[tuple[str, Any]]): List of arguments passed to the function.

    Returns:
        str: String representation of the function's signature.

    """
    args_repr = [f"{a[0]}={a[1]!r}" for a in list_of_args]
    return ", ".join(args_repr)


def loggable(
    _func: Callable | None = None,
    *,
    log_params: bool = True,
    log_primitive_params_only: bool = True,
    log_response: bool = False,
    params_to_mask: list[str] | None = None,
) -> Callable:
    """Log function execution details.

    Includies start/end time,parameters, responses, and execution time. By default, only primitive
    parameters (bool, str, int, float, None) are logged and response values
    are suppressed unless specified.

    Args:
        _func (Callable, optional): Function to wrap with the decorator. Defaults to None.
        log_params (bool, optional): Whether to log function parameters. Defaults to True.
        log_primitive_params_only (bool, optional): Whether to log only primitive parameters. Defaults to True.
        log_response (bool, optional): Whether to log function responses. Defaults to False.
        params_to_mask (Optional[List[str]], optional): List of parameter names to mask in logs. Defaults to None.

    Returns:
        Callable: A wrapped function with logging functionality.

    """
    if params_to_mask is None:
        params_to_mask = []

    def decorator_log(func: Callable) -> Callable:
        """Wrap the target function and adds logging.

        Args:
            func (Callable): The function to be wrapped.

        Returns:
            Callable: The wrapped function with logging added.

        """

        @functools.wraps(func)
        def wrapper(*args: tuple[object, ...], **kwargs: dict[str, object]) -> object:
            """Add logging before and after the decorated function's execution.

            Args:
                *args (Any): Positional arguments passed to the function.
                **kwargs (Any): Keyword arguments passed to the function.

            Returns:
                Any: The result of the decorated function.

            """
            logger = CustomLogger.get_logger()

            # Prepare function signature details
            sig_keys = inspect.signature(func).parameters.keys()
            kw_vals = tuple(kwargs[k] for k in sig_keys if kwargs.get(k) is not None)
            list_of_args = list(zip(sig_keys, args + kw_vals))

            # AWS-specific logging setup if environment variables are available
            if os.getenv("AWS_EXECUTION_ENV"):
                aws_request_id = (
                    os.getenv("AWS_REQUEST_ID")
                    if func.__name__ not in ("handler", "lambda_handler")
                    else get_aws_context_value(list_of_args, "aws_request_id")
                )
                aws_log_stream_name = (
                    os.getenv("AWS_LAMBDA_LOG_STREAM_NAME")
                    if func.__name__ not in ("handler", "lambda_handler")
                    else get_aws_context_value(list_of_args, "log_stream_name")
                )

                os.environ["AWS_REQUEST_ID"] = (
                    aws_request_id
                    if aws_request_id is not None
                    and func.__name__ not in ("handler", "lambda_handler")
                    else os.getenv("AWS_REQUEST_ID", "")
                )

                logger.configure(
                    extra={
                        "aws_request_id": aws_request_id,
                        "aws_log_stream_name": aws_log_stream_name,
                    }
                )

            # Logging function parameters
            if log_params:
                list_of_args = suppress_args_to_mask(list_of_args, params_to_mask)
                if log_primitive_params_only:
                    list_of_filtered_args = suppress_non_primitive_args(list_of_args)
                    signature = get_func_signature(list_of_filtered_args)
                else:
                    signature = get_func_signature(list_of_args)

                start_msg = f"{func.__name__} [{signature}]"
            else:
                start_msg = f"{func.__name__}"

            logger.info(start_msg + " : start")
            try:
                # Measure execution time
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()

                # Log response and execution time
                base_end_msg = f"{start_msg} : end : time taken [{round(end - start, 5)}]s : response : [{type(result)}="
                end_msg = (
                    f"{base_end_msg}<suppressed>]"
                    if not log_response
                    else f"{base_end_msg}<{result}>]"
                )

                logger.info(end_msg)
            except Exception:
                logger.exception(f"Exception raised in function {func.__name__}.")
                raise
            else:
                return result

        return wrapper

    if _func is None:
        return decorator_log
    return decorator_log(_func)
