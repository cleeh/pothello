import pygame

from shared import *

class palette:
	def __init__(self):
		pygame.init()
		pygame.font.init()
		self.font = pygame.font.SysFont('Comic Sans MS', 16)

		width = ROW_COUNT * SQUARE_SIZE + SCORE_BOARD_WIDTH
		height = COLUMN_COUNT * SQUARE_SIZE
		size = (width, height)
		self.screen = pygame.display.set_mode(size)

	def change_font(self, size, font='Comic Sans MS'):
		self.font = pygame.font.SysFont(font, size)

	def print_text(self, string, x, y, color):
		rtext = self.font.render(string, False, color)
		self.screen.blit(rtext, dest=(x, y))

	def draw_score_board(self, board_color=BLACK, font_color=WHITE):
		height = SQUARE_SIZE*COLUMN_COUNT
		pygame.draw.rect(self.screen, board_color, (SQUARE_SIZE*ROW_COUNT, 0, SCORE_BOARD_WIDTH, height))
		self.change_font(30)
		self.print_text("Score Board", ROW_COUNT*SQUARE_SIZE+11, 30, font_color)
		self.change_font(20)
		self.print_text("<Black>  vs  <White>", ROW_COUNT*SQUARE_SIZE+10, 100, font_color)

	def draw_score(self, black_score, white_score, score_color=WHITE, font_size=23, board_color=BLACK):
		self.change_font(font_size)
		pygame.draw.rect(self.screen, board_color, (SQUARE_SIZE*ROW_COUNT+36, 140, 40, font_size*1.5))
		self.print_text(str(black_score), ROW_COUNT*SQUARE_SIZE+36, 140, score_color)
		pygame.draw.rect(self.screen, board_color, (SQUARE_SIZE*ROW_COUNT+146, 140, 40, font_size*1.5))
		self.print_text(str(white_score), ROW_COUNT*SQUARE_SIZE+146, 140, score_color)

	def draw_turn(self, stone_color, panel_color=TEAL):
		pygame.draw.rect(self.screen, panel_color, (SQUARE_SIZE*ROW_COUNT+20, SQUARE_SIZE*COLUMN_COUNT-120, 160, 60))
		pygame.draw.circle(self.screen, stone_color, (SQUARE_SIZE*ROW_COUNT+100, SQUARE_SIZE*COLUMN_COUNT-120+30), RADIUS)

	def draw_board(self):
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT):
				pygame.draw.rect(self.screen, BLACK, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Frame
				pygame.draw.rect(self.screen, GREEN, (c*SQUARE_SIZE + FRAME_THICKNESS, r*SQUARE_SIZE, SQUARE_SIZE - 2*FRAME_THICKNESS, SQUARE_SIZE - 2*FRAME_THICKNESS))  # Background

	def draw_stone(self, x, y, color):
		pygame.draw.circle(self.screen, color, (int(x*SQUARE_SIZE + SQUARE_SIZE/2), int(y*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)

	def update(self):
		pygame.display.update()