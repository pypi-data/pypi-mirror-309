# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bpln_proto/commander/service/v2/runner_comm.proto
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
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n1bpln_proto/commander/service/v2/runner_comm.proto\x12\x1f\x62pln_proto.commander.service.v2\x1a,bpln_proto/commander/service/v2/common.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xf7\x03\n\x0cRunnerAction\x12\x36\n\x06job_id\x18\x01 \x01(\x0b\x32&.bpln_proto.commander.service.v2.JobId\x12\x44\n\x06\x61\x63tion\x18\x02 \x01(\x0e\x32\x34.bpln_proto.commander.service.v2.RunnerAction.Action\x12\x45\n\x0bjob_request\x18\x03 \x01(\x0b\x32+.bpln_proto.commander.service.v2.JobRequestH\x00\x88\x01\x01\x12\x10\n\x08trace_id\x18\x04 \x01(\t\x12\x16\n\x0eparent_span_id\x18\x05 \x01(\t\x12L\n\x08job_args\x18\x06 \x03(\x0b\x32:.bpln_proto.commander.service.v2.RunnerAction.JobArgsEntry\x1a.\n\x0cJobArgsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"j\n\x06\x41\x63tion\x12\x16\n\x12\x41\x43TION_UNSPECIFIED\x10\x00\x12\x10\n\x0c\x41\x43TION_START\x10\x01\x12\x11\n\rACTION_CANCEL\x10\x02\x12\x11\n\rACTION_UPLOAD\x10\x03\x12\x10\n\x0c\x41\x43TION_QUERY\x10\x04\x42\x0e\n\x0c_job_request"\xf8\x04\n\nJobRequest\x12\x0e\n\x06\x64\x65tach\x18\x02 \x01(\x08\x12\x43\n\x04\x61rgs\x18\x0b \x03(\x0b\x32\x35.bpln_proto.commander.service.v2.JobRequest.ArgsEntry\x12:\n\x06status\x18\x06 \x01(\x0e\x32*.bpln_proto.commander.service.v2.JobStatus\x12\x1b\n\x13scheduled_runner_id\x18\x08 \x01(\t\x12\x1d\n\x10physical_plan_v2\x18\t \x01(\x0cH\x00\x88\x01\x01\x12\x18\n\x10scheduling_error\x18\n \x01(\t\x12\x0c\n\x04user\x18\x0c \x01(\t\x12.\n\ncreated_at\x18\r \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0b\x66inished_at\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bread_branch\x18\x0f \x01(\t\x12\x14\n\x0cwrite_branch\x18\x10 \x01(\t\x12\x43\n\x04tags\x18\x11 \x03(\x0b\x32\x35.bpln_proto.commander.service.v2.JobRequest.TagsEntry\x1a+\n\tArgsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x13\n\x11_physical_plan_v2J\x04\x08\x04\x10\x05J\x04\x08\x07\x10\x08J\x04\x08\x05\x10\x06J\x04\x08\x03\x10\x04J\x04\x08\x01\x10\x02R\x05stepsR\x10physical_plan_id"\xa1\x03\n\x11TriggerRunRequest\x12\x10\n\x08zip_file\x18\x01 \x01(\x0c\x12\x16\n\x0emodule_version\x18\x02 \x01(\t\x12\x17\n\x0f\x63lient_hostname\x18\x04 \x01(\t\x12J\n\x04\x61rgs\x18\x05 \x03(\x0b\x32<.bpln_proto.commander.service.v2.TriggerRunRequest.ArgsEntry\x12\x17\n\x0fis_flight_query\x18\x06 \x01(\x08\x12\x1d\n\x10query_for_flight\x18\x07 \x01(\tH\x00\x88\x01\x01\x12\x13\n\x06run_id\x18\x08 \x01(\tH\x01\x88\x01\x01\x12\r\n\x05\x63\x61\x63he\x18\n \x01(\x08\x12\x16\n\tnamespace\x18\x0b \x01(\tH\x02\x88\x01\x01\x1a+\n\tArgsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x13\n\x11_query_for_flightB\t\n\x07_run_idB\x0c\n\n_namespaceJ\x04\x08\t\x10\nJ\x04\x08\x03\x10\x04R\rmeta_snapshotR\x13\x61llocation_strategy*\xa1\x01\n\tJobStatus\x12\x1a\n\x16JOB_STATUS_UNSPECIFIED\x10\x00\x12\x16\n\x12JOB_STATUS_PENDING\x10\x01\x12\x16\n\x12JOB_STATUS_RUNNING\x10\x02\x12\x18\n\x14JOB_STATUS_COMPLETED\x10\x03\x12\x15\n\x11JOB_STATUS_FAILED\x10\x04\x12\x17\n\x13JOB_STATUS_CANCELED\x10\x05\x42-Z+github.com/BauplanLabs/commander/service/v2b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, 'bpln_proto.commander.service.v2.runner_comm_pb2', _globals
)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['DESCRIPTOR']._options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z+github.com/BauplanLabs/commander/service/v2'
    _globals['_RUNNERACTION_JOBARGSENTRY']._options = None
    _globals['_RUNNERACTION_JOBARGSENTRY']._serialized_options = b'8\001'
    _globals['_JOBREQUEST_ARGSENTRY']._options = None
    _globals['_JOBREQUEST_ARGSENTRY']._serialized_options = b'8\001'
    _globals['_JOBREQUEST_TAGSENTRY']._options = None
    _globals['_JOBREQUEST_TAGSENTRY']._serialized_options = b'8\001'
    _globals['_TRIGGERRUNREQUEST_ARGSENTRY']._options = None
    _globals['_TRIGGERRUNREQUEST_ARGSENTRY']._serialized_options = b'8\001'
    _globals['_JOBSTATUS']._serialized_start = 1727
    _globals['_JOBSTATUS']._serialized_end = 1888
    _globals['_RUNNERACTION']._serialized_start = 166
    _globals['_RUNNERACTION']._serialized_end = 669
    _globals['_RUNNERACTION_JOBARGSENTRY']._serialized_start = 499
    _globals['_RUNNERACTION_JOBARGSENTRY']._serialized_end = 545
    _globals['_RUNNERACTION_ACTION']._serialized_start = 547
    _globals['_RUNNERACTION_ACTION']._serialized_end = 653
    _globals['_JOBREQUEST']._serialized_start = 672
    _globals['_JOBREQUEST']._serialized_end = 1304
    _globals['_JOBREQUEST_ARGSENTRY']._serialized_start = 1140
    _globals['_JOBREQUEST_ARGSENTRY']._serialized_end = 1183
    _globals['_JOBREQUEST_TAGSENTRY']._serialized_start = 1185
    _globals['_JOBREQUEST_TAGSENTRY']._serialized_end = 1228
    _globals['_TRIGGERRUNREQUEST']._serialized_start = 1307
    _globals['_TRIGGERRUNREQUEST']._serialized_end = 1724
    _globals['_TRIGGERRUNREQUEST_ARGSENTRY']._serialized_start = 1140
    _globals['_TRIGGERRUNREQUEST_ARGSENTRY']._serialized_end = 1183
# @@protoc_insertion_point(module_scope)
