# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/crisis/module/v1/module.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


@dataclass(eq=False, repr=False)
class Module(betterproto.Message):
    """Module is the config object of the crisis module."""

    fee_collector_name: str = betterproto.string_field(1)
    """fee_collector_name is the name of the FeeCollector ModuleAccount."""

    authority: str = betterproto.string_field(2)
    """
    authority defines the custom module authority. If not set, defaults to the
    governance module.
    """
