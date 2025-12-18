import pygame
import sys
import random
from player import Player
from enemy import Enemy
from level_loader import load_level
from fireball import Fireball
from utils import resource_path

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frostbound Run")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GOLD = (255, 215, 0)

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ---------------- PLAYER ----------------
player = Player(100, 400)

lives = 3
invincible_timer = 0
INVINCIBLE_TIME = 60

# ---------------- TILE CONFIG ----------------
GROUND_TILE_SIZE = 64
FLOAT_TILE_WIDTH = 140
FLOAT_TILE_HEIGHT = 32

def load_scaled(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

GROUND_TILES = [
    load_scaled(resource_path(f"assets/tiles/tile{i}.png"), (GROUND_TILE_SIZE, GROUND_TILE_SIZE))
    for i in range(1, 9)
]

FLOAT_TILES = [
    load_scaled(resource_path(f"assets/tiles/tile{i}.png"), (FLOAT_TILE_WIDTH, FLOAT_TILE_HEIGHT))
    for i in range(1, 5)
]

# ---------------- BACKGROUND ----------------
bg_image = load_scaled(resource_path("assets/images/bg.jpg"), (WIDTH, HEIGHT))

# ---------------- EXIT GATE ----------------
GATE_SIZE = (80, 120)
gate_image = load_scaled(resource_path("assets/images/gate.png"), GATE_SIZE)

# ---------------- LEVEL STATE ----------------
current_level = 1
MAX_LEVEL = 5

level_complete = False
level_complete_timer = 0
LEVEL_COMPLETE_DELAY = 120

game_over = False
game_won = False

# ---------------- FIREBALLS ----------------
fireballs = []
diamond_img = pygame.image.load(resource_path("assets/images/diamond.png")).convert_alpha()
diamond_img = pygame.transform.scale(diamond_img, (40, 40))

# ---------------- LOAD LEVEL ----------------
def load_current_level():
    global player_start_pos, ground_blocks, floating_blocks
    global coins, enemies, platforms, exit_rect, level_width
    fireballs.clear()

    (
        player_start_pos,
        ground_blocks,
        floating_blocks,
        coins,
        enemy_data,
        exit_rect
    ) = load_level(
        resource_path(f"levels/level{current_level}.json"),
        GROUND_TILES,
        FLOAT_TILES
    )

    enemies = [Enemy(*e) for e in enemy_data]

    # ---- FORCE GROUND FROM X = 0 ----
    leftmost_x = min(b["rect"].left for b in ground_blocks)
    if leftmost_x > 0:
        y = ground_blocks[0]["rect"].y
        tiles_needed = leftmost_x // GROUND_TILE_SIZE
        for i in range(tiles_needed):
            ground_blocks.append({
                "image": random.choice(GROUND_TILES),
                "rect": pygame.Rect(i * GROUND_TILE_SIZE, y, GROUND_TILE_SIZE, GROUND_TILE_SIZE)
            })

    # ---- LEVEL WIDTH ----
    level_width = max(b["rect"].right for b in ground_blocks)

    # ---- BARRIERS ----
    LEFT_BARRIER = pygame.Rect(-100, 0, 100, HEIGHT)
    RIGHT_BARRIER = pygame.Rect(level_width, 0, 100, HEIGHT)

    platforms = (
        [b["rect"] for b in ground_blocks] +
        [b["rect"] for b in floating_blocks] +
        [LEFT_BARRIER, RIGHT_BARRIER]
    )

    # ---- GATE ON GROUND ----
    exit_rect.size = GATE_SIZE
    ground_top = max(b["rect"].top for b in ground_blocks)
    exit_rect.bottom = ground_top + 2

    player.rect.topleft = player_start_pos
    player.velocity_y = 0

    return enemies

enemies = load_current_level()

score = 0
running = True

# ================= MAIN LOOP =================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (game_over or game_won) and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                lives = 3
                score = 0
                current_level = 1
                game_over = False
                game_won = False
                enemies = load_current_level()

    if not game_over and not game_won:
        keys = pygame.key.get_pressed()

        if not level_complete:
            player.move(keys)
            player.apply_gravity()
            player.update(platforms)
        else:
            player.velocity_y = 0

        # ---- FIRE INPUT ----
        if keys[pygame.K_f] and player.can_fire():
            fx = player.rect.centerx
            fy = player.rect.centery
            fireballs.append(Fireball(fx, fy, player.direction))
            player.fire_cooldown = player.FIRE_DELAY

        # ---- UPDATE FIREBALLS ----
        for fireball in fireballs[:]:
            fireball.update()

            if fireball.rect.right < 0 or fireball.rect.left > level_width:
                fireballs.remove(fireball)
                continue

            for enemy in enemies:
                if fireball.rect.colliderect(enemy.rect) and enemy.alive:
                    enemy.die()
                    if fireball in fireballs:
                        fireballs.remove(fireball)
                    break


        # ---- CAMERA CLAMP ----
        camera_x = player.rect.centerx - WIDTH // 2
        camera_x = max(0, min(camera_x, level_width - WIDTH))

        # ---- HARD PLAYER LIMITS ----
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > level_width:
            player.rect.right = level_width

        # ---- COINS ----
        for coin in coins[:]:
            if player.rect.colliderect(coin):
                coins.remove(coin)
                score += 1

        # ---- ENEMIES ----
        if invincible_timer > 0:
            invincible_timer -= 1

        for enemy in enemies:
            enemy.update(platforms)
            if (
                not level_complete
                and invincible_timer == 0
                and enemy.alive
                and player.rect.colliderect(enemy.rect)
            ):
                lives -= 1
                invincible_timer = INVINCIBLE_TIME
                player.rect.topleft = player_start_pos
                player.velocity_y = 0
                if lives <= 0:
                    game_over = True

        # ---- GATE ----
        if not level_complete and player.rect.colliderect(exit_rect):
            level_complete = True
            level_complete_timer = LEVEL_COMPLETE_DELAY

        if level_complete:
            level_complete_timer -= 1
            if level_complete_timer <= 0:
                level_complete = False
                current_level += 1
                if current_level > MAX_LEVEL:
                    game_won = True
                else:
                    enemies = load_current_level()

    # ================= DRAW =================
    if game_won:
        screen.fill(WHITE)
        win_text = big_font.render("YOU WIN", True, BLACK)
        retry = font.render("Press R to Restart", True, BLACK)
        screen.blit(win_text, win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))
        screen.blit(retry, retry.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))

    elif game_over:
        screen.fill(WHITE)
        text = big_font.render("GAME OVER", True, RED)
        retry = font.render("Press R to Restart", True, BLACK)
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
        screen.blit(retry, retry.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))

    else:
        screen.blit(bg_image, (0, 0))

        for b in ground_blocks:
            r = b["rect"].copy()
            r.x -= camera_x
            screen.blit(b["image"], r)

        for b in floating_blocks:
            r = b["rect"].copy()
            r.x -= camera_x+5
            screen.blit(b["image"], r)

        gate_draw = exit_rect.copy()
        gate_draw.x -= camera_x
        screen.blit(gate_image, gate_draw)

        for coin in coins:
            r = coin.copy()
            r.x -= camera_x
            screen.blit(diamond_img, r)

        for enemy in enemies:
            enemy.draw(screen, camera_x)

        for fireball in fireballs:
            fireball.draw(screen, camera_x)

        if invincible_timer % 10 < 5:
            player.draw(screen, camera_x)

        screen.blit(font.render(f"Score: {score}", True, BLACK), (20, 20))
        screen.blit(font.render(f"Lives: {lives}", True, RED), (20, 50))
        screen.blit(font.render(f"Level: {current_level}", True, BLACK), (20, 80))

        if level_complete:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            text = big_font.render("LEVEL COMPLETE", True, WHITE)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
