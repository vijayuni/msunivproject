import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences  
import numpy as np
import pickle

model = load_model('model.h5')

test_data = ["Green investment boom and electric car sales: six key things about Biden’s climate bill","Channel boat deaths prompt fresh anger over asylum policy", "England hit back to beat Colombia and set up World Cup semi with Australia"]
max_length = 20  # Adjust this based on your model's input size

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

sequences = tokenizer.texts_to_sequences(test_data)
padded_sequences = pad_sequences(sequences, padding='post', maxlen=max_length)

predictions = model.predict(padded_sequences)

labels = ['tech', 'sports', 'world', 'entertainment', 'health']
predicted_classes = [labels[np.argmax(pred)] for pred in predictions]

for i, prediction in enumerate(predicted_classes):
    print(f"Article '{test_data[i]}' is predicted to be in category: {prediction}")
