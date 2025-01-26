import json

from re import search
from requests import post, Response
from requests.exceptions import ConnectionError
from time import sleep
from urllib3 import disable_warnings #type: ignore[import-untyped]
from urllib3.exceptions import InsecureRequestWarning #type: ignore[import-untyped]

from utils.net_utils import wait_for_disconnect, wait_for_ping
from utils.hostname_utils import get_next_hostname
from utils.ip_utils import get_next_ip

disable_warnings(InsecureRequestWarning)

def make_api_call(config: dict, headers: dict, payload: dict, json: bool = True) -> dict | Response:
    ipmi_api_url: str = config['ipmi_api_url']
    api_response: Response = post(
        ipmi_api_url,
        headers = headers,
        json = payload,
        verify = False
    )

    return api_response.json() if json else api_response

def get_token(config: dict) -> dict | None:
    headers: dict = {}
    payload: dict = {
        'cmd': 'WEB_LOGIN',
        'data': { 
            'user': config['default_username'], 
            'pass': config['default_password'] 
        }
    }
    try:
        auth_response: Response = make_api_call(config, headers, payload, False) #type: ignore[assignment]
        response_session_id: str = str(
            search(
                r'(session_id=[a-z0-9]+)', 
                str(auth_response.headers['Set-Cookie'])
            ).group(1) #type: ignore[union-attr]
        )
        response_token = str(auth_response.json()['data'][0]['token'])
        return { 'session_id': response_session_id, 'token': response_token }
    
    except ConnectionError:
        sleep(config['retry_wait_time'])
        get_token(config)
    
    except Exception as error:
        print(f'Unable to get token: {error}, retrying...')
        sleep(config['retry_wait_time'])
        get_token(config)
        
    return None

def get_mac(config: dict) -> list[int] | None:
    default_node_ip: str = config['default_node_ip']  
    ipmi_api_url: str = config['ipmi_api_url']
    try:
        token: dict = get_token(config) #type: ignore[assignment]
        headers: dict = { 
            'Cookie': token['session_id'],
            'X-CSRF-Token': token['token']
        }
        payload: dict = {
            'cmd': 'WEB_LAN_GET_INFO_V2',
            'data': None
        }
        config_response: dict = make_api_call(config, headers, payload) #type: ignore[assignment]
        status_code: int = int(config_response['success'])
        config_successful: bool = status_code == 0

        if config_successful:
            mac_address: list[int] = config_response['data'][0]['macaddr']
            return mac_address

    except TypeError as error:
        pass
            
    except Exception as error:
        print(f'{error=}')
                    
    return None    

def push_config(config: dict, node_hostname: str, node_ip: str, netmask: str, gateway: str, retry: bool = False) -> None:
    def retry_config():
        print(f'Unable to push configuration for \'{node_hostname}\', retrying...')
        sleep(config['retry_wait_time'])
        push_config(config, node_hostname, node_ip, netmask, gateway, True)

    default_node_ip: str = config['default_node_ip']  
    ipmi_api_url: str = config['ipmi_api_url']
    if not config.get('current_mac'):
        print(f'Please connect to {node_hostname}.')
    if wait_for_ping(default_node_ip):
        while True:
            current_mac: list[int] | None = get_mac(config)
            if bool(current_mac):
                config['current_mac'] = current_mac
                break
            else:
                sleep(1)
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
            config_response: dict = make_api_call(config, headers, payload) #type: ignore[assignment]
            status_code: int = int(config_response['success'])
            config_successful: bool = status_code == 0

            if config_successful:
                next_hostname: str = get_next_hostname(config, node_hostname) #type: ignore[assignment]
                print(f'{node_hostname} ({node_ip}) successfully configured !\nPlease disconnect {node_hostname} and connect {next_hostname}.')
                sleep(1)
                while True:
                    current_mac = get_mac(config)
                    if bool(current_mac) and current_mac != config['current_mac']:
                        break
                    sleep(1)
                
                next_ip: str = get_next_ip(config, node_ip)
                push_config(config, next_hostname, next_ip, netmask, gateway, False)
            else:
                retry_config()
                
        except Exception as error:
            print(f'{error=}')
            retry_config()
                    
    return None
