from pyipr_sensor_lib.ipr_sensor_decoder import IPRSensorDecoder
from pyipr_sensor_lib.ipr_serial_interface import IPRSerialInterface

# *****************************************************************************************
# Using the library to communicate with the sensor through the USB port
# Use the code below as an example to save the raw binary data to a file
# *****************************************************************************************
# Read the entire file as a single byte string
binary_file_path = "./"
binary_file_name = 'binary_data_example_01.bin'

# Create an object for the sensor connected on the serial port
obj = IPRSerialInterface()
obj.serial_setup("COM5")        # Change the COM port to the one used by the sensor
obj.serial_open()               # Open the serial port with predefined setting for the strain sensor

# Initiate the binary data stream from the sensor
obj.serial_ipr_start_binary_read()      # Start the binary datastream from the sensor
# obj.serial_ipr_stop_binary_read()     # Stop the binary datastream from the sensor

# Create a parser object
ipr_obj = IPRSensorDecoder()
while True:
    ipr_obj.save_binary_data(binary_file_path, binary_file_name, obj.serial_read_binary())
