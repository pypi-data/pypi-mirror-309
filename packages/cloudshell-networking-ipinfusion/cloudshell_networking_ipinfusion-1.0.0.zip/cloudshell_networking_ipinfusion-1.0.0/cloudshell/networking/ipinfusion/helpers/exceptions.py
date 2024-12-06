#!/usr/bin/python


class IPInfusionBaseException(Exception):
    """Base IPInfusion exception."""


class IPInfusionSNMPException(IPInfusionBaseException):
    """IPInfusion enable/disable SNMP configuration exception."""


class IPInfusionSaveRestoreException(IPInfusionBaseException):
    """IPInfusion save/restore configuration exception."""


class IPInfusionConnectivityException(IPInfusionBaseException):
    """IPInfusion connectivity exception."""


class IPInfusionFirmwareException(IPInfusionBaseException):
    """IPInfusion load firmware exception."""
