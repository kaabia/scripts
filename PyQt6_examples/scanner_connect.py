#!/usr/bin/env python

from PyQt6.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QLowEnergyController
from PyQt6.QtCore import QCoreApplication, QLoggingCategory
import enum

class BluetoothScanner:

    class DiscoveryStatus(enum.Flag):
        BLE_DISCOVERY_NOT_STARTED   = 0x00
        BLE_DISCOVERY_ONGOING       = 0x01
        BLE_DISCOVERY_FINISHED      = 0x02

    DEFAULT_DEVICE_NAME_FILTER = "CONTI_"
    m_device = list()
    m_device_name_filter = str(DEFAULT_DEVICE_NAME_FILTER)
    mStatus = DiscoveryStatus.BLE_DISCOVERY_NOT_STARTED

    def __init__(self):
        #QLoggingCategory.setFilterRules("qt.bluetooth* = true")
        self.mStatus = self.DiscoveryStatus.BLE_DISCOVERY_NOT_STARTED
        # Create a QBluetoothDeviceDiscoveryAgent object
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent()
        # set Low Energy Discovery Timeout to 10 seconds
        self.discovery_agent.setLowEnergyDiscoveryTimeout(3000)
        # Connect the deviceDiscovered signal to the device_discovered method
        self.discovery_agent.deviceDiscovered.connect(self.device_discovered)
        # Connect the finished signal to the quit method of the QCoreApplication object
        self.discovery_agent.finished.connect(self.discovery_finished)

    def start(self):
        # Start the device discovery process
        print("Scanning for Bluetooth devices...")
        self.discovery_agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)
        self.mStatus = self.DiscoveryStatus.BLE_DISCOVERY_ONGOING

    #def device_discovered(self, device_info):
    def device_discovered(self, device_info, **kwargs):
        # This method is called when a device is discovered during the scan
        # Print the device's address and name to the console
        if(True ==  str(device_info.name()).startswith(self.m_device_name_filter)):
            self.m_device.append(device_info)
            print(f"\tFound device: {device_info.address().toString()} , Name {device_info.name()}")
            print(f"Connecting to device: {device_info.address().toString()}")
            self.controller = QLowEnergyController.createCentral(self.m_device[0])

    def get_queued_devices(self):
        print("Get discovered devices list :")
        #discovered_devices  = self.discovery_agent.discoveredDevices()
        #for dev in discovered_devices:
        #    print(f"DEV : Mac = {dev.address().toString()}, Name = {dev.name()}")

        for dev in self.m_device:
            print(f"DEV : Mac = {dev.address().toString()}, Name = {dev.name()}")

        return self.m_device

    def set_filter(self, device_name:str = DEFAULT_DEVICE_NAME_FILTER ):
        self.m_device_name_filter = device_name

    def discovery_finished(self, *args, **kwargs):
        self.mStatus = self.DiscoveryStatus.BLE_DISCOVERY_FINISHED
        #self.get_queued_devices()
        self.controller.connected.connect(self.connected)
        self.controller.disconnected.connect(self.disconnected)
        self.controller.errorOccurred.connect(self.ConnectionError)
        self.controller.connectToDevice()
        print(f"Connect requested")

    def connected(self):
        print("Connected to device!")

    def disconnected(self):
        print("Disconnected from device!")

    def ConnectionError(self):
        print("Error Occured")

    def GetDiscoveryStatus(self):
        return self.mStatus


if __name__ == '__main__':
    # Create a QCoreApplication object to run the event loop
    app = QCoreApplication([])
    # Create a BluetoothScanner object
    scanner = BluetoothScanner()
    # Set scan filer based on device name
    scanner.set_filter(device_name="Kaabia")
    # Start the device discovery process
    scanner.start()
    # Run the event loop until the discovery process is finished
    app.exec()