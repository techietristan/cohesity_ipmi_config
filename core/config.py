from argparse import ArgumentParser, Namespace
from pydantic_settings import BaseSettings, SettingsConfigDict
from sys import argv


def parse_args(system_arguments: list[str]) -> Namespace:
    parser = ArgumentParser(description = 'A configuration utility for Cohesity IPMIs')
    parser.add_argument('-g', '--gateway',          default = False,    required = True,    type = str, help = 'Specify the default gateway to configure.')
    parser.add_argument('-m', '--netmask',          default = False,    required = True,    type = str, help = 'Specify the subnet mask to configure.')
    parser.add_argument('-n', '--node_hostname',    default = False,    required = True,    type = str, help = 'Specify the first node hostname.')
    parser.add_argument('-i', '--node_ip',          default = False,    required = True,    type = str, help = 'Specify the first node IP address.')
    parser.add_argument('-v', '--verify',           default = False,    required = False,               help = 'Attempt to ping each node sequentially.', action = 'store_true')
    parser.add_argument('--increment',              default = False,    required = False,               help = 'Increment the existing node IP address after each configuration.', action = 'store_true')
    parser.add_argument('--model',                  default = None,     required = False,   type = str, help = 'Specify which model of node to configure (C5000 and C6000 series supported)')
    
    return parser.parse_args()

args: Namespace = parse_args(argv)

class InitialSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file = '.env', extra = 'ignore')
    default_username: str
    default_password: str
    http_version: str
    default_node_ip: str
    node_letters: list[str] | None
    retry_wait_time: int
    verify: bool = args.verify
    increment: bool = args.increment
    model: str = args.model

initial_settings: InitialSettings = InitialSettings()

class Config(InitialSettings):
    model_config = SettingsConfigDict(env_file = '.env', extra = 'ignore')
    ipmi_api_url: str = f'{initial_settings.http_version}://{initial_settings.default_node_ip}/unix_proxy.fcgi' 
    first_node_ip: str = args.node_ip
    node_default_gateway: str = args.gateway
    node_subnet_mask: str = args.netmask
    node_hostname: str = args.node_hostname

settings: Config = Config()








