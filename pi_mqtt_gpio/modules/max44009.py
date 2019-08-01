from pi_mqtt_gpio.modules import GenericSensor
import time

REQUIREMENTS = ("smbus",)
CONFIG_SCHEMA = {
    "i2c_bus_num": {"type": "integer", "required": True, "empty": False},
    "chip_addr": {"type": "integer", "required": True, "empty": False},
}


class Sensor(GenericSensor):
    """
    Implementation of Sensor class for the MAX44009 light sensor
    """

    def __init__(self, config):
        import smbus

        self.bus = smbus.SMBus(config["i2c_bus_num"])
        self.address = config["chip_addr"]

    def setup_sensor(self, config):
        return True  # nothing to do here

    def get_value(self, config):
        """get the light value from the sensor"""
        value = False

        self.bus.write_byte_data(self.address, 0x02, 0x40)
        time.sleep(0.5)
        data = self.bus.read_i2c_block_data(self.address, 0x03, 2)
        # Convert the data to lux 
        exponent = (data[0] & 0xF0) >> 4
        mantissa = ((data[0] & 0x0F) << 4) | (data[1] & 0x0F)
        value = ((2 ** exponent) * mantissa) * 0.045
        return value

    