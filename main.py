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

# 1-Player
def one_man_game(loading_step=0):
	# initialize game
	game_quit = False
	game_sequence = 0
	game = pothello()

	# initialize cnn
	cnn = brain()
	cnn.init()
	if loading_step > 0:
		cnn.restore(loading_step)
	else:
		cnn.restore()

	# examine
	vcount = {'b':0, 'w':0, 'd':0}
	pcount = {'correct':0, 'fail':0}
	while not game_quit:
		spot = None
		# player-turn
		flag = True
		if game.turn == SBLACK:
			
			while flag:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						col = int(event.pos[1]/SQUARE_SIZE)  # y
						row = int(event.pos[0]/SQUARE_SIZE)  # x
						spot = {'x':row, 'y':col}

						if game.verify(row, col):
							game.put(row, col)
							flag = False
							break
						else:
							continue
					flag = True
		# supervised-learned AI
		elif game.turn == SWHITE:
			state = game.feature_spots()
			spot = cnn.predict(state)
			#print(spot)
			if game.verify(spot['x'], spot['y']):
				print('CNN predicted!')
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
			print('#---------- <{0}> statistics ----------#'.format(game_sequence))
			print('<AI> accuracy: {0}'.format((pcount['correct']/(pcount['correct']+pcount['fail']))*100))
			print('<AI> victory: {0}'.format(vcount['w']/game_sequence*100))
			print('<AI> lose: {0}'.format(vcount['b']/game_sequence*100))
			print('<AI> Draw: {0}'.format(vcount['d']/game_sequence*100))
		
		# check putable
		if game.check_putable() == False:
			print('# turn is omitted')
			game.change_turn()
		game.update()

# 2-Player
def two_man_game():
	# initialize game
	game_quit = False
	game_sequence = 0

	game = pothello()
	cnn = brain()
	cnn.init()

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
					game.draw_stone(2, 4, RED)

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

# SL policy network training (random vs random)
def supervised_learning(batch_size=SAVE_STEPS, notify_sequence=1000):
	# initialize game
	game_sequence = 0
	game_quit = False
	game = pothello()

	# initialize cnn
	state_log = []
	action_log = []
	cnn = brain()

	# start training
	omit_flag = False
	while not game_quit:
		# auto_put
		spot = game.auto_put(False)
		if spot ==  None:
			omit_flag = True
			game.change_turn()
			continue
		game.record(spot['x'], spot['y'], omit_flag)
		game.put(spot['x'], spot['y'])
		game.occupy(spot['x'], spot['y'])	
		game.change_turn()
		omit_flag = False

		# check victory
		victor = game.check_victory()
		if victor==SBLACK or victor==SWHITE:
			game_sequence += 1
			game.reset()

			if game_sequence%notify_sequence == 0:
				print('<game sequence> ' + str(game_sequence))

			for i in game.log:
				if i['omit']:
						game.change_turn()

				if i['turn'] == victor:
					state = game.feature_spots()
					action = i['y']*COLUMN_COUNT + i['x']
					state_log.append(state)
					action_log.append(action)

				game.put(i['x'], i['y'])
				game.occupy(i['x'], i['y'])
				game.change_turn()

			if game_sequence%batch_size == 0:
				cnn.train(state_log, action_log)
				state_log = []
				action_log = []

			# save model
			if game_sequence%SAVE_STEPS == 0:
				cnn.save(game_sequence)

		# reset game
		if victor != SNONE:
			game.reset()
			game.log = []			

		if game_sequence >= SAVE_STEPS*SAVE_MAX_TO_KEEP:
			break

# Random vs AI
def cnn_vs_random(loading_step, attempt_number=200):
	# initialize game
	game_sequence = 0
	game_quit = False
	game = pothello()

	# initialize cnn
	cnn = brain()
	cnn.restore(loading_step)

	# examine
	vcount = {'b':0, 'w':0, 'd':0}
	pcount = {'correct':0, 'fail':0}
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
				print('auto_put')
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
		elif victor==SWHITE:
			vcount['w'] += 1
		elif victor==DRAW:
			vcount['d'] += 1
		if victor==SBLACK or victor==SWHITE or victor==DRAW:
			game_sequence += 1
			game.reset()
			if game_sequence%20 == 0:
				print('#---------- <{0}> statistics ----------#'.format(game_sequence))
				print('<AI> accuracy: {0}'.format((pcount['correct']/(pcount['correct']+pcount['fail']))*100))
				print('<AI> victory: {0}'.format(vcount['w']/game_sequence*100))
				print('<AI> lose: {0}'.format(vcount['b']/game_sequence*100))
				print('<AI> Draw: {0}'.format(vcount['d']/game_sequence*100))
		
		# check putable
		if game.check_putable() == False:
			game.change_turn()

		game.update()

		if game_sequence >= attempt_number:
			break


if __name__ == '__main__':
	#one_man_game()
	#two_man_game()
	#supervised_learning()
	cnn_vs_random(loading_step=20000, attempt_number=500)