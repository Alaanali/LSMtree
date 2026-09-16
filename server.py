import asyncio

from kv_store import KVSTORE
from protocol import (
    HOST,
    PORT,
    Message,
    Operation,
    Response,
    ResponseCode,
    decode_message,
    encode_response,
    recv_socket_message,
    send_socket_message,
)

db = KVSTORE()


def _handle_message(buf: bytes) -> Response:
    message: Message = decode_message(buf)
    code = ResponseCode.OK
    payload = b""
    match message.op:
        case Operation.GET:
            value: bytes = db.get(message.key)
            if value is not None:
                payload = value
            else:
                code = ResponseCode.NOT_FOUND
        case Operation.SET:
            db.set(message.key, message.value)

        case _:
            code = ResponseCode.ERROR

    return Response(code=code, payload=payload)


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while True:
            raw_message = await recv_socket_message(reader)
            try:
                rsp = _handle_message(raw_message)
            except Exception as e:
                rsp = Response(code=ResponseCode.ERROR, payload=str(e).encode())
            await send_socket_message(writer, encode_response(rsp))
    except asyncio.IncompleteReadError:
        pass
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handler, HOST, PORT)
    print(f"Starting server and accepting connection at {HOST}:{PORT}")
    async with server:
        await server.serve_forever()


asyncio.run(main())
