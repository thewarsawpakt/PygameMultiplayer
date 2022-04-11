import pygame
import enum


class PlayerStates(enum.Enum):
    PLAYER_IDLING = 0
    PLAYER_MOVING = 1
    PLAYER_JUMPING = 2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = (255, 255, 255)
        self.image = pygame.Surface([64, 64])
        self.rect = self.image.get_rect()
        self.image.fill(self.color, self.rect)
        self.display = pygame.display.get_surface()
        self.state = PlayerStates.PLAYER_IDLING
        self.velocity = 1

    def move(self, keys, dt):
        #  if self.state == PlayerStates.PLAYER_JUMPING:
        #      return False

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
        return True

    def draw(self):
        self.display.blit(self.image, (self.rect.x, self.rect.y))


pygame.init()
display = pygame.display.set_mode((500, 500))
running = True
FPS = 120.0
clock = pygame.time.Clock()
bob = Player()
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    bob.move(pygame.key.get_pressed(), dt)
    display.fill((0, 0, 0))
    bob.draw()
    pygame.display.flip()

pygame.quit()
