
from app.models.request import MathRequest
from app.database import db


def test_create_math_request(app):
    """
    Test creating a new MathRequest and saving it to the database.
    This test checks if the MathRequest can be created with all required fields
    and if it is saved correctly in the database.
    It also verifies that the fields are correctly populated.
    """
    with app.app_context():
        request = MathRequest(
            operation='factorial',
            input_value='5',
            result='120',
            processing_time=0.001
        )

        db.session.add(request)
        db.session.commit()

        assert request.id is not None
        assert request.operation == 'factorial'
        assert request.input_value == '5'
        assert request.result == '120'
        assert isinstance(request.processing_time, float)


def test_fetch_saved_request(app):
    """
    Test fetching a saved MathRequest from the database.
    This test checks if a MathRequest can be retrieved from the database
    after it has been saved, and verifies that the retrieved data matches
    the data that was saved.
    """
    with app.app_context():
        new_request = MathRequest(
            operation='fibonacci',
            input_value='10',
            result='55',
            processing_time=0.002
        )
        db.session.add(new_request)
        db.session.commit()

        fetched_request = MathRequest.query.get(new_request.id)
        assert fetched_request is not None
        assert fetched_request.operation == 'fibonacci'
        assert fetched_request.input_value == '10'
        assert fetched_request.result == '55'


def test_missing_required_field(app):
    """
    Test creating a MathRequest without a required field.
    This test checks if the application correctly raises an error
    when trying to create a MathRequest without the 'operation' field,
    which is a required field in the MathRequest model.
    """
    with app.app_context():
        request = MathRequest(
            input_value='12',
            result='144',
            processing_time=0.003
        )

        db.session.add(request)

        try:
            db.session.commit()
            assert False, "Expected an error due to missing 'operation' field"
        except Exception as e:
            db.session.rollback()
            assert 'NOT NULL constraint failed' in str(e), ("Expected a "
                                                            "NOT NULL constraint error")


def test_update_request(app):
    """
    Test updating an existing MathRequest.
    This test checks if an existing MathRequest can be updated
    with new data, specifically updating the 'result' field.
    It verifies that the update is correctly saved in the database.
    """
    with app.app_context():
        request = MathRequest(
            operation='power',
            input_value='2^4',
            result='',
            processing_time=0.001
        )
        db.session.add(request)
        db.session.commit()

        # Update the request
        request.result = '16'
        db.session.commit()

        updated_request = MathRequest.query.get(request.id)
        assert updated_request.result == '16'


def test_delete_request(app):
    """
    Test deleting a MathRequest from the database.
    This test checks if a MathRequest can be deleted from the database
    and verifies that it is no longer retrievable after deletion.
    """
    with app.app_context():
        request = MathRequest(
            operation='factorial',
            input_value='3',
            result='6',
            processing_time=0.001
        )
        db.session.add(request)
        db.session.commit()

        db.session.delete(request)
        db.session.commit()

        deleted_request = MathRequest.query.get(request.id)
        assert deleted_request is None, "Expected the request to be deleted"
