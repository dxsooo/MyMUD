from config import HOST, PORT
from db import DB
import re
from socket import error as socket_error
import socket
import threading
from player import Player


class TelnetConnection:
    def __init__(self, conn_info):
        self.conn, self.addr = conn_info
        self.conn.setblocking(0)

    def send(self, queue):
        try:
            for index, line in enumerate(queue):
                if index != (len(queue) - 1):
                    line += '\r\n'
                self.conn.send(line)
            del queue[:]
        except socket_error:
            return False
        else:
            return True

    def recv(self):
        try:
            new_stuff = self.conn.recv(256)
        except socket_error:
            return False
        else:
            new_stuff = new_stuff.replace('\n', '').replace('\r', '')
            new_stuff = re.sub(r"\xff((\xfa.*?\xf0)|(..))", '', new_stuff)
            if new_stuff:
                return new_stuff
            return False

    def close(self):
        self.conn.close()


class TelnetHandler(threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.daemon = True  # So this thread will exit when the main thread does
        self.server = s
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((HOST, PORT))

    def run(self):
        self.listener.listen(5)
        while 1:
            connection = TelnetConnection(self.listener.accept())
            new_player = Player(connection, self.server)
            self.server.player_list_lock.acquire()
            self.server.player_add(new_player)
            self.server.player_list_lock.release()


class Server:
    def __init__(self):
        self.db = DB()
        self.player_list = {}
        self.player_list_lock = threading.Lock()
        self.player_delete = []

    def start(self):
        while 1:
            self.player_list_lock.acquire()
            list_keys = self.player_list.keys()
            for key in list_keys:
                self.player_list[key].do_tick()
            self.cleanup()
            list_keys = self.player_list.keys()
            for key in list_keys:
                self.player_list[key].send_output()
            self.player_list_lock.release()

    def cleanup(self):
        for player in self.player_delete:
            del self.player_list[player]
        self.player_delete = []

    def tell_all(self, message, player):
        list_keys = self.player_list.keys()
        for key in list_keys:
            if player.uuid == key:
                omessage = "> YOU said: " + message
            else:
                omessage = player.name + " said: " + message
            self.player_list[key].out_que.append(omessage)

    def player_add(self, player):
        key = player.uuid
        self.player_list[key] = player


if __name__ == '__main__':
    s = Server()
    handler = TelnetHandler(s)
    handler.start()
    s.start()
