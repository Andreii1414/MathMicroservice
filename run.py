from app import create_app
from app.database import init_db
import sys
from threading import Thread
from app.consumers.zmq_log_consumer import ZMQLogConsumer


# Start the ZMQ log consumer in a separate thread
def start_zmq_consumer():
    consumer = ZMQLogConsumer()
    zmq_consumer_thread = Thread(target=consumer.run, daemon=True)
    zmq_consumer_thread.start()


app = create_app()
sys.set_int_max_str_digits(100_000)

if __name__ == "__main__":
    init_db(app)
    start_zmq_consumer()
    app.run()
