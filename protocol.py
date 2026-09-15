import struct
import asyncio

HOST = "127.0.0.1"
PORT = 65432


async def send_message(writer: asyncio.StreamWriter, message: bytes):
    length_prefix = struct.pack("!I", len(message))
    writer.write(length_prefix + message)
    await writer.drain()



async def recv_message(reader: asyncio.StreamReader) -> bytes:
    header = await  reader.readexactly(4)
    (message_length, )  = struct.unpack("!I", header)
    return await reader.readexactly(message_length)

