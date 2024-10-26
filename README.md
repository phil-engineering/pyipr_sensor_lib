# PyIPR Sensor Lib

Python library for IPR strain sensor.

## Getting Started
The code below can be used as a first example to explore the sensor capabilities.
```python
from pyipr_sensor_lib.ipr_sensor_decoder import IPRSensorDecoder
from pyipr_sensor_lib.ipr_serial_interface import IPRSerialInterface

# Create an object for the sensor connected on the serial port
obj = IPRSerialInterface()
obj.serial_setup("COM5")
obj.serial_open()
# Initiate the binary data stream from the sensor
obj.serial_ipr_start_binary_read()

# Create a parser object
ipr_obj = IPRSensorDecoder()
# Read in continuous mode the binary data, parse it and display the converted values
while True:
    ipr_obj.analyse_packet(obj.serial_ipr_read_telegram())
```
Output example:
```python
STRAIN X: -2674.73 uStrain ; STRAIN Y: 1030.04 uStrain ; STRAIN Z: 1784.62 uStrain
STRAIN P1: 1410.99 uStrain ; STRAIN P2: 1599.27 uStrain ; STRAIN ANGLE: -42.33 degrees
STRAIN X: 2951.65 uStrain ; STRAIN Y: 1029.30 uStrain ; STRAIN Z: 2347.25 uStrain
STRAIN P1: 1973.63 uStrain ; STRAIN P2: 1599.27 uStrain ; STRAIN ANGLE: -81.71 degrees
STRAIN X: -2674.73 uStrain ; STRAIN Y: 1217.58 uStrain ; STRAIN Z: 2534.80 uStrain
STRAIN P1: 2161.17 uStrain ; STRAIN P2: 1599.27 uStrain ; STRAIN ANGLE: -81.71 degrees
STRAIN X: 2951.65 uStrain ; STRAIN Y: -95.97 uStrain ; STRAIN Z: 1409.52 uStrain
STRAIN P1: 660.81 uStrain ; STRAIN P2: 1599.27 uStrain ; STRAIN ANGLE: 64.57 degrees
ACC. X: 13.48 G ; ACC. Y: -15.02 G ; ACC. Z: -13.01 G
```

### Other functionalities
Get the sensor system status:
```python
print(obj.serial_ipr_get_system_status())
```
Output:
```python
Humidty      : 48.0 %
Pressure     : 999.2 HPa
Temperature  : +21.1 C
Battery      : 2.92 V
Material     : MILD-STEEL
Time (RTC)   : 2001-01-01-00-11-17
Firmware Ver : 2.00A
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
