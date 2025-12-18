import pygame

TILE_SIZE = 32

def load_tileset(path):
    sheet = pygame.image.load(path).convert_alpha()
    tiles = []

    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()

    for y in range(0, sheet_height, TILE_SIZE):
        for x in range(0, sheet_width, TILE_SIZE):
            tile = sheet.subsurface(
                pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            )
            tiles.append(tile)

    return tiles
