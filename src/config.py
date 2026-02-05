from utils.paths import get_project_root, get_assets_path, get_image_path, get_font_path

icon_path = get_project_root() / "assets" / "icon" / "icon.png"

SCENE_WIDTH = 1920
SCENE_HEIGHT = 1080

COLORS = {
    'background': (30, 30, 40),
    'surface': (40, 40, 50),
    'primary': (70, 130, 180),
    'secondary': (100, 200, 100),
    'accent': (255, 165, 0),
    'text': (255, 255, 255),
    'text_secondary': (200, 200, 200),
    'border': (60, 60, 70),
    'hover': (90, 160, 220),
    'active': (255, 100, 100),
}

SIZES = {
    'border_radius': 8,
    'border_width': 2,
    'button_height': 40,
    'card_padding': 16,
    'text_small': 14,
    'text_medium': 18,
    'text_large': 24,
    'text_title': 36,
}