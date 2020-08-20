import numpy as np
from tabulate import tabulate

def perceptron(weights, inputs, bias, activation_function="tanh"):
    """
    Builds a simple perceptron using the given input, weights,
    bias values and activation function.
    - **parameters**, **types**, **return** and **return types**::

        :param weights: Network weights (positive indicate excitattory
                        and negative indicate inhibitory)
        :param inputs: Network inputs
        :param bias: Network bias to ensure correct output
        :param activation_function: The activation function to be used
        :type weights: numpy array-like
        :type inputs: numpy array-like
        :type bias: numeric, integer
        :type activation_function: string
        :return: network activation value
        :rtype: numeric, float
    """
    activation_function = str(activation_function).lower()
    model = np.add(np.dot(inputs, weights), bias)
    if activation_function == "symmetric_hard_limit":
        logit = symmetric_hard_limit(model)
    elif activation_function == "binary_step":
        logit = binary_step(model)
    elif activation_function == "bipolar_step":
        logit = bipolar_step(model)
    elif activation_function == "saturating_linear_transfer":
        logit = saturating_linear_transfer(model)
    elif activation_function == "tanh":
        logit = tanh(model)
    elif activation_function == "log_sigmoidal":
        logit = log_sigmoidal(model)
    return round(logit,2)

def symmetric_hard_limit(y_in):
    if y_in >= 0:
        return 1
    return -1

def binary_step(y_in):
    if y_in >= 0:
        return 1
    return 0

def bipolar_step(y_in):
    if y_in >= 0:
        return 1
    return -1

def saturating_linear_transfer(y_in):
    if y_in < 0:
        return 0
    elif 0 <= y_in and y_in <= 1:
        return y_in
    else:
        return 1

def tanh(y_in):
    return np.tanh(y_in)

def log_sigmoidal(y_in):
    return 1 / (1 + np.exp(-y_in))

def compute(data, weights, bias, activation_function):
    """
    Computes truth table for logic gate by
    implementing an MP neuron using the input specified.
    - **parameters**, **types**, **return** and **return types**::

        :param data: X1 and X2 values
        :param weights: Network weights
        :param bias: Network Bias
        :param activation_function: The activation function to use
        :type data: numpy array-like
        :type weights: numpy array-like
        :type bias: numeric, integer
        :type activation_function: string
        :return: calculated truth table
        :rtype: dict
    """
    weights = np.array(weights)
    output = np.array([ perceptron(weights, datum, bias, activation_function) for datum in data ])
    return output

def main():
    """
    Driver function for the script, sets up the inputs, weights
    and bias and then finds network output for all the required
    activation functions.
    """
    # Initial setup
    x1 = 0.7
    x2 = 0.8
    weights = [0.2,0.3]
    bias = 0.9
    activation_functions = ["symmetric_hard_limit", "binary_step", "bipolar_step", "saturating_linear_transfer", "tanh", "log_sigmoidal"]
    result = []
    
    # Calculate network output for each activation function
    for activation_function in activation_functions:
        y = compute(np.array([ [x1, x2] ]), weights, bias, activation_function)[0]
        result.append({"x1":x1, "x2": x2, "y": y, "activation_function": activation_function})
    
    # Pretty-print output
    print(tabulate(result, headers="keys"))

if __name__ == '__main__':
    main()
