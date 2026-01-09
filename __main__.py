import sys #type: ignore['import-untyped']

from time import sleep

from core.config import settings
from utils.api_utils import push_config
from utils.ip_utils import get_netmask
from utils.net_utils import ping_scan
from utils.sys_utils import exit_with_code

def main() -> int:
    try:
        print(settings)
        # config['ipmi_api_url'] = f'{config['http_version']}://{config['default_node_ip']}/unix_proxy.fcgi'
        # args: Namespace = parse_args(sys.argv)
        # node_hostname, node_ip, gateway, netmask, verify = args.node_hostname, args.node_ip, args.gateway, get_netmask(args.netmask), args.verify
        # if verify:
        #     ping_scan(config, node_hostname, node_ip, True)
        # else:
        #     push_config(config, node_hostname, node_ip, netmask, gateway)

    except KeyboardInterrupt:
        print('Keyboard interrupt received, exiting script.')
        exit_with_code(130)

    return 0

if __name__ == '__main__':
    main()