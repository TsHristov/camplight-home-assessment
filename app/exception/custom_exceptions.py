from fastapi import HTTPException


class ValidationError(HTTPException):
    """Base exception for validation errors."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=message)


class EmptyTextError(ValidationError):
    """Exception raised when text is empty."""

    def __init__(self):
        super().__init__(message="Text cannot be empty")


class TextTooLongError(ValidationError):
    """Exception raised when text exceeds maximum length."""

    def __init__(self):
        super().__init__(message="Text exceeds the maximum threshold of 5000 symbols")


class InvalidStyleError(ValidationError):
    """Exception raised when style is invalid."""

    def __init__(self, valid_styles: list[str]):
        super().__init__(message=f"Style must be one of: {', '.join(valid_styles)}")
