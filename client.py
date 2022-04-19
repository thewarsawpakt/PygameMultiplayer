import pygame
import pickle
import socket
import threading
from common import *

running = True  # Variable that is used to break out of the pygame loop


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
        self.velocity = 2

    @property
    def display(self):
        return pygame.display.get_surface()

    def move(self, *args):
        pass

    def draw(self):
        self.display.blit(self.image, (self.rect.x, self.rect.y))

    def dump(self):
        """
        Allows for this object to be sent over a packet, as pygame surfaces cannot be pickled.
        :return: pygame.rect.Rect representation of its position
        """
        return self.rect


class Player(Entity):
    """
    Main movable player.
    """
    def __init__(self):
        super().__init__()

    def move(self, keys):
        """
        Takes in the delta time and keys pressed
        :param keys: Result from pygame.key.get_pressed()
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
        self.rect.clamp_ip(self.display.get_rect())

        if x or y:
            return True


class NetworkedPlayer(Entity):
    """
    Entity that is used to draw networked players.
    """
    def __init__(self):
        super().__init__((0, 255, 0))
        self.previous_rect = self.rect

    def move(self, rect):
        self.previous_rect = self.rect
        self.rect = rect

    def check_update(self):
        if self.previous_rect == self.rect:
            return False
        return True


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
        while rect := pickle.loads(self.socket.recv(PACKET_SIZE)):
            # Receives data from the server and updates our player2 position
            self.player2.move(rect)

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
            self.display.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    socket_monitor.join(0.5)
                    return
            if self.player.move(pygame.key.get_pressed()):
                # Update our position with the server
                packet = Packet(PacketPriority.PRIORITY, type=PacketType.MOVING, data=self.player.dump())
                self.player.draw()
            else:
                # Make sure that the server knows we are still connected
                packet = Packet(PacketPriority.DROPPABLE, type=PacketType.IDLE, data=None)
            if self.player2.check_update():
                self.player2.draw()
            self.socket.send(pickle.dumps(packet))
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
    pygame.quit()
