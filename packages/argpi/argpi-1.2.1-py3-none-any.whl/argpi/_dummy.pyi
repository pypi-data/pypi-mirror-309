from abc import ABC
import inspect

from .exceptions import _driverclasserror

from typing import Self

class _configuration(ABC):
    """`Configuration blueprint/builder class`

    -------------------------------------------------

    This class is meant to be inherited to create a
    `Configurations` class which will contain all
    conditional (boolean) and value based argument data.

    -------------------------------------------------
    
    This class can be either initialized globally for a
    `Driver` class (which contains static methods) or can
    be passed as a parameter to individual functions.
    
    For each attribute `(self.<attr-name>)`, a method will
    be created dynamically named `set_<attr-name>`, which
    will take one value. If you want to create your own function
    you can do that.

    Example:
    ```python
    from argpi import _configuration, _driver

    class Configurations(_configuration):
        def __init__(self) -> None:
            # define attributes here
            self.attribute_1 = True
            self.attribute_2 = "Some Value"

            # init the super class
            super().__init__()
    
    class Drivers:
        @staticmethod
        def some_method(config: Configurations) -> None:
            if config.attribute_1:
                # do something
            elif config.attribute_2 is not None:
                # do something
            else:
                # do something else
    ```

    The above defined `Configurations` class will have two
    methods dynamically created: `set_attribute_1` and
    `set_attribute_2`, which can be used to set the 
    attributes using `PathWays` class.
    """

    def __init__(self) -> None:
        """create the setter functions dynamically."""
        ...

class _driver_meta(type):
    """Internal class for allowing only static methods
    in the `_driver` class.
    
    The `_driver` class can only have static methods,
    to create other or normal methods add `'_'` before
    the method name.
    """
    def __new__(cls, name, bases, classes): ...


class _driver(metaclass=_driver_meta):
    """`Driver blueprint class.`
    
    --------------------------------------------------

    This class is meant to be inherited to create the
    `Driver` class which will contain static methods for
    all functions related to the base arguments.

    -------------------------------------------------

    The method in this class can either have a parameter
    that accepts the `Configurations` class or can access
    it globally.
    """
    ...