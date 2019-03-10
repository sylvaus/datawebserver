import socket
import struct
import time
from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler

HEADER_SIZE = 2

DICT_TYPE_SIZE = {
    0: 4,  # int
    1: 4,  # float
}

DICT_TYPE_PARSING = {
    0: "<i",  # int
    1: "<f",  # float
}


class ThreadedTCPRequestHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        """
        Header 1 byte name size, 1 byte param type
        :return:
        """
        name_size, param_type = self.request.recv(HEADER_SIZE)
        data = self.request.recv(name_size + DICT_TYPE_SIZE[param_type])
        name = str(data[0:name_size], "ascii")
        value = struct.unpack(DICT_TYPE_PARSING[param_type], data[name_size:])[0]
        self.server.queue.put((name, (time.time(), value)))


class DataServer(ThreadingMixIn, TCPServer):
    def __init__(self, server_address, request_handler_class, bind_and_activate=True, data_queue=None):
        TCPServer.__init__(self, server_address, request_handler_class, bind_and_activate)
        self.queue = data_queue


def print_val(queue):
    for i in range(3):
        print(queue.get())


if __name__ == '__main__':
    HOST, PORT = "192.168.0.101", 8889


    # data_queue = Queue()
    # data_server = DataServer((HOST, PORT), ThreadedTCPRequestHandler, data_queue=data_queue)
    #
    # data_server_thread = threading.Thread(target=data_server.serve_forever)
    # data_server_thread.start()

    def client(name, value):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(bytes([len(name), 0]) + bytes(name, 'ascii') + struct.pack("<i", value))


    client("arduino_2", 1)
    time.sleep(1)
    client("arduino_1", 2)
    time.sleep(1)
    client("arduino_1", 3)
    time.sleep(1)

    # data_server.shutdown()
    # print_val(data_queue)
