class ArgumentDoesNotHaveAValue(Exception):
    """Exception for when an argument does not have
    a value but queried."""
    ...

class FetchValueTypeError(Exception):
    """Error Exception related to Fetch"""
    ...


class OrchestrationFault(Exception):
    """General Exception for any errors in orchestration."""
    ...

class DefinitionError(Exception):
    """General Exception for Definition Error."""
    ...