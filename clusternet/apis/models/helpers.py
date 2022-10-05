import re

IPV4_ADDRESS = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

def get_ipv4_address(ip: str) -> str:
    if(re.match(IPV4_ADDRESS, ip) is None):
        raise Exception('IP does not match a IPV4 address')
    return ip