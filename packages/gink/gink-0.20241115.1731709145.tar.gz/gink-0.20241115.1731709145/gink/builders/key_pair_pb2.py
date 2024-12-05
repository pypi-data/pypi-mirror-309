# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/key_pair.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/key_pair.proto',
  package='gink',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14proto/key_pair.proto\x12\x04gink\"1\n\x07KeyPair\x12\x12\n\npublic_key\x18\x01 \x01(\x0c\x12\x12\n\nsecret_key\x18\x02 \x01(\x0c\x62\x06proto3'
)




_KEYPAIR = _descriptor.Descriptor(
  name='KeyPair',
  full_name='gink.KeyPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_key', full_name='gink.KeyPair.public_key', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_key', full_name='gink.KeyPair.secret_key', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=79,
)

DESCRIPTOR.message_types_by_name['KeyPair'] = _KEYPAIR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

KeyPair = _reflection.GeneratedProtocolMessageType('KeyPair', (_message.Message,), {
  'DESCRIPTOR' : _KEYPAIR,
  '__module__' : 'proto.key_pair_pb2'
  # @@protoc_insertion_point(class_scope:gink.KeyPair)
  })
_sym_db.RegisterMessage(KeyPair)


# @@protoc_insertion_point(module_scope)
