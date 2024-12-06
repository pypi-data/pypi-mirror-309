#!/usr/bin/python
from cloudshell.networking.ipinfusion.flows.ipinfusion_disable_snmp_flow import (
    IPInfusionDisableSnmpFlow,
)
from cloudshell.networking.ipinfusion.flows.ipinfusion_enable_snmp_flow import (
    IPInfusionEnableSnmpFlow,
)
from cloudshell.snmp.snmp_configurator import (
    EnableDisableSnmpConfigurator,
    EnableDisableSnmpFlowInterface,
)


class IPInfusionEnableDisableSnmpFlow(EnableDisableSnmpFlowInterface):
    DEFAULT_SNMP_VIEW = "quali_snmp_view"
    DEFAULT_SNMP_GROUP = "quali_snmp_group"

    def __init__(self, cli_handler, logger, resource_config):
        """Enable snmp flow."""
        self._logger = logger
        self._cli_handler = cli_handler
        self._resource_config = resource_config

    def enable_snmp(self, snmp_parameters):
        IPInfusionEnableSnmpFlow(self._cli_handler, self._logger).enable_flow(
            snmp_parameters, self._resource_config.vrf_management_name
        )

    def disable_snmp(self, snmp_parameters):
        IPInfusionDisableSnmpFlow(self._cli_handler, self._logger).disable_flow(
            snmp_parameters, self._resource_config.vrf_management_name
        )


class IPInfusionSnmpHandler(EnableDisableSnmpConfigurator):
    def __init__(self, resource_config, logger, cli_handler):
        self.cli_handler = cli_handler
        enable_disable_snmp_flow = IPInfusionEnableDisableSnmpFlow(
            self.cli_handler, logger, resource_config
        )
        super().__init__(enable_disable_snmp_flow, resource_config, logger)
