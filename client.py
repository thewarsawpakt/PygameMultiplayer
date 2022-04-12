import pygame
import pickle
import socket
import threading
from common import *

running = True
FPS = 120.0
SERVER_ADDRESS = ("127.0.0.1", 20000)


class Entity(pygame.sprite.Sprite):
    def __init__(self, color=(255, 255, 0)):
        super().__init__()
        self.color = color
        self.image = pygame.Surface([64, 64])
        self.rect = self.image.get_rect()
        self.image.fill(self.color, self.rect)
        self.velocity = 1

    def move(self, *args):
        pass

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def dump(self):
        return self.rect.x, self.rect.y


class Player(Entity):
    def __init__(self):
        super().__init__()

    def move(self, keys, dt):
        pass
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
        while packet := pickle.loads(self.socket.recv(1024)):
            self.player2.move(packet.data)

    def run(self):
        self.socket.connect(SERVER_ADDRESS)
        socket_monitor = threading.Thread(target=self.handle_server)
        socket_monitor.start()
        while self.running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if self.player.move(pygame.key.get_pressed(), dt):
                packet = Packet(PacketPriority.PRIORITY, type=PacketType.MOVING, data=self.player.dump())
                self.socket.send(pickle.dumps(packet))
            self.display.fill((255, 255, 255))
            self.player.draw(self.display)
            self.player2.draw(self.display)
            pygame.display.flip()
        socket_monitor.join()


if __name__ == "__main__":
    Game().run()
    pygame.quit()
