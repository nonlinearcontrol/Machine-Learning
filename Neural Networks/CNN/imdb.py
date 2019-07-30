########## imdb.py ##########

# 7/29/2019

'''

This script implements a RNN on the  
imdb data set

'''
print('Running...'); print('\n')

#########
# Imports
#########

import tensorflow as tf
from tensorflow import keras
import numpy as np
print(tf.__version__)

################
# Define dataset
################

'''
Initialize the dataset -->
- Dataset of 25,000 movies reviews from 
IMDB, labeled by sentiment (positive/negative)
- It has already been preprocessed 
such that the reviews (sequences 
of words) have been converted to 
sequences of integers, where each 
integer represents a specific word 
in a dictionary.
- For convenience, words are indexed by 
overall frequency in the dataset, so that 
for instance the integer "3" encodes the 
3rd most frequent word in the data.
- This allows for quick filtering operations such 
as: "only consider the top 10,000 most common words, 
but eliminate the top 20 most common words".
'''
imdb = keras.datasets.imdb

'''
x_train, x_test: list of sequences, which are 
lists of indexes (integers). If the num_words 
argument was specific, the maximum possible index 
value is num_words-1. If the maxlen argument was 
specified, the largest possible sequence length is maxlen

y_train, y_test: list of integer labels (1 or 0)
'''
(train_data, train_labels),(test_data, test_labels) = imdb.load_data(num_words = 10000)
# means you’ll only keep the top 10,000 most frequently occurring words in the training data

####################
# Understand dataset
####################

# understand the shape of the train data
print('Shape of train_data:', train_data.shape)

# understand the length of the train_data dn train_labels
print("Training entries: {}, labels: {}".format(len(train_data), len(train_labels)))

# look at the first review in the train_data set
print('First review:', train_data[0])

# movie reviews can be different lengths
print(  'len(train_data[0]):', len(train_data[0]), 
        '|',
        'len(train_data[1]):', len(train_data[1]),
        '|',
        'len(train_data[2]):', len(train_data[2]),
        '|',
        'len(train_data[3]):', len(train_data[3])
)

# A dictionary mapping words to an integer index
word_index = imdb.get_word_index()

# The first indices are reserved
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2  # unknown
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

def decode_review(text):
    return ' '.join([reverse_word_index.get(i, '?') for i in text])

print(decode_review(train_data[0]))
