import tensorflow as tf
import os

BOARD_SIZE_X = 12
BOARD_SIZE_Y = 12
LENGTH_OF_PROGRAM = 4


def load_data(filename, no_of_records):
    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    _, serialized = reader.read(filename_queue)
    features = tf.parse_single_example(serialized, features={
        "program": tf.FixedLenFeature([], tf.string),
        "boards": tf.FixedLenFeature([], tf.string)})
    program_raw = tf.decode_raw(features['program'], tf.uint8)
    program = tf.cast(tf.reshape(program_raw, [4]), tf.int32)
    boards_raw = tf.decode_raw(features['boards'], tf.uint8)
    boards = tf.cast(tf.reshape(boards_raw, [3 * BOARD_SIZE_X * BOARD_SIZE_Y]), tf.float32)
    # this causes records to be read
    return tf.train.batch([boards, program], no_of_records)


#
# define variables here
#

sess = tf.Session()
sess.run(tf.global_variables_initializer())
X, Y = load_data("training_set.tfrecord", 1000)
Xt, Yt = load_data("test_set.tfrecord", 100)

coord = tf.train.Coordinator()
# queue runner for filename queue
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

#
# insert your code here
#

coord.request_stop()
coord.join(threads)
sess.close()
