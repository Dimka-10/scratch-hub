import pygame

def render_main_screen(screen):
	screen.fill((0, 0, 0))
	pygame.draw.rect(screen, (0, 255, 0), (200, 100, 50, 50), border_radius=10)