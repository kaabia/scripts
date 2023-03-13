#!/usr/bin/env python

from PyQt6.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QLowEnergyController
from PyQt6.QtCore import QCoreApplication, QLoggingCategory
import enum
from time import sleep

class BluetoothScanner:

    class DiscoveryStatus(enum.Flag):
        BLE_DISCOVERY_NOT_STARTED   = 0x00
        BLE_DISCOVERY_ONGOING       = 0x01
        BLE_DISCOVERY_FINISHED      = 0x02

    DEFAULT_DEVICE_NAME_FILTER = "CONTI_"

    m_device_name_filter = str(DEFAULT_DEVICE_NAME_FILTER)
    mStatus = DiscoveryStatus.BLE_DISCOVERY_NOT_STARTED

    def __init__(self):
        #QLoggingCategory.setFilterRules("qt.bluetooth* = true")
        self.mStatus = self.DiscoveryStatus.BLE_DISCOVERY_NOT_STARTED
        # Create a QBluetoothDeviceDiscoveryAgent object
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent()
        # set Low Energy Discovery Timeout to 10 seconds
        self.discovery_agent.setLowEnergyDiscoveryTimeout(5000)
        # Connect the deviceDiscovered signal to the device_discovered method
        self.discovery_agent.deviceDiscovered.connect(self.device_discovered)
        # Connect the finished signal to the quit method of the QCoreApplication object
        self.discovery_agent.finished.connect(self.discovery_finished)

        self.m_device = list()

    def start(self):
        # Start the device discovery process
        print("Scanning for Bluetooth devices...")
        self.discovery_agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)
        self.mStatus = self.DiscoveryStatus.BLE_DISCOVERY_ONGOING

    def device_discovered(self, device_info):
        # This method is called when a device is discovered during the scan
        # Print the device's address and name to the console
        if(True ==  str(device_info.name()).startswith(self.m_device_name_filter)):
            print(f"\tFound device: {device_info.address().toString()} , Name {device_info.name()}")
            self.m_device.append(QBluetoothDeviceInfo(device_info))

    def get_queued_devices(self):
        return self.m_device

    def set_filter(self, device_name:str = DEFAULT_DEVICE_NAME_FILTER ):
        self.m_device_name_filter = device_name

    def discovery_finished(self, *args, **kwargs):
        self.mStatus = self.DiscoveryStatus.BLE_DISCOVERY_FINISHED
        device_list = self.get_queued_devices()
        print(f"Get discovered devices list : len = {len(device_list)}")
        for dev in device_list:
            print(f"DEV : Mac = {dev.address().toString()}, Name = {dev.name()}")
        conn_dev = QBluetoothDeviceInfo(device_list[0])
        self.connectTo(conn_dev)

    def connectTo(self, dev):
        print(f"Connecting to device: {dev.address().toString()}")
        self.controller = QLowEnergyController.createCentral(dev)
        self.controller.connected.connect(self.connected)
        self.controller.disconnected.connect(self.disconnected)
        self.controller.errorOccurred.connect(self.ConnectionError)
        self.controller.connectToDevice()


    def connected(self):
        print("Connected to device!")
        sleep(10)
        print("Time to disconnect from device!")
        self.controller.disconnect()

    def disconnected(self):
        print("Disconnected from device!")
        QCoreApplication.quit()

    def ConnectionError(self):
        print("Error Occured")
        QCoreApplication.quit()

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
