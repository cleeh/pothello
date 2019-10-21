import tensorflow as tf
import numpy as np
import math

from shared import *

class brain:
	def __init__(self):
		#-------------------- Model --------------------#
		# Placeholder
		self.input = tf.placeholder(tf.float32, shape=[None, COLUMN_COUNT, ROW_COUNT, FACTORS])
		self.target = tf.placeholder(tf.float32, shape=[None, OUTPUTS])
		self.keep_prob = tf.placeholder(tf.float32)

		# Convolution
		w1 = tf.Variable(tf.truncated_normal(shape=[7, 7, FACTORS, HIDDEN1], stddev=0.01), name='w1')
		b1 = tf.Variable(tf.constant(0.1, shape=[HIDDEN1]), dtype=tf.float32, name='b1')
		h1 = tf.nn.relu(tf.nn.conv2d(self.input ,w1, strides=[1, 1, 1, 1], padding='SAME') + b1)
		p1 = tf.nn.max_pool(h1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

		w2 = tf.Variable(tf.truncated_normal(shape=[5, 5, HIDDEN1, HIDDEN2], stddev=0.01), name='w2')
		b2 = tf.Variable(tf.constant(0.1, shape=[HIDDEN2]), dtype=tf.float32, name='b2')
		h2 = tf.nn.relu(tf.nn.conv2d(p1 ,w2, strides=[1, 1, 1, 1], padding='SAME') + b2)
		p2 = tf.nn.max_pool(h2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

		w3 = tf.Variable(tf.truncated_normal(shape=[3, 3, HIDDEN2, HIDDEN3], stddev=0.01), name='w3')
		b3 = tf.Variable(tf.constant(0.1, shape=[HIDDEN3]), dtype=tf.float32, name='b3')
		h3 = tf.nn.relu(tf.nn.conv2d(p2 ,w3, strides=[1, 1, 1, 1], padding='SAME') + b3)
		p3 = tf.nn.max_pool(h3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

		w4 = tf.Variable(tf.truncated_normal(shape=[1, 1, HIDDEN3, HIDDEN4], stddev=0.01), name='w4')
		b4 = tf.Variable(tf.constant(0.1, shape=[HIDDEN4]), dtype=tf.float32, name='b4')
		h4 = tf.nn.relu(tf.nn.conv2d(p3 ,w4, strides=[1, 1, 1, 1], padding='SAME') + b4)
		p4 = tf.nn.max_pool(h4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

		# Fully-Connected Layer
		w_fc1 = tf.Variable(tf.truncated_normal(shape=[1 * 1 * HIDDEN4, NEURONS], stddev=0.01), name='w_fc1')
		b_fc1 = tf.Variable(tf.constant(0.1, shape=[NEURONS]), dtype=tf.float32, name='b_fc1')
		h_pool2_flat = tf.reshape(p4, [-1, 1 * 1 * HIDDEN3])
		h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)

		# Drop Out
		h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

		# Softmax Layer
		w_fc2 = tf.Variable(tf.truncated_normal(shape=[NEURONS, OUTPUTS]), name='w_fc2')
		b_fc2 = tf.Variable(tf.constant(0.1, shape=[OUTPUTS]), name='b_fc2')

		self.y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)

		#-------------------- Train & Evaluation --------------------#
		# Train
		self.cost = tf.reduce_mean(-tf.reduce_sum(self.target * tf.log(self.y_conv), reduction_indices=1))
		self.optimizer = tf.train.AdamOptimizer(LEARNINGRATE).minimize(self.cost)

		# Evaluation
		correction = tf.equal(tf.argmax(self.y_conv, 1), tf.argmax(self.target, 1))
		self.accuracy = tf.reduce_mean(tf.cast(correction, tf.float32))

		#-------------------- Session & Saver --------------------#
		self.sess = tf.Session()
		self.saver = tf.train.Saver(max_to_keep=SAVE_MAX_TO_KEEP)

	def train(self, state, action):
		# reshape
		state = np.reshape(state, [-1, COLUMN_COUNT, ROW_COUNT, FACTORS])

		# label
		label = np.zeros((1, SIZE), dtype=float)
		label[0][action] = 1.0

		# train
		output, _, train_accuracy = self.sess.run([self.y_conv, self.optimizer, self.accuracy], feed_dict={self.input:state, self.target:label, self.keep_prob:1.0})
		#print("training accuracy {0}".format(train_accuracy))

	def init(self):
		self.sess.run(tf.global_variables_initializer())

	def save(self, step=0):
		ckpt_path = self.saver.save(self.sess, MODEL_PATH, global_step=step, write_meta_graph=False)
		print('saved ckpt file:', ckpt_path)

	def restore(self, step=0):
		#if os.path.exists(MODEL_PATH + '.meta'):
		if step > 0:
			self.saver.restore(self.sess, MODEL_PATH)
		else:
			self.saver.restore(self.sess, tf.train.latest_checkpoint(MODEL_DIRECTORY))