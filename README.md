# Math Microservice

This project is a microservice built with **Flask**, designed to expose endpoints for performing mathematical operations such as **fibonacci**, **factorial**, and **power**. It features **multithreaded processing**, **structured ZeroMQ logging**, **request persistence**, **caching**, and **schema validation**, all following a clean **MVC architecture**.

---

## Key Features

- REST API
- Multithreaded execution via an asynchronous worker
- Caching using Flask-Cache
- Pydantic-based input validation and response formatting
- Structured logging over ZeroMQ (PUB/SUB)
- SQLAlchemy ORM for request persistence
- Clear separation of concerns via controller/service layers
- Complete unit testing suite using pytest

---

## Package Overview

### `app/`
This is the core application package, containing all modules for configuration, logic, and routing.

- **`config.py`** loads environment variables (like DB URL, cache settings) and exposes app-wide configuration.
- **`__init__.py`** initializes the Flask app, sets up the database instance, **logger**, and the asynchronous worker pool.
- **`database.py`** handles SQLAlchemy database binding and engine setup.

---

### `app/models/`
Defines the SQLAlchemy model used to persist each request. The model includes fields like: operation name, input values, result, timestamp, execution time

---

### `app/utils/`
Provides supporting utilities:

- **`cache.py`** initializes the cache object used for memoization
- **`errors.py`** defines custom exception classes for validation and logic errors
- **`worker.py`** implements a threaded worker for running compute-heavy tasks asynchronously
- **`zmq_logger.py`** sets up a ZeroMQ publisher that sends structured log messages (level (Info/Error), message, context, source)

---

### `app/consumers/`
Implements the ZeroMQ log consumer. It subscribes to the logging address, receives structured log messages, and outputs them for monitoring.

---

### `app/schemas/`
Houses Pydantic models that enforce strict validation rules for each operation type. For example:

- Fibonacci only accepts integers ≥ 0
- Power requires a float base and integer exponent
- Response schema ensures consistent API replies

---

### `app/services/`
Encapsulates the pure mathematical logic. The `math_service.py` file includes static methods for each computation (factorial, fibonacci, power). 

---

### `app/routes/`
Defines the HTTP API endpoints using Flask route decorators. Each route delegates the request to a corresponding controller method. Endpoints include:

- `/ping` (health check)
- `/api/fibonacci`
- `/api/factorial`
- `/api/power`
- `/api/requests` 
- `/` (serves a simple HTML page with links to available API endpoints) 

---

### `app/controllers/`
Contains the main controller logic for handling requests. Each mathematical operation is:

1. Validated using Pydantic schemas
2. Executed via a cached and threaded call to the service layer
3. Persisted in the database
4. Logged as a structured event (ZMQLogger + ZMQLogConsumer)
5. Returned as a formatted response (also validated using a Pydantic schema)


---


### `app/templates/`
Includes a simple `index.html` file with links to API endpoints. Useful as a visual interface or testing page.

---

## Testing

The `tests/` directory contains unit tests for all core components:

- API route tests
- Service logic tests (math operations)
- Schema validation tests
- Model persistence tests
- Error handling and utility tests

`conftest.py` includes reusable fixtures and configuration for pytest.

### Test Coverage

![Coverage](/images/test_coverage.png)

---

### Running Tests

![Tests](/images/tests.png)

---

# Project Structure

![Project Structure](/images/structure.png)

