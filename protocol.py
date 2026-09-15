import struct


HOST = "127.0.0.1"
PORT = 65432


def sendall(conn, message: bytes):
    length_prefix = struct.pack("!I", len(message))
    conn.sendall(length_prefix +message)



def recvall(conn) -> bytes:
    buf = b''

    header = conn.recv(4)
    (message_length,)  = struct.unpack("!I", header)
    while len(buf) < message_length:
        buf += conn.recv(message_length - len(buf))

    return buf



