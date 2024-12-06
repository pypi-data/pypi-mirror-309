#!/usr/bin/env python3
"""
Module: nexgraph.py
Description: NexGraph Python library for Nextech force gauges.
Author: Shawn Myratchapon
Website: https://simplyshawn.co.th
NexGraph: https://nexgraphapp.com
Version: 1.0.3
"""

import time
import platform
import serial
import serial.tools.list_ports

class NexGraph:
    """
        NexGraph Python Library
        - Finds and connects to Nextech devices over USB serial port
        - Send and receive data to and from the device
            - Download saved values
            - Get device information
            - Query different force value formats
            - Send commands Print, Reset, Zero, Unit, and Mode
        
        Attributes:
        - `device_info`: string: Device model, and details.
        - `device_path`: string: Path or port device is connected to.
        
        Methods:
        - `find()`: Searches for connected USB serial devices.
        - `connect()`: Tries to connect to the device on device_path.
        - `get_info()`: Returns the device information.
        - `print_value()`: Returns the current value or max value from the device.
        - `zero()`: Zeroes the current value on the device.
        - `mode()`: Changes the mode (track and peak) on the device.
        - `unit()`: Changes the unit of measurement on the device.
        - `reset()`: Resets the value on the device.
        - `peak_tension()`: Returns the current peak tension value.
        - `peak_compression()`: Returns the current peak compression value.
        - `download()`: Return the data stored on the device memory.
        - `mini_output()`: Returns the current value in mini format.
        - `short_output()`: Returns the current value in short format.
        - `long_output()`: Returns the current value in long format.
    """

    def __init__(self,device_path = ""):
        self.device_info: str = ""
        self.device_path: str = device_path if device_path else ""
        self.device_command: dict = {
            "svalue": 'v'.encode(),
            "print": 'x'.encode(),
            "lvalue": 'l'.encode(),
            "mvalue": 'L'.encode(),
            "ptension": 'p'.encode(),
            "pcompress": 'c'.encode(),
            "info": '!'.encode(),
            "download": 'd'.encode(),
            "zero": 'z'.encode(),
            "reset": 'r'.encode(),
            "unit": 'u'.encode(),
            "mode": 'm'.encode()
        }
        self.usb_serial = None

    def print_error(self, error_type):
        """Prints the corresponding error message."""
        match error_type:
            case "os":
                print(f"OS error connecting to device on {self.device_path}.")
            case "perm":
                print(f"Permission error connecting to device on {self.device_path}.")

    def find(self) -> bool:
        """Finds USB serial devices.
        
        Returns: boolean: "True" if a device was found.
        """
        usb_ports = serial.tools.list_ports.comports(include_links=True)
        device_found: bool = False

        for port in usb_ports:
            if platform.system() == 'Windows':
                if "COM" in port.device and "FTDI" in port.manufacturer:
                    device_found = True
                    self.device_path = port.device
            elif platform.system() == 'Darwin':
                if "usbserial" in port.device and "FTDI" in port.manufacturer:
                    self.device_path = f"/dev/tty.{port.device.split('.')[1]}"
                    device_found = True
            elif platform.system() == 'Linux':
                if "ttyUSB" in port.device and "FTDI" in port.manufacturer:
                    self.device_path = port.device
                    device_found = True

        return device_found

    def connect(self) -> bool:
        """Connect to Nextech force gauge.

        Returns: boolean: "True" if connection was successful.
        """
        status: bool = False
        if self.device_path:
            self.usb_serial = serial.Serial(port=self.device_path,
                                            bytesize=8,
                                            baudrate=38400,
                                            timeout=2,
                                            stopbits=serial.STOPBITS_ONE)
            try:
                self.usb_serial.write(self.device_command['info'])
                time.sleep(0.1)

                if self.usb_serial.in_waiting:
                    self.device_info += self.usb_serial.readline().decode("Ascii")
                    arr_info = self.device_info.split()

                    if arr_info and ("DFS" in arr_info[0] or "DFT" in arr_info[0]):
                        status = True
                        return status

                return status
            except PermissionError:
                self.print_error("perm")
                return status
            except OSError:
                self.print_error("os")
                return status
        else:
            print("The device connection path is empty.")
            return status

    def get_info(self) -> str:
        """Gets the device details.

        Returns:
            string: Model number, Current offset, Overload counter."""
        return self.device_info

    def print_value(self) -> str:
        """Send a print command to the device.
        
        Returns:
            boolean: "True" if successful."""
        try:
            print_output: str = ""
            self.usb_serial.write(self.device_command['print'])
            time.sleep(0.1)
            while self.usb_serial.in_waiting:
                print_output += self.usb_serial.readline().decode("Ascii")

            return print_output
        except OSError:
            self.print_error("os")
            return None

    def zero(self) -> bool:
        """Send the zero/tare command to the device.
        
        Returns:
            boolean: "True" if successful."""
        status: bool = False
        try:
            self.usb_serial.write(self.device_command['zero'])
            status = True
            return status
        except OSError:
            self.print_error("os")
            return status

    def mode(self) -> bool:
        """Send the change mode command to the device.
        
        Returns:
            boolean: "True" if successful."""
        status: bool = False
        try:
            self.usb_serial.write(self.device_command['mode'])
            status = True
            return status
        except OSError:
            self.print_error("os")
            return status

    def unit(self) -> bool:
        """Send the change unit command to the device.
        
        Returns:
            boolean: "True" if successful."""
        status: bool = False
        try:
            self.usb_serial.write(self.device_command['unit'])
            status = True
            return status
        except OSError:
            self.print_error("os")
            return status

    def reset(self) -> bool:
        """Send the reset values command to the device.
        
        Returns:
            boolean: "True" if successful."""
        status: bool = False
        try:
            self.usb_serial.write(self.device_command['reset'])
            status=True
            return status
        except OSError:
            self.print_error("os")
            return status

    def peak_tension(self) -> str:
        """Get the current peak tension value from the device.
        
        Returns:
            string: Current peak tension value."""
        try:
            peak_tension: str = ""
            self.usb_serial.write(self.device_command['ptension'])
            time.sleep(0.1)
            while self.usb_serial.in_waiting:
                peak_tension += self.usb_serial.readline().decode("Ascii")

            return peak_tension
        except OSError:
            self.print_error("os")
            return None

    def peak_compression(self) -> str:
        """Get the current peak compression value from the device.
        
        Returns:
            string: Current peak compression value."""
        try:
            peak_compression: str = ""
            self.usb_serial.write(self.device_command['pcompress'])
            time.sleep(0.1)
            while self.usb_serial.in_waiting:
                peak_compression += self.usb_serial.readline().decode("Ascii")

            return peak_compression
        except OSError:
            self.print_error("os")
            return None

    def download(self) -> str:
        """Download stored data from device memory.
        
        Returns:
            string: Stored tension and compression values."""
        try:
            self.usb_serial.write(self.device_command["download"])
            time.sleep(0.1)
            mem_data: str = ""
            while self.usb_serial.in_waiting > 0:
                try:
                    mem_data += self.usb_serial.read_all().decode("Ascii")
                    time.sleep(0.1)
                except UnicodeDecodeError:
                    continue
            return mem_data
        except OSError:
            self.print_error("os")
            return None

    def _get_output(self, command_key: str) -> str:
        """Helper method to get output from Nextech Gauge.
        
        Args:
            command_key (str): The command key to send to the device.
        
        Returns:
            str: Current value from the device.
        """
        try:
            self.usb_serial.write(self.device_command[command_key])
            time.sleep(0.1)
            s_output: str = ""
            while self.usb_serial.in_waiting:
                s_output += self.usb_serial.readline().decode("Ascii")
            return s_output
        except (OSError, serial.SerialException) as e:
            self.print_error(str(e))
            return ""

    def mini_output(self) -> str:
        """Get mini output from Nextech Gauge.
        
        Returns:
            str: Current value from the device. Mini format.
        """
        return self._get_output("mvalue")

    def short_output(self) -> str:
        """Get short output from Nextech Gauge.
        
        Returns:
            str: Current value from the device. Short format.
        """
        return self._get_output("svalue")

    def long_output(self) -> str:
        """Get the long output from Nextech Gauge.
        
        Returns:
            str: Current value from the device. Long format.
        """
        return self._get_output("lvalue")

    def disconnect(self) -> bool:
        """Disconnect from the Nextech Gauge.
        
        Returns:
            boolean: "True" if garcefully disconnected."""
        status: bool = False
        try:
            self.usb_serial.close()
            self.usb_serial = None
            status = True
            return status
        except OSError:
            self.print_error("os")
            return status
