import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("udp client start")
while True:
    data = raw_input("please input content:")
    client.sendto(bytes(data).encode(), ("127.0.0.1", 17800))
    if data == "quit":
        break
print("udp client finish")
client.close()