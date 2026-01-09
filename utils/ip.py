from ipaddress import IPv4Address as ip
from ipaddress import ip_network as network

def get_next_ip(config: dict, ip_address: str) -> str:
    return str(ip(ip_address) + 1)

def get_netmask(netmask: str) -> str:
    try:
        subnet_mask: str = str(ip(netmask))
    except ValueError:
        subnet_mask_bits: int = int(netmask.replace('/', ''))
        subnet_mask = str(network(f'0.0.0.0/{subnet_mask_bits}').netmask)
    
    return subnet_mask

