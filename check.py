import subprocess
import platform
import socket
import uuid
import psutil
import requests

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(2, 7)][::-1])
    return mac

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error:
        return None

def is_virtual_mac(mac_address):
    return mac_address.startswith("00:1a:2b")

def is_virtual_cpu():
    return psutil.virtual_memory().percent > 90

def is_virtual_system():
    system_info = platform.uname()
    return "Microsoft" in system_info.system or "VMware" in system_info.system or "VirtualBox" in system_info.system

def get_virtualization_info():
    try:
        result = subprocess.check_output(["lscpu"])
        return result.decode("utf-8")
    except subprocess.CalledProcessError:
        return None

def is_virtualization_enabled():
    virtualization_info = get_virtualization_info()
    if virtualization_info and ("QEMU" in virtualization_info or "VirtIO" in virtualization_info or "KVM" in virtualization_info):
        return True
    else:
        return False

def is_virtual_ip(ip_address):
    virtual_ip_addresses = ["192.168.122.1", "10.0.2.15", "172.17.0.1"]
    return ip_address in virtual_ip_addresses

def get_country_name(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        data = response.json()
        return data.get("country_name")
    except Exception as e:
        print(f"Error fetching country information: {e}")
        return None

def print_system_info():
    print("Thông tin hệ thống:")
    print(f"- Địa chỉ MAC: {get_mac_address()}")
    print(f"- Địa chỉ IP: {get_ip_address()}")
    print(f"- Quốc gia: {get_country_name(get_ip_address())}")
    print(f"- Thông tin CPU: {get_virtualization_info()}")

def is_virtual_machine():
    mac_address = get_mac_address()
    ip_address = get_ip_address()

    if (
        is_virtual_mac(mac_address)
        or is_virtual_cpu()
        or is_virtual_system()
        or is_virtual_ip(ip_address)
        or is_virtualization_enabled()
    ):
        print("Đây có thể là máy ảo.")
        print_system_info()
    else:
        print("Đây là máy thật.")
        print_system_info()

is_virtual_machine()
