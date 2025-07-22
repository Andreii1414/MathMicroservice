import zmq
import orjson
import socket


class ZMQLogger:
    """
    A ZeroMQ-based logger that sends structured log messages over a PUB socket.
    """
    def __init__(self, address="tcp://localhost:5555"):
        """
        Initialize the ZMQLogger with a PUB socket.
        :param address: The ZeroMQ address to connect to (default: tcp://localhost:5555)
        """
        self.address = address
        self.hostname = socket.gethostname()
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.connect(self.address)

    def log(self, level: str, message: str, context: dict = None):
        """
        Send a structured log message.
        :param level: Log level (e.g., "info", "warning", "error")
        :param message: Log message
        :param context: Additional context for the log message (optional)
        :raises ValueError: If the log level is not recognized
        :raises Exception: If sending the message fails
        """
        payload = {
            "level": level.lower(),
            "message": message,
            "context": context or {},
            "source": self.hostname
        }

        try:
            self.publisher.send_multipart([
                level.upper().encode(),
                orjson.dumps(payload)
            ])
        except Exception as e:
            print(f"[ZMQ Logger Error] Failed to send log message: {e}")

    def close(self):
        """
        Close the ZeroMQ publisher and terminate the context.
        """
        self.publisher.close()
        self.context.term()
