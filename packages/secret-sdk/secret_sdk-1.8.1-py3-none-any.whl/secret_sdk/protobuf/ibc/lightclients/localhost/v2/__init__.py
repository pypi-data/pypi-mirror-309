# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: ibc/lightclients/localhost/v2/localhost.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto

from ....core.client import v1 as ___core_client_v1__


@dataclass(eq=False, repr=False)
class ClientState(betterproto.Message):
    """ClientState defines the 09-localhost client state"""

    latest_height: "___core_client_v1__.Height" = betterproto.message_field(1)
    """the latest block height"""
