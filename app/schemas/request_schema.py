from pydantic import BaseModel, conint


class FibonacciRequest(BaseModel):
    """
    Schema for validating Fibonacci request data.
    """
    n: conint(ge=0)


class PowerRequest(BaseModel):
    """
    Schema for validating Power request data.
    """
    base: float
    exponent: int


class FactorialRequest(BaseModel):
    """
    Schema for validating Factorial request data.
    """
    n: conint(ge=0)


class ResultResponse(BaseModel):
    operation: str
    input_value: str
    result: str
    processing_time: float
