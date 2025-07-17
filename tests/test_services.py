import pytest
from app.services.math_service import MathService


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (5, 5),
        (10, 55),
        (15, 610),
    ]
)
def test_calculate_fibonacci(n, expected):
    result = MathService.calculate_fibonacci(n)
    assert result == expected, f"Expected {expected} but got {result} for n={n}"


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 1),
        (1, 1),
        (3, 6),
        (3, 6),
        (5, 120),
        (7, 5040)
    ]
)
def test_factorial(n, expected):
    if n < 0:
        with pytest.raises(ValueError):
            MathService.factorial(n)
    else:
        result = MathService.factorial(n)
        assert result == expected, f"Expected {expected} but got {result} for n={n}"


@pytest.mark.parametrize(
    "base, exponent, expected",
    [
        (2, 0, 1),
        (2, 1, 2),
        (2, 3, 8),
        (3, 2, 9),
        (5, -1, 0.2),
        (10, -2, 0.01)
    ]
)
def test_power(base, exponent, expected):
    result = MathService.power(base, exponent)
    assert result == expected, (f"Expected {expected} but got {result} "
                                f"for base={base}, exponent={exponent}")
