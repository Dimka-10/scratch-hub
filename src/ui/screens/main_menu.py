import pygame
import sys
from pathlib import Path

SRC_PATH = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SRC_PATH))

from utils.windows_size import windows_surface

def render_main_screen(screen):
	screen.fill((0, 0, 0))
	pygame.draw.rect(screen, (0, 255, 0), (200, 100, 50, 50), border_radius=10)
	scene_surface, draw_rect, scale = windows_surface(screen, 640, 360)
	scene_surface.fill((255, 0, 0))
	screen.fill((0, 0, 0))
	screen.blit(scene_surface, draw_rect)