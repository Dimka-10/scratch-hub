import pygame

pygame.init()

screen = pygame.display.set_mode((640, 360), pygame.RESIZABLE)
pygame.display.set_caption("Scratch hub")

BACKGROUND = (40, 44, 52)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    
    screen.fill(BACKGROUND)
    
    pygame.display.flip()

pygame.quit()