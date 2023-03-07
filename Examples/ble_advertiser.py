from PySide6.QtCore import QByteArray, QCoreApplication
from PySide6.QtBluetooth import QLowEnergyAdvertisingData, QBluetoothUuid, \
                                QLowEnergyCharacteristicData, QLowEnergyCharacteristic, QLowEnergyServiceData, \
                                QLowEnergyController, QLowEnergyAdvertisingParameters
from typing import Sequence


# Define Bluetooth Advertiser class
class BluetoothAdvertiser:

    # Initialize the class with required Advertising Data and Parameters using QLowEnergyAdvertisingData class
    def __init__(self):
        # Set up Advertising Data
        self.m_advertisingData = QLowEnergyAdvertisingData()
        # Set discoverability for other devices to establish connection
        self.m_advertisingData.setDiscoverability(QLowEnergyAdvertisingData.Discoverability.DiscoverabilityGeneral)
        # Include power level in advertising payload
        self.m_advertisingData.setIncludePowerLevel(True)
        # Set Device name
        self.m_advertisingData.setLocalName("BLE_ADVERTISER")
        # Set default Heart rate service to offerin its minimal form
        self.m_advertisingData.setServices([QBluetoothUuid.ServiceClassUuid.HeartRate])

        # Add caracteristic
        self.charData = QLowEnergyCharacteristicData()
        self.charData.setUuid(QBluetoothUuid.CharacteristicType.HeartRateMeasurement)
        self.charData.setValue(QByteArray(2,0))
        self.charData.setProperties(QLowEnergyCharacteristic.PropertyType.Notify)
        # Add Service
        self.serviceData = QLowEnergyServiceData()
        self.serviceData.setType(QLowEnergyServiceData.ServiceType.ServiceTypePrimary)
        self.serviceData.setUuid(QBluetoothUuid.ServiceClassUuid.HeartRate)
        self.serviceData.addCharacteristic(self.charData)
        # Advertising and Listening for Incoming Connections
        self.leController = QLowEnergyController.createPeripheral()
        self.leController.addService(self.serviceData)

    # Start advertising
    def startAdvertising(self):
        #self.leController.connect(self.controller_notification)
        parameters = QLowEnergyAdvertisingParameters()
        # Start advertising with the given advertising data
        self.leController.startAdvertising(parameters,
                                           self.m_advertisingData,
                                           self.m_advertisingData)

    def controller_notification(self, characteristic, newValue):
        print(f"Notification received. Characteristic: {characteristic.uuid()}, Value: {newValue}")


        # For specific aspects such as setting the advertising interval or controlling which devices are allowed to connect
        # QLowEnergyAdvertisingParameters  class is configured


if __name__ == '__main__':
    # Create a QCoreApplication object to run the event loop
    app = QCoreApplication([])
    # Create a BluetoothScanner object
    advertiser = BluetoothAdvertiser()
    # Set advertising
    advertiser.startAdvertising()
    # Run the event loop until the discovery process is finished
    app.exec()