"""
В модуле decorators.py
Этот модуль будет использоваться для размещения декораторов.
"""

from datetime import datetime
from functools import wraps
from typing import Any, Callable

log_file = "mylog.txt"


def log(filename: str | None = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timer_start = datetime.now()
            func_name: str = str(func.__name__)
            message = f"{func_name} ok"
            try:
                result = func(*args, **kwargs)
                return result
            except ValueError as error_1:
                message = f"{func_name} error: {error_1}. Inputs: {args}, {kwargs}"
                raise
            except Exception as error_2:
                message = f"{func_name} unexpected error: {error_2}. Inputs: {args}, {kwargs}"
                raise
            finally:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                timer_delta = datetime.now() - timer_start
                data_log = f"{timestamp} {message} {timer_delta.microseconds} мксек\n"
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(data_log)
                else:
                    print(data_log)

        return wrapper

    return decorator


@log(log_file)
def my_function(x: int, y: int) -> int:
    """Простая функция суммирования аргументов"""
    return x + y


my_function(1, 2)
