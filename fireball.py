import pygame
from utils import resource_path
class Fireball:
    def __init__(self, x, y, direction):
        self.image = pygame.image.load(resource_path("assets/images/fireball.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.direction = direction
        self.speed = 12

        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += self.speed * self.direction

    def draw(self, screen, camera_x):
        r = self.rect.copy()
        r.x -= camera_x
        screen.blit(self.image, r)
