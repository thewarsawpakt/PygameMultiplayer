import pygame
import pickle
import socket
import threading
from common import *

running = True  # Variable that is used to break out of the pygame loop
FPS = 120.0  # How many times per second we are updating the display
SERVER_ADDRESS = ("127.0.0.1", 20000)  # Address of the server we will be connecting to
PACKET_SIZE = 512


class Entity(pygame.sprite.Sprite):
    """
    Container for a basic object that can be drawn.
    """
    def __init__(self, color=(255, 255, 0)):
        super().__init__()
        self.color = color
        self.image = pygame.Surface([16, 16])
        self.rect = self.image.get_rect()
        self.image.fill(self.color, self.rect)
        self.velocity = 1

    def move(self, *args):
        pass

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def dump(self):
        """
        Allows for this object to be sent over a packet, as pygame surfaces cannot be pickled.
        :return: Tuple of its position
        """
        return self.rect.x, self.rect.y


class Player(Entity):
    """
    Main movable player.
    """
    def __init__(self):
        super().__init__()

    def move(self, keys, dt):
        """
        Takes in the delta time and keys pressed
        :param keys: Result from pygame.key.get_pressed()
        :param dt: Milliseconds since last frame
        :return: Boolean stating whether to redraw the player or not.
        """
        x, y = 0, 0
        if keys[pygame.K_w]:
            y -= self.velocity
        if keys[pygame.K_s]:
            y += self.velocity
        if keys[pygame.K_a]:
            x -= self.velocity
        if keys[pygame.K_d]:
            x += self.velocity

        self.rect.move_ip(x, y)

        if x or y:
            return True


class NetworkedPlayer(Entity):
    """
    Entity that is used to draw networked players.
    """
    def __init__(self):
        super().__init__((0, 255, 0))

    def move(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Game:
    def __init__(self, window_size=(500, 500)):
        pygame.init()
        self.display = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.player2 = NetworkedPlayer()
        self.display = pygame.display.get_surface()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def handle_server(self):
        """
        Handles information from the server and updates player2's position
        :return: None
        """
        while packet := pickle.loads(self.socket.recv(PACKET_SIZE)):
            # Receives data from the server and updates our player2 position
            self.player2.move(packet.data)

    def run(self):
        """
        Main method of the game
        :return: None
        """
        self.socket.connect(SERVER_ADDRESS)
        # Create thread to update player2 position and to
        socket_monitor = threading.Thread(target=self.handle_server)
        socket_monitor.start()
        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    socket_monitor.join(0.5)
                    return

            if self.player.move(pygame.key.get_pressed(), dt):
                # Update our position with the server
                packet = Packet(PacketPriority.PRIORITY, type=PacketType.MOVING, data=self.player.dump())
            else:
                # Make sure that the server knows we are still connected
                packet = Packet(PacketPriority.DROPPABLE, type=PacketType.IDLE, data=None)
            self.socket.send(pickle.dumps(packet))
            self.display.fill((255, 255, 255))
            self.player.draw(self.display)
            self.player2.draw(self.display)
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
    pygame.quit()
