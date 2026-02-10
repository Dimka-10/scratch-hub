import pygame
import sys
from pathlib import Path

SRC_PATH = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SRC_PATH))

from config import SCENE_WIDTH, SCENE_HEIGHT, COLORS, SIZES, error_image_path, settings_icon
from utils.windows_size import windows_surface, pos_on_screen
from utils.projects_utils import number_projects, number_blocks, number_days, projects_list
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
    MENU_HEIGHT = 50
    PADDING_X = 20
    PADDING_Y = (MENU_HEIGHT - 30)
    SECTION_SPACING = 15
    LINE_WIDTH = 2

    up_menu_rect = pygame.Rect(0, 0, SCENE_WIDTH, MENU_HEIGHT)
    draw_rect(screen, up_menu_rect, COLORS['up_menu'])
    draw_rect(screen, up_menu_rect, (100, 100, 100), 0, LINE_WIDTH)
    
    current_x = PADDING_X

    title_text = "SCRATCH HUB"
    title_font_size = 24
    draw_text(screen, title_text, 
              (current_x, PADDING_Y), 
              (255, 255, 255), font_size=title_font_size, align='topleft')

    title_width, _ = get_text_size(title_text, title_font_size)
    current_x += title_width + SECTION_SPACING

    draw_line(screen, (current_x, 0), (current_x, MENU_HEIGHT), 
              (100, 100, 100), LINE_WIDTH)
    current_x += LINE_WIDTH + SECTION_SPACING

    icon_size = 30
    draw_image(screen, settings_icon, (current_x, PADDING_Y // 2), (icon_size, icon_size))
    current_x += icon_size + SECTION_SPACING

    draw_line(screen, (current_x, 0), (current_x, MENU_HEIGHT), 
              (100, 100, 100), LINE_WIDTH)
    current_x += LINE_WIDTH + SECTION_SPACING

    projects_text = f"Проектов: {number_projects()}"
    projects_font_size = 20
    projects_width, _ = get_text_size(projects_text, projects_font_size)

    max_width = SCENE_WIDTH - current_x - SECTION_SPACING * 3
    if projects_width > max_width / 3:
        projects_font_size = 16
        projects_width, _ = get_text_size(projects_text, projects_font_size)
    
    draw_text(screen, projects_text, 
              (current_x, PADDING_Y), 
              (255, 255, 255), font_size=projects_font_size, align='topleft')
    current_x += projects_width + SECTION_SPACING

    draw_line(screen, (current_x, 0), (current_x, MENU_HEIGHT), 
              (100, 100, 100), LINE_WIDTH)
    current_x += LINE_WIDTH + SECTION_SPACING

    blocks_text = f"Блоков: {number_blocks()}"
    blocks_font_size = 20
    blocks_width, _ = get_text_size(blocks_text, blocks_font_size)
    
    if blocks_width > max_width / 3:
        blocks_font_size = 16
        blocks_width, _ = get_text_size(blocks_text, blocks_font_size)
    
    draw_text(screen, blocks_text, 
              (current_x, PADDING_Y), 
              (255, 255, 255), font_size=blocks_font_size, align='topleft')
    current_x += blocks_width + SECTION_SPACING

    draw_line(screen, (current_x, 0), (current_x, MENU_HEIGHT), 
              (100, 100, 100), LINE_WIDTH)
    current_x += LINE_WIDTH + SECTION_SPACING

    days_text = f"Дней: {number_days()}"
    days_font_size = 20
    days_width, _ = get_text_size(days_text, days_font_size)
    
    if days_width > max_width / 3:
        days_font_size = 16
        days_width, _ = get_text_size(days_text, days_font_size)
    
    draw_text(screen, days_text, 
              (current_x, PADDING_Y), 
              (255, 255, 255), font_size=days_font_size, align='topleft')


def render_object_menu(screen):
    object_menu_rect = pygame.Rect(SCENE_WIDTH - 650, 50, 650, SCENE_HEIGHT - 50)
    draw_rect(screen, object_menu_rect, COLORS['object_menu'])
    draw_rect(screen, object_menu_rect, (70, 90, 110), 0, 2)

    draw_text(screen, "ОБЪЕКТЫ", 
              (SCENE_WIDTH - 325, 80), 
              (255, 255, 255), font_size=20, align='center')

def render_projects_menu(screen):
    projects_menu_rect = pygame.Rect(0, 50, SCENE_WIDTH - 650, SCENE_HEIGHT - 50)
    draw_rect(screen, projects_menu_rect, COLORS['projects_menu'])
    draw_rect(screen, projects_menu_rect, (90, 70, 50), 0, 2)
    
    list_projects = projects_list()

    CARD_WIDTH = 200
    CARD_HEIGHT = 200
    CARD_MARGIN_X = 10
    CARD_MARGIN_Y = 10
    CARDS_PER_ROW = max(1, (SCENE_WIDTH - 650 - CARD_MARGIN_X) // (CARD_WIDTH + CARD_MARGIN_X))

    scroll_offset = 0
    
    projectsY = 0
    projectsX = 0
    card_count = 0
    
    for i, project in enumerate(list_projects):
        x = CARD_MARGIN_X + projectsX * (CARD_WIDTH + CARD_MARGIN_X)
        y = 60 + projectsY * (CARD_HEIGHT + CARD_MARGIN_Y) - scroll_offset

        if y + CARD_HEIGHT > 50 and y < SCENE_HEIGHT:
            name = project.get('name', 'Без названия')
            image = project.get('image', None)
            platform = project.get('platform', 'Неизвестно')
            date = project.get('date', '--.--.----')
            
            render_projects(screen, x, y, name, image, platform, date)
        
        projectsX += 1
        card_count += 1

        if projectsX >= CARDS_PER_ROW:
            projectsX = 0
            projectsY += 1

        if card_count >= 36:
            break

    if not list_projects:
        draw_text(screen, "Нет проектов", 
                  ((SCENE_WIDTH - 650) // 2, 150), 
                  (150, 150, 150), font_size=24, align='center')
        draw_text(screen, "Нажмите '+' чтобы создать первый проект", 
                  ((SCENE_WIDTH - 650) // 2, 190), 
                  (120, 120, 120), font_size=16, align='center')

def render_projects(screen, x, y, name, image, platform, data):
    projects_rect = pygame.Rect(x, y, 200, 200)
    draw_rect(screen, projects_rect, COLORS['projects_bg'], radius=14)

    temp_surface = pygame.Surface((1, 1))

    font_name = pygame.font.Font(None, 20)
    max_chars = 15
    display_name = name[:max_chars] + "..." if len(name) > max_chars else name
    
    draw_text(screen, display_name, 
              (x + 100, y + 180), 
              (255, 255, 255), font_size=20, align='center')

    max_platform_chars = 15
    display_platform = platform[:max_platform_chars] + "..." if len(platform) > max_platform_chars else platform
    draw_text(screen, display_platform,
              (x + 10, y + 10),
              (200, 200, 200), font_size=14, align='topleft')

    draw_text(screen, data,
              (x + 190, y + 10),
              (180, 180, 180), font_size=12, align='topright')

def get_text_size(text, font_size=18):
    """
    Простая функция для измерения текста.
    """
    # Временный шрифт для измерения
    temp_font = pygame.font.Font(None, font_size)
    text_surface = temp_font.render(text, True, (255, 255, 255))
    return text_surface.get_size()

def truncate_text_simple(text, max_chars):
    """
    Простая обрезка текста по количеству символов.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars-3] + "..."