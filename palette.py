import pygame

from shared import *

class palette:
	def __init__(self):
		height = COLUMN_COUNT * SQUARE_SIZE
		width = ROW_COUNT * SQUARE_SIZE
		size = (width, height)

		pygame.init()
		self.screen = pygame.display.set_mode(size)

	def draw_board(self):
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):
				pygame.draw.rect(self.screen, BLACK, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Frame
				pygame.draw.rect(self.screen, GREEN, (c*SQUARE_SIZE + FRAME_THICKNESS, r*SQUARE_SIZE, SQUARE_SIZE - 2*FRAME_THICKNESS, SQUARE_SIZE - 2*FRAME_THICKNESS))  # Background

	def draw_stone(self, x, y, color):
		pygame.draw.circle(self.screen, color, (int(x*SQUARE_SIZE + SQUARE_SIZE/2), int(y*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)

	def update(self):
		pygame.display.update()