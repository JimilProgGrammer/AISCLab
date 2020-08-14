"""
Python script to demonstrate the XOR logic gate
using two-level McCulloh - Pitts network.
X1 XOR X2 == (X1 AND NOT X2) OR (X2 AND NOT X1)

.. author::
    Jimil
"""
import numpy as np

def perceptron(weights, inputs, bias):
    """
    Builds a simple perceptron using the given input, weights
    and bias values.
    - **parameters**, **types**, **return** and **return types**::

        :param weights: Network weights (positive indicate excitattory
                        and negative indicate inhibitory)
        :param inputs: Network inputs
        :param bias: Network bias to ensure correct output
        :type weights: numpy array-like
        :type inputs: numpy array-like
        :type bias: numeric, integer
        :return: network activation value
        :rtype: numeric, float
    """
    model = np.add(np.dot(inputs, weights), bias)
    logit = activation_function(model)
    return logit

def activation_function(model):
    """
    Implements the custom activation function
    using the threshold logic.
    - **parameters**, **types**, **return** and **return types**::

        :param model: Weighted sum input
        :type model: Numeric, float
        :return: activated value
        :rtype: numeric, integer
    """
    if model >= 2:
        return 1
    return 0

def compute(data, logic_gate, weights, bias):
    """
    Computes truth table for logic gate by
    implementing an MP neuron using the input specified.
    - **parameters**, **types**, **return** and **return types**::

        :param data: X1 and X2 values
        :param logic_gate: The logic gate to implement
        :param weights: Network weights
        :param bias: Network Bias
        :type data: numpy array-like
        :type logic_gate: string
        :type weights: numpy array-like
        :type bias: numeric, integer
        :return: calculated truth table
        :rtype: dict
    """
    weights = np.array(weights)
    output = np.array([ perceptron(weights, datum, bias) for datum in data ])
    return output

def main():
    """
    Driver function for the script, declares a two-bit dataset
    and applies the two-level MP network to calculate XOR output.
    
    Network 1   | Weights   | Bias
                | [2,-1]    | 0
    -------------------------------
    Network 2   | Weights   | Bias
                | [2,2]     | 0
    -------------------------------
    
    Activation function:
        - y = activate(weighted_sum) = 0    if weighted_sum < 2
                                     = 1    if weighted_sum >= 2
    """
    dataset = np.array([
      [0, 0],
      [0, 1],
      [1, 0],
      [1, 1]
    ])
    
    """
    For every row in dataset,
        a.] Extract x1 and x2 values
        b.] Calculate network1 output = x1 AND x2'
        c.] Calculate network2 output = x2 AND x1'
        d.] Calculate XOR output = network1 OR network2
    """
    for i in range(len(dataset)):
        x1 = dataset[i][0]
        x2 = dataset[i][1]
        network1 = compute(np.array([ [x1, x2] ]), "and", [2,-1], 0)[0]
        print(str(x1) + " AND NOT " + str(x2) + " => " + str(network1))
        network2 = compute(np.array([ [x2, x1] ]), "and", [2,-1], 0)[0]
        print(str(x2) + " AND NOT " + str(x1) + " => " + str(network2))
        output = compute(np.array([ [network1, network2] ]), "or", [2,2], 0)
        print(str(network1) + " OR " + str(network2) + " => " + str(output[0]))
        print("Thus, " + str(network1) + " XOR " + str(network2) + " => " + str(output[0]))
        print("---------------------------------------------")

if __name__ == '__main__':
    main()
