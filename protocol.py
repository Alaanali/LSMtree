import asyncio
import struct
from dataclasses import dataclass
from enum import IntEnum

HOST = "127.0.0.1"
PORT = 65432


class Operation(IntEnum):
    GET = 1
    SET = 2


class ResponseCode(IntEnum):
    OK = 1
    ERROR = 2
    NOT_FOUND = 3


@dataclass
class Message:
    op: Operation
    key: bytes
    value: bytes


@dataclass
class Response:
    code: ResponseCode
    payload: bytes


def _create_length_prefixed_message(s: bytes) -> bytes:
    return struct.pack("!I", len(s)) + s


async def send_socket_message(writer: asyncio.StreamWriter, message: bytes):
    writer.write(_create_length_prefixed_message(message))
    await writer.drain()


async def recv_socket_message(reader: asyncio.StreamReader) -> bytes:
    header = await reader.readexactly(4)
    (message_length,) = struct.unpack("!I", header)
    return await reader.readexactly(message_length)


# total_size | Operation | key size | key | value size | vlaue
def encode_message(m: Message):
    return (
        struct.pack("!H", m.op.value)
        + _create_length_prefixed_message(m.key)
        + _create_length_prefixed_message(m.value)
    )


def encode_response(rsp: Response):
    return struct.pack("!H", rsp.code.value) + _create_length_prefixed_message(
        rsp.payload
    )


class _Reader:
    def __init__(self, buf: bytes):
        self.offset = 0
        self.buf = buf

    def fmt(self, f: str) -> int:
        (value,) = struct.unpack_from(f, self.buf, self.offset)
        self.offset += struct.calcsize(f)
        return value

    def _bytes(self, n: int) -> bytes:
        chunk = self.buf[self.offset : self.offset + n]
        self.offset += n
        return chunk

    def prefixed(self):
        return self._bytes(self.fmt("!I"))

    def u16(self) -> int:
        return self.fmt("!H")


def decode_message(msg: bytes):
    r = _Reader(msg)
    return Message(op=Operation(r.u16()), key=r.prefixed(), value=r.prefixed())


def decode_response(rsp: bytes):
    r = _Reader(rsp)
    return Response(code=ResponseCode(r.u16()), payload=r.prefixed())
