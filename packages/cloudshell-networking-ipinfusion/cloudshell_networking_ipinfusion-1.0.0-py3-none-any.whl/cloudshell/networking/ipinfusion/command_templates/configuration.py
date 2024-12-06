# !/usr/bin/pythoncloudshell

from cloudshell.cli.command_template.command_template import CommandTemplate

SAVE_CONFIG_REMOTE = CommandTemplate("copy {src} {protocol_type} {dst} vrf {vrf}")
LOAD_CONFIG_REMOTE = CommandTemplate(
    "copy {protocol_type} {src} {dst} [append{append}] [store{store}] vrf {vrf}"
)
SAVE_CONFIG_LOCAL = CommandTemplate("write [file {file_path}]")
LOAD_CONFIG_LOCAL = CommandTemplate(
    "copy file {file_path} {config} [append{append}] [store{store}]"
)
