import tensorflow as tf
import os

BOARD_SIZE_X = 12
BOARD_SIZE_Y = 12
LENGTH_OF_PROGRAM = 4

sess = None


def init():
    global sess
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    # your code to load the trained neural network into memory


def inference(X):
# your code to run the network on the provided input

def solve(boxBoard, startBoard, goalBoard):
    X = tf.reshape(tf.cast([boxBoard, startBoard, goalBoard], tf.float32), [1, 3 * BOARD_SIZE_X * BOARD_SIZE_Y])
    return list(sess.run(tf.to_int32(tf.arg_max(inference(X), 1))))
