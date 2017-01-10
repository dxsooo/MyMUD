import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# DB
DB_NAME = os.path.join(ROOT_DIR, "MyMUD.db")
TB_NAME = "PLAYERS"
TB_COLUMNS = ['name', 'password', 'create_time', 'last_login', 'last_logout']

# Runtime
HOST = '127.0.0.1'
PORT = 4020
PID_FILE = os.path.join(ROOT_DIR, "MyMUD.pid")
