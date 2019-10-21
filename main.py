import pygame
import sys
import tensorflow as tf

from shared import *
from palette import *
from board import *
from othello import *
from pothello import *
from slearn import *

import numpy as np

if __name__ == '__main__':
	# Game init
	game_quit = False
	game_sequence = 0

	game = pothello()
	cnn = brain()
	cnn.init()

	# Random vs AI
	vcount = {'b':0, 'w':0, 'd':0}
	pcount = {'correct':0, 'fail':0}
	cnn.restore()
	while not game_quit:
		spot = None
		# auto_put
		if game.turn == SBLACK:
			spot = game.auto_put()
		# supervised-learned AI
		elif game.turn == SWHITE:
			state = game.feature_spots()
			spot = cnn.predict(state)
			if game.verify(spot['x'], spot['y']):
				pcount['correct'] += 1
				game.put(spot['x'], spot['y'])
			else:
				pcount['fail'] += 1
				spot = game.auto_put()
		# error
		else:
			raise RuntimeError('unknown turn state')

		# update game state
		game.occupy(spot['x'], spot['y'])
		game.change_turn()

		# check victory
		victor = game.check_victory()
		if victor==SBLACK:
			vcount['b'] += 1
			#print('<game over> random win')
		elif victor==SWHITE:
			vcount['w'] += 1
			#print('<game over> AI win')
		elif victor==DRAW:
			vcount['d'] += 1
			#print('<game over> draw')
		if victor==SBLACK or victor==SWHITE or victor==DRAW:
			game_sequence += 1
			game.reset()
			if game_sequence%100 == 0:
				print('#---------- <{0}> statistics ----------#'.format(game_sequence))
				print('<AI> accuracy: {0}'.format((pcount['correct']/(pcount['correct']+pcount['fail']))*100))
				print('<AI> victory count: {0}'.format(vcount['w']/game_sequence))
				print('<AI> lose count: {0}'.format(vcount['b']/game_sequence))
				print('<AI> Draw: {0}'.format(vcount['d']/game_sequence))
		
		# check putable
		if game.check_putable() == False:
			#print('# turn is omitted')
			game.change_turn()

		# show game
		#game.update()
		#game.show()



	''' supervised-learning
	# Train start
	omit_flag = False
	while not game_quit:
		# auto_put
		spot = game.auto_put(False)
		if spot ==  None:
			omit_flag = True
			game.change_turn()
			continue
		game.occupy(spot['x'], spot['y'])	
		game.record(spot['x'], spot['y'], omit_flag)
		game.change_turn()
		#game.show()
		omit_flag = False

		# check victory
		victor = game.check_victory()
		if victor==SBLACK or victor==SWHITE:
			print('#---------- <{0}> Training ----------#'.format(game_sequence))
			game.reset()
			for i in game.log:
				if i['turn'] == victor:
					if i['omit']:
						game.change_turn()
					state = game.feature_spots()
					action = i['y']*COLUMN_COUNT + i['x']
					cnn.train(state, action)

					game.put(i['x'], i['y'], False)
					game.occupy(i['x'], i['y'])
					game.change_turn()
			# save model
			game_sequence += 1
			if game_sequence%SAVE_STEPS == 0:
				cnn.save(game_sequence)

		# reset game
		if victor != SNONE:
			game.reset()
			game.log = []
	'''



	''' 2-Player
	# Game start
	while not game_quit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				col = int(event.pos[1]/SQUARE_SIZE)  # y
				row = int(event.pos[0]/SQUARE_SIZE)  # x

				if game.verify(row, col):
					game.put(row, col)
					game.occupy(row, col)
					game.change_turn()

					victor = game.check_victory()
					if victor == SBLACK:
						print('<game over> black is win')
						game.reset()
					elif victor == SWHITE:
						print('<game over> white is win')
						game.reset()
					elif victor == DRAW:
						print('<game over> draw')
						game.reset()
					
					if game.check_putable() == False:
						print('no spot to put on. turn is omitted')
						game.change_turn()

					game.update()
					game.show()
	'''