import serial

DEBUG_MODE = False
DEBUG_SERIAL_RECEIVE = False

def format_command(text):
    _array = bytearray()
    _array.extend(map(ord, "{}\r".format(text)))
    return _array

class IPRSerialInterface:
    def __init__(self):
        # Display the Python Serial library only in debug mode
        if DEBUG_MODE:
            print("Python serial port library version: {}".format(serial.VERSION))
        # Create the serial port object
        self._serial_port_obj = serial.Serial()
        # Variable used to know if the sensor is sending binary data. Assume it is at the beginning
        self.is_binary_reading_running = True
        print("Initiating IPRSerialInterface -> DONE")

    def serial_setup(self, com_port_name):
        # Setup the serial port for strain sensor
        self._serial_port_obj.port = com_port_name  # COM port
        self._serial_port_obj.baudrate = 921600  # Baudrate
        self._serial_port_obj.timeout = 0.25  # 0.25 second timeout

    def serial_open(self):
        try:
            # Open serial port only if it's not open yet
            if not self._serial_port_obj.isOpen():
                self._serial_port_obj.open()  # Try to open serial port
                print("Connected to USB port : {}".format(self._serial_port_obj.isOpen()))
        except Exception as _error:  # Catch the error is serial port is not able to connect
            print(_error)

    def serial_close(self):
        self._serial_port_obj.close()

    def serial_read_binary(self):
        # Read 1 character at a time from the serial port
        _data = self._serial_port_obj.read(1)
        if DEBUG_SERIAL_RECEIVE:
            print(_data)
        return _data

    def serial_ipr_get_system_status(self):
        # Check if the sensor sends binary data. If so, stop it before sending commands
        self.serial_ipr_check_if_data_reading()
        # Send command to sensor to get the system status
        self._serial_port_obj.write(format_command("$"))  # Sending the '$'

        # Read all the data from the serial port, until character '>'
        _telegram = self.serial_ipr_read_text_from_sensor()

        return ''.join(_telegram)[:-1]

    def serial_ipr_get_sensor_tare(self):
        # Check if the sensor sends binary data. If so, stop it before sending commands
        self.serial_ipr_check_if_data_reading()
        # Send command to sensor to get the tare saved on the sensor's internal memory
        self._serial_port_obj.write(format_command("tare"))  # Query the sensor tare

        # Read all the data from the serial port, until character '>'
        _telegram = self.serial_ipr_read_text_from_sensor()

        return ''.join(_telegram).split("tare\n")[-1][:-1]

    def serial_ipr_get_sensor_material_type(self):
        # Check if the sensor sends binary data. If so, stop it before sending commands
        self.serial_ipr_check_if_data_reading()
        self._serial_port_obj.write(format_command("material"))  # Query the sensor material

        # Read all the data from the serial port, until character '>'
        _telegram = self.serial_ipr_read_text_from_sensor()

        return ''.join(_telegram).split("Material = ")[-1][:-1]

    def serial_ipr_get_sensor_gain(self):
        # Check if the sensor sends binary data. If so, stop it before sending commands
        self.serial_ipr_check_if_data_reading()
        # Send command to sensor to get the gain/multiplier saved on the sensor's internal memory
        self._serial_port_obj.write(format_command("transfer"))  # Query the sensor gain

        # Read all the data from the serial port, until character '>'
        _telegram = self.serial_ipr_read_text_from_sensor()

        return ''.join(_telegram).split("transfer\n")[-1][:-1]

    def serial_ipr_get_sensor_strain_offset(self):
        # Check if the sensor sends binary data. If so, stop it before sending commands
        self.serial_ipr_check_if_data_reading()
        # Send command to sensor to get the offset saved on the sensor's internal memory
        self._serial_port_obj.write(format_command("offset"))  # Query the sensor offset

        # Read all the data from the serial port, until character '>'
        _telegram = self.serial_ipr_read_text_from_sensor()

        return ''.join(_telegram).split("offset\n")[-1][:-1]

    def serial_ipr_get_sensor_name(self):
        # Check if the sensor sends binary data. If so, stop it before sending commands
        self.serial_ipr_check_if_data_reading()
        # Send command to sensor to get the name saved on the sensor's internal memory
        self._serial_port_obj.write(format_command("name"))  # Query the sensor name

        # Read all the data from the serial port, until character '>'
        _telegram = self.serial_ipr_read_text_from_sensor()

        return ''.join(_telegram).split("Name : ")[-1][:-1]

    def serial_ipr_set_sensor_name(self, sensor_name):
        # Check if the sensor sends binary data. If so, stop it before sending commands
        self.serial_ipr_check_if_data_reading()
        self._serial_port_obj.write(format_command("name {}".format(sensor_name)))  # Set the new sensor name

        # Read all the data from the serial port, until character '>'
        self.serial_ipr_read_text_from_sensor()

    def serial_ipr_start_binary_read(self):
        # Send command to sensor to start the binary datastream from the sensor to the PC
        self._serial_port_obj.write(format_command("<scanmb-start>"))  # Sending the start sequence
        self.is_binary_reading_running = True

    def serial_ipr_stop_binary_read(self):
        # Send command to sensor to stop the binary datastream
        self._serial_port_obj.write(format_command("<scanmb-stop>"))  # Sending the stop sequence
        self.is_binary_reading_running = False

    def serial_ipr_check_if_data_reading(self):
        # Check if the sensor outputs binary data
        if self.is_binary_reading_running:
            # If the sensor is sending continuous binary data, send the command to stop
            self.serial_ipr_stop_binary_read()
            # Routine to read the last bytes in the buffer to clear it. Exit once no more bytes are available for read
            _stop_character_found = False
            _telegram = list()
            # Read the serial port until the bytes read are empty (no more bytes)
            while not _stop_character_found:
                data = self.serial_read_binary()    # Read 1 byte at a time
                if data == b'':     # If no byte is read. The serial port reached timeout value
                    _stop_character_found = True

    def serial_ipr_read_telegram(self):
        _start_char_found = False
        _telegram = list()
        while not _start_char_found:
            data = self.serial_read_binary().hex()
            if data == '08':
                _start_char_found = True
            else:
                _telegram.append(data)
        return ''.join(_telegram)

    def serial_ipr_read_text_from_sensor(self):
        _stop_character_found = False
        _telegram = list()
        while not _stop_character_found:
            data = self.serial_read_binary()
            if data == b'>':
                _stop_character_found = True
            else:
                if data not in (b'\n', b'\r', b'$'):
                    _telegram.append(data.decode("utf-8"))
                elif data == b'\r':
                    if len(_telegram) >= 1:
                        if _telegram[-1] != "\n":
                            _telegram.append("\n")

        return _telegram

