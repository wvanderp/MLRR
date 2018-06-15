import tensorflow as tf

from createBoardAndProgram import *

BOARD_SIZE_X = 12
BOARD_SIZE_Y = 12
NO_OF_BOXES = 10
LENGTH_OF_PROGRAM = 4

TRAINING_SET = 1000
TEST_SET = 100


def createSet(number, filename):
    writer = tf.python_io.TFRecordWriter(filename)
    for i in range(number):
        boxBoard, startX, startY, goalX, goalY, program = createBoardAndProgram(BOARD_SIZE_X, BOARD_SIZE_Y, NO_OF_BOXES,
                                                                                LENGTH_OF_PROGRAM)
        startBoard = [[0] * BOARD_SIZE_X for i in range(BOARD_SIZE_Y)]
        startBoard[startY][startX] = 1
        goalBoard = [[0] * BOARD_SIZE_X for i in range(BOARD_SIZE_Y)]
        goalBoard[goalY][goalX] = 1

        program = sess.run(tf.cast(program, tf.uint8)).tobytes()
        boards = sess.run(tf.cast([boxBoard, startBoard, goalBoard], tf.bool)).tobytes()

        example = tf.train.Example(features=tf.train.Features(feature={
            "program": tf.train.Feature(bytes_list=tf.train.BytesList(value=[program])),
            "boards": tf.train.Feature(bytes_list=tf.train.BytesList(value=[boards]))}))
        writer.write(example.SerializeToString())
    writer.close()


sess = tf.Session()
createSet(TRAINING_SET, "training_set.tfrecord")
createSet(TEST_SET, "test_set.tfrecord")
sess.close()
