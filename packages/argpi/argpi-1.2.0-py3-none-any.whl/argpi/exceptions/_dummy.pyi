class _driverclasserror(Exception):
    """If the class that inherits `_driver` class
    has methods other than static methods, this error
    is raised.
    
    To create other type of methods, add `'_'` before
    the method name."""