import zmq
import orjson


class ZMQLogConsumer:
    """
    ZMQ Log Consumer that listens for log messages on a specified ZMQ address.
    """
    def __init__(self, address="tcp://localhost:5555", topics=None):
        """
        Initializes the ZMQ Log Consumer.
        :param address: The ZMQ address to bind the subscriber socket.
        :param topics: List of topics to subscribe to. Defaults to ["INFO", "ERROR"].
        """
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.address = address
        self.topics = topics or ["INFO", "ERROR"]

    def setup(self):
        """
        Sets up the ZMQ subscriber socket. Binds to the specified address and subscribes
        to the given topics.
        """
        self.subscriber.bind(self.address)
        for topic in self.topics:
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)
        print(f"ZMQ Log Consumer bound to {self.address} and listening "
              f"for topics: {self.topics}")

    def handle_message(self, topic: bytes, payload: bytes):
        """
        Handles incoming messages from the ZMQ subscriber. Parses the message and prints
        it to the console.
        """

        try:
            log = orjson.loads(payload)
            print(f"[{topic.decode()}] {log['message']} from {log['source']} - "
                  f"{log.get('context', {})}")
        except Exception as e:
            print(f"[ZMQ Consumer Error] Failed to parse message: {e}")

    def run(self):
        """
        Starts the ZMQ Log Consumer. It will run indefinitely, listening for messages
        """
        self.setup()
        while True:
            topic, payload = self.subscriber.recv_multipart()
            self.handle_message(topic, payload)
