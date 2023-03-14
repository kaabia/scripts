#!/usr/bin/env python

from PyQt6.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QLowEnergyController
from PyQt6.QtCore import QCoreApplication, QLoggingCategory, QTimer
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

    def set_filter(self, device_name:str = DEFAULT_DEVICE_NAME_FILTER ):
        self.m_device_name_filter = device_name

    def startDiscovering(self):
        # Start the device discovery process
        print("Scanning for Bluetooth devices...")
        self.discovery_agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)
        self.mStatus = self.DiscoveryStatus.BLE_DISCOVERY_ONGOING

    def stopDiscovering(self):
        # Start the device discovery process
        print("Stop scanning for Bluetooth devices...")
        self.discovery_agent.stop()

    def connectTo(self, dev):
        print(f"Connecting to device: {dev.address().toString()}")
        self.controller = QLowEnergyController.createCentral(dev)
        self.controller.connected.connect(self.connected)
        self.controller.disconnected.connect(self.disconnected_from_device)
        self.controller.errorOccurred.connect(self.error_hander)
        #self.controller.stateChanged.connect(self.state_changed)
        self.controller.connectToDevice()

    def disconnect(self):
        # Disconnect from remote BLE device
        print("Disconnect from device is requested ")
        self.controller.disconnectFromDevice()

    def GetDiscoveryStatus(self):
        return self.mStatus

    # discovery_agent callbacks
    def device_discovered(self, device_info):
        # This method is called when a device is discovered during the scan
        # Print the device's address and name to the console
        if(True ==  str(device_info.name()).startswith(self.m_device_name_filter)):
            print(f"\tFound device: {device_info.address().toString()} , Name {device_info.name()}")
            self.m_device.append(QBluetoothDeviceInfo(device_info))


    def discovery_finished(self, *args, **kwargs):
        self.mStatus = self.DiscoveryStatus.BLE_DISCOVERY_FINISHED
        device_list = self.get_queued_devices()
        print(f"Get discovered devices list : len = {len(device_list)}")
        for dev in device_list:
            print(f"DEV : Mac = {dev.address().toString()}, Name = {dev.name()}")
        conn_dev = QBluetoothDeviceInfo(device_list[0])
        self.connectTo(conn_dev)

    def get_queued_devices(self):
        return self.m_device

    # CONTROLER signals callback:
    def state_changed(self, *args, **Kwargs):
        if args[0] == QLowEnergyController.ControllerState.UnconnectedState:
            print("ADVERTISER STATE >> IDLE ")
        elif args[0] == QLowEnergyController.ControllerState.ConnectingState:
            print("ADVERTISER STATE >> CONNECTING ")
        elif args[0] == QLowEnergyController.ControllerState.ConnectedState:
            print("ADVERTISER STATE >> CONNECTED ")
        elif args[0] == QLowEnergyController.ControllerState.DiscoveringState:
            print("ADVERTISER STATE >> DISCOVERING ")
        elif args[0] == QLowEnergyController.ControllerState.DiscoveredState:
            print("ADVERTISER STATE >> DISCOVERED ")
        elif args[0] == QLowEnergyController.ControllerState.ClosingState:
            print("ADVERTISER STATE >> CLOSING ")

    def connected(self):
        print("Connected to device!")
        QTimer.singleShot(10000, self.disconnect)

    def disconnected_from_device(self):
        print("Disconnected from device!")
        QCoreApplication.quit()

    def error_hander(self, *args, **Kwargs):
        print(f"Error Occured {args}, {Kwargs}")
        QCoreApplication.quit()

if __name__ == '__main__':
    # Create a QCoreApplication object to run the event loop
    app = QCoreApplication([])
    # Create a BluetoothScanner object
    scanner = BluetoothScanner()
    # Set scan filer based on device name
    scanner.set_filter(device_name="CONTI_001")
    # Start the device discovery process
    scanner.startDiscovering()
    # Run the event loop until the discovery process is finished
    app.exec()
