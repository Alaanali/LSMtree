import asyncio
from protocol import HOST, PORT, send_message, recv_message

async def handler(reader:asyncio.StreamReader, writer:asyncio.StreamWriter):
    try:
        while True:
            message = await recv_message(reader)
            await send_message(writer, b"Got this from you ((" + message + b")) Thank you")
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