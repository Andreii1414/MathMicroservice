class MathService:

    @staticmethod
    def calculate_fibonacci(n: int) -> int:
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    @staticmethod
    def power(base: float, exponent: int) -> float:
        if exponent == 0:
            return 1
        elif exponent < 0:
            return 1 / MathService.power(base, -exponent)
        else:
            return base * MathService.power(base, exponent - 1)

    @staticmethod
    def factorial(n: int) -> int:
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n in (0, 1):
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
