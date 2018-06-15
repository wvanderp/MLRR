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


training_steps = 1000


def loss(x, y):
    # compute loss over training data X and expected outputs Y
    return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=combine(x), labels=y))


def train(loss_func):
    # train / adjust model parameters according to computed total loss
    learning_rate = 0.01
    return tf.train.GradientDescentOptimizer(learning_rate).minimize(loss_func)


def train(loss_func):
    # train / adjust model parameters according to computed total loss
    learning_rate = 0.01
    return tf.train.GradientDescentOptimizer(learning_rate).minimize(loss_func)


sess = tf.Session()
sess.run(tf.global_variables_initializer())
X, Y = load_data("training_set.tfrecord", 1000)
Xt, Yt = load_data("test_set.tfrecord", 100)

coord = tf.train.Coordinator()
# queue runner for filename queue
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

# actual training loop
for step in range(training_steps):
    sess.run(train_op)
    # log loss every step for visualisation in TensorBoard
    writer.add_summary(sess.run(summary), step + initial_step)
    # for debugging and learning purposes, see how the loss gets decremented thru training steps
    if step % 100 == 0:
        print("loss: ", sess.run(loss_func))

coord.request_stop()
coord.join(threads)
sess.close()
