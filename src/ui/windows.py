import pygame
from pathlib import Path

def create_screen(width, height, name, icon):
    pygame.display.set_caption(name)
    icon_surface = pygame.image.load(str(icon))
    pygame.display.set_icon(icon_surface)
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen