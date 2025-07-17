import pydantic
import pytest
from app.schemas.request_schema import (
    FibonacciRequest,
    PowerRequest,
    FactorialRequest,
    ResultResponse
)


def test_valid_fibonacci_request():
    request = FibonacciRequest(n=5)
    assert request.n == 5


def test_invalid_fibonacci_request():
    with pytest.raises(pydantic.ValidationError):
        FibonacciRequest(n=-1)


def test_invalid_fibonacci_request_type():
    with pytest.raises(pydantic.ValidationError):
        FibonacciRequest(n="five")


def test_valid_power_request():
    request = PowerRequest(base=2.5, exponent=3)
    assert request.base == 2.5
    assert request.exponent == 3


@pytest.mark.parametrize(
    "payload",
    [
        {"base": "x", "exponent": 2},
        {"base": 2.0, "exponent": "wrong"},
        {"base": None, "exponent": 2},
        {"exponent": 2},
        {"base": 2}
    ]
)
def test_invalid_power_request(payload):
    with pytest.raises(pydantic.ValidationError):
        PowerRequest(**payload)


def test_valid_factorial_request():
    request = FactorialRequest(n=5)
    assert request.n == 5


def test_invalid_factorial_request():
    with pytest.raises(pydantic.ValidationError):
        FactorialRequest(n=-1)


def test_valid_result_response():
    response = ResultResponse(
        operation="fibonacci",
        input_value="5",
        result="120",
        processing_time=0.00012
    )

    assert response.operation == "fibonacci"
    assert response.input_value == "5"
    assert response.result == "120"
    assert isinstance(response.processing_time, float)


def test_invalid_result_response():
    with pytest.raises(pydantic.ValidationError):
        ResultResponse(
            operation="fibonacci",
            input_value="5",
            result=120,
            processing_time="fast"
        )

    with pytest.raises(pydantic.ValidationError):
        ResultResponse(
            operation="fibonacci",
            input_value="5",
            result="120"
        )
