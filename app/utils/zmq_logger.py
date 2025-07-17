import zmq
import orjson
import socket


class ZMQLogger:
    def __init__(self, address="tcp://localhost:5555"):
        self.address = address
        self.hostname = socket.gethostname()
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.connect(self.address)

    def log(self, level: str, message: str, context: dict = None):
        """
        Send a structured log message.
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
        self.publisher.close()
        self.context.term()
