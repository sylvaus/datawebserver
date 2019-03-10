import configparser
import socket
import struct
import time


def client(host, port, name, value):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(bytes([len(name), 0]) + bytes(name, 'ascii') + struct.pack("<i", value))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("../app.ini")
    if config.getboolean("server.data", "auto_host"):
        host = socket.gethostbyname(socket.gethostname())
    else:
        host = config.getboolean("server.data", "host")
    port = config.getint("server.data", "port")

    client(host, port, "arduino_2", 1)
    time.sleep(1)
    client(host, port, "arduino_1", 2)
    time.sleep(1)
    client(host, port, "arduino_1", 3)
    time.sleep(1)
