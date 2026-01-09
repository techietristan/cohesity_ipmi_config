from enum import IntEnum
from pydantic import AliasChoices, Field #type: ignore

NodeIP = Field(
    validation_alias = AliasChoices('i', 'node_ip'),
    description = 'Specify the first node IP address.')

Gateway = Field(
    validation_alias = AliasChoices('g', 'gateway'),
    description = 'Specify the default gateway to configure.')

NodeHostname = Field(
    validation_alias = AliasChoices('n', 'node_hostname'),
    description = 'Specify the first node hostname.')

NodeSubnetMask = Field(
    validation_alias = AliasChoices('m', 'netmask'),
    description = 'Specify the subnet mask to configure.')

Verify = Field(
    validation_alias = AliasChoices('v', 'verify'),
    description = 'Attempt to ping each node sequentially.')

Increment = Field(
    validation_alias = AliasChoices('increment'),
    description = 'Increment the existing node IP address after each configuration.')

NodeModel = Field(
    validation_alias = AliasChoices('model', 'node_model'),
    description = 'Specify which model of node to configure (C5000 and C6000 series supported)')

NodeSeriesEnum = IntEnum('NodeSeriesEnum', [('c5000_series', 5), ('c6000_series', 6)])
