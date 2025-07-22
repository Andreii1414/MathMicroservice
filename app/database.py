from app import db


def init_db(app):
    """
    Initializes the database by creating all tables defined in the models.
    This function should be called once to set up the database schema.
    :param app: The Flask application instance.
    """
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")
