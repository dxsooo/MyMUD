import socket

print("udp client1 start")
client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect(("127.0.0.1", 17800))
data1 = client1.recv(1024)
print str(data1)
client1.send(b'I am client1')
client1.close()
print("udp client1 finish")

print("udp client2 start")
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect(("127.0.0.1", 17800))
data2 = client2.recv(1024)
print str(data2)
client2.send(b'I am client2')
client2.close()
print("udp client2 finish")