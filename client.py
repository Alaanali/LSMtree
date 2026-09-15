import socket
from protocol import HOST, PORT, sendall, recvall


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((HOST, PORT))
    sendall(c, b"Hello Alaa" * 5000)
    msg = recvall(c)

print(f"Received {msg}")