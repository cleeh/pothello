#import tensorflow as tf
import numpy as np
import pygame
import sys
import random
from shared import *
from palette import *
from board import *
from othello import *

if __name__ == '__main__':
	# Game init
	game_quit = False
	game = othello()

	# Game start
	while not game_quit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				col = int(event.pos[1]/SQUARE_SIZE)  # y
				row = int(event.pos[0]/SQUARE_SIZE)  # x

				if game.verify(row, col):
					game.put(row, col)
					game.occupy(row, col)
					game.change_turn()

					victory_flag = game.check_victory()
					if victory_flag == SBLACK:
						print('<game over> black is win')
						game.reset()
					elif victory_flag == SWHITE:
						print('<game over> white is win')
						game.reset()
					elif victory_flag == DRAW:
						print('<game over> draw')
						game.reset()
					
					if game.check_putable() == False:
						print('no spot to put on. turn is omitted')
						game.change_turn()

					game.update()
					game.show()