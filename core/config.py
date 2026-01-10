from pydantic import AfterValidator, IPvAnyAddress # type: ignore
from pydantic_settings import BaseSettings, CliImplicitFlag, CliSettingsSource, CliSuppress, PydanticBaseSettingsSource, SettingsConfigDict# type: ignore
from sys import argv
from typing import Annotated

from models import *
from utils.ip import validate_netmask

class InitialSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file = '.env', extra = 'ignore')
    default_username: CliSuppress[str]
    default_password: CliSuppress[str]
    http_version: CliSuppress[str]
    default_node_ip: CliSuppress[IPvAnyAddress]
    node_letters: CliSuppress[list[str] | None]
    retry_wait_time: CliSuppress[int]
    
initial_settings: InitialSettings = InitialSettings()

class Config(InitialSettings):
    ipmi_api_url: CliSuppress[str] = f'{initial_settings.http_version}://{initial_settings.default_node_ip}/unix_proxy.fcgi' 
    first_node_ip: IPvAnyAddress = NodeIP
    node_default_gateway: IPvAnyAddress = Gateway
    node_hostname: str = NodeHostname
    node_subnet_mask: Annotated[str, AfterValidator(validate_netmask)] = NodeSubnetMask
    verify: CliImplicitFlag[bool] = Verify
    increment: CliImplicitFlag[bool] = Increment
    node_model: str = NodeModel

    @classmethod
    def settings_customise_sources(
            cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings
        ) -> tuple[PydanticBaseSettingsSource, ...]:
        return CliSettingsSource(settings_cls, cli_parse_args = True), dotenv_settings

config: Config = Config()
