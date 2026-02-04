import pygame
from ui.windows import create_screen
from ui.screens.main_menu import render_main_screen
from utils.paths import get_project_root
from ui.window_manager import run_loop

def main():
    pygame.init()

    icon_path = get_project_root() / "assets" / "icon" / "icon.png"

    global screen
    screen = create_screen(640, 360, "Scratch hub", icon_path)
    
    def screen_events(event):
        if event.type == pygame.VIDEORESIZE:
            global screen
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    
    def render_handler(screen):
        render_main_screen(screen)
    
    run_loop(
        screen=screen,
        event_handler=screen_events,
        render_handler=render_handler,
        fps=60
    )

if __name__ == "__main__":
    main()