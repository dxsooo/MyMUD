import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 17800))
server.listen(5)
print("tcp server start")
while True:
    conn, addr = server.accept()
    print("client connect, address: ", addr)
    conn.send(b"welcome to server")
    data = conn.recv(1024)
    print data
    conn.close()
print("tcp server finish")
server.close()