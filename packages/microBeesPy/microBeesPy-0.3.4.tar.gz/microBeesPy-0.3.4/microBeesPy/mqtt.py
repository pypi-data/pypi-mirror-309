import logging
import paho.mqtt.client as mqtt

_LOGGER = logging.getLogger(__name__)

class MicrobeesMqtt:
    """Class to handle MQTT communication with the microBees platform."""
    
    def __init__(self, broker, port, username, password, client_id, on_message_callback=None):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client_id = client_id
        self.on_message_callback = on_message_callback

        # Create MQTT client instance
        self.client = mqtt.Client(client_id=client_id)
        self.client.username_pw_set(username, password)

        # Use the new API for setting callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message if on_message_callback else None

    def _on_connect(self, client, userdata, flags, rc):
        """Handle connection to the broker."""
        if rc != 0:
            _LOGGER.error(f"Failed to connect with error code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """Handle disconnection from the broker."""

    def _on_message(self, client, userdata, message):
        """Handle incoming messages."""
        if self.on_message_callback:
            self.on_message_callback(message)

    def connect(self):
        """Connect to the MQTT broker."""
        self.client.connect(self.broker, self.port)

    def disconnect(self):
        """Disconnect from the MQTT broker."""
        self.client.disconnect()

    def subscribe(self, topic, qos=0):
        """Subscribe to a specific topic."""
        self.client.subscribe(topic, qos)

    def publish(self, topic, payload, qos=0):
        """Publish a message to a topic."""
        self.client.publish(topic, payload, qos)

    def loop_forever(self):
        """Start the network loop."""
        self.client.loop_forever()
