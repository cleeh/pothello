import os
import math
import random
import numpy as np
import tensorflow as tf
import keras
from keras.layers import Activation, BatchNormalization, Conv2D, Input, Dense, Flatten, Softmax
from keras.models import Model, Sequential, load_model
from keras.optimizers import SGD
from keras.utils import to_categorical

from slearn import *
from shared import *

class replayer:
	def __init__(self):
		self.memory = []
		pass

	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))
		if len(self.memory) > MEMORY_SIZE:
			del self.memory[0]

	def replay(self, batch_size=SIZE):
		if len(self.memory) >= batch_size:
			return random.sample(self.memory, batch_size)
		else:
			return random.sample(self.memory, len(self.memory))

class rbrain(sbrain, replayer):
	def __init__(self):
		sbrain.__init__(self)
		replayer.__init__(self)

	def rtrain(self, batch_size=SIZE, epoch=2):
		state_list = []
		target_f_list = []
		for state, action, reward, next_state, done in self.replay(batch_size):
			state_list.append(state)

			target = reward
			if not done:
				target = reward + GAMMA*np.amax(self.predict_raw(next_state)[0])

			target_f = self.predict_raw(state)
			target_f[0][action] = target
			target_f_list.append(target_f)
		state_list = np.reshape(state_list, [-1, COLUMN_COUNT, ROW_COUNT, FACTORS])
		target_f_list = np.reshape(target_f_list, [-1, SIZE])
		hist = self.model.fit(state_list, target_f_list, epochs=epoch)
		print(hist.history)

	def rsave(self, step=0):
		self.model.save(REINFORCEMENT_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT)
		print('{0} is saved'.format(REINFORCEMENT_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT))

	def rrestore(self, step=0):
		if os.path.exists(REINFORCEMENT_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT):
			self.model = load_model(REINFORCEMENT_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT)
		else:
			raise RuntimeError("no model named '{0}'".format(REINFORCEMENT_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT))