import random

from shared import *
from palette import *
from board import *

class othello(board, palette):
	def __init__(self):
		board.__init__(self)
		palette.__init__(self)
		self.reset()

	def reset(self):
		super().clear()
		self.draw_board()
		self.draw_stone(3, 3, BLACK)
		self.draw_stone(4, 4, BLACK)
		self.draw_stone(3, 4, WHITE)
		self.draw_stone(4, 3, WHITE)
		self.update()

	def put(self, x, y):
		super().set(x, y)
		if self.turn == SBLACK:
			self.draw_stone(x, y, BLACK)
		elif self.turn == SWHITE:
			self.draw_stone(x, y, WHITE)

	def auto_put(self):
		list = []
		for i in range(COLUMN_COUNT):
			for j in range(ROW_COUNT):
				if self.verify(j, i):
					list.append((j, i))

		if len(list) > 0:
			random_spot = list[random.randrange(0, len(list))]
			self.put(random_spot[0], random_spot[1])
			return {'x':random_spot[0], 'y':random_spot[1]}
		else:
			return None

	def draw_stones(self):
		for i in range(COLUMN_COUNT):
			for j in range(ROW_COUNT):
				target = self.get(j, i)
				if target == SBLACK:
					self.draw_stone(j, i, BLACK)
				elif target == SWHITE:
					self.draw_stone(j, i, WHITE)

	def verify(self, x, y, color = None):
		origin = self.get(x, y)
		if origin == SBLACK or origin == SWHITE:
			return False

		target = color
		if target is None:
			target = self.turn

		other = SNONE
		if target is SBLACK:
			other = SWHITE
		elif target is SWHITE:
			other = SBLACK

		vlist = (
		(-1, -ROW_COUNT, -1, '-'),  # West
		(1, ROW_COUNT, 1, '-'),  # East
		(1, COLUMN_COUNT, 1, '|'),  # South
		(-1, -COLUMN_COUNT, -1, '|'),  # North
		(1, max(ROW_COUNT, COLUMN_COUNT), 1, '/'),  # Northern-East
		(-1, -max(ROW_COUNT, COLUMN_COUNT), -1, '/'),  # Southern-West
		(-1, -max(ROW_COUNT, COLUMN_COUNT), -1, '\\'),  # Northern-West
		(1, max(ROW_COUNT, COLUMN_COUNT), 1, '\\')  # Southern-East
		)
		for i in range(8):
			flag = False
			stone = SNONE
			for j in range(vlist[i][0], vlist[i][1], vlist[i][2]):
				if vlist[i][3] == '-':  # Horizontal
					if x+j < 0 or x+j >= ROW_COUNT:
						break
					stone = self.get(x+j, y)
				elif vlist[i][3] == '|':  # Vertical
					if y+j < 0 or y+j >= COLUMN_COUNT:
						break
					stone = self.get(x, y+j)
				elif vlist[i][3] == '/':  # Slash
					if x+j < 0 or x+j >= ROW_COUNT or y-j < 0 or y-j >= COLUMN_COUNT:
						break
					stone = self.get(x+j, y-j)
				elif vlist[i][3] == '\\':  # Backslash
					if x+j < 0 or x+j >= ROW_COUNT or y+j < 0 or y+j >= COLUMN_COUNT:
						break
					stone = self.get(x+j, y+j)

				if stone == target:
					if flag: return True
					else: break
				elif stone == other:
					flag = True
				elif stone == SNONE:
					break
		return False

	def occupy(self, x, y, color = None):
		target = color
		if target is None:
			target = self.turn

		other = SNONE
		if target is SBLACK:
			other = SWHITE
		elif target is SWHITE:
			other = SBLACK

		vlist = [
		(-1, -ROW_COUNT, -1, '-'),  # West
		(1, ROW_COUNT, 1, '-'),  # East
		(1, COLUMN_COUNT, 1, '|'),  # South
		(-1, -COLUMN_COUNT, -1, '|'),  # North
		(1, max(ROW_COUNT, COLUMN_COUNT), 1, '/'),  # Northern-East
		(-1, -max(ROW_COUNT, COLUMN_COUNT), -1, '/'),  # Southern-West
		(-1, -max(ROW_COUNT, COLUMN_COUNT), -1, '\\'),  # Northern-West
		(1, max(ROW_COUNT, COLUMN_COUNT), 1, '\\')  # Southern-East
		]
		for i in range(8):
			flag = False
			stone = SNONE
			position = None
			olist = []
			for j in range(vlist[i][0], vlist[i][1], vlist[i][2]):
				if vlist[i][3] == '-':  # Horizontal
					if x+j < 0 or x+j >= ROW_COUNT:
						olist.clear()
						break
					position = (x+j, y)
					stone = self.get(x+j, y)
				elif vlist[i][3] == '|':  # Vertical
					if y+j < 0 or y+j >= COLUMN_COUNT:
						olist.clear()
						break
					position = (x, y+j)
					stone = self.get(x, y+j)
				elif vlist[i][3] == '/':  # Slash
					if x+j < 0 or x+j >= ROW_COUNT or y-j < 0 or y-j >= COLUMN_COUNT:
						olist.clear()
						break
					position = (x+j, y-j)
					stone = self.get(x+j, y-j)
				elif vlist[i][3] == '\\':  # Backslash
					if x+j < 0 or x+j >= ROW_COUNT or y+j < 0 or y+j >= COLUMN_COUNT:
						olist.clear()
						break
					position = (x+j, y+j)
					stone = self.get(x+j, y+j)

				if stone == target:
					if flag:
						for arg in olist:
							self.set(arg[0], arg[1], target)
							if target == SBLACK:
								self.draw_stone(arg[0], arg[1], BLACK)
							elif target == SWHITE:
								self.draw_stone(arg[0], arg[1], WHITE)
					else:
						olist.clear()
						break
				elif stone == other:
					flag = True
					olist.append(position)
				elif stone == SNONE:
					olist.clear()
					break

	def check_victory(self):
		# Check whether board is full of stones
		numbers = self.count()
		if numbers[0] + numbers[1] == SIZE:
			if numbers[0] > numbers[1]:  # Black is win
				return SBLACK
			elif numbers[0] < numbers[1]:  # White is win
				return SWHITE
			else:  # Draw
				return DRAW

		# Check whether colors of all stone are same each other
		if numbers[1] == 0:
			return SBLACK
		elif numbers[0] == 0:
			return SWHITE

		# Check whether there is no location stones can be put on
		for i in range(COLUMN_COUNT):
			for j in range(ROW_COUNT):
				black_flag = self.verify(j, i, SBLACK)
				white_flag = self.verify(j, i, SWHITE)
				if black_flag or white_flag:
					return SNONE

		if numbers[0] > numbers[1]:  # Black is win
			return SBLACK
		elif numbers[0] < numbers[1]:  # White is win
			return SWHITE
		else:  # Draw
			return DRAW

	def check_putable(self, turn=SNONE):
		if turn == SNONE:
			turn = self.turn
		
		for i in range(COLUMN_COUNT):
			for j in range(ROW_COUNT):
				if self.verify(j, i, turn):
					return True

		return False