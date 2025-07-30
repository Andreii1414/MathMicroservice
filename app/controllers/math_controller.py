from flask import request, jsonify
from app.schemas.request_schema import (FibonacciRequest, PowerRequest,
                                        FactorialRequest, ResultResponse,)
from app.services.math_service import MathService
from app import worker
from app import db
from app.models.request import MathRequest
from app.models.log import LogEntry
from pydantic import ValidationError
from app.utils.cache import cache
from app.utils.errors import (ValidationAppError,
                              CalculationAppError, AppError)
import time
from app import logger


class MathController:
    """
    Controller for handling math operations like Fibonacci, Power, and Factorial.
    It uses asynchronous processing and caching for performance.
    """
    @staticmethod
    @cache.memoize()
    def _get_cached_fibonacci(n):
        return worker.run(MathService.calculate_fibonacci, n).result()

    @staticmethod
    @cache.memoize()
    def _get_cached_power(base, exponent):
        return worker.run(MathService.power, base, exponent).result()

    @staticmethod
    @cache.memoize()
    def _get_cached_factorial(n):
        return worker.run(MathService.factorial, n).result()

    def _save_request(self, operation, input_value, result, processing_time):
        """
        Save the math request to the database.
        """
        record = MathRequest(
            operation=operation,
            input_value=input_value,
            result=str(result),
            processing_time=processing_time
        )
        db.session.add(record)
        db.session.commit()

    def _build_response(self, operation, input_value, result, processing_time):
        """
        Build a standardized response for the math operations, verified by Pydantic.
        """
        return ResultResponse(
            operation=operation,
            input_value=input_value,
            result=str(result),
            processing_time=processing_time
        )

    def factorial(self):
        """
        Handle the factorial operation. Validates input, calculates factorial,
        caches the result, and returns a standardized response.
        """
        try:
            data = FactorialRequest(**request.json)
            start = time.perf_counter()
            result = self._get_cached_factorial(data.n)
            duration = time.perf_counter() - start

            self._save_request("factorial", str(data.n), result, duration)
            logger.log("info", f"Factorial of {data.n} calculated in {duration:.4f}s",
                       context={"n": data.n}, operation="Factorial")

            response = self._build_response("factorial", str(data.n), result, duration)
            return jsonify(response.dict()), 200

        except ValidationError as e:
            logger.log("ERROR", "Validation error",
                       {"errors": e.errors(), "input": request.json}, "Factorial")
            return ValidationAppError(e.errors).to_response()

        except ValueError as e:
            logger.log("ERROR", "Calculation error",
                       {"error": str(e), "input": request.json}, operation="Factorial")
            return CalculationAppError(str(e)).to_response()

        except Exception as e:
            logger.log("ERROR", "Internal error",
                       {"error": str(e), "input": request.json}, operation="Factorial")
            return AppError(str(e)).to_response()

    def fibonacci(self):
        """
        Handle the Fibonacci operation. Validates input, calculates Fibonacci number,
        caches the result, and returns a standardized response.
        """
        try:
            data = FibonacciRequest(**request.json)
            start = time.perf_counter()
            result = self._get_cached_fibonacci(data.n)
            duration = time.perf_counter() - start

            self._save_request("fibonacci", str(data.n), result, duration)
            logger.log("info", f"Fibonacci({data.n}) calculated in {duration:.4f}s",
                       context={"n": data.n}, operation="Fibonacci")

            response = self._build_response("fibonacci", str(data.n), result, duration)
            return jsonify(response.dict()), 200

        except ValidationError as e:
            logger.log("ERROR", "Validation error",
                       {"errors": e.errors(), "input": request.json}, "Fibonacci")
            return ValidationAppError(e.errors).to_response()

        except ValueError as e:
            logger.log("ERROR", "Calculation error",
                       {"error": str(e), "input": request.json}, operation="Fibonacci")
            return CalculationAppError(str(e)).to_response()

        except Exception as e:
            logger.log("ERROR", "Internal error",
                       {"error": str(e), "input": request.json}, operation="Fibonacci")
            return AppError(str(e)).to_response()

    def power(self):
        """
        Handle the power operation. Validates input, calculates power,
        caches the result, and returns a standardized response.
        """
        try:
            data = PowerRequest(**request.json)
            start = time.perf_counter()
            result = self._get_cached_power(data.base, data.exponent)
            duration = time.perf_counter() - start

            input_str = f"{data.base}^{data.exponent}"
            self._save_request("power", input_str, result, duration)
            logger.log("info", f"Power({input_str}) calculated in {duration:.4f}s",
                       {"base": data.base, "exponent": data.exponent}, "Power")

            response = self._build_response("power", input_str, result, duration)
            return jsonify(response.dict()), 200

        except ValidationError as e:
            logger.log("ERROR", "Validation error",
                       {"errors": e.errors(), "input": request.json}, operation="Power")
            return ValidationAppError(e.errors).to_response()

        except ValueError as e:
            logger.log("ERROR", "Calculation error",
                       {"error": str(e), "input": request.json}, operation="Power")
            return CalculationAppError(str(e)).to_response()

        except Exception as e:
            logger.log("ERROR", "Internal error",
                       {"error": str(e), "input": request.json}, operation="Power")
            return AppError(str(e)).to_response()

    def get_requests(self):
        try:
            op = request.args.get("operation")
            query = MathRequest.query
            if op:
                query = query.filter_by(operation=op)
            rows = query.all()

            result = [{
                "id": r.id,
                "operation": r.operation,
                "input_value": r.input_value,
                "result": r.result,
                "processing_time": r.processing_time,
                "timestamp": r.timestamp.isoformat() if r.timestamp else None
            } for r in rows]

            return jsonify(result), 200

        except Exception as e:
            logger.log("ERROR", "Failed to retrieve requests",
                       {"error": str(e)}, operation="GetRequests")
            return AppError(str(e)).to_response()

    def get_logs(self):
        """
        Retrieve logs from the database.
        """
        try:
            logs = LogEntry.query.all()
            result = [{
                "id": log.id,
                "level": log.level,
                "message": log.message,
                "details": log.details,
                "operation": log.operation,
                "created_at": log.created_at.isoformat()
            } for log in logs]

            return jsonify(result), 200

        except Exception as e:
            logger.log("ERROR", "Failed to retrieve logs",
                       {"error": str(e)}, operation="GetLogs")
            return AppError(str(e)).to_response()
