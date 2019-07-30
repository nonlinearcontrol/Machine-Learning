from numpy import exp, array, dot, random, mean, abs
from random import seed
seed(1)

# create activation function - sigmoid
def sigmoid(x, deriv = False):
    if deriv == True:
        return x * (1 - x)
    return 1 / (1 + exp(-x))

# input data set is a matrix
# each row is a different training example
# each coloumn represents a different neuron
X = array([ [0, 0, 1], 
            [0, 1, 1], 
            [1, 0, 1], 
            [1, 1, 1]])

# output dataset - 4 examples, 1 output neuron each
y = array([ [0], 
            [1], 
            [1],
            [0]])

# create synapse matrices - connections between each neuron in 1 layer to every neuron in the next layer
# 3 layers in network --> 2 synapses matrices required
# each synapse has a random weight assigned to it
syn0 = 2*random.random((3, 4)) - 1
syn1 = 2*random.random((4, 1)) - 1

# training step
# for loop over the training code to optimize the network for the given data set
# start off by creating out first layer - its just our input data
# next comes the predicition step - perform matrix multiplication between each layer and its synapse
# then, run sigmoid function on all the values in the matrix to create the next layer
# the next layer creates a prediciton of the output data
# then, do the same thing on that layer to get our next layer - more refined prediction
# now that we have a prediction of the output data in layer two, lets compare it to the expected output data using subtraction
# this gives the error rate
# also want to print out average error rate at set itnerval to make sure it goes down every time
# next, multiply error rate by the result of the signoid function. the function is used to get the derivative of our output prediction from layer 2
# this will give us a delta, which we use to reduce the error rate of our predictions when we update our synapses every iteration
# then, we want to see how much layer 1 contributed to the error in layer 2 --> called back propagation
# we get this error by multiplying layer 2's delta by synapse 1's transpose
# then get layer 1's delta by multiplying its error by the result of our sigmoid function
# the function is used to get the derivative of layer 1
# now that we have deltas for each of our layers, we can use them to update our synapse weights to reduce the error rate more and more every iteration
# this is an algorithm called gradient descent
# to do this, multiply each layer by a delta
# finally, print the predicted output

for i in range(20000):
    l0 = X
    l1 = sigmoid(dot(l0, syn0))
    l2 = sigmoid(dot(l1, syn1))
    l2_error = y - l2
    # print(l2)
    if (i % 10000) == 0:
        print('Error:' + str(mean(abs(l2_error))))
    l2_delta = l2_error * sigmoid(l2, deriv = True)
    l1_error = l2_delta.dot(syn1.T)
    l1_delta = l1_error * sigmoid(l1, deriv = True)

    # update weights
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)

# print results
print('Output after training')
for i in l2:
    print(*i)