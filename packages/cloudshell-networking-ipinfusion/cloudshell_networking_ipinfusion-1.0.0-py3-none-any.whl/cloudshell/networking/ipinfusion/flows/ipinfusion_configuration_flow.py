#!/usr/bin/python

from cloudshell.networking.ipinfusion.command_actions.save_restore_actions import (
    SaveRestoreActions,
)
from cloudshell.networking.ipinfusion.command_actions.system_actions import (
    SystemActions,
)
from cloudshell.networking.ipinfusion.helpers.exceptions import (
    IPInfusionSaveRestoreException,
)
from cloudshell.shell.flows.configuration.basic_flow import AbstractConfigurationFlow
from cloudshell.shell.flows.utils.networking_utils import UrlParser


class IPInfusionConfigurationFlow(AbstractConfigurationFlow):
    DEFAULT_CONFIG_NAME = "Quali.cfg"
    DEFAULT_LOCAL_PATH = "/var/quali/"
    REMOTE_PROTOCOLS = ["ftp", "tftp", "scp"]

    def __init__(self, cli_handler, resource_config, logger):
        super().__init__(logger, resource_config)
        self._cli_handler = cli_handler

    @property
    def _file_system(self):
        """Determine device file system type."""
        return "local"

    def _save_flow(self, folder_path, configuration_type, vrf_management_name=None):
        """Execute flow which save selected file to the provided destination.

        :param folder_path: destination path where file will be saved
        :param configuration_type: source file, which will be saved
        :param vrf_management_name: Virtual Routing and Forwarding Name
        :return: saved configuration file name
        """
        if not configuration_type.endswith("-config"):
            configuration_type += "-config"

        if configuration_type not in ["running-config", "startup-config"]:
            raise IPInfusionSaveRestoreException(
                "Device doesn't support saving '{}' configuration type".format(
                    configuration_type
                ),
            )

        url = UrlParser().parse_url(folder_path)
        scheme = url.get("scheme")
        avail_protocols = self.REMOTE_PROTOCOLS + [self._file_system]
        if scheme not in avail_protocols:
            raise IPInfusionSaveRestoreException(
                f"Unsupported protocol type {scheme}."
                f"Available protocols: {avail_protocols}"
            )

        with self._cli_handler.get_cli_service(
            self._cli_handler.enable_mode
        ) as enable_session:
            save_action = SaveRestoreActions(enable_session, self._logger)
            system_action = SystemActions(enable_session, self._logger)

            if scheme in self.REMOTE_PROTOCOLS:
                save_action.save_configuration_to_remote(
                    conf_type=configuration_type,
                    protocol_type=scheme,
                    destination=folder_path,
                    vrf=vrf_management_name,
                )
            else:
                if configuration_type == "running-config":
                    filename = url.get("filename", self.DEFAULT_CONFIG_NAME)
                    config_path = url.get("path", self.DEFAULT_LOCAL_PATH)
                    if not config_path.endswith("/"):
                        config_path += "/"
                    full_path = "/".join([config_path, filename])  # not os.path.join
                    system_action.create_folder(folder_path=config_path)
                    save_action.save_configuration_to_local(local_path=full_path)
                else:
                    raise IPInfusionSaveRestoreException("")

    def _restore_flow(
        self, path, configuration_type, restore_method, vrf_management_name
    ):
        """Execute flow which save selected file to the provided destination.

        :param path: the path to the configuration file, including the configuration
            file name
        :param restore_method: the restore method to use when restoring the
            configuration file. Possible Values are append and override
        :param configuration_type: the configuration type to restore.
            Possible values are startup and running
        :param vrf_management_name: Virtual Routing and Forwarding Name
        """
        if not configuration_type.endswith("-config"):
            configuration_type += "-config"

        if configuration_type not in ["running-config", "startup-config"]:
            raise IPInfusionSaveRestoreException(
                "Device doesn't support restoring '{}' configuration type".format(
                    configuration_type
                ),
            )

        if not restore_method:
            restore_method = "override"

        url = UrlParser().parse_url(path)
        scheme = url.get("scheme")
        avail_protocols = self.REMOTE_PROTOCOLS + [self._file_system]
        if scheme not in avail_protocols:
            raise IPInfusionSaveRestoreException(
                f"Unsupported protocol type {scheme}."
                f"Available protocols: {avail_protocols}"
            )

        with self._cli_handler.get_cli_service(
            self._cli_handler.enable_mode
        ) as enable_session:
            save_action = SaveRestoreActions(enable_session, self._logger)

            if configuration_type == "startup-config":
                append = False
                store = False
            else:
                store = True
                if restore_method == "append":
                    append = True
                else:
                    append = False

            if scheme in self.REMOTE_PROTOCOLS:
                "copy {protocol_type} {src} {dst} [append{append}] store vrf {vrf}"
                save_action.load_configuration_from_remote(
                    conf_type=configuration_type,
                    protocol_type=scheme,
                    source=path,
                    append=append,
                    store=store,
                    vrf=vrf_management_name,
                )
            else:
                "copy file {file_path} {config} [append{append}] [store{store}]"
                filename = url.get("filename", self.DEFAULT_CONFIG_NAME)
                config_path = url.get("path", self.DEFAULT_LOCAL_PATH)
                if not config_path.endswith("/"):
                    config_path += "/"
                full_path = "/".join([config_path, filename])  # not os.path.join
                save_action.load_configuration_from_local(
                    file_path=full_path,
                    conf_type=configuration_type,
                    append=append,
                    store=store,
                )
