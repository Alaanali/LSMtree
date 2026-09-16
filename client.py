import asyncio
from protocol import HOST, PORT,encode_message,Message,Operation,  send_socket_message,Response, recv_socket_message, decode_response

class Client:

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def _request(self, msg: Message) -> Response:
        msg_bytes = encode_message(msg)
        await send_socket_message(self.writer, msg_bytes)
        rsp_raw = await recv_socket_message(self.reader)
        return decode_response(rsp_raw)
    
    async def set(self, key: bytes, value:bytes) -> Response:
        msg = Message(op=Operation.SET, key=key, value=value)
        return await self._request(msg)

    async def get(self, key:bytes) -> Response:
        msg = Message(op=Operation.GET, key=key, value=b'')
        return await self._request(msg)
  
    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    @classmethod
    async def create(cls):
        return cls(*await asyncio.open_connection(HOST, PORT))

async def main():
    client = await Client.create()

    rsp = await client.set(key=b'name', value=b'alaa')
    print(rsp.code, rsp.payload)

    rsp = await client.get(key=b'name')
    print(rsp.code, rsp.payload)

    rsp = await client.get(key=b'age')
    print(rsp.code, rsp.payload)

    await client.close()

   
asyncio.run(main())