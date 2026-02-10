import pygame
from typing import Tuple, List
from config import SCENE_WIDTH, SCENE_HEIGHT, COLORS, SIZES
from utils.windows_size import windows_surface, pos_on_screen
from config import COLORS, SIZES, SCENE_WIDTH, SCENE_HEIGHT, IMAGES_DIR, ICONS_DIR
from pathlib import Path

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

def draw_image(scene_surface, image_path, position, size=None, align="topleft"):
    try:
        if isinstance(image_path, (str, Path)):
            if isinstance(image_path, str):
                path_obj = Path(image_path)
            else:
                path_obj = image_path

            if len(path_obj.parts) == 1 and not path_obj.exists():
                from config import IMAGES_DIR
                full_path = IMAGES_DIR / path_obj
            else:
                full_path = path_obj

            if not full_path.exists():
                print(f"Файл не найден: {full_path}")
                if 'IMAGES_DIR' in locals():
                    print(f"   Ожидалось в: {IMAGES_DIR}")
                return _draw_placeholder(scene_surface, position, size or (100, 100), align)

            image = pygame.image.load(str(full_path)).convert_alpha()
        elif isinstance(image_path, pygame.Surface):
            image = image_path
        else:
            raise TypeError(f"Неверный тип image_path: {type(image_path)}")

        if size:
            scaled_size = (_scale_value(size[0]), _scale_value(size[1]))
            image = pygame.transform.scale(image, scaled_size)

        image_rect = image.get_rect()

        scaled_pos = _scale_point(position[0], position[1])

        if align == 'center':
            image_rect.center = scaled_pos
        elif align == 'midtop':
            image_rect.midtop = scaled_pos
        elif align == 'midbottom':
            image_rect.midbottom = scaled_pos
        elif align == 'midleft':
            image_rect.midleft = scaled_pos
        elif align == 'midright':
            image_rect.midright = scaled_pos
        elif align == 'bottomleft':
            image_rect.bottomleft = scaled_pos
        elif align == 'bottomright':
            image_rect.bottomright = scaled_pos
        elif align == 'topleft':
            image_rect.topleft = scaled_pos
        elif align == 'topright':
            image_rect.topright = scaled_pos
        else:
            image_rect.topleft = scaled_pos

        scene_surface.blit(image, image_rect)
        return image_rect
        
    except Exception as e:
        print(f"Ошибка загрузки изображения {image_path}: {e}")
        return _draw_placeholder(scene_surface, position, size or (100, 100), align)


