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
        while self.server.running:
            header = self.request.recv(HEADER_SIZE)
            if len(header) == 0:
                return
            name_size, param_type = header

            body_size = name_size + DICT_TYPE_SIZE[param_type]
            body = self.request.recv(body_size)
            if len(body) == 0:
                return

            name = str(body[0:name_size], "ascii")
            value = struct.unpack(DICT_TYPE_PARSING[param_type], body[name_size:])[0]
            self.server.queue.put((name, (time.time(), value)))


class DataServer(ThreadingMixIn, TCPServer):
    def __init__(self, server_address, request_handler_class,
                 bind_and_activate=True, data_queue=None):
        TCPServer.__init__(self, server_address, request_handler_class, bind_and_activate)
        self.queue = data_queue
        self.running = False

    def serve_forever(self, *args, **kwargs):
        self.running = True
        TCPServer.serve_forever(self, *args, **kwargs)

    def shutdown(self):
        self.running = False
        TCPServer.shutdown(self)
