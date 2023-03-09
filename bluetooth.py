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

    def start_scan(self):
        self.send_command("scan on")

    def stop_scan(self):
        self.send_command("scan off")

    def get_devices(self):
        self.send_command("devices")
        devices = []
        while True:
            output = self.get_output()
            if output.startswith("Device "):
                address = output[7:]
                devices.append(address)
                self._run_callback("discovered", address)
            elif output == "":
                break
        return devices

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

    bt = Bluetoothctl()
    bt.connected.connect(device_connected_callback)
    bt.disconnected(device_connected_callback)
    bt.discovered(device_discovered_callback)

    bt.start_scan()

    # Wait for devices to be discovered
    time.sleep(10)

    bt.stop_scan()
    devices = bt.get_devices()
    print("Devices:")
    for device in devices:
        print(device)

    # Connect to first device found
    if devices:
        device_to_connect = devices[0]
        bt.connect_device(device_to_connect)

    # Wait for device to be connected
    time.sleep(10)

    bt.disconnect_device(device_to_connect)

    bt.stop()

