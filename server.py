import socketserver
import pickle
from common import *
import socket

SERVER_ADDR = ("127.0.0.1", 20000)


class GameUDPServer(socketserver.ThreadingUDPServer):
    def __init__(self, server_address, request_handler_class):
        super().__init__(server_address, request_handler_class, True)
        self.clients = set()

    def broadcast(self, data, source):
        for client in self.clients:
            if client == source:
                continue
            self.socket.sendto(data, client)


class ThreadedPacketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        if self.client_address not in self.server.clients:
            self.server.clients.add(self.client_address)
            print("New client added:", self.client_address)
        packet = pickle.loads(self.request[0])
        if packet.type == PacketType.DISCONNECT:
            self.server.clients.remove(self.client_address)
        self.server.broadcast(self.request[0], self.client_address)


if __name__ == "__main__":
    server = GameUDPServer(SERVER_ADDR, ThreadedPacketHandler)
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.serve_forever(5)
    except KeyboardInterrupt:
        server.shutdown()
