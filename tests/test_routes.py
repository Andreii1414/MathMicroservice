def test_health(client):
    """
    Test the health check endpoint to ensure it returns a 200 status code.
    """
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json == {'message': 'pong'}


def test_pow_valid(client):
    """
    Test the power endpoint with valid input to ensure it returns the correct result.
    """
    response = client.post('/api/power', json={'base': 2, 'exponent': 5})
    assert response.status_code == 200
    data = response.get_json()

    assert data['operation'] == 'power'
    assert data['input_value'] == '2.0^5'
    assert data['result'] == str(32.0)
    assert isinstance(data['processing_time'], float)


def test_pow_invalid(client):
    """
    Test the power endpoint with invalid input (negative exponent) to ensure
    it returns a 400 status code.
    """
    response = client.post('/api/power', json={'base': 'a', 'exponent': 5})
    assert response.status_code == 400
    data = response.get_json()

    assert data['status'] == "error"
    assert data['type'] == "validation"


def test_fibonacci_valid(client):
    """
    Test the Fibonacci endpoint with valid input to ensure it returns
    the correct result.
    """
    response = client.post('/api/fibonacci', json={'n': 10})
    assert response.status_code == 200
    data = response.get_json()

    assert data['operation'] == 'fibonacci'
    assert data['input_value'] == '10'
    assert data['result'] == str(55)
    assert isinstance(data['processing_time'], float)


def test_fibonacci_invalid(client):
    """
    Test the Fibonacci endpoint with invalid input (negative number) to ensure
    it returns a 400 status code.
    """
    response = client.post('/api/fibonacci', json={'n': -5})
    assert response.status_code == 400
    data = response.get_json()

    assert data['status'] == "error"
    assert data['type'] == "validation"


def test_fibonacci_invalid_type(client):
    """
    Test the Fibonacci endpoint with invalid input type (non-integer) to ensure
    it returns a 400 status code.
    """
    response = client.post('/api/fibonacci', json={'n': 'a'})
    assert response.status_code == 400
    data = response.get_json()

    assert data['status'] == "error"
    assert data['type'] == "validation"


def test_factorial_valid(client):
    """
    Test the factorial endpoint with valid input to ensure it returns
    the correct result.
    """
    response = client.post('/api/factorial', json={'n': 5})
    assert response.status_code == 200
    data = response.get_json()

    assert data['operation'] == 'factorial'
    assert data['input_value'] == '5'
    assert data['result'] == str(120)
    assert isinstance(data['processing_time'], float)


def test_factorial_invalid(client):
    """
    Test the factorial endpoint with invalid input (negative number) to ensure
    it returns a 400 status code.
    """
    response = client.post('/api/factorial', json={'n': -1})
    assert response.status_code == 400
    data = response.get_json()

    assert data['status'] == "error"
    assert data['type'] == "validation"


def test_factorial_invalid_type(client):
    """
    Test the factorial endpoint with invalid input type (non-integer) to ensure
    it returns a 400 status code.
    """
    response = client.post('/api/factorial', json={'n': 'a'})
    assert response.status_code == 400
    data = response.get_json()

    assert data['status'] == "error"
    assert data['type'] == "validation"
