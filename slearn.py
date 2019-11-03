import os
import math
import numpy as np
import tensorflow as tf
import keras
from keras.layers import Activation, BatchNormalization, Conv2D, Input, Dense, Flatten, Softmax
from keras.models import Model, Sequential, load_model
from keras.optimizers import SGD
from keras.utils import to_categorical

from shared import *

class brain:
	def __init__(self):
		#-------------------- Model --------------------#
		inputs = Input(shape=(COLUMN_COUNT, ROW_COUNT, FACTORS))

		x = self.conv_block(inputs)
		for i in range(RESIDUALS):
			x = self.residual_block(x)
		policy_out = self.policy_head(x)
		value_head = self.value_head(x)

		self.model = Model(inputs=[inputs], outputs=[policy_out])
		self.model.compile(optimizer=SGD(lr=LEARNING_RATE), loss='categorical_crossentropy', metrics=['accuracy'])

	def conv_block(self, x):
		y = Conv2D(HIDDENS, (3, 3), padding='same')(x)
		y = BatchNormalization()(y)
		y = Activation('relu')(y)
		return y

	def residual_block(self, x):
		y = Conv2D(HIDDENS, (3, 3), padding='same')(x)
		y = BatchNormalization()(y)
		y = Activation('relu')(y)
		y = Conv2D(HIDDENS, (3, 3), padding='same')(y)
		y = BatchNormalization()(y)
		y = keras.layers.add([x, y])
		y = Activation('relu')(y)
		return y

	def policy_head(self, x):
		y = Conv2D(2, (1, 1), padding='same')(x)
		y = BatchNormalization()(y)
		y = Activation('relu')(y)
		y = Flatten()(y)
		y = Dense(OUTPUTS, activation='sigmoid')(y)
		y = Softmax()(y)
		return y

	def value_head(self, x):
		y = Conv2D(1, (1, 1), padding='same')(x)
		y = BatchNormalization()(y)
		y = Activation('relu')(y)
		y = Dense(256)(y)
		y = Activation('relu')(y)
		y = Dense(1)(y)
		y = Activation('tanh')(y)
		return y

	def predict(self, state):
		# reshape
		state = np.reshape(state, [1, COLUMN_COUNT, ROW_COUNT, FACTORS])

		# predict
		prediction = self.model.predict(state)
		prediction = prediction.argmax()

		return {'x':int(prediction%COLUMN_COUNT), 'y':int(prediction/COLUMN_COUNT)} 

	def train(self, state, action, epoch=2):
		# reshape
		state = np.reshape(state, [-1, COLUMN_COUNT, ROW_COUNT, FACTORS])
		action = to_categorical(action, OUTPUTS)
		action = np.reshape(action, [-1, OUTPUTS])

		hist = self.model.fit(state, action, epochs=epoch)
		print(hist.history)

	def save(self, step=0):
		self.model.save(SUPERVISED_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT)
		print('{0} is saved'.format(SUPERVISED_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT))

	def restore(self, step=0):
		if os.path.exists(SUPERVISED_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT):
			self.model = load_model(SUPERVISED_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT)
		else:
			raise RuntimeError("no model named '{0}'".format(SUPERVISED_MODEL_NAME + SEPERATOR + str(step) + MODEL_FORMAT))