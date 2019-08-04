from pi_mqtt_gpio.modules import GenericSensor
ALLOWED_TYPES = ["dht11", "dht22"]
CONFIG_SCHEMA = {
    "pin": dict(type="integer", required=True, empty=False),
    "type": dict(
        type="string", required=True, empty=False, allowed=ALLOWED_TYPES + list(map(str.upper, ALLOWED_TYPES))
    ),
}
SENSOR_SCHEMA = {
    "type": dict(
        type="string",
        required=False,
        empty=False,
        default="temperature",
        allowed=["temperature", "humidity"],
    )
}


class Sensor(GenericSensor):
    """
    Implementation of Sensor class for the DHT22 temperature sensor.
    """

    def __init__(self, config):
        import pi_mqtt_gpio.utils.dht as dht
        self.temperature = -1
        self.humidity = -1
        sensor_type = config["type"].lower()

        if sensor_type == "dht22":
            self.sensor = dht.DHT22(pin=config["pin"])
        elif sensor_type == "dht11":
            self.sensor = dht.DHT11(pin=config["pin"])
        else:
            raise Exception("Supported sensor types: DHT22, DHT11")


    def setup_sensor(self, config):
        return True  # nothing to do here

    def get_value(self, config):
        """get the temperature or humidity value from the sensor"""
        result = self.sensor.read()
        if not result.error_code:
            self.humidity, self.temperature = result.humidity, result.temperature
        if config["type"] == "temperature":
            return self.temperature
        if config["type"] == "humidity":
            return self.humidity
        return None
