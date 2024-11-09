from pyipr_sensor_lib.ipr_sensor_decoder import IPRSensorDecoder
from pyipr_sensor_lib.ipr_serial_interface import IPRSerialInterface

# *****************************************************************************************
# Using the library to parse binary data coming from the sensor previously saved in a file
# Use the code below as an example to
# *****************************************************************************************
# Read the entire file as a single byte string
binary_file_path = "./"
binary_file_name = 'binary_data_example.bin'

# Create an object to parse the data from the sensor or a binary file
ipr_obj = IPRSensorDecoder()
ipr_obj.decode_from_binary_file(binary_file_path, binary_file_name)
# ipr_obj.code()

# # *****************************************************************************************
# # Using the library to communicate with the sensor through the USB port
# # Use the code below as an example to setup the sensor and read data in real-time
# # *****************************************************************************************
# # Create an object for the sensor connected on the serial port
# obj = IPRSerialInterface()
# obj.serial_setup("COM5")        # Change the COM port to the one used by the sensor
# obj.serial_open()               # Open the serial port with predefined setting for the strain sensor
#
# print(obj.serial_ipr_get_system_status())               # Print the sensor status
# # print(obj.serial_ipr_get_sensor_name())               # Print the sensor name
# # obj.serial_ipr_set_sensor_name("new_sensor_name")     # Change the sensor name
# # print(obj.serial_ipr_get_sensor_tare())               # Print the tare saved in the sensor's memory (Default is X=Y=Z=0)
# # print(obj.serial_ipr_get_sensor_gain())               # Print the gain/multiplier for strain (Default is X=Y=Z=0)
# # print(obj.serial_ipr_get_sensor_material_type())      # Print the sensor material set for strain calculations
#
# # Initiate the binary data stream from the sensor
# obj.serial_ipr_start_binary_read()      # Start the binary datastream from the sensor
# # obj.serial_ipr_stop_binary_read()     # Stop the binary datastream from the sensor
#
# # Create a parser object
# ipr_obj = IPRSensorDecoder()
# # Read in continuous mode the binary data, parse it and display the converted values
# while True:
#     ipr_obj.analyse_packet(obj.serial_ipr_read_telegram())
