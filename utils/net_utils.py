import os, subprocess

from time import sleep

from utils.hostname_utils import get_next_hostname
from utils.ip_utils import get_next_ip

def host_pings(ip_address: str, attempts_remaining: int = 1000) -> bool:
    if attempts_remaining == 0:
        return False

    is_windows: bool = os.sys.platform.lower() ==  'win32' #type: ignore[attr-defined]
    count_param: str = '-n' if is_windows else '-c'
    host_is_pinging: bool = subprocess.run(
        [ 'ping', count_param, '1', ip_address ],
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL         
    ).returncode == 0

    if host_is_pinging:
        return True

    return host_pings(ip_address, attempts_remaining -1)

def wait_for_ping(ip_address: str) -> bool:
    if host_pings(ip_address):
        return True

    return False

def wait_for_disconnect(ip_address: str) -> bool:
    host_is_pinging: bool = True
    while host_is_pinging:
        host_is_pinging = host_pings(ip_address, 1)
        sleep(1)
    return True

def ping_scan(config: dict, hostname: str | None, ip_address: str, first_host: bool = False) -> None:
    if first_host:
        print(f'Please connect to {hostname}.')
    if host_pings(ip_address):
        next_hostname: str | None = get_next_hostname(config, hostname)
        next_ip: str = get_next_ip(config, ip_address)
        print(f'{hostname} is reachable at {ip_address}! Please disconnect {hostname} and connect {next_hostname}.')
        ping_scan(config, next_hostname, next_ip)
    else:
        print(f'Unable to reach {hostname} at {ip_address}.')
