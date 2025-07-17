import zmq
import orjson


class ZMQLogConsumer:
    def __init__(self, address="tcp://localhost:5555", topics=None):
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.address = address
        self.topics = topics or ["INFO", "ERROR"]

    def setup(self):
        self.subscriber.bind(self.address)
        for topic in self.topics:
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)
        print(f"ZMQ Log Consumer bound to {self.address} and listening "
              f"for topics: {self.topics}")

    def handle_message(self, topic: bytes, payload: bytes):
        try:
            log = orjson.loads(payload)
            print(f"[{topic.decode()}] {log['message']} from {log['source']} - "
                  f"{log.get('context', {})}")
        except Exception as e:
            print(f"[ZMQ Consumer Error] Failed to parse message: {e}")

    def run(self):
        self.setup()
        while True:
            topic, payload = self.subscriber.recv_multipart()
            self.handle_message(topic, payload)
