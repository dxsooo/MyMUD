import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'server'))

from config import HOST, PORT


def main():
    # connect
    telnet_string = 'telnet ' + HOST + ' ' + str(PORT)
    os.system(telnet_string)


if __name__ == '__main__':
    main()
