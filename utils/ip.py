from ipaddress import IPv4Address as ip
from ipaddress import ip_network as network
from ipaddress import NetmaskValueError

def is_power_of_two(number: str | int) -> bool:
    try:
        decimal: int = int(number)
        return bool(decimal & (decimal - 1) == 0 and decimal != 0)
    except Exception:
        return False

def get_next_ip(ip_address: str) -> str | None:
    bare_ip_address: str = str(ip_address).strip()
    try:
        return str(ip(bare_ip_address) + 1)
    except Exception:
        return None

def get_netmask(netmask: str) -> str | None:
    bare_netmask: str = str(netmask).strip()
    try:
        subnet_mask: str = str(ip(bare_netmask))
        network_bits: int = int(ip(subnet_mask))
        host_bits: int = 2**32 - network_bits
        print(f'{network_bits=}, {2**32=}')
        if not is_power_of_two(host_bits) or not 1 < host_bits < 2**32 - 1:
            return None
    except ValueError:
        try:
            subnet_mask_bits: int = int(bare_netmask.replace('/', ''))
            subnet_mask = str(network(f'0.0.0.0/{subnet_mask_bits}').netmask)
            if not bool(0 < subnet_mask_bits < 32):
                return None
        except (NetmaskValueError, ValueError):
            return None

    return subnet_mask

def is_netmask(netmask: str) -> bool:
    try:
        subnet_mask: str = get_netmask(netmask)
        return bool(subnet_mask)
    except Exception:
        return False
    
def validate_netmask(netmask: str) -> None:
    if not(is_netmask(netmask)):
        raise ValueError
    else:
        return get_netmask(netmask)

