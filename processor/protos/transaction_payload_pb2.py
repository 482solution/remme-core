# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_payload.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='transaction_payload.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x19transaction_payload.proto\"5\n\x12TransactionPayload\x12\x0f\n\x07payload\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x03 \x01(\tb\x06proto3')
)




_TRANSACTIONPAYLOAD = _descriptor.Descriptor(
  name='TransactionPayload',
  full_name='TransactionPayload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payload', full_name='TransactionPayload.payload', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='method', full_name='TransactionPayload.method', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=82,
)

DESCRIPTOR.message_types_by_name['TransactionPayload'] = _TRANSACTIONPAYLOAD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TransactionPayload = _reflection.GeneratedProtocolMessageType('TransactionPayload', (_message.Message,), dict(
  DESCRIPTOR = _TRANSACTIONPAYLOAD,
  __module__ = 'transaction_payload_pb2'
  # @@protoc_insertion_point(class_scope:TransactionPayload)
  ))
_sym_db.RegisterMessage(TransactionPayload)


# @@protoc_insertion_point(module_scope)
