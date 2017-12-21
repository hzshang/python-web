# -*- coding: utf-8 -*-
import threading
import socket
import traceback

from request import request
import select


class Server(object):
    """a web framwork"""

    def __init__(self, data):
        self.address = data['listen_address']
        self.port = data['port']
        self.threadPool = data['pool']
        self.root = data['root']
        self.index = data['index']
        self.time_out = data['time_out']

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.address, self.port))
        self.sock.listen(self.threadPool)
        while True:
            try:
                client_socket, client_address = self.sock.accept()
            except Exception as e:
                raise
            else:
                print "Connect from %s: %s\r\n" % client_address
                t = threading.Thread(target=self.__handle_connection, args=(client_socket, client_address))
                t.daemon = True
                t.start()

    def __handle_connection(self, sock, address):
        while True:
            try:
                re = request(self.root, self.index)
                re.process_data(sock)
                payload = re.get_response()
                sock.send(payload)
            except Exception as e:
                traceback.print_exc()
                sock.close()
                break
        print "disconnect from %s: %s\n" % address
