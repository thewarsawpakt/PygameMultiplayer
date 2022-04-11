import socketserver
import pickle
from common import *

SERVER_ADDR = ("127.0.0.1", 20000)


class ThreadedPacketHandler(socketserver.BaseRequestHandler):
    clients = []

    @classmethod
    def broadcast(cls, data: bytes):
        for client in cls.clients:
            if client._closed:
                cls.clients.remove(client)
            else:
                client.send(data)

    def handle(self):
        if self.client_address not in ThreadedPacketHandler.clients:
            ThreadedPacketHandler.append(self.request)
        packet: Packet = pickle.dumps(self.request.recv(1024))
        if packet.type_ == PacketType.DISCONNECT:
            ThreadedPacketHandler.broadcast(pickle.dumps(packet))
        if packet.type_ == PacketType.MOVING:
            pass
        if packet.type_ == PacketType.IDLE:
            pass


if __name__ == "__main__":
    server = socketserver.ThreadingUDPServer(SERVER_ADDR, ThreadedPacketHandler)

    try:
        server.serve_forever(5)
    except KeyboardInterrupt:
        server.shutdown()
