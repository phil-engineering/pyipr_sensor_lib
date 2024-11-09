import regex as re

from pyipr_sensor_lib.ipr_parser import *

class IPRSensorDecoder:

    def __init__(self):
        self._list_of_data = 0
        # self._serial_port_obj = IPRSerialInterface()
        self.ipr_parser_obj = None
        print("Initiating IPRSensorDecoder -> DONE")

    def decode_from_binary_file(self, filepath, filename):
        with open(filepath + filename, 'rb') as fh:
            content = fh.read().hex()
        for _data in re.split('08', content)[1:]:
            self.analyse_packet(_data)

    def analyse_packet(self, packet):
        self.ipr_parser_obj = IPRParser(packet)
        if self.ipr_parser_obj.parser_check_telegram_validity(packet):
            self.ipr_parser_obj.parser_hex_to_byte(packet, len(packet))
            self.ipr_parser_obj.parser_get_header()

            if self.ipr_parser_obj.parser_get_id_name() == "STRAIN":
                if len(packet) >= self.ipr_parser_obj.MIN_PACKET_LENGTH_STRAIN:
                    self.ipr_parser_obj.parser_get_strain()
                    self.ipr_parser_obj.parser_scale_strain_xyz()
                    self.ipr_parser_obj.parser_scale_strain_p1p2()
                    self.print_strain()
                else:
                    print("STRAIN: Data string too short to be process")
            elif self.ipr_parser_obj.parser_get_id_name() == "ENVIRONMENT":
                if len(packet) >= self.ipr_parser_obj.MIN_PACKET_LENGTH_ENVIRONMENT:
                    self.ipr_parser_obj.parser_get_environment()
                    self.ipr_parser_obj.parser_scale_environment()
                    self.print_environment()
                else:
                    print("ENVIRONMENT: Data string too short to be process")
            elif self.ipr_parser_obj.parser_get_id_name() == "ACCELERATION":
                if len(packet) >= self.ipr_parser_obj.MIN_PACKET_LENGTH_ACCELERATION:
                    self.ipr_parser_obj.parser_get_acceleration()
                    self.ipr_parser_obj.parser_scale_acceleration()
                    self.print_acceleration()
                else:
                    print("ACCELERATION: Data string too short to be process")

    def print_strain(self):
        print("STRAIN X: {:.2f} uStrain ; STRAIN Y: {:.2f} uStrain ; STRAIN Z: {:.2f} uStrain"
              .format(self.ipr_parser_obj.parser_scale_strain_xyz()[0],
                      self.ipr_parser_obj.parser_scale_strain_xyz()[1],
                      self.ipr_parser_obj.parser_scale_strain_xyz()[2]))
        print("STRAIN P1: {:.2f} uStrain ; STRAIN P2: {:.2f} uStrain ; STRAIN ANGLE: {:.2f} degrees"
              .format(self.ipr_parser_obj.parser_scale_strain_p1p2()[3],
                      self.ipr_parser_obj.parser_scale_strain_p1p2()[4],
                      self.ipr_parser_obj.parser_scale_strain_p1p2()[5]))

    def print_environment(self):
        print("VBATT: {:.2f} V ; PRESSURE: {:.2f} hP ; HUMIDITY: {:.2f}% ; TEMPERATURE: {:.2f}°C"
              .format(self.ipr_parser_obj.parser_scale_environment()[0],
                      self.ipr_parser_obj.parser_scale_environment()[1],
                      self.ipr_parser_obj.parser_scale_environment()[2],
                      self.ipr_parser_obj.parser_scale_environment()[3]))

    def print_acceleration(self):
        print("ACC. X: {:.2f} G ; ACC. Y: {:.2f} G ; ACC. Z: {:.2f} G"
              .format(self.ipr_parser_obj.parser_scale_acceleration()[0],
                      self.ipr_parser_obj.parser_scale_acceleration()[1],
                      self.ipr_parser_obj.parser_scale_acceleration()[2]))