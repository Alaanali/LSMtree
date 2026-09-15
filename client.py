import asyncio
from protocol import HOST, PORT, send_message, recv_message


async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    await send_message(writer, b"Hello Server")
    message = await recv_message(reader)
    print(message)
    writer.close()
    await writer.wait_closed()

asyncio.run(main())