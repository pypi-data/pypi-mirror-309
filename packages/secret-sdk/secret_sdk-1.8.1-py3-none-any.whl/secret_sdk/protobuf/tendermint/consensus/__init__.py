# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: tendermint/consensus/types.proto, tendermint/consensus/wal.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
)

import betterproto

from .. import types as _types__
from ..libs import bits as _libs_bits__


@dataclass(eq=False, repr=False)
class NewRoundStep(betterproto.Message):
    """
    NewRoundStep is sent for every step taken in the ConsensusState. For every
    height/round/step transition
    """

    height: int = betterproto.int64_field(1)
    round: int = betterproto.int32_field(2)
    step: int = betterproto.uint32_field(3)
    seconds_since_start_time: int = betterproto.int64_field(4)
    last_commit_round: int = betterproto.int32_field(5)


@dataclass(eq=False, repr=False)
class NewValidBlock(betterproto.Message):
    """
    NewValidBlock is sent when a validator observes a valid block B in some
    round r, i.e., there is a Proposal for block B and 2/3+ prevotes for the
    block B in the round r. In case the block is also committed, then IsCommit
    flag is set to true.
    """

    height: int = betterproto.int64_field(1)
    round: int = betterproto.int32_field(2)
    block_part_set_header: "_types__.PartSetHeader" = betterproto.message_field(3)
    block_parts: "_libs_bits__.BitArray" = betterproto.message_field(4)
    is_commit: bool = betterproto.bool_field(5)


@dataclass(eq=False, repr=False)
class Proposal(betterproto.Message):
    """Proposal is sent when a new block is proposed."""

    proposal: "_types__.Proposal" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class ProposalPol(betterproto.Message):
    """ProposalPOL is sent when a previous proposal is re-proposed."""

    height: int = betterproto.int64_field(1)
    proposal_pol_round: int = betterproto.int32_field(2)
    proposal_pol: "_libs_bits__.BitArray" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class BlockPart(betterproto.Message):
    """BlockPart is sent when gossipping a piece of the proposed block."""

    height: int = betterproto.int64_field(1)
    round: int = betterproto.int32_field(2)
    part: "_types__.Part" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class Vote(betterproto.Message):
    """Vote is sent when voting for a proposal (or lack thereof)."""

    vote: "_types__.Vote" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class HasVote(betterproto.Message):
    """
    HasVote is sent to indicate that a particular vote has been received.
    """

    height: int = betterproto.int64_field(1)
    round: int = betterproto.int32_field(2)
    type: "_types__.SignedMsgType" = betterproto.enum_field(3)
    index: int = betterproto.int32_field(4)


@dataclass(eq=False, repr=False)
class VoteSetMaj23(betterproto.Message):
    """
    VoteSetMaj23 is sent to indicate that a given BlockID has seen +2/3 votes.
    """

    height: int = betterproto.int64_field(1)
    round: int = betterproto.int32_field(2)
    type: "_types__.SignedMsgType" = betterproto.enum_field(3)
    block_id: "_types__.BlockId" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class VoteSetBits(betterproto.Message):
    """
    VoteSetBits is sent to communicate the bit-array of votes seen for the
    BlockID.
    """

    height: int = betterproto.int64_field(1)
    round: int = betterproto.int32_field(2)
    type: "_types__.SignedMsgType" = betterproto.enum_field(3)
    block_id: "_types__.BlockId" = betterproto.message_field(4)
    votes: "_libs_bits__.BitArray" = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class Message(betterproto.Message):
    new_round_step: "NewRoundStep" = betterproto.message_field(1, group="sum")
    new_valid_block: "NewValidBlock" = betterproto.message_field(2, group="sum")
    proposal: "Proposal" = betterproto.message_field(3, group="sum")
    proposal_pol: "ProposalPol" = betterproto.message_field(4, group="sum")
    block_part: "BlockPart" = betterproto.message_field(5, group="sum")
    vote: "Vote" = betterproto.message_field(6, group="sum")
    has_vote: "HasVote" = betterproto.message_field(7, group="sum")
    vote_set_maj23: "VoteSetMaj23" = betterproto.message_field(8, group="sum")
    vote_set_bits: "VoteSetBits" = betterproto.message_field(9, group="sum")


@dataclass(eq=False, repr=False)
class MsgInfo(betterproto.Message):
    """MsgInfo are msgs from the reactor which may update the state"""

    msg: "Message" = betterproto.message_field(1)
    peer_id: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class TimeoutInfo(betterproto.Message):
    """TimeoutInfo internally generated messages which may update the state"""

    duration: timedelta = betterproto.message_field(1)
    height: int = betterproto.int64_field(2)
    round: int = betterproto.int32_field(3)
    step: int = betterproto.uint32_field(4)


@dataclass(eq=False, repr=False)
class EndHeight(betterproto.Message):
    """
    EndHeight marks the end of the given height inside WAL. @internal used by
    scripts/wal2json util.
    """

    height: int = betterproto.int64_field(1)


@dataclass(eq=False, repr=False)
class WalMessage(betterproto.Message):
    event_data_round_state: "_types__.EventDataRoundState" = betterproto.message_field(
        1, group="sum"
    )
    msg_info: "MsgInfo" = betterproto.message_field(2, group="sum")
    timeout_info: "TimeoutInfo" = betterproto.message_field(3, group="sum")
    end_height: "EndHeight" = betterproto.message_field(4, group="sum")


@dataclass(eq=False, repr=False)
class TimedWalMessage(betterproto.Message):
    """
    TimedWALMessage wraps WALMessage and adds Time for debugging purposes.
    """

    time: datetime = betterproto.message_field(1)
    msg: "WalMessage" = betterproto.message_field(2)
