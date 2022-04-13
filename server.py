import socketserver
import pickle
import socket


from common import *
from checks import correct_wall_collide, correct_player_collide

SERVER_ADDR = ("127.0.0.1", 20000)
TICK_RATE = 125


class GameUDPServer(socketserver.ThreadingUDPServer):
    """
    Threaded UDP Server class, instantiates our handler and can broadcast game data
    """

    def __init__(self, server_address, request_handler_class):
        super().__init__(server_address, request_handler_class, True)
        self.clients = set()

    def broadcast(self, data: bytes, source: tuple):
        """
        Sends message to all clients.
        :param data: Pickled data of what is going to be sent.
        :param source: Tuple of the client address
        :return: None
        """
        for client in self.clients:
            if client == source:  # Don't send client's packet back to it
                continue
            self.socket.sendto(data, client)


class ThreadedPacketHandler(socketserver.BaseRequestHandler):
    """
    Handles client packets
    """

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        """
        Receives and parses the client data
        :return: None
        """

        if self.client_address not in self.server.clients:
            # If this is a new client, add it to our server's list so that we can broadcast to it
            self.server.clients.add(self.client_address)
        packet = pickle.loads(self.request[0])  # Load the packet's actual data
        if packet.type == PacketType.DISCONNECT:
            # If the client wants to disconnect, then we will remove it from our broadcasting list
            self.server.clients.remove(self.client_address)
        if packet.type == PacketType.IDLE:
            return
        if packet.type == PacketType.MOVING:
            packet.data = correct_wall_collide(packet.data)

        # Send to all connected clients
        self.server.broadcast(pickle.dumps(packet.data), self.client_address)


def main():
    server = GameUDPServer(SERVER_ADDR, ThreadedPacketHandler)
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # This makes development easier
    try:
        server.serve_forever(5)
    except KeyboardInterrupt:
        server.scheduler_thread.join(5)
        server.shutdown()


if __name__ == "__main__":
    main()
