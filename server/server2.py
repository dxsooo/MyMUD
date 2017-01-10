import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 17800))
print("udp server start")
while True:
    data, addr = server.recvfrom(1024)
    text = str(data).decode()
    print "address:%s data:%s" % (addr, text)
    if text == "quitc":
        break
print("udp server finish")
server.close()
