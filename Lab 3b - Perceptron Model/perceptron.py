from random import seed
from random import randrange
import numpy as np

# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0

# Make a prediction with weights
def predict(row, weights):
    activation = weights[0]
    for i in range(len(row)-1):
        activation += weights[i + 1] * row[i]
    return 1.0 if activation >= 0.0 else 0.0

# Estimate Perceptron weights using stochastic gradient descent
def train_weights(train, y_true, l_rate, n_epoch):
    weights = [0.0 for i in range(len(train[0]))]
    for epoch in range(n_epoch):
        predictions = []
        for row in train:
            prediction = predict(row, weights)
            predictions.append(prediction)
            error = row[-1] - prediction
            weights[0] = weights[0] + l_rate * error
            for i in range(len(row)-1):
                weights[i + 1] = weights[i + 1] + l_rate * error * row[i]
        accuracy = accuracy_metric(y_true, predictions)
        if epoch%100 == 0:
            print("[INFO] Epoch " + str(epoch) + " -> Weights: " + str(weights) + "; Accuracy: " + str(accuracy_metric(y_true, predictions)))
    return weights

# Perceptron Algorithm With Stochastic Gradient Descent
def perceptron(train, test, y_true, l_rate, n_epoch):
    predictions = list()
    weights = train_weights(train, y_true, l_rate, n_epoch)
    for row in test:
        prediction = predict(row, weights)
        predictions.append(prediction)
    return(predictions)

l_rate = 0.01
n_epoch = 501
train = [
    [0.96,0.6,0],
    [0.83,-0.43,1],
    [0.63,0.97,0],
    [0.12,0.88,0],
    [0.62,-0.43,1],
    [-0.78,0.99,0],
    [-0.58,0.71,0]
]
test = [
    [0.67,-0.23,1],
    [0.73,0.34,0],
    [0.27,-0.56,1]
]

print("#-------------- Training Data --------------#")
print(train)
print("#-------------------------------------------#")

print("#-------------- Testing Data --------------#")
print(test)
print("#------------------------------------------#")

y_true = [x[2] for x in train]
predictions = perceptron(train, test, y_true, l_rate, n_epoch)

y_test = [x[2] for x in test]
print("#-------------- Result --------------#")
print("True:      " + str(y_test))
print("Predicted: " + str(predictions))
print("Accuracy:  " + str(accuracy_metric(y_test, predictions)))
print("#------------------------------------#")
