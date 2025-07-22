from flask import jsonify


class AppError(Exception):
    """
    Base class for all application errors.
    """
    status_code = 500
    error_type = "internal"

    def __init__(self, details="Unexpected error occurred"):
        self.details = details

    def to_response(self):
        return jsonify({
            "status": "error",
            "type": self.error_type,
            "details": self.details
        }), self.status_code


class ValidationAppError(AppError):
    """
    Exception raised for validation errors in the application.
    """
    status_code = 400
    error_type = "validation"

    def __init__(self, validation_errors):
        super().__init__(details=str(validation_errors))


class CalculationAppError(AppError):
    """
    Exception raised for errors during calculations in the application.
    """
    status_code = 500
    error_type = "calculation"

    def __init__(self, message="Error during calculation"):
        super().__init__(details=message)
