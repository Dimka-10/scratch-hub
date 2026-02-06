import pygame
import sys
from pathlib import Path

SRC_PATH = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SRC_PATH))

from config import SCENE_WIDTH, SCENE_HEIGHT, COLORS, SIZES, error_image_path, settings_icon
from utils.windows_size import windows_surface, pos_on_screen
from ui.renderer import *


def render_main_screen(screen):
    scene_surface, draw_rect, scale = update_scene(screen)

    screen.fill((0, 0, 0))
    scene_surface.fill(COLORS["background"])

    render_projects_menu(scene_surface)
    render_object_menu(scene_surface)
    render_up_menu(scene_surface)

    screen.blit(scene_surface, draw_rect)

#=============================

def render_up_menu(screen):
    up_menu_rect = pygame.Rect(0, 0, SCENE_WIDTH, 50)
    draw_rect(screen, up_menu_rect, COLORS['up_menu'])
    draw_rect(screen, up_menu_rect, (100, 100, 100), 0, 2)

    draw_text(screen, "SCRATCH HUB", 
              (20, 20), 
              (255, 255, 255), font_size=24, align='topleft')

    draw_line(screen, (150, 0), (150, 50), (100, 100, 100), 2)

    draw_image(screen, settings_icon, (165, 10), (30, 30))
    draw_line(screen, (210, 0), (210, 50), (100, 100, 100), 2)
    # Количество проектов
    # Общее количество блоков
    # Количество дней в году когда занимался проектами


def render_object_menu(screen):
    object_menu_rect = pygame.Rect(SCENE_WIDTH - 720, 50, 720, SCENE_HEIGHT - 50)
    draw_rect(screen, object_menu_rect, COLORS['object_menu'])
    draw_rect(screen, object_menu_rect, (70, 90, 110), 0, 2)

    draw_text(screen, "ОБЪЕКТЫ", 
              (SCENE_WIDTH - 360, 80), 
              (255, 255, 255), font_size=20, align='center')

def render_projects_menu(screen):
    projects_menu_rect = pygame.Rect(0, 50, SCENE_WIDTH - 720, SCENE_HEIGHT - 50)
    draw_rect(screen, projects_menu_rect, COLORS['projects_menu'])
    draw_rect(screen, projects_menu_rect, (90, 70, 50), 0, 2)

    draw_text(screen, "ПРОЕКТЫ", 
              ((SCENE_WIDTH - 720) // 2, 80), 
              (255, 255, 255), font_size=20, align='center')