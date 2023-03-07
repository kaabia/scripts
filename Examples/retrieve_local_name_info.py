from PySide6.QtBluetooth import QBluetoothLocalDevice

localDevice = QBluetoothLocalDevice()

localDeviceName = ''
# Check if Bluetooth is available on this device
if localDevice.isValid():
    # Turn Bluetooth on
    localDevice.powerOn()
    # Read local device name
    localDeviceName = localDevice.name()
    # Make it visible to others
    localDevice.setHostMode(QBluetoothLocalDevice.HostDiscoverable)
    # Get connected devices
    remotes = localDevice.connectedDevices()
    print("Local device name:", localDeviceName)
    print("Connected devices:", len(remotes))