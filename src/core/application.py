import pygame

def screen_events(event):
    if event.type == pygame.VIDEORESIZE:
        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

def update():
	pass