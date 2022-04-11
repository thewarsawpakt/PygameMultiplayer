import socketserver


SERVER_ADDR = ("127.0.0.1", 20000)


class ThreadedPacketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass


if __name__ == "__main__":
    server = socketserver.ThreadingUDPServer(SERVER_ADDR, ThreadedPacketHandler)

    try:
        server.serve_forever(5)
    except KeyboardInterrupt:
        server.shutdown()
