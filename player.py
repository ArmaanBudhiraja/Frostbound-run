import pygame

class Player:
    def __init__(self, x, y):
        self.scale = 0.1
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8

        self.idle_img = self.load_image("assets/player/idle.png")
        self.walk_imgs = [
            self.load_image("assets/player/walk1.png"),
            self.load_image("assets/player/walk2.png")
        ]
        self.jump_imgs = [
            self.load_image("assets/player/jump1.png"),
            self.load_image("assets/player/jump2.png"),
            self.load_image("assets/player/jump2.png"),
            self.load_image("assets/player/jump3.png"),
            self.load_image("assets/player/jump4.png")
        ]

        w, h = self.idle_img.get_size()
        self.rect = pygame.Rect(x, y, w, h)

        self.velocity_y = 0
        self.on_ground = False
        self.was_on_ground = False
        self.direction = 1
        self.dx = 0

        self.image = self.idle_img
        self.walk_frame = 0
        self.walk_speed = 0.15
        self.landing_timer = 0
        self.landing_duration = 12

        # Fireball cooldown
        self.fire_cooldown = 0
        self.FIRE_DELAY = 30

    def load_image(self, path):
        img = pygame.image.load(path).convert_alpha()
        w, h = img.get_size()
        return pygame.transform.scale(img, (int(w * self.scale), int(h * self.scale)))

    def can_fire(self):
        return self.fire_cooldown == 0

    def move(self, keys):
        self.dx = 0
        moving = False

        if keys[pygame.K_a]:
            self.dx = -self.speed
            self.direction = -1
            moving = True

        if keys[pygame.K_d]:
            self.dx = self.speed
            self.direction = 1
            moving = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        self.animate(moving)

    def apply_gravity(self):
        self.velocity_y += self.gravity
        if self.velocity_y > 20:
            self.velocity_y = 20

    def update(self, platforms):
        self.rect.x += self.dx
        for p in platforms:
            if self.rect.colliderect(p):
                if self.dx > 0:
                    self.rect.right = p.left
                elif self.dx < 0:
                    self.rect.left = p.right

        self.rect.y += self.velocity_y
        self.was_on_ground = self.on_ground
        self.on_ground = False

        for p in platforms:
            if self.rect.colliderect(p):
                if self.velocity_y > 0:
                    self.rect.bottom = p.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = p.bottom
                    self.velocity_y = 0

        if not self.was_on_ground and self.on_ground:
            self.landing_timer = self.landing_duration

    def animate(self, moving):
        if not self.on_ground:
            if self.velocity_y < -2:
                self.image = self.jump_imgs[1]
            elif -2 <= self.velocity_y <= 2:
                self.image = self.jump_imgs[2]
            else:
                self.image = self.jump_imgs[3]

        elif self.landing_timer > 0:
            self.image = self.jump_imgs[4]
            self.landing_timer -= 1

        elif moving:
            self.walk_frame += self.walk_speed
            if self.walk_frame >= len(self.walk_imgs):
                self.walk_frame = 0
            self.image = self.walk_imgs[int(self.walk_frame)]

        else:
            self.image = self.idle_img

        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen, camera_x):
        r = self.rect.copy()
        r.x -= camera_x
        screen.blit(self.image, r)
