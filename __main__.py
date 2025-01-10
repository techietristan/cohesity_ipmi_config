import sys#type: ignore['import-untyped']

from time import sleep
from argparse import Namespace

from utils.api_utils import push_config
from utils.arg_utils import parse_args
from utils.sys_utils import exit_with_code

config: dict = {
    'default_username': 'admin',
    'default_password': 'admin',
    'http_version': 'https',
    'default_node_ip': '192.168.1.1',
    'node_letters': ('a', 'b', 'c', 'd'),
    'retry_wait_time': 2,
}

def main(config: dict = config) -> int:
    try:
        config['ipmi_api_url'] = f'{config['http_version']}://{config['default_node_ip']}/unix_proxy.fcgi'
        args: Namespace = parse_args(sys.argv)
        node_hostname, node_ip, gateway, netmask, = args.node_hostname, args.node_ip, args.gateway, get_netmask(args.netmask)
        push_config(config, node_hostname, node_ip, netmask, gateway)

    except KeyboardInterrupt:
        print('Keyboard interrupt received, exiting script.')
        exit_with_code(130)

    return 0

if __name__ == '__main__':
    main()