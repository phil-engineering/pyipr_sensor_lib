from pyipr_sensor_lib.ipr_sensor_decoder import IPRSensorDecoder
from pyipr_sensor_lib.ipr_serial_interface import IPRSerialInterface

# Matplotlib is only used at this level to plot the data. The IPR library has no dependence on Matplotlib
import matplotlib.pyplot as plt

# *****************************************************************************************
# Using the library to parse binary data coming from the sensor previously saved in a file
# Use the code below as an example to
# *****************************************************************************************
# Read the entire file as a single byte string
binary_file_path = "./"
binary_file_name = 'binary_data_example_01.bin'

# Create an object to parse the data from the sensor or a binary file
ipr_obj = IPRSensorDecoder()
telegram_list = ipr_obj.load_from_binary_file(binary_file_path, binary_file_name)

strain_list = list([list(),list(),list()])
acceleration_list = list([list(),list(),list()])
environment_list = list([list(),list(),list(),list()])
# Analyse each telegram in the list. Each telegram contains either Strain, Acceleration, or Environment data
for _telegram in telegram_list:
    ipr_obj.analyse_packet(_telegram)
    if ipr_obj.ipr_decoder_is_packet_valid():
        if ipr_obj.get_packet_type() == ipr_obj.TYPE_STRAIN:
            strain_list[0].append(ipr_obj.get_strain_xyz(ipr_obj.STRAIN_AXIS_X))    # Get Strain X scaled value
            strain_list[1].append(ipr_obj.get_strain_xyz(ipr_obj.STRAIN_AXIS_Y))    # Get Strain Y scaled value
            strain_list[2].append(ipr_obj.get_strain_xyz(ipr_obj.STRAIN_AXIS_Z))    # Get Strain Z scaled value
        if ipr_obj.get_packet_type() == ipr_obj.TYPE_ACCELERATION:
            acceleration_list[0].append(ipr_obj.get_acceleration_xyz(ipr_obj.ACCEL_AXIS_X))    # Get Acceleration X scaled value
            acceleration_list[1].append(ipr_obj.get_acceleration_xyz(ipr_obj.ACCEL_AXIS_Y))    # Get Acceleration Y scaled value
            acceleration_list[2].append(ipr_obj.get_acceleration_xyz(ipr_obj.ACCEL_AXIS_Z))    # Get Acceleration Z scaled value
        if ipr_obj.get_packet_type() == ipr_obj.TYPE_ENVIRONMENT:
            environment_list[0].append(ipr_obj.get_environment(ipr_obj.ENVIRONMENT_VBAT))  # Get Battery Voltage
            environment_list[1].append(ipr_obj.get_environment(ipr_obj.ENVIRONMENT_PRES))  # Get Pressure
            environment_list[2].append(ipr_obj.get_environment(ipr_obj.ENVIRONMENT_HUMI))  # Get Humidity
            environment_list[3].append(ipr_obj.get_environment(ipr_obj.ENVIRONMENT_TEMP))  # Get Temperature

# The code below allows to plot the scaled value of strain X, Y, Z
fig, axs = plt.subplots(3)
# Setup the graph title and subtitles
fig.suptitle('Example: Plotting uStrain with Matplotlib')
axs[0].set_title('uStrain X')
axs[1].set_title('uStrain Y')
axs[2].set_title('uStrain Z')
# Plot the data in each subplot
axs[0].plot(range(0, len(strain_list[0])), strain_list[0], 'tab:blue')
axs[1].plot(range(0, len(strain_list[1])), strain_list[1], 'tab:orange')
axs[2].plot(range(0, len(strain_list[2])), strain_list[2], 'tab:green')
# Remove the X axis for subplots
for ax in axs.flat:
    ax.label_outer()
# Display the plot
plt.show()

# The code below allows to plot the scaled value of acceleration X, Y, Z
fig, axs = plt.subplots(3)
# Setup the graph title and subtitles
fig.suptitle('Example: Plotting acceleration with Matplotlib')
axs[0].set_title('Acceleration X')
axs[1].set_title('Acceleration Y')
axs[2].set_title('Acceleration Z')
# Plot the data in each subplot
axs[0].plot(range(0, len(acceleration_list[0])), acceleration_list[0], 'tab:blue')
axs[1].plot(range(0, len(acceleration_list[1])), acceleration_list[1], 'tab:orange')
axs[2].plot(range(0, len(acceleration_list[2])), acceleration_list[2], 'tab:green')
# Remove the X axis for subplots
for ax in axs.flat:
    ax.label_outer()
# Display the plot
plt.show()

# The code below allows to plot the scaled value of environment
fig, axs = plt.subplots(4)
# Setup the graph title and subtitles
fig.suptitle('Example: Plotting environment data with Matplotlib')
axs[0].set_title('Battery Voltage')
axs[1].set_title('Pressure')
axs[2].set_title('Humidity')
axs[3].set_title('Temperature')
# Plot the data in each subplot
axs[0].plot(range(0, len(environment_list[0])), environment_list[0], 'tab:blue')
axs[1].plot(range(0, len(environment_list[1])), environment_list[1], 'tab:orange')
axs[2].plot(range(0, len(environment_list[2])), environment_list[2], 'tab:green')
axs[3].plot(range(0, len(environment_list[3])), environment_list[3], 'tab:red')
# Remove the X axis for subplots
for ax in axs.flat:
    ax.label_outer()
# Display the plot
plt.show()
