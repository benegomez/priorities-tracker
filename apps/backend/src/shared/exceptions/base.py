class DomainException(Exception):
    pass


class ValidationException(DomainException):
    pass


class AuthenticationException(DomainException):
    """Credentials invalid or token expired — maps to HTTP 401."""
    pass


class AuthorizationException(DomainException):
    """User lacks permission — maps to HTTP 403."""
    pass


class BusinessRuleViolation(DomainException):
    """A business rule (BR-XXX) was violated — maps to HTTP 409."""
    pass
