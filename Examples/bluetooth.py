import threading
import subprocess
import time
from collections import defaultdict

class Bluetoothctl:
    def __init__(self):
        self.process = subprocess.Popen(["bluetoothctl"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.callbacks = defaultdict(list)
        self.running = True
        self.output_thread = threading.Thread(target=self._output_thread)
        self.output_thread.start()

        class callback:
            def __init__(self, clbk_type) -> None:
                self.callback_type = clbk_type
            def connect(self, func):
                self.callbacks[self.callback_type].append(func)

        self.connected = callback('connected')
        self.disconnected = callback('disconnected')
        self.discovered = callback('discovered')

    def _output_thread(self):
        while self.running:
            output = self.get_output()
            if output.startswith("Device "):
                address = output[7:]
                self._run_callback("discovered", address)
            elif output.startswith("Connected "):
                address = output[10:]
                self._run_callback("connected", address)
            elif output.startswith("Disconnected "):
                address = output[13:]
                self._run_callback("disconnected", address)

    def send_command(self, command):
        self.process.stdin.write((command + '\n').encode())
        self.process.stdin.flush()

    def get_output(self):
        return self.process.stdout.readline().decode().strip()

    def StartDiscovering(self):
        self.send_command("scan on")

    def StopDiscovering(self):
        self.send_command("scan off")

    def GetQueuedqueued_Devices(self):
        self.send_command("queued_devices")
        queued_devices = []
        while True:
            output = self.get_output()
            if output.startswith("Device "):
                address = output[7:]
                queued_devices.append(address)
                self._run_callback("discovered", address)
            elif output == "":
                break
        return queued_devices

    def start_advertising(self, name):
        cmd = 'echo -e "discoverable on\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = 'echo -e "pairable on\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = f'echo -e "agent NoInputNoOutput\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = f'echo -e "remove {self.mac_address}\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = f'echo -e "add ad\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = f'echo -e "select-adv-packet 0\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = f'echo -e "add-name {name}\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = f'echo -e "show\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = f'echo -e "power on\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)
        cmd = f'echo -e "advertise on\\nquit" | bluetoothctl'
        subprocess.call(cmd, shell=True)

    def pair_device(self, address):
        self.send_command(f"pair {address}")

    def trust_device(self, address):
        self.send_command(f"trust {address}")

    def connect_device(self, address):
        self.send_command(f"connect {address}")

    def disconnect_device(self, address):
        self.send_command(f"disconnect {address}")

    def remove_device(self, address):
        self.send_command(f"remove {address}")

    def _run_callback(self, event_type, *args):
        for callback in self.callbacks[event_type]:
            callback(*args)

    def stop(self):
        self.running = False
        self.process.kill()
        self.output_thread.join()


def device_connected_callback(address):
    print(f"Device connected: {address}")

def device_disconnected_callback(address):
    print(f"Device disconnected: {address}")

def device_discovered_callback(address):
    print(f"Device discovered: {address}")

if __name__ == "__main__":

    ble_dev = Bluetoothctl()

    # Advertise examle
    ble_dev.StartAdvertising()
    time.sleep(10)
    ble_dev.StopAdvertising()



    # # Connect example
    # ble_dev.connected.connect(device_connected_callback)
    # ble_dev.disconnected(device_connected_callback)
    # ble_dev.discovered(device_discovered_callback)
    # ble_dev.StartDiscovering()
    # # Wait for devices to be discovered
    # time.sleep(10)
    # # Stop discovering
    # ble_dev.StopDiscovering()
    # # Get queued BLE devices
    # queued_devices = ble_dev.GetQueuedqueued_Devices()
    # # Print available scanned BLE devices
    # print("queued_Devices:")
    # for device in queued_devices:
    #     print(device)
    # # Connect to first device found
    # if queued_devices:
    #     device_to_connect = queued_devices[0]
    #     ble_dev.connect_device(device_to_connect)
    # # Wait for device to be connected
    # time.sleep(10)
    # # Disconnect from device
    # ble_dev.disconnect_device(device_to_connect)

    ble_dev.stop()

