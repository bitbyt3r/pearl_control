import paho.mqtt.client
import random
import time

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

class MessageBus():
    def __init__(self, broker: str, port: int, client_id: str | None = None, username: str | None = None, password: str | None = None):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.active = False

        if not self.client_id:
            self.client_id = f'pearl-mini-{random.randint(0, 1000)}'
        
        self.client = paho.mqtt.client.Client(self.client_id, transport="websockets")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc: int):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        if not self.active:
            return
        print(f"Disconnected with result code: {rc}")
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            print(f"Reconnecting in {reconnect_delay} seconds...")
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                print("Reconnected successfully!")
                return
            except Exception as err:
                print(f"{err}. Reconnect failed. Retrying...")

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        print(f"Reconnect failed after {reconnect_count} attempts. Exiting...")

    def on_message(self, client, userdata, msg):
        print("on message")
        print(msg.topic, msg.payload)

    def __enter__(self):
        self.active = True
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.active = False
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic: str, message: str):
        self.client.publish(topic, message)

    def subscribe(self, topic: str):
        print(self.client.subscribe(topic))