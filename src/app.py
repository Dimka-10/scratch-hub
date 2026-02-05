import pygame
from ui.windows import create_screen
from ui.screens.main_menu import render_main_screen
from ui.window_manager import run_loop
from core.application import update, screen_events
from config import icon_path

def main():
    pygame.init()

    global screen
    screen = create_screen(640, 360, "Scratch hub", icon_path)
    
    run_loop(
        screen=screen,
        event_handler=screen_events,
        update_handler=update,
        render_handler=render_main_screen,
        fps=60
    )

if __name__ == "__main__":
    main()