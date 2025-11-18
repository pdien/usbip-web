import subprocess
import re
import cfg

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def run_sudo_cmd(cmd):
    return subprocess.run('sh -c "echo {} | sudo -S {}"'.format(cfg.sudo_pass,cmd), shell=True, capture_output=True, text=True)

def get_usb_devices():
    output = run_cmd('usbip list -l')
    return list(filter(bool, re.sub(r"(\r\n|\n|\r)", "", output.stdout).split(' - ')))

def get_device_id(device):
    device_id = re.search(r"\(.{4}:.{4}\)", device).group(0)
    return re.sub(r"\(|\)", "", device_id)

def get_bus_id(device):
    bus_id = re.search(r"busid\s+\d\-\d\.\d", device).group(0)
    return re.sub(r"\s", "=", bus_id)

def bind_usb_device(bus_id):
    return run_sudo_cmd("usbip bind --{}".format(bus_id))

def unbind_usb_device(bus_id):
    return run_sudo_cmd("usbip unbind --{}".format(bus_id))

def unbind_all_devices():
    devices = get_usb_devices()
    for device in devices:
        bus_id = get_bus_id(device)
        unbind_usb_device(bus_id)
