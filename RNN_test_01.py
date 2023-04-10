import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Load data
data = pd.read_csv('data.csv')

# Preprocessing
scaler = MinMaxScaler(feature_range=(0, 1))
data[['rsi', 'fast_ma', 'slow_ma', 'ema']] = scaler.fit_transform(data[['rsi', 'fast_ma', 'slow_ma', 'ema']])
data['Sell_Profit_240Min'] = data['Sell_Profit_240Min'].astype(int)
data = data[['rsi', 'fast_ma', 'slow_ma', 'ema', 'Sell_Profit_240Min']].values
n_samples = len(data)
n_train = int(n_samples * 0.8)

# Define hyperparameters
n_steps = 5000
n_inputs = 4
n_neurons = 100
n_outputs = 2
learning_rate = 0.001
n_epochs = 100

# Define input and output placeholders
X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
y = tf.placeholder(tf.int32, [None])

# Define RNN cell and dynamic RNN
cell = tf.nn.rnn_cell.BasicRNNCell(num_units=n_neurons)
outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)

# Define output layer
logits = tf.layers.dense(states, n_outputs)

# Define loss function and optimizer
xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
loss = tf.reduce_mean(xentropy)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(loss)

# Define evaluation metric
correct = tf.nn.in_top_k(logits, y, 1)
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

# Train the model
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(n_epochs):
        X_batch = []
        y_batch = []
        for i in range(n_train - n_steps):
            X_batch.append(data[i:i+n_steps, :-1])
            y_batch.append(data[i+n_steps-1, -1])
        X_batch = np.array(X_batch)
        y_batch = np.array(y_batch)
        sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
        if epoch % 10 == 0:
            acc_train = accuracy.eval(feed_dict={X: X_batch, y: y_batch})
            print(epoch, "Train accuracy:", acc_train)
    
    # Evaluate the model on the test set
    X_test = []
    y_test = []
    for i in range(n_train, n_samples - n_steps):
        X_test.append(data[i:i+n_steps, :-1])
        y_test.append(data[i+n_steps-1, -1])
    X_test = np.array(X_test)
    y_test = np.array(y_test)
    acc_test = accuracy.eval(feed_dict={X: X_test, y: y_test})
    print("Test accuracy:", acc_test)
