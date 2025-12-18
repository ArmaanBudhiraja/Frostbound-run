import json
import pygame
import random

GROUND_TILE_SIZE = 64
FLOAT_TILE_WIDTH = 96
FLOAT_TILE_HEIGHT = 32

def load_level(path, ground_tiles, float_tiles):
    with open(path, "r") as f:
        data = json.load(f)

    # Player start
    player_start = tuple(data["player_start"])

    # Ground blocks
    ground_blocks = []
    for start_x, y, count in data["ground"]:
        for i in range(count):
            x = start_x + i * GROUND_TILE_SIZE
            ground_blocks.append({
                "image": random.choice(ground_tiles),
                "rect": pygame.Rect(x, y, GROUND_TILE_SIZE, GROUND_TILE_SIZE)
            })

    # Floating platforms
    floating_blocks = []
    for x, y in data.get("floating_platforms", []):
        img = random.choice(float_tiles)
        rect = img.get_rect(topleft=(x, y))
        floating_blocks.append({
            "image": img,
            "rect": rect
        })


    # Coins
    coins = [pygame.Rect(x, y, 20, 20) for x, y in data["coins"]]

    # Enemies
    enemies = data["enemies"]

    # Exit
    exit_rect = pygame.Rect(data["exit"][0], data["exit"][1], 64, 64)

    return (
        player_start,
        ground_blocks,
        floating_blocks,
        coins,
        enemies,
        exit_rect
    )
