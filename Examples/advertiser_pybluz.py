import subprocess
import time

class BluetoothCtl:
    def __init__(self):
        subprocess.call(['sudo', 'systemctl', 'start', 'bluetooth'])
        self.mac_address = self.get_mac_address()
        
    def get_mac_address(self):
        cmd = 'hciconfig | grep "BD Address" | cut -f2 -d" "'
        mac_address = subprocess.check_output(cmd, shell=True).decode().strip()
        return mac_address
    
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

        cmd = 'echo -e "discoverable on\\nquit" | bluetoothctl'\\

if __name__ == '__main__':
    bt = BluetoothCtl()
    bt.start_advertising('badr')