from typing import get_type_hints


def enforce_types(func):
    """
    A decorator to enforce type hints at runtime.
    """

    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        arg_names = func.__code__.co_varnames[: func.__code__.co_argcount]
        positional_args = dict(zip(arg_names, args))
        all_args = {**positional_args, **kwargs}

        for arg_name, expected_type in hints.items():
            if arg_name in all_args:
                actual_value = all_args[arg_name]
                if not isinstance(actual_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be {expected_type.__name__}, "
                        f"but got {type(actual_value).__name__} ({actual_value})"
                    )
        return func(*args, **kwargs)

    return wrapper
