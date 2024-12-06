from abc import ABC
import inspect

from .exceptions import _driverclasserror

class _configuration(ABC):
    def __init__(self) -> None:
        child = self.__class__

        attributes = {
            k for k,v in vars(self).items()
        }

        methods = {func for func, _ in inspect.getmembers(child, inspect.isfunction)}

        for attr in attributes:
            expected = f"set_{attr}"
            if expected not in methods:

                def setter(self, value, attr=attr):
                    setattr(self, attr, value)
                    return None
                
                setattr(child, expected, setter)

class _driver_meta(type):
    def __new__(cls, name, bases, classes):
        # ensure all the methods are @staticmethod or start with _
        for attr_name, attr_value in classes.items():
            if callable(attr_value):
                if not attr_name.startswith("_") and not isinstance(attr_value, staticmethod):
                    raise _driverclasserror(
                        f"Method {attr_name} in <class '{name}'> must be either a static method "
                        f"or named with a leading underscore (_)."
                    )
        
        return super().__new__(cls, name, bases, classes)

class _driver(metaclass=_driver_meta):
    pass