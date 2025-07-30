from math import factorial

class MathService:

    @staticmethod
    def calculate_fibonacci(n: int) -> int:
        """
        Calculate the nth Fibonacci number using an iterative approach.
        :param n: The position in the Fibonacci sequence (0-indexed).
        :return: The nth Fibonacci number.
        """
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    @staticmethod
    def power(base: float, exponent: int) -> float:
        """
        Calculate the power of a base raised to an exponent using recursion.
        :param base: The base number.
        :param exponent: The exponent to raise the base to.
        :return: The result of base raised to the exponent.
        """
        if exponent == 0:
            return 1
        elif exponent < 0:
            return 1 / MathService.power(base, -exponent)
        else:
            return base * MathService.power(base, exponent - 1)

    @staticmethod
    def factorial(n: int) -> int:
        """
        Calculate the factorial of a non-negative integer n.
        :param n: A non-negative integer.
        :return: The factorial of n.
        """
        return factorial(n)
