# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: audioID.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='audioID.proto',
  package='audioIDProto',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\raudioID.proto\x12\x0c\x61udioIDProto\"0\n\x11\x61\x64\x64NewSongRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05\x61udio\x18\x02 \x01(\x0c\" \n\x0f\x61\x64\x64NewSongReply\x12\r\n\x05reply\x18\x01 \x01(\t2]\n\x0b\x41udioIDgrpc\x12N\n\naddNewSong\x12\x1f.audioIDProto.addNewSongRequest\x1a\x1d.audioIDProto.addNewSongReply\"\x00\x62\x06proto3'
)




_ADDNEWSONGREQUEST = _descriptor.Descriptor(
  name='addNewSongRequest',
  full_name='audioIDProto.addNewSongRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='audioIDProto.addNewSongRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='audio', full_name='audioIDProto.addNewSongRequest.audio', index=1,
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
  serialized_start=31,
  serialized_end=79,
)


_ADDNEWSONGREPLY = _descriptor.Descriptor(
  name='addNewSongReply',
  full_name='audioIDProto.addNewSongReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='reply', full_name='audioIDProto.addNewSongReply.reply', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=81,
  serialized_end=113,
)

DESCRIPTOR.message_types_by_name['addNewSongRequest'] = _ADDNEWSONGREQUEST
DESCRIPTOR.message_types_by_name['addNewSongReply'] = _ADDNEWSONGREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

addNewSongRequest = _reflection.GeneratedProtocolMessageType('addNewSongRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDNEWSONGREQUEST,
  '__module__' : 'audioID_pb2'
  # @@protoc_insertion_point(class_scope:audioIDProto.addNewSongRequest)
  })
_sym_db.RegisterMessage(addNewSongRequest)

addNewSongReply = _reflection.GeneratedProtocolMessageType('addNewSongReply', (_message.Message,), {
  'DESCRIPTOR' : _ADDNEWSONGREPLY,
  '__module__' : 'audioID_pb2'
  # @@protoc_insertion_point(class_scope:audioIDProto.addNewSongReply)
  })
_sym_db.RegisterMessage(addNewSongReply)



_AUDIOIDGRPC = _descriptor.ServiceDescriptor(
  name='AudioIDgrpc',
  full_name='audioIDProto.AudioIDgrpc',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=115,
  serialized_end=208,
  methods=[
  _descriptor.MethodDescriptor(
    name='addNewSong',
    full_name='audioIDProto.AudioIDgrpc.addNewSong',
    index=0,
    containing_service=None,
    input_type=_ADDNEWSONGREQUEST,
    output_type=_ADDNEWSONGREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_AUDIOIDGRPC)

DESCRIPTOR.services_by_name['AudioIDgrpc'] = _AUDIOIDGRPC

# @@protoc_insertion_point(module_scope)