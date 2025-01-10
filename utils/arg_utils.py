from argparse import ArgumentParser, Namespace

def parse_args(system_arguments: list[str]) -> Namespace:
    parser = ArgumentParser(description = 'A configuration utility for Cohesity IPMIs')
    parser.add_argument('-g', '--gateway',          default = False, required = True, type = str, help = 'Specify the default gateway to configure.')
    parser.add_argument('-m', '--netmask',          default = False, required = True, type = str, help = 'Specify the subnet mask to configure.')
    parser.add_argument('-n', '--node_hostname',    default = False, required = True, type = str, help = 'Specify the first node hostname.')
    parser.add_argument('-i', '--node_ip',          default = False, required = True, type = str, help = 'Specify the first node IP address.')

    return parser.parse_args()