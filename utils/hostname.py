from re import search, Match

def get_next_node_hostname(hostname: str, node_letters: list[str]) -> str | None:
    hostname_parts: Match[str] | None = search(r'(\D+)(\d+)(\w)', hostname)
    hostname_base, hostname_number, node_letter = hostname_parts.group(1), hostname_parts.group(2), hostname_parts.group(3) #type: ignore[union-attr]
    hostname_number_digits: int = len(hostname_number)
    next_node_letter_index: int = (node_letters.index(node_letter) + 1) % len(node_letters)
    next_node_letter: str = node_letters[next_node_letter_index]
    next_hostname_number: str = str(int(hostname_number) + 1).rjust(hostname_number_digits, '0') if next_node_letter_index == 0 else hostname_number
    next_hostname: str = f'{hostname_base}{next_hostname_number}{next_node_letter}'

    return next_hostname

def get_next_server_hostname(hostname: str) -> str | None:
    hostname_parts: Match[str] | None = search(r'(\D+)(\d+)', hostname)
    hostname_base, hostname_number = hostname_parts.group(1), hostname_parts.group(2) #type: ignore[union-attr]
    hostname_number_digits: int = len(hostname_number)
    next_hostname_number: str = str(int(hostname_number) + 1).rjust(hostname_number_digits, '0')
    next_hostname: str = f'{hostname_base}{next_hostname_number}'

    return next_hostname

def get_next_hostname(config: dict, hostname: str) -> str | None:
    try:
        stripped_hostname: str = hostname.strip()
        node_letters: list(str) = config.node_letters
        is_node: bool = bool(stripped_hostname[-1] in node_letters)
    
        return get_next_node_hostname(stripped_hostname, node_letters)\
            if is_node\
            else get_next_server_hostname(stripped_hostname)
        
    except (AttributeError, ValueError):
        return None