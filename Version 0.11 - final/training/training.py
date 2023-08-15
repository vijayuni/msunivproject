import tensorflow as tf 
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv('news_headlines.csv')

training_data,testing_data =  train_test_split(df.iloc[:5000,:],test_size=0.2)

plt.plot(training_data['news_category'].value_counts())
plt.plot(testing_data['news_category'].value_counts())
plt.title('Train-Test Split Visualization')
plt.show()

def tokenization_(training_headings, testing_headings, max_length=20, vocab_size = 5000):
    tokenizer = Tokenizer(num_words = vocab_size, oov_token= '<oov>')
 
    tokenizer.fit_on_texts(training_headings)
    word_index = tokenizer.word_index
    training_sequences = tokenizer.texts_to_sequences(training_headings)
    training_padded = pad_sequences(training_sequences, padding= 'post', maxlen = max_length, truncating='post')
 
    testing_sequences = tokenizer.texts_to_sequences(testing_headings)
    testing_padded = pad_sequences(testing_sequences, padding= 'post', maxlen = max_length, truncating='post')
 
    return tokenizer, training_padded, testing_padded

tokenizer, X_train, X_test = tokenization_(training_data['news_headline'], testing_data['news_headline'])
 
labels = {'sports': [1, 0, 0, 0, 0],
          'tech': [0, 1, 0, 0, 0],
          'world': [0, 0, 1, 0, 0],
          'health': [0, 0, 0, 1, 0],
          'entertainment': [0, 0, 0, 0, 1]}

Y_train = np.array([labels[y] for y in training_data['news_category']])
Y_test = np.array([labels[y] for y in testing_data['news_category']])

def build_model(n, vocab_size, embedding_size):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Embedding(vocab_size, embedding_size, input_length=n))
    model.add(tf.keras.layers.GlobalAveragePooling1D()) 
    model.add(tf.keras.layers.Dense(5, activation = 'softmax'))  
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics='accuracy')
    print(model.summary())
    return model

max_length = 20
vocab_size = 5000
embedding_size = 128

model = build_model(max_length, vocab_size, embedding_size)

epochs = 25
history = model.fit(X_train, Y_train, validation_data = (X_test, Y_test), epochs = epochs)

# Save the model
model.save("model.h5")

# Save the tokenizer
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
