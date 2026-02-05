import pygame
import sys
from pathlib import Path
from config import SCENE_WIDTH, SCENE_HEIGHT, COLORS, SIZES

SRC_PATH = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SRC_PATH))

from utils.windows_size import windows_surface, pos_on_screen
from ui.renderer import *

def render_main_screen(screen):
    scene_surface, draw_rect, scale = update_scene(screen)

    screen.fill((0, 0, 0))
    scene_surface.fill((10, 10, 10))

    draw_triangle(scene_surface, [(100, 100), (150, 50), (200, 100)], "primary")

    center_x = SCENE_WIDTH // 2
    center_y = SCENE_HEIGHT // 2
    draw_circle(scene_surface, (center_x, center_y), 50, "secondary")
    
    # Прямоугольник (кнопка)
    draw_button(scene_surface, (50, 200, 150, 40), "Нажми меня")
    
    # Текст
    draw_text(scene_surface, "Scratch Hub", 
              (SCENE_WIDTH // 2, 20), 
              "text", font_size=36, align='center')
    
    # Прогресс-бар
    draw_progress_bar(scene_surface, (50, 300, 200, 20), 0.75)
    
    # Сетка для отладки (раскомментируйте при необходимости)
    # draw_grid(scene_surface, cell_size=50)
    
    # 5. Отображаем сцену на экране
    screen.blit(scene_surface, draw_rect)
    
    # 6. Рамка вокруг сцены (опционально)
    pygame.draw.rect(screen, (0, 255, 255), draw_rect, 2)

    screen.blit(scene_surface, draw_rect)