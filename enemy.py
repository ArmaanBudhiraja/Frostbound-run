import pygame
from utils import resource_path
class Enemy:
    def __init__(self, x, y, left_limit, right_limit):
        self.scale = 0.1
        self.speed = 1
        self.anim_speed = 0.15
        self.gravity = 0.8

        self.walk_imgs = [
            self.load_image(resource_path("assets/enemy/walk1.png")),
            self.load_image(resource_path("assets/enemy/walk2.png")),
            self.load_image(resource_path("assets/enemy/walk3.png"))
        ]
        self.dead_img = self.load_image(resource_path("assets/enemy/dead.png"))

        w, h = self.walk_imgs[0].get_size()
        self.rect = pygame.Rect(x, y, w, h)

        self.left_limit = left_limit
        self.right_limit = right_limit
        self.direction = 1

        self.alive = True
        self.dying = False
        self.dead = False
        self.velocity_y = 0

        self.frame_index = 0
        self.image = self.walk_imgs[0]

    def load_image(self, path):
        img = pygame.image.load(path).convert_alpha()
        w, h = img.get_size()
        return pygame.transform.scale(img, (int(w * self.scale), int(h * self.scale)))

    def die(self):
        if self.alive:
            self.alive = False
            self.dying = True
            self.velocity_y = -10

    def update(self, platforms):
        if self.dead:
            return

        if self.alive:
            self.rect.x += self.speed * self.direction

            if self.rect.left <= self.left_limit:
                self.direction = 1
            elif self.rect.right >= self.right_limit:
                self.direction = -1

            self.frame_index += self.anim_speed
            if self.frame_index >= len(self.walk_imgs):
                self.frame_index = 0

            self.image = self.walk_imgs[int(self.frame_index)]
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

        elif self.dying:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            for p in platforms:
                if self.rect.colliderect(p) and self.velocity_y > 0:
                    self.rect.bottom = p.top
                    self.velocity_y = 0
                    self.dying = False
                    self.dead = True
                    self.image = self.dead_img
                    break

    def draw(self, screen, camera_x):
        r = self.rect.copy()
        r.x -= camera_x
        screen.blit(self.image, r)
