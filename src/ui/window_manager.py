import pygame
from typing import Callable

def run_loop(screen: pygame.Surface, 
                  event_handler: Callable = None,
                  update_handler: Callable = None, 
                  render_handler: Callable = None,
                  fps: int = 60):

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            
            if event_handler:
                event_handler(event)
        
        if update_handler:
            update_handler()
        
        screen.fill((30, 30, 40))
        
        if render_handler:
            render_handler(screen)

        pygame.display.flip()

        clock.tick(fps)
    
    pygame.quit()