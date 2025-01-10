import os, subprocess

from time import sleep

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