def _draw_placeholder(scene_surface, position, size, align="topleft"):
    scaled_size = (_scale_value(size[0]), _scale_value(size[1]))
    scaled_pos = _scale_point(position[0], position[1])

    placeholder = pygame.Surface(scaled_size, pygame.SRCALPHA)

    for y in range(scaled_size[1]):
        color_value = int(100 + 100 * (y / scaled_size[1]))
        pygame.draw.line(placeholder, (color_value, color_value, color_value), 
                        (0, y), (scaled_size[0], y), 1)

    pygame.draw.rect(placeholder, (100, 100, 255), 
                    (0, 0, scaled_size[0], scaled_size[1]), 2)

    pygame.draw.line(placeholder, (255, 100, 100), 
                    (0, 0), (scaled_size[0], scaled_size[1]), 2)
    pygame.draw.line(placeholder, (255, 100, 100), 
                    (scaled_size[0], 0), (0, scaled_size[1]), 2)

    font = pygame.font.Font(None, min(24, scaled_size[1] // 3))
    text_surf = font.render("No Image", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(scaled_size[0]//2, scaled_size[1]//2))
    placeholder.blit(text_surf, text_rect)

    placeholder_rect = placeholder.get_rect()
    if align == 'center':
        placeholder_rect.center = scaled_pos
    elif align == 'topleft':
        placeholder_rect.topleft = scaled_pos
    elif align == 'midtop':
        placeholder_rect.midtop = scaled_pos
    elif align == 'midbottom':
        placeholder_rect.midbottom = scaled_pos
    elif align == 'midleft':
        placeholder_rect.midleft = scaled_pos
    elif align == 'midright':
        placeholder_rect.midright = scaled_pos
    elif align == 'bottomleft':
        placeholder_rect.bottomleft = scaled_pos
    elif align == 'bottomright':
        placeholder_rect.bottomright = scaled_pos
    elif align == 'topright':
        placeholder_rect.topright = scaled_pos
    else:
        placeholder_rect.topleft = scaled_pos

    scene_surface.blit(placeholder, placeholder_rect)
    return placeholder_rect


def draw_icon(scene_surface, icon_name, position, size=32, color=None):
    try:
        from config import ICONS_DIR

        icon_path = ICONS_DIR / f"{icon_name}.png"

        if not icon_path.exists():
            for ext in ['.png', '.jpg', '.jpeg', '.svg']:
                alt_path = ICONS_DIR / f"{icon_name}{ext}"
                if alt_path.exists():
                    icon_path = alt_path
                    break

        if not icon_path.exists():
            print(f"Иконка не найдена: {icon_name} в {ICONS_DIR}")
            return _draw_icon_placeholder(scene_surface, icon_name, position, size)

        return draw_image(scene_surface, icon_path, position, (size, size), align='center')
        
    except ImportError:
        print("Не удалось импортировать ICONS_DIR из config.py")
        return _draw_icon_placeholder(scene_surface, icon_name, position, size)
    except Exception as e:
        print(f"Ошибка рисования иконки {icon_name}: {e}")
        return _draw_icon_placeholder(scene_surface, icon_name, position, size)


def _draw_icon_placeholder(scene_surface, icon_name, position, size):
    scaled_pos = _scale_point(position[0], position[1])
    scaled_size = _scale_value(size)

    icon_surface = pygame.Surface((scaled_size, scaled_size), pygame.SRCALPHA)

    pygame.draw.rect(icon_surface, (100, 150, 255), 
                    (0, 0, scaled_size, scaled_size), border_radius=scaled_size//4)

    if icon_name and len(icon_name) > 0:
        letter = icon_name[0].upper()
        font_size = max(12, scaled_size // 2)
        font = pygame.font.Font(None, font_size)
        text_surf = font.render(letter, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(scaled_size//2, scaled_size//2))
        icon_surface.blit(text_surf, text_rect)

    icon_rect = icon_surface.get_rect(center=scaled_pos)
    scene_surface.blit(icon_surface, icon_rect)
    
    return icon_rect


def draw_sprite(scene_surface, sprite_sheet, frame_rect, position, scale=1.0):
    try:
        frame = sprite_sheet.subsurface(frame_rect)

        if scale != 1.0:
            new_width = _scale_value(frame_rect.width * scale)
            new_height = _scale_value(frame_rect.height * scale)
            frame = pygame.transform.scale(frame, (new_width, new_height))
        else:
            new_width = _scale_value(frame_rect.width)
            new_height = _scale_value(frame_rect.height)
            frame = pygame.transform.scale(frame, (new_width, new_height))

        scaled_pos = _scale_point(position[0], position[1])
        frame_rect = frame.get_rect(center=scaled_pos)
        scene_surface.blit(frame, frame_rect)
        
        return frame_rect
        
    except Exception as e:
        print(f"Ошибка рисования спрайта: {e}")
        return _draw_placeholder(scene_surface, position, 
                               (frame_rect.width * scale, frame_rect.height * scale), 
                               align='center')


def draw_background(scene_surface, image_path, tile=False):
    try:
        if isinstance(image_path, (str, Path)):
            path_obj = Path(image_path) if isinstance(image_path, str) else image_path

            if len(path_obj.parts) == 1 and not path_obj.exists():
                from config import IMAGES_DIR
                full_path = IMAGES_DIR / path_obj
            else:
                full_path = path_obj
            
            if not full_path.exists():
                print(f"⚠Фоновое изображение не найдено: {full_path}")
                raise FileNotFoundError
            
            background = pygame.image.load(str(full_path)).convert()
        else:
            background = image_path

        scene_width, scene_height = scene_surface.get_size()
        
        if tile:
            bg_width, bg_height = background.get_size()
            
            for x in range(0, scene_width, bg_width):
                for y in range(0, scene_height, bg_height):
                    scene_surface.blit(background, (x, y))
        else:
            background = pygame.transform.scale(background, (scene_width, scene_height))
            scene_surface.blit(background, (0, 0))
            
    except Exception as e:
        print(f"Ошибка загрузки фона {image_path}: {e}")
        scene_surface.fill((30, 30, 50))
        for y in range(0, scene_height, 20):
            alpha = int(255 * (y / scene_height))
            pygame.draw.line(scene_surface, (40, 40, 60, alpha), 
                           (0, y), (scene_width, y), 20)


def draw_rounded_image(scene_surface, image_path, position, size, radius=10):
    try:
        if isinstance(image_path, (str, Path)):
            path_obj = Path(image_path) if isinstance(image_path, str) else image_path

            if len(path_obj.parts) == 1 and not path_obj.exists():
                from config import IMAGES_DIR
                full_path = IMAGES_DIR / path_obj
            else:
                full_path = path_obj
            
            if not full_path.exists():
                print(f"Изображение для rounded не найдено: {full_path}")
                return _draw_placeholder(scene_surface, position, size, align='topleft')
            
            image = pygame.image.load(str(full_path)).convert_alpha()
        else:
            image = image_path

        scaled_size = (_scale_value(size[0]), _scale_value(size[1]))
        scaled_radius = _scale_value(radius)
        image = pygame.transform.scale(image, scaled_size)

        mask_surface = pygame.Surface(scaled_size, pygame.SRCALPHA)
        pygame.draw.rect(mask_surface, (255, 255, 255, 255), 
                        (0, 0, *scaled_size), border_radius=scaled_radius)

        image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        scaled_pos = _scale_point(position[0], position[1])
        scene_surface.blit(image, scaled_pos)
        
    except Exception as e:
        print(f"Ошибка рисования rounded image: {e}")
        return _draw_placeholder(scene_surface, position, size, align='topleft')


def draw_button_with_icon(scene_surface, rect, text, icon_name=None, 
                         icon_position="left", icon_size=24, **kwargs):
    btn_rect = draw_button(scene_surface, rect, "", **kwargs)
    
    if icon_name:
        icon_x, icon_y = btn_rect.center
        
        if icon_position == "left":
            icon_x = btn_rect.x + _scale_value(icon_size) // 2 + 10
            text_x = icon_x + _scale_value(icon_size) + 10
            text_y = btn_rect.centery
            draw_icon(scene_surface, icon_name, (icon_x, icon_y), icon_size)
            draw_text(scene_surface, text, (text_x, text_y), 
                     kwargs.get('text_color', 'text'), 
                     kwargs.get('font_size', max(14, rect.height // 2)), 
                     align='center')
            
        elif icon_position == "right":
            icon_x = btn_rect.right - _scale_value(icon_size) // 2 - 10
            text_x = icon_x - _scale_value(icon_size) - 10
            text_y = btn_rect.centery
            draw_icon(scene_surface, icon_name, (icon_x, icon_y), icon_size)
            draw_text(scene_surface, text, (text_x, text_y), 
                     kwargs.get('text_color', 'text'), 
                     kwargs.get('font_size', max(14, rect.height // 2)), 
                     align='center')
            
        elif icon_position == "top":
            icon_y = btn_rect.y + _scale_value(icon_size) // 2 + 5
            text_x = btn_rect.centerx
            text_y = icon_y + _scale_value(icon_size) + 5
            draw_icon(scene_surface, icon_name, (btn_rect.centerx, icon_y), icon_size)
            draw_text(scene_surface, text, (text_x, text_y), 
                     kwargs.get('text_color', 'text'), 
                     kwargs.get('font_size', max(14, rect.height // 2)), 
                     align='center')
            
        elif icon_position == "bottom":
            icon_y = btn_rect.bottom - _scale_value(icon_size) // 2 - 5
            text_x = btn_rect.centerx
            text_y = icon_y - _scale_value(icon_size) - 5
            draw_icon(scene_surface, icon_name, (btn_rect.centerx, icon_y), icon_size)
            draw_text(scene_surface, text, (text_x, text_y), 
                     kwargs.get('text_color', 'text'), 
                     kwargs.get('font_size', max(14, rect.height // 2)), 
                     align='center')
    else:
        draw_text(scene_surface, text, btn_rect.center, 
                 kwargs.get('text_color', 'text'), 
                 kwargs.get('font_size', max(14, rect.height // 2)), 
                 align='center')
    
    return btn_rect

def get_text_size(text, font_size=18, font_path=None):
    temp_surface = pygame.Surface((1, 1), pygame.SRCALPHA)

    scaled_font_size = _scale_value(font_size)
    
    if font_path:
        font = pygame.font.Font(font_path, scaled_font_size)
    else:
        font = pygame.font.Font(None, scaled_font_size)

    text_surface = font.render(text, True, (255, 255, 255))
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()

    virtual_width = int(text_width / _current_scale) if _current_scale > 0 else text_width
    virtual_height = int(text_height / _current_scale) if _current_scale > 0 else text_height
    
    return virtual_width, virtual_height

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
    'draw_image',
    'draw_icon',
    'draw_sprite',
    'draw_background',
    'draw_rounded_image',
    'draw_button_with_icon',
    'get_text_size',
]