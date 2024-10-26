from pyipr_sensor_lib.ipr_sensor_decoder import IPRSensorDecoder
from pyipr_sensor_lib.ipr_serial_interface import IPRSerialInterface

# Create an object for the sensor connected on the serial port
obj = IPRSerialInterface()
obj.serial_setup("COM5")
obj.serial_open()

# Print the sensor state
print(obj.serial_ipr_get_system_status())

# Initiate the binary data stream from the sensor
obj.serial_ipr_start_binary_read()

# Create a parser object
ipr_obj = IPRSensorDecoder()
# Read in continuous mode the binary data, parse it and display the converted values
while True:
    ipr_obj.analyse_packet(obj.serial_ipr_read_telegram())