import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def scan_ip(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return f"{ip}"
    return None

def scan_range(ips_to_scan, port):
    results = []
    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = {executor.submit(scan_ip, ip, port): ip for ip in ips_to_scan}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results

def main():
    port = int(input("Nhập cổng cần kiểm tra: "))
    start_ip = input("Nhập địa chỉ IP bắt đầu: ")
    end_ip = input("Nhập địa chỉ IP kết thúc: ")
    start_ip_obj = ipaddress.ip_address(start_ip)
    end_ip_obj = ipaddress.ip_address(end_ip)
    num_ips = int(end_ip_obj) - int(start_ip_obj) + 1

    print(f"Số lượng IP cần phải quét: {num_ips}")  
    print("________________________________")

    ips_to_scan = [str(ipaddress.ip_address(ip)) for ip in range(int(start_ip_obj), int(end_ip_obj) + 1)]
    chunk_size = 100

    start_time = time.time()

    all_results = []
    for i in range(0, len(ips_to_scan), chunk_size):
        chunk = ips_to_scan[i:i + chunk_size]
        results = scan_range(chunk, port)
        all_results.extend(results)
        for result in results:
            print(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Quét xong {num_ips} IP trong {elapsed_time:.2f} giây.")

if __name__ == "__main__":
    main()