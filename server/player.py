import datetime


class Player:
    def __init__(self, connection, server):
        self.conn = connection
        self.uuid = self.conn
        self.name = ""
        self.password = ""
        self.server = server
        self.in_que = []
        self.out_que = []
        self.out_que.append("===== Welcome to MyMUD =====")
        self.state = "init"
        self.innew = False
        self.log_in()

    def send_output(self):
        if len(self.out_que) > 0:
            if self.state == "online":
                self.out_que.append('> ')
            alive = self.conn.send(self.out_que)

            if not alive:
                self.log_out()

    def read_input(self):
        if len(self.in_que) > 0:
            arg = self.in_que[0].strip().replace('\r', '').replace('\n', '')
            del self.in_que[0]
            self.valid_input(arg)

    def get_input(self):
        data = self.conn.recv()
        if data:
            self.in_que.append(data)

    def valid_input(self, arg):
        if self.state == "init":
            if arg == "new":
                message = "Enter name: "
                self.out_que.append(message)
                self.innew = True
            else:
                if self.name == "":
                    self.verify_name(arg)
                else:
                    self.verify_password(arg)
        elif self.state == "online":
            if arg == "info":
                row = self.server.db.select_login(self.name)
                message = "name: " + self.name + "\n"
                message += "online: " + str(
                    datetime.datetime.now() - datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'))
                self.out_que.append(message)
            elif arg == "quit":
                self.log_out()
            elif arg == "chat":
                message = "Cannot send empty chat"
                self.out_que.append(message)
            elif len(arg) >= 5 and arg[:5] == "chat ":
                message = arg[5:]
                self.server.tell_all(message, self)
            else:
                message = "Useless input!"
                self.out_que.append(message)

    def verify_name(self, arg):
        if not self.server.db.check_exist(arg):
            if not self.innew:
                message = "No player named '" + arg + "' exists!"
                self.out_que.append(message)
                self.log_in()
            else:
                self.name = arg
                self.out_que.append("Enter password: ")
        else:
            self.name = arg
            row = self.server.db.select_pwd(self.name)
            if row:
                self.password = row[0]
                self.out_que.append("Enter password: ")

    def verify_password(self, arg):
        if self.password == "":
            self.password = arg
            self.server.db.insert_item([self.name, self.password, datetime.datetime.now(), None, None])
        if self.password != arg:
            message = "password error, please enter again: "
            self.out_que.append(message)
        else:
            self.state = "online"
            self.server.db.update_login((datetime.datetime.now(), self.name))
            message = "** Login Success! **\ncommands: info|quit|chat [words]"
            self.out_que.append(message)

    def log_in(self):
        intro_message = 'Type "new" to create a new player. Or, enter an existed player name.\nname: '
        self.out_que.append(intro_message)

    def log_out(self):
        try:
            self.conn.close()
        except:
            pass
        self.server.db.update_logout((datetime.datetime.now(), self.name))
        self.server.player_delete.append(self.uuid)

    def do_tick(self):
        self.get_input()
        self.read_input()
