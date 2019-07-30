########## rorb_feed_forward_nn.py ##########

'''

- This script creates a simple feed-forward neural network
- The chosen activation function is a sigmoid
- The network is able to predict an un-classified data point

'''

#########
# imports
#########

from numpy import exp, random, linspace
from matplotlib import pyplot as plt

################
# define dataset
################

'''

data set is list of x,y data points with a classifier of either True (1) or False (0)
X      Y   Classifier
---------------------
1      1      1
5      8      0
2      1      1
>>>

'''
data_set = [[1, 1, 1],
            [2, 1, 1],
            [5, 8, 0], 
            [2, 1, 1],
            [0, 9, 1], 
            [1, 8, 1],
            [3, 0, 0],
            [3, 1, 0],
            [7, 6, 0], 
            [1, 9, 1],
            [9, 4, 0], 
            [3, 7, 0],
            [1, 2, 1], 
            [2, 9, 0],
            [0, 3, 1], 
            [8, 2, 0], 
            [6, 4, 0],
            [6, 1, 0],
            [1, 8, 0],
            [1, 6, 1],
            [8, 8, 0],
            [1, 3, 1]]

###############################################
# define hyperparameters and initial conditions
###############################################

learning_rate = 0.001
iterations = 100000
w1 = random.randn()
w2 = random.randn()
b = random.randn()
n = 1000
fgn = 1

###########################
# define the neural network
###########################

'''
x
  \
   w1, b
    \
     classification
    /
   w2, b 
  /
 y 

'''

def sigmoid(x):
    '''
    - the chosen activation function for our network
    '''
    return 1 / (1 + exp(-x))

def sigmoid_dot(x):
    '''
    - the chosen activation function's derivative
    '''
    return exp(x) / (exp(x) + 1)**2

def training_loop(learning_rate, iterations, w1, w2, b, n):
    '''
    define the training loop where we minizie a cost function to optimize our weights and bias
    '''
    costs = [] # initialize a list that will append our costs so we can visualize it being minimized
    for i in range(iterations):
        data_point = data_set[random.randint(len(data_set))]
        x = data_point[0] * w1 + data_point[1] * w2 + b
        prediction = sigmoid(x)
        target = data_point[2]

        # define the cost function to be minimized
        cost = (prediction - target)**2

        # print cost data to the screen after every n iterations
        if i % n == 0:
            cost = 0
            for j in range(len(data_set)):
                data_point = data_set[j]
                prediction = sigmoid(data_point[0] * w1 + data_point[1] * w2 + b)
                cost += (prediction - data_point[2])**2
            costs.append(cost)

        # define partial derivatives 
        deltcost_deltprediction = 2 * (prediction - target)
        deltprediction_deltx = sigmoid_dot(x)
        deltx_deltw1 = data_point[0]
        deltx_deltw2 = data_point[1]
        deltx_deltb = 1.0
        deltcost_deltx = deltcost_deltprediction * deltprediction_deltx
        deltcost_deltw1 = deltcost_deltx * deltx_deltw1
        deltcost_deltw2 = deltcost_deltx * deltx_deltw2
        deltcost_deltb = deltcost_deltx * deltx_deltb

        # update our synapse weights through back propagation
        w1 = w1 - learning_rate * deltcost_deltw1
        w2 = w2 - learning_rate * deltcost_deltw2
        b = b - learning_rate * deltcost_deltb

    return costs, w1, w2, b

###########################################################################################
# train our network, predict our mystery point's classification, and visualize some results
###########################################################################################

# train the network to minimize the cost function and update the weights/bias
costs, w1, w2, b = training_loop(learning_rate, iterations, w1, w2, b, n)
fig = plt.figure(num = ('Figure '+ str(fgn) + ': Cost versus n iterations')) # create a blank figure and change its title
plt.plot(costs, label = 'Cost per n iterations') # plot the costs
fgn += 1

# define a mystery data point that has not been classified yet. the network will attempt to classify it
mystery_point = [5, 2]

# attempt to classify the mystery data point
x = mystery_point[0] * w1 +  mystery_point[1] * w2 + b
predicted_classification = sigmoid(x)
print('The mystery data point has been classified as:', predicted_classification)

# visualize the solution
fig = plt.figure(num = ('Figure '+ str(fgn) + ': Classification of the Domain')) # create a blank figure and change its title
for i in linspace(0, 10, 20):
    for j in linspace(0, 10, 20):
        x = i * w1 + j * w2 + b
        prediction = sigmoid(x)
        color = 'b'
        if prediction > 0.5:
            color = 'r'
        plt.scatter([i], [j], c = color, alpha = 0.2)
for i in range(len(data_set)):
    color = 'r'
    if data_set[i][2] == 0:
        color = 'b'
    plt.scatter([data_set[i][0]], [data_set[i][1]], c = color)
plt.scatter([mystery_point[0]], [mystery_point[1]], c = 'k')

# show the plots
plt.show()