# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bpln_proto/commander/service/v2/code_snapshot_run.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from bauplan._bpln_proto.commander.service.v2 import (
    common_pb2 as bpln__proto_dot_commander_dot_service_dot_v2_dot_common__pb2,
)


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n7bpln_proto/commander/service/v2/code_snapshot_run.proto\x12\x1f\x62pln_proto.commander.service.v2\x1a,bpln_proto/commander/service/v2/common.proto"\xc8\x02\n\x16\x43odeSnapshotRunRequest\x12M\n\x12job_request_common\x18\x01 \x01(\x0b\x32\x31.bpln_proto.commander.service.v2.JobRequestCommon\x12\x10\n\x08zip_file\x18\x02 \x01(\x0c\x12\x10\n\x03ref\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tnamespace\x18\x04 \x01(\tH\x01\x88\x01\x01\x12H\n\x07\x64ry_run\x18\x05 \x01(\x0e\x32\x37.bpln_proto.commander.service.v2.JobRequestOptionalBool\x12\x13\n\x0btransaction\x18\x06 \x01(\t\x12\x0e\n\x06strict\x18\x07 \x01(\t\x12\r\n\x05\x63\x61\x63he\x18\x08 \x01(\t\x12\x0f\n\x07preview\x18\t \x01(\tB\x06\n\x04_refB\x0c\n\n_namespace"\xa7\x02\n\x17\x43odeSnapshotRunResponse\x12O\n\x13job_response_common\x18\x01 \x01(\x0b\x32\x32.bpln_proto.commander.service.v2.JobResponseCommon\x12\x13\n\x0bsnapshot_id\x18\x02 \x01(\t\x12\x14\n\x0csnapshot_uri\x18\x03 \x01(\t\x12\x0b\n\x03ref\x18\x04 \x01(\t\x12\x11\n\tnamespace\x18\x05 \x01(\t\x12\x0f\n\x07\x64ry_run\x18\x06 \x01(\x08\x12\x13\n\x0btransaction\x18\x07 \x01(\t\x12\x0e\n\x06strict\x18\x08 \x01(\t\x12\r\n\x05\x63\x61\x63he\x18\t \x01(\t\x12\x0f\n\x07preview\x18\n \x01(\t\x12\x1a\n\x12user_branch_prefix\x18\x0b \x01(\tB-Z+github.com/BauplanLabs/commander/service/v2b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, 'bpln_proto.commander.service.v2.code_snapshot_run_pb2', _globals
)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['DESCRIPTOR']._options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z+github.com/BauplanLabs/commander/service/v2'
    _globals['_CODESNAPSHOTRUNREQUEST']._serialized_start = 139
    _globals['_CODESNAPSHOTRUNREQUEST']._serialized_end = 467
    _globals['_CODESNAPSHOTRUNRESPONSE']._serialized_start = 470
    _globals['_CODESNAPSHOTRUNRESPONSE']._serialized_end = 765
# @@protoc_insertion_point(module_scope)
