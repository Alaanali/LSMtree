import socket
from protocol import HOST, PORT, sendall, recvall

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Starting server and listening on {HOST}:{PORT}")
    conn, addr = s.accept()

    with conn:
        print(f"Connected by {addr}")
        msg = recvall(conn)
        sendall(conn, b"server got " + msg +  b" Thanks")
