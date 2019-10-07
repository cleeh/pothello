import numpy as np

from shared import *

class board:
	def __init__(self):
		self.clear()

	def clear(self):
		self.turn = SBLACK
		self.stone = np.zeros(SIZE)
		self.set(3, 3, SBLACK)
		self.set(4, 4, SBLACK)
		self.set(3, 4, SWHITE)
		self.set(4, 3, SWHITE)

	def set(self, x, y, color=None):
		if color is None:
			self.stone[y*COLUMN_COUNT + x] = self.turn
		elif color is SBLACK:
			self.stone[y*COLUMN_COUNT + x] = SBLACK
		elif color is SWHITE:
			self.stone[y*COLUMN_COUNT + x] = SWHITE

	def get(self, x, y):
		return int(self.stone[y*COLUMN_COUNT + x])

	def count(self):
		black_count = white_count = 0
		for i in self.stone:
			if i == SBLACK:
				black_count += 1
			elif i == SWHITE:
				white_count += 1
		return (black_count, white_count)

	def show(self):
		# show state
		numbers = self.count()
		state = '<board - '
		if self.turn == SBLACK:
			state += 'black> b('
		elif self.turn == SWHITE:
			state += 'white> b('
		state += str(numbers[0]) + ') w(' + str(numbers[1]) + ')'
		print(state)

		# show board
		for i in range(COLUMN_COUNT):
			line = ''
			for j in range(ROW_COUNT):
				line += str(self.get(j, i)) + ' '
			print(line)
		
	def change_turn(self):
		if self.turn is SBLACK:
			self.turn = SWHITE
		elif self.turn is SWHITE:
			self.turn = SBLACK
		else:
			print('<change_turn> unknown turn')