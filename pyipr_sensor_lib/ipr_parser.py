from array import array

class IPRParser:
    MIN_PACKET_LENGTH_STRAIN = 27
    MIN_PACKET_LENGTH_ENVIRONMENT = 1
    MIN_PACKET_LENGTH_ACCELERATION = 20

    def __init__(self, telegram):
        self._byte_data = list()
        self.invalid_data_list = list()
        self.invalid_data_number = 0

        # ID, ID_CRC, Sequence, Timestamp
        self.raw_header = array('f', [0, 0, 0, 0])
        self.packet_type = None

        self.raw_strain = array('f', [0, 0, 0, 0, 0, 0])
        self.raw_env = array('f', [0, 0, 0, 0])
        self.raw_acc = array('f', [0, 0, 0])

        self.scaled_strain = array('f', [0, 0, 0, 0, 0, 0])
        self.scaled_env = array('f', [0, 0, 0, 0])
        self.scaled_acc = array('f', [0, 0, 0])
        
        self.telegram = telegram

    @staticmethod
    def parser_compute_crc(byte0):
        # Compute the XOR between bit 1 and 0 of BYTE 0
        return bool(int(byte0, 16) & 0x02) ^ bool(int(byte0, 16) & 0x01)

    @staticmethod
    def convert_numeric_to_scale(value_to_convert, in_min, in_max, out_min, out_max):
        _interpolation = 0
        if value_to_convert != 0:
            _slope = (out_max - out_min) / (in_max - in_min)
            _offset = out_min - _slope
            # Linear slope: Y = A*X + B
            _interpolation = _slope * value_to_convert + _offset

        return _interpolation
    
    def parser_hex_to_byte(self, _data, _length):
        for i in range(0, _length, 2):
            self._byte_data.append(_data[i:i+2])

    def parser_check_telegram_validity(self, telegram):
        _is_valid = False
        if len(telegram) >= 1:
            self.parser_hex_to_byte(telegram, 2)  # Only convert the BYTE 0
            _id_crc_computed = self.parser_compute_crc(self._byte_data[0])

            # Remove the data in the list that is invalid
            if (self.parser_get_id_crc() != _id_crc_computed) or (len(telegram) <= 10):
                # print(i, _id, _id_crc, _id_crc_computed, len(i))
                self.invalid_data_list.append(telegram)
                self.invalid_data_number += 1
            else:
                _is_valid = True
            # print(_id, _id_crc, _id_crc_computed, len(i))
            # print(int(i, 16))
        else:
            self.invalid_data_list.append(telegram)
            self.invalid_data_number += 1

        return _is_valid

    def parser_get_id(self):
        self.raw_header[0] = int(self._byte_data[0], 16) & 0x03
        return self.raw_header[0]

    def parser_get_id_name(self):
        if self.parser_get_id() == 0x00:
            self.packet_type = "STRAIN"
        elif self.parser_get_id() == 0x01:
            self.packet_type = "ENVIRONMENT"
        elif self.parser_get_id() == 0x02:
            self.packet_type = "ACCELERATION"
        else:
            self.packet_type = "PACKET ERROR"
        return self.packet_type

    def parser_get_id_crc(self):
        self.raw_header[1] = (int(self._byte_data[0], 16) & 0x04) >> 2
        return self.raw_header[1]

    def parser_get_sequence(self):
        self.raw_header[2] = int(self._byte_data[0], 16) & 0x38
        return self.raw_header[2]

    def parser_get_timestamp(self):
        self.raw_header[3] = (((int(self._byte_data[4], 16) & 0x01) << 26) + (int(self._byte_data[3], 16) << 18) + (int(self._byte_data[2], 16) << 10)
                           + (int(self._byte_data[1], 16) << 2) + ((int(self._byte_data[0], 16) & 0xC0) >> 6))
        return self.raw_header[3]

    def parser_get_header(self):
        self.parser_get_id()
        self.parser_get_id_crc()
        self.parser_get_sequence()
        self.parser_get_timestamp()

    def parser_get_strain(self):
        # Extract strain XYZ
        self.raw_strain[0] = ((int(self._byte_data[5], 16) & 0x3F) << 7) + ((int(self._byte_data[4], 16) & 0xFE) >> 1)
        self.raw_strain[1] = ((int(self._byte_data[7], 16) & 0x07) << 10) + (int(self._byte_data[6], 16) << 2) + ((int(self._byte_data[5], 16) & 0xC0) >> 6)
        self.raw_strain[2] = (int(self._byte_data[8], 16) << 5) + ((int(self._byte_data[7], 16) & 0xF8) >> 3)
        # Extract principal strain P1, P2 and angle
        self.raw_strain[3] = ((int(self._byte_data[10], 16) & 0x1F) << 8) + int(self._byte_data[9], 16)
        self.raw_strain[4] = (((int(self._byte_data[12], 16) & 0x03) << 11) + ((int(self._byte_data[11], 16) & 0x1F) << 3) + ((int(self._byte_data[10], 16) & 0xE0) >> 5))
        self.raw_strain[5] = ((int(self._byte_data[13], 16) & 0x7F) << 6) + ((int(self._byte_data[12], 16) & 0xFC) >> 2)
        return self.raw_strain

    def parser_get_environment(self):
        # VBatt voltage
        self.raw_env[0] = ((int(self._byte_data[5], 16) & 0x02) << 7) + ((int(self._byte_data[4], 16) & 0xFE) >> 1)
        # Pressure
        self.raw_env[1] = (int(self._byte_data[6], 16) << 6) + ((int(self._byte_data[5], 16) & 0xFC) >> 2)
        # Humidity
        self.raw_env[2] = ((int(self._byte_data[8], 16) & 0x02) << 8) + int(self._byte_data[7], 16)
        # Temperature
        self.raw_env[3] = ((int(self._byte_data[9], 16) & 0x1F) << 6) + ((int(self._byte_data[8], 16) & 0xFC) >> 2)
        return self.raw_env

    def parser_get_acceleration(self):
        self.raw_acc[0] = ((int(self._byte_data[5], 16) & 0x1F) << 7) + ((int(self._byte_data[4], 16) & 0xFE) >> 1)
        self.raw_acc[1] = ((int(self._byte_data[7], 16) & 0x01) << 11) + (int(self._byte_data[6], 16) << 3) + ((int(self._byte_data[5], 16) & 0xE0) >> 5)
        self.raw_acc[2] = ((int(self._byte_data[8], 16) & 0x1F) << 7) + ((int(self._byte_data[7], 16) & 0xFE) >> 1)
        return self.raw_acc

    def parser_scale_strain_xyz(self):
        self.scaled_strain[0] = self.convert_numeric_to_scale(self.raw_strain[0], 1, 8191, -3000, 3000)
        self.scaled_strain[1] = self.convert_numeric_to_scale(self.raw_strain[1], 1, 8191, -3000, 3000)
        self.scaled_strain[2] = self.convert_numeric_to_scale(self.raw_strain[2], 1, 8191, -3000, 3000)
        return self.scaled_strain

    def parser_scale_strain_p1p2(self):
        self.scaled_strain[3] = self.convert_numeric_to_scale(self.raw_strain[3], 1, 8191, -3000, 3000)
        self.scaled_strain[4] = self.convert_numeric_to_scale(self.raw_strain[4], 1, 8191, -3000, 3000)
        self.scaled_strain[5] = self.convert_numeric_to_scale(self.raw_strain[5], 1, 8191, -90, 90)
        return self.scaled_strain

    def parser_scale_environment(self):
        self.scaled_env[0] = self.convert_numeric_to_scale(self.raw_env[0], 1, 511, 0, 4)
        self.scaled_env[1] = self.convert_numeric_to_scale(self.raw_env[1], 1, 16383, 0, 1200)
        self.scaled_env[2] = self.convert_numeric_to_scale(self.raw_env[2], 1, 1023, 0, 100)
        self.scaled_env[3] = self.convert_numeric_to_scale(self.raw_env[3], 1, 2047, -60, 115)
        return self.scaled_env

    def parser_scale_acceleration(self):
        self.scaled_acc[0] = self.convert_numeric_to_scale(self.raw_acc[0], 1, 4095, -16, 16)
        self.scaled_acc[1] = self.convert_numeric_to_scale(self.raw_acc[1], 1, 4095, -16, 16)
        self.scaled_acc[2] = self.convert_numeric_to_scale(self.raw_acc[2], 1, 4095, -16, 16)
        return self.scaled_acc
