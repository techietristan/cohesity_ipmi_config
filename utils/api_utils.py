import json

from re import search
from requests import post, Response
from time import sleep
from urllib3 import disable_warnings #type: ignore[import-untyped]
from urllib3.exceptions import InsecureRequestWarning #type: ignore[import-untyped]

from utils.net_utils import wait_for_disconnect, wait_for_ping
from utils.hostname_utils import get_next_hostname
from utils.ip_utils import get_next_ip

disable_warnings(InsecureRequestWarning)

def get_token(config: dict) -> dict | None:
    payload: dict = {
        'cmd': 'WEB_LOGIN',
        'data': { 
            'user': config['default_username'], 
            'pass': config['default_password'] 
        }
    }
    try:
        auth_response: Response = post(
            config['ipmi_api_url'],
            headers = {},
            json = payload,
            verify = False
        )
        response_session_id: str = str(
            search(
                r'(session_id=[a-z0-9]+)', 
                str(auth_response.headers['Set-Cookie'])
            ).group(1) #type: ignore[union-attr]
        )
        response_token = str(auth_response.json()['data'][0]['token'])
        return { 'session_id': response_session_id, 'token': response_token }
    
    except Exception as error:
        print(f'Unable to get token: {error}, retrying...')
        sleep(config['retry_wait_time'])
        get_token(config)
    
    return None

def push_config(config: dict, node_hostname: str, node_ip: str, netmask: str, gateway: str, retry: bool = False) -> None:
    def retry_config():
        print(f'Unable to push configuration for \'{node_hostname}\', retrying...')
        sleep(config['retry_wait_time'])
        push_config(config, node_hostname, node_ip, netmask, gateway, True)

    default_node_ip: str = config['default_node_ip']  
    ipmi_api_url: str = config['ipmi_api_url']
    print(f'Please connect to {node_hostname}.')
    if wait_for_ping(default_node_ip):
        try:
            token: dict = get_token(config) #type: ignore[assignment]
            headers: dict = { 
                'Cookie': token['session_id'],
                'X-CSRF-Token': token['token']
            }
            payload: dict = {
                'cmd': 'WEB_LAN_SET_INFO',
                'data': {
                    'ipv': 4,
                    'ipv4netmode': 1,
                    'ipv4addr': node_ip,
                    'subnetmask': netmask,
                    'ipv4defgateway': gateway,
                    'lanchannel': 1
                }
            }
            config_response: Response = post(
                ipmi_api_url,
                headers = headers,
                json = payload,
                verify = False
            )
            status_code: int = int(config_response.json()['success'])
            config_successful: bool = status_code == 0

            if config_successful:
                print(f'{node_hostname} ({node_ip}) successfully configured !\nPlease disconnect {node_hostname}')
                wait_for_disconnect(default_node_ip)
                next_hostname: str = get_next_hostname(config, node_hostname) #type: ignore[assignment]
                next_ip: str = get_next_ip(config, node_ip)
                push_config(config, next_hostname, next_ip, netmask, gateway, False)
            else:
                retry_config()
                
        except Exception as error:
            print(f'{error=}')
            retry_config()
                    
    return None    