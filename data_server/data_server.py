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
    def __init__(self, server_address, request_handler_class,
                 bind_and_activate=True, data_queue=None):
        TCPServer.__init__(self, server_address, request_handler_class, bind_and_activate)
        self.queue = data_queue
