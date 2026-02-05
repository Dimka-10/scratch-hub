import pygame

def windows_surface(screen, width, height):
    screen_width, screen_height = screen.get_size()
    
    scene_ratio = width / height
    screen_ratio = screen_width / screen_height
    
    if screen_ratio > scene_ratio:
        scale_factor = screen_height / height
        scaled_width = int(width * scale_factor)
        scaled_height = screen_height
        
        scene_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        
        x = (screen_width - scaled_width) // 2
        y = 0
        draw_rect = pygame.Rect(x, y, scaled_width, scaled_height)
        
    else:
        scale_factor = screen_width / width
        scaled_width = screen_width
        scaled_height = int(height * scale_factor)

        scene_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        
        x = 0
        y = (screen_height - scaled_height) // 2
        draw_rect = pygame.Rect(x, y, scaled_width, scaled_height)
    
    return scene_surface, draw_rect, scale_factor

def pos_on_screen(screen, width, height, x, y):
    scene_surface, draw_rect, scale_factor = windows_surface(screen, width, height)

    screen_x = int(x * scale_factor) + draw_rect.x
    screen_y = int(y * scale_factor) + draw_rect.y
    
    return screen_x, screen_y

def screen_to_virtual(screen, width, height, screen_x, screen_y):
    scene_surface, draw_rect, scale_factor = windows_surface(screen, width, height)

    if not draw_rect.collidepoint(screen_x, screen_y):
        return None

    x = int((screen_x - draw_rect.x) / scale_factor)
    y = int((screen_y - draw_rect.y) / scale_factor)
    
    return x, y