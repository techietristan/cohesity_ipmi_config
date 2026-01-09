from argparse import ArgumentParser, Namespace
from pydantic import AliasChoices, Field, IPvAnyAddress, ValidationError
from pydantic_settings import BaseSettings, CliImplicitFlag, CliSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict # type: ignore
from sys import argv


# def parse_args(system_arguments: list[str]) -> Namespace:
#     parser = ArgumentParser(description = 'A configuration utility for Cohesity IPMIs')
#     parser.add_argument('-g', '--gateway',          required = True,    type = str, help = 'Specify the default gateway to configure.')
#     parser.add_argument('-m', '--netmask',          required = True,    type = str, help = 'Specify the subnet mask to configure.')
#     parser.add_argument('-n', '--node_hostname',    required = True,    type = str, help = 'Specify the first node hostname.')
#     parser.add_argument('-i', '--node_ip',          required = True,    type = str, help = 'Specify the first node IP address.')
#     parser.add_argument('-v', '--verify',           required = False,               help = 'Attempt to ping each node sequentially.', action = 'store_true')
#     parser.add_argument('--increment',              required = False,               help = 'Increment the existing node IP address after each configuration.', action = 'store_true')
#     parser.add_argument('--model',                  required = False,               help = 'Specify which model of node to configure (C5000 and C6000 series supported)')
    
#     return parser.parse_args()

# args: Namespace = parse_args(argv)

class InitialSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file = '.env', extra = 'ignore')
    default_username: str
    default_password: str
    http_version: str
    default_node_ip: IPvAnyAddress
    node_letters: list[str] | None
    retry_wait_time: int
    
initial_settings: InitialSettings = InitialSettings()

class Config(InitialSettings):
    ipmi_api_url: str = f'{initial_settings.http_version}://{initial_settings.default_node_ip}/unix_proxy.fcgi' 
    first_node_ip: IPvAnyAddress = Field(validation_alias = AliasChoices('i', 'node_ip'))
    node_default_gateway: IPvAnyAddress = Field(validation_alias = AliasChoices('g', 'gateway'))
    node_hostname: str = Field(validation_alias = AliasChoices('n', 'node_hostname'))
    node_subnet_mask: str = Field(validation_alias = AliasChoices('m', 'netmask'))
    verify: CliImplicitFlag[bool] = Field(validation_alias = AliasChoices('v', 'verify'))
    increment: CliImplicitFlag[bool] = Field(validation_alias = AliasChoices('increment'))
    node_model: str = Field(validation_alias = AliasChoices('model', 'node_model'))

    @classmethod
    def settings_customise_sources(
            cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings
        ) -> tuple[PydanticBaseSettingsSource, ...]:
        return CliSettingsSource(settings_cls, cli_parse_args = True), dotenv_settings

settings: Config = Config()
