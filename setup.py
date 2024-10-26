from setuptools import setup

setup(
    name='pyipr_sensor_lib',
    version='0.1.0',
    description='A example Python package',
    url='https://github.com/phil-engineering/pyipr_sensor_lib',
    author='Philippe Bourgault',
    packages=['pyipr_sensor_lib'],
    install_requires=['pyserial>=3.5',
                      'numpy',
                      ],
)