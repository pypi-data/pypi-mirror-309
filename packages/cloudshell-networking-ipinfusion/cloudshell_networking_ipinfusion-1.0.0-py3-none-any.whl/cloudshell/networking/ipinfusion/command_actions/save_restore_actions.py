#!/usr/bin/python

from cloudshell.cli.command_template.command_template_executor import (
    CommandTemplateExecutor,
)
from cloudshell.networking.ipinfusion.command_templates import configuration
from cloudshell.networking.ipinfusion.helpers.exceptions import (
    IPInfusionSaveRestoreException,
)


class SaveRestoreActions:
    def __init__(self, cli_service, logger):
        """Save and Restore actions."""
        self._cli_service = cli_service
        self._logger = logger

    def save_configuration_to_remote(self, conf_type, protocol_type, destination, vrf):
        """Save configuration to remote location."""
        output = CommandTemplateExecutor(
            self._cli_service, configuration.SAVE_CONFIG_REMOTE
        ).execute_command(
            src=conf_type, protocol_type=protocol_type, dst=destination, vrf=vrf
        )

        if "curl:" in output:
            err_msg = output.split("curl")[-1]
            raise IPInfusionSaveRestoreException(f"Error during coping file: {err_msg}")
        elif "error" in output.lower():
            raise IPInfusionSaveRestoreException(f"Error during coping file: {output}")

    def save_configuration_to_local(self, local_path):
        """Save configuration to remote location."""
        output = CommandTemplateExecutor(
            self._cli_service, configuration.SAVE_CONFIG_LOCAL
        ).execute_command(file_path=local_path)
        if "% " in output:
            msg = "Saving configuration to local failed."
            self._logger.error(f"{msg} {output}")
            raise IPInfusionSaveRestoreException(msg)

    def load_configuration_from_remote(
        self, conf_type, protocol_type, source, append, store, vrf
    ):
        """Load configuration from file."""
        if store and append:
            output = CommandTemplateExecutor(
                self._cli_service, configuration.LOAD_CONFIG_REMOTE
            ).execute_command(
                protocol_type=protocol_type,
                src=source,
                dst=conf_type,
                append="",
                store="",
                vrf=vrf,
            )
        elif store and not append:
            output = CommandTemplateExecutor(
                self._cli_service, configuration.LOAD_CONFIG_REMOTE
            ).execute_command(
                protocol_type=protocol_type,
                src=source,
                dst=conf_type,
                store="",
                vrf=vrf,
            )
        else:
            output = CommandTemplateExecutor(
                self._cli_service, configuration.LOAD_CONFIG_REMOTE
            ).execute_command(
                protocol_type=protocol_type, src=source, dst=conf_type, vrf=vrf
            )

        if "curl:" in output:
            err_msg = output.split("curl")[-1]
            raise IPInfusionSaveRestoreException(f"Error during coping file: {err_msg}")
        elif "error" in output.lower():
            raise IPInfusionSaveRestoreException(f"Error during coping file: {output}")

    def load_configuration_from_local(self, file_path, conf_type, append, store):
        """Load configuration from file."""
        if store and append:
            output = CommandTemplateExecutor(
                self._cli_service, configuration.LOAD_CONFIG_LOCAL
            ).execute_command(
                file_path=file_path, config=conf_type, append="", store=""
            )
        elif store and not append:
            output = CommandTemplateExecutor(
                self._cli_service, configuration.LOAD_CONFIG_LOCAL
            ).execute_command(file_path=file_path, config=conf_type, store="")
        else:
            output = CommandTemplateExecutor(
                self._cli_service, configuration.LOAD_CONFIG_LOCAL
            ).execute_command(file_path=file_path, config=conf_type)

        if "% " in output:
            msg = f"Loading configuration from local file {file_path} failed."
            self._logger.error(f"{msg} {output}")
            raise IPInfusionSaveRestoreException(msg)
