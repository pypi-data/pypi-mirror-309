# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: secret/registration/remote_attestation/v1beta1/types.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto


@dataclass(eq=False, repr=False)
class QuoteReport(betterproto.Message):
    id: str = betterproto.string_field(1)
    timestamp: str = betterproto.string_field(2)
    version: int = betterproto.uint64_field(3)
    isv_enclave_quote_status: str = betterproto.string_field(4)
    platform_info_blob: str = betterproto.string_field(5)
    isv_enclave_quote_body: str = betterproto.string_field(6)
    advisory_ids: List[str] = betterproto.string_field(7)


@dataclass(eq=False, repr=False)
class QuoteReportBody(betterproto.Message):
    mr_enclave: str = betterproto.string_field(1)
    mr_signer: str = betterproto.string_field(2)
    report_data: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class QuoteReportData(betterproto.Message):
    version: int = betterproto.uint64_field(1)
    sign_type: int = betterproto.uint64_field(2)
    report_body: "QuoteReportBody" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class EndorsedAttestationReport(betterproto.Message):
    report: bytes = betterproto.bytes_field(1)
    signature: bytes = betterproto.bytes_field(2)
    signing_cert: bytes = betterproto.bytes_field(3)


@dataclass(eq=False, repr=False)
class Sgxec256Signature(betterproto.Message):
    gx: str = betterproto.string_field(1)
    gy: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class PlatformInfoBlob(betterproto.Message):
    sgx_epid_group_flags: int = betterproto.uint32_field(1)
    sgx_tcb_evaluation_flags: int = betterproto.uint32_field(2)
    pse_evaluation_flags: int = betterproto.uint32_field(3)
    latest_equivalent_tcb_psvn: str = betterproto.string_field(4)
    latest_pse_isvsvn: str = betterproto.string_field(5)
    latest_psda_svn: str = betterproto.string_field(6)
    xeid: int = betterproto.uint32_field(7)
    gid: int = betterproto.uint32_field(8)
    sgx_ec256_signature_t: "Sgxec256Signature" = betterproto.message_field(9)
