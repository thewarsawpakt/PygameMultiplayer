import pygame
import threading
import sys

running = True
FPS = 120.0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = (255, 0, 0)
        self.image = pygame.Surface([64, 64])
        self.rect = self.image.get_rect()
        self.image.fill(self.color, self.rect)
        self.velocity = 1

    def move(self, keys, dt):
        x, y = 0, 0
        if keys[pygame.K_w]:
            y -= self.velocity
        if keys[pygame.K_s]:
            y += self.velocity
        if keys[pygame.K_a]:
            x -= self.velocity
        if keys[pygame.K_d]:
            x += self.velocity

        self.rect.move_ip(x * dt, y * dt)

        if x or y:
            return True

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


class Game:
    def __init__(self, window_size=(500, 500)):
        pygame.init()
        self.display = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.sprites = pygame.sprite.Group()
        self.display = pygame.display.get_surface()

    def run(self):
        print("running")
        while self.running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            if self.player.move(pygame.key.get_pressed(), dt):
                self.display.fill((255, 255, 255))
                self.player.draw(self.display)
                pygame.display.flip()


if __name__ == "__main__":
    Game().run()
    pygame.quit()
