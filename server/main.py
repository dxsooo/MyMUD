import sys
import os
from config import DB_NAME, PID_FILE, ROOT_DIR
from db import DB
from subprocess import Popen
import signal


def is_running():
    if os.path.exists(PID_FILE):
        f = open(PID_FILE, 'r')
        pid = int(f.read())
        f.close()
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return pid
    return False


def setup():
    if os.path.exists(DB_NAME):
        print "Game had been setup, you can start the game with arg 'start' or reset the game with arg 'reset'"
    else:
        reset()


def start():
    if not is_running():
        if not os.path.exists(DB_NAME):
            reset()
        pid = Popen(['python', os.path.join(ROOT_DIR, 'server.py')]).pid
        f = open(PID_FILE, 'w')
        f.write(str(pid))
        f.close()
        print "Game is running"
    else:
        print "Game is already running!"


def stop():
    pid = is_running()
    if pid:
        os.kill(pid, signal.SIGKILL)
        os.remove(PID_FILE)
        print "Game has been stopped."
    else:
        print "Game is not running!"


def reset():
    pid = is_running()
    if pid:
        print "Game is running, please stop it first"
    else:
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        # create db
        db = DB()
        db.set_default()
        print "Game setup"


def show_db():
    if not os.path.exists(DB_NAME):
        print "No DB found! Please setup or reset the game first"
    else:
        db = DB()
        db.print_all()


def main():
    if len(sys.argv) == 2:
        option = sys.argv[1].lower()
        if option == 'setup':
            setup()
        elif option == 'start':
            start()
        elif option == 'stop':
            stop()
        elif option == 'reset':
            reset()
        elif option == 'show_db':
            show_db()
        else:
            print "options: setup | start | stop | reset | show_db \n"
    else:
        print "options: setup | start | stop | reset | show_db \n"


if __name__ == '__main__':
    main()
