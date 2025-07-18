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

## Running the Service from a Docker Image

### Download the Docker image
Download the image archive (`math-service.tar`) from the following link:
[Download math-service Docker image](https://github.com/Andreii1414/MathMicroservice/releases/download/v1.0.0/math-service.tar)

### Load the image into Docker
Once downloaded, load the image into your local Docker environment:

```bash
docker load -i math-service.tar
```

### Run the Docker container
Start the service using the following command:

```bash
docker run -d -p 5000:5000 --name math-api math-service
```

### Stop or remove the Docker container
To stop the running container, use:

```bash
docker stop math-api
```
To remove the container, use:

```bash
docker rm -f math-api
```

### Testing the API

Once the container is running, you can test the API using `curl` or any API client like Postman.

#### Example: Compute power

```bash
curl -X POST http://localhost:5000/api/power \
  -H "Content-Type: application/json" \
  -d '{"base": 2, "exponent": 10}'
```

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

The ZMQ-based logger is used primarily as a demonstration of a distributed logging mechanism. While it currently only prints messages to the console, it would be highly valuable in a production setting where logs originate from multiple services, are stored persistently (e.g., in a file or database), or are visualized through a centralized dashboard for monitoring and analysis.

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

#### `/ping`
Health check endpoint. Returns a simple `"pong"` response.

<details>
<summary>Show example</summary>

**Request:**

```bash
curl http://localhost:5000/ping
```
**Response:**

```json
{
  "message": "pong"
}
```
</details>

#### `/api/fibonacci`
Computes the n-th Fibonacci number. Expects a POST request with JSON input.
<details>
<summary>Show example</summary>

**Request:**

```bash
curl -X POST http://localhost:5000/api/fibonacci \
  -H "Content-Type: application/json" \
  -d '{"n": 10}'
```

**Response:**

```json
{
  "operation": "fibonacci",
  "input_value": "7",
  "result": "13",
  "processing_time": 0.0023
}
```
</details>


#### `/api/factorial`
Computes the factorial of n. Expects a POST request with JSON input.

<details>
<summary>Show example</summary>

**Request:**

```bash
curl -X POST http://localhost:5000/api/factorial \
  -H "Content-Type: application/json" \
  -d '{"n": 5}'
```

**Response:**

```json
{
  "operation": "factorial",
  "input_value": "5",
  "result": "120",
  "processing_time": 0.0015
}
```
</details>


#### `/api/power`
Computes the power of a base raised to an exponent. Expects a POST request with JSON input.

<details>
<summary>Show example</summary>

**Request:**

```bash
curl -X POST http://localhost:5000/api/power \
  -H "Content-Type: application/json" \
  -d '{"base": 2, "exponent": 10}'
```

**Response:**

```json
{
  "operation": "power",
  "input_value": "2^10",
  "result": "1024.0",
  "processing_time": 0.0018
}
```
</details>


#### `/api/requests` 
Returns a list of past math requests. Supports optional query param operation.

<details>
<summary>Show example</summary>

**Request:**

```bash
curl http://localhost:5000/api/requests?operation=fibonacci
```

**Response:**

```json
[
  {
    "id": 1,
    "operation": "fibonacci",
    "input_value": "7",
    "result": "13",
    "timestamp": "2023-10-01T12:00:00Z",
    "processing_time": 0.0023
  },
  {
    "id": 2,
    "operation": "fibonacci",
    "input_value": "10",
    "result": "55",
    "timestamp": "2023-10-01T12:01:00Z",
    "processing_time": 0.0025
  }
]
```
</details>


#### `/`
Serves a simple HTML page with links to the available API endpoints.


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

A benchmark test compares AsyncWorker with max_workers=1 and max_workers=5 to evaluate the impact of parallel execution. The test dispatches multiple CPU-intensive tasks and measures total execution time.
Results indicate that concurrent task execution with a higher worker count leads to significantly better performance on CPU-bound operations.


![Worker](/images/test_worker.png)

### Test Coverage

![Coverage](/images/test_coverage.png)

---

### Running Tests

![Tests](/images/tests.png)

---

# Project Structure

![Project Structure](/images/structure.png)

