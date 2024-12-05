# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: tendermint/blockchain/types.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto

from .. import types as _types__


@dataclass(eq=False, repr=False)
class BlockRequest(betterproto.Message):
    """BlockRequest requests a block for a specific height"""

    height: int = betterproto.int64_field(1)


@dataclass(eq=False, repr=False)
class NoBlockResponse(betterproto.Message):
    """
    NoBlockResponse informs the node that the peer does not have block at the
    requested height
    """

    height: int = betterproto.int64_field(1)


@dataclass(eq=False, repr=False)
class BlockResponse(betterproto.Message):
    """BlockResponse returns block to the requested"""

    block: "_types__.Block" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class StatusRequest(betterproto.Message):
    """StatusRequest requests the status of a peer."""

    pass


@dataclass(eq=False, repr=False)
class StatusResponse(betterproto.Message):
    """StatusResponse is a peer response to inform their status."""

    height: int = betterproto.int64_field(1)
    base: int = betterproto.int64_field(2)


@dataclass(eq=False, repr=False)
class Message(betterproto.Message):
    block_request: "BlockRequest" = betterproto.message_field(1, group="sum")
    no_block_response: "NoBlockResponse" = betterproto.message_field(2, group="sum")
    block_response: "BlockResponse" = betterproto.message_field(3, group="sum")
    status_request: "StatusRequest" = betterproto.message_field(4, group="sum")
    status_response: "StatusResponse" = betterproto.message_field(5, group="sum")
