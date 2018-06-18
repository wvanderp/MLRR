import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# continue https://www.youtube.com/watch?v=BhpvH5DuVu8
mnist = input_data.read_data_sets("C:\\temp", one_hot=True)

# constants for how many nodes each layer has
n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

# amount of output nodes
n_classes = 10

# how many examples are there in each batch
batch_size = 100

# input placeholder
x = tf.placeholder('float', [None, 784])
# output placeholder
y = tf.placeholder('float', [None, 10])


# here we define the network
def neural_network_model(data):
    # define the layers
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([784, n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}

    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}

    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}

    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes]))}

    # here we link the layer and define the activation function
    # the formula is (previous layer * weights) + a bias
    # were the bias is magic
    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.add(tf.matmul(l3, output_layer['weights']), output_layer['biases'])

    return output


# here we train the network
def train_neural_network(x):
    # get a prediction for an input x
    prediction = neural_network_model(x)
    # calculate the cost
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))

    # run the optimiser on the network
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    # how many batches
    hm_epochs = 10

    # start tensorflow
    with tf.Session() as sess:
        # initiate the placeholders
        sess.run(tf.initialize_all_variables())
        for epoch in range(hm_epochs):
            # the reset the loss
            epoch_loss = 0
            # run through batch
            for _ in range(int(mnist.train.num_examples / batch_size)):
                # a magic function from mnist that gets a batch of input and output
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                # run the optimiser and cost function on the baches
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})

                # add the loss to the current batch
                epoch_loss += c
            # print some feedback
            print('epock', epoch, 'out of', hm_epochs, ", loss: ", epoch_loss)

        # calculate the amount of correct answers and calculate the correctness
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        # print some more
        print('accuracy: ', accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))


# start the program
train_neural_network(x)
