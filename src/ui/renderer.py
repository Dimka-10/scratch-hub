import pygame
from typing import Tuple, List
from config import SCENE_WIDTH, SCENE_HEIGHT, COLORS, SIZES
from utils.windows_size import windows_surface, pos_on_screen

_current_scale = 1.0
_current_draw_rect = None

def update_scene(screen):
    global _current_scale, _current_draw_rect
    
    scene_surface, draw_rect, scale_factor = windows_surface(
        screen, SCENE_WIDTH, SCENE_HEIGHT
    )
    
    _current_scale = scale_factor
    _current_draw_rect = draw_rect
    
    return scene_surface, draw_rect, scale_factor

def _get_color(color):
    if isinstance(color, str) and color in COLORS:
        return COLORS[color]
    return color

def _scale_point(x, y):
    return (int(x * _current_scale), int(y * _current_scale))

def _scale_value(value):
    return int(value * _current_scale)

def draw_triangle(scene_surface, points, color):
    scaled_points = [_scale_point(x, y) for x, y in points]
    color_data = _get_color(color)
    pygame.draw.polygon(scene_surface, color_data, scaled_points)

def draw_line(scene_surface, start_pos, end_pos, color, width=1):
    scaled_start = _scale_point(*start_pos)
    scaled_end = _scale_point(*end_pos)
    color_data = _get_color(color)
    pygame.draw.line(scene_surface, color_data, scaled_start, scaled_end, width)

def draw_circle(scene_surface, center, radius, color, width=0):
    scaled_center = _scale_point(*center)
    scaled_radius = _scale_value(radius)
    color_data = _get_color(color)
    pygame.draw.circle(scene_surface, color_data, scaled_center, scaled_radius, width)

def draw_rect(scene_surface, rect, color, radius=0, width=0):
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(rect)
    
    scaled_rect = pygame.Rect(
        _scale_point(rect.x, rect.y)[0],
        _scale_point(rect.x, rect.y)[1],
        _scale_value(rect.width),
        _scale_value(rect.height)
    )
    
    color_data = _get_color(color)
    
    if radius > 0:
        scaled_radius = _scale_value(radius)
        pygame.draw.rect(scene_surface, color_data, scaled_rect, 
                        width, border_radius=scaled_radius)
    else:
        if width == 0:
            scene_surface.fill(color_data, scaled_rect)
        else:
            pygame.draw.rect(scene_surface, color_data, scaled_rect, width)

def draw_text(scene_surface, text, position, color="text", 
              font_size=18, font_path=None, align="topleft"):
    scaled_position = _scale_point(*position)
    scaled_font_size = _scale_value(font_size)
    color_data = _get_color(color)
    
    if font_path:
        font = pygame.font.Font(font_path, scaled_font_size)
    else:
        font = pygame.font.Font(None, scaled_font_size)
    
    text_surface = font.render(text, True, color_data)
    text_rect = text_surface.get_rect()

    if align == 'center':
        text_rect.center = scaled_position
    elif align == 'midtop':
        text_rect.midtop = scaled_position
    elif align == 'midbottom':
        text_rect.midbottom = scaled_position
    elif align == 'midleft':
        text_rect.midleft = scaled_position
    elif align == 'midright':
        text_rect.midright = scaled_position
    elif align == 'bottomleft':
        text_rect.bottomleft = scaled_position
    elif align == 'bottomright':
        text_rect.bottomright = scaled_position
    elif align == 'topleft':
        text_rect.topleft = scaled_position
    elif align == 'topright':
        text_rect.topright = scaled_position
    else:
        text_rect.topleft = scaled_position

    scene_surface.blit(text_surface, text_rect)
    return text_rect

def draw_button(scene_surface, rect, text, 
                color="primary", text_color="text",
                hovered=False, pressed=False, 
                font_size=None, radius=8):
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(rect)
    
    if isinstance(color, str):
        base_color = COLORS.get(color, COLORS['primary'])
    else:
        base_color = color
    
    if isinstance(text_color, str):
        txt_color = COLORS.get(text_color, COLORS['text'])
    else:
        txt_color = text_color
    
    if pressed:
        btn_color = COLORS.get('active', (255, 100, 100))
    elif hovered:
        btn_color = COLORS.get('hover', 
                              tuple(min(c + 30, 255) for c in base_color))
    else:
        btn_color = base_color
    
    draw_rect(scene_surface, rect, btn_color, radius)
    
    draw_rect(scene_surface, rect, "border", radius, width=2)

    if font_size is None:
        font_size = max(14, rect.height // 2)
    
    text_x = rect.x + rect.width // 2
    text_y = rect.y + rect.height // 2
    draw_text(scene_surface, text, (text_x, text_y), 
              text_color, font_size, align='center')
    return rect

def draw_progress_bar(scene_surface, rect, progress, 
                      color="primary", bg_color="surface"):
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(rect)

    if isinstance(bg_color, str):
        background = COLORS.get(bg_color, COLORS['surface'])
    else:
        background = bg_color
    
    if isinstance(color, str):
        fill_color = COLORS.get(color, COLORS['primary'])
    else:
        fill_color = color

    draw_rect(scene_surface, rect, background, radius=rect.height // 2)

    if progress > 0:
        fill_width = max(rect.height, int(rect.width * progress))
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        draw_rect(scene_surface, fill_rect, fill_color, radius=rect.height // 2)

    percent_text = f"{int(progress * 100)}%"
    text_x = rect.x + rect.width // 2
    text_y = rect.y + rect.height // 2
    draw_text(scene_surface, percent_text, (text_x, text_y), 
              "text", rect.height // 2, align='center')
    return rect

def draw_grid(scene_surface, cell_size=100, color=(255, 255, 255, 50)):
    color_data = _get_color(color) if isinstance(color, str) else color
    
    for x in range(0, SCENE_WIDTH, cell_size):
        start = _scale_point(x, 0)
        end = _scale_point(x, SCENE_HEIGHT)
        pygame.draw.line(scene_surface, color_data, start, end, 1)
  
    for y in range(0, SCENE_HEIGHT, cell_size):
        start = _scale_point(0, y)
        end = _scale_point(SCENE_WIDTH, y)
        pygame.draw.line(scene_surface, color_data, start, end, 1)

__all__ = [
    'update_scene',
    'draw_triangle',
    'draw_line',
    'draw_circle',
    'draw_rect',
    'draw_text',
    'draw_button',
    'draw_progress_bar',
    'draw_grid',
]