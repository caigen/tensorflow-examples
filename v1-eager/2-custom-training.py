"""
ref:
https://tensorflow.google.cn/tutorials/eager/custom_training
"""
import os
os.environ["KMP_WARNINGS"] = "0"

import tensorflow.compat.v1 as tf

tf.enable_eager_execution()

print("====constant====")
x = tf.zeros([10, 10])
x += 2
print(x)

print("====variable====")
v = tf.Variable(1.0)
print(v.numpy())

v.assign(3.0)
print(v.numpy())

v.assign(tf.square(v))
print(v.numpy())

print("====model====")
class Model: #(object):
    def __init__(self):
        self.W = tf.Variable(5.0)
        self.b = tf.Variable(0.0)

    def __call__(self, x):
        return self.W * x + self.b

model = Model()
print(model)
print(model(3.0).numpy())

print("====loss function: MSE ====")
def loss(predicted_y, desired_y):
    return tf.reduce_mean(tf.square(predicted_y - desired_y))
print(loss)

print("====training data====")
TRUE_W = 3.0
TRUE_b = 2.0
NUM_EXAMPLES = 1000

inputs = tf.random.normal(shape=[NUM_EXAMPLES])
noise = tf.random.normal(shape=[NUM_EXAMPLES])
outputs = inputs * TRUE_W + TRUE_b + noise

import matplotlib.pyplot as plt

plt.scatter(inputs, outputs, c="b")
plt.scatter(inputs, outputs, c="r")
plt.show()

print("Current loss:")
print(loss(model(inputs), outputs).numpy())

print("====training loop====")
def train(model, inputs, outputs, learning_rate):
    with tf.GradientTape() as t:
        current_loss = loss(model(inputs), outputs)
    dW, db = t.gradient(current_loss, [model.W, model.b])
    model.W.assign_sub(learning_rate * dW)
    model.b.assign_sub(learning_rate * db)

model = Model()

Ws, bs = [], []
epochs = range(10)
for epoch in epochs:
    Ws.append(model.W.numpy())
    bs.append(model.b.numpy())
    current_loss = loss(model(inputs), outputs)

    train(model, inputs, outputs, learning_rate=0.1)
    print("Epoch %2d: W=%1.2f b=%1.2f, loss=%2.5f" % (epoch, Ws[-1], bs[-1], current_loss))

plt.plot(epochs, Ws, "r",
         epochs, bs, "b")
plt.plot([TRUE_W] * len(epochs), "r--",
         [TRUE_b] * len(epochs), "b--")
plt.legend(["W", "b", "true W", "true b"])
plt.show()