import numpy as np
import pandas as pd
import zipfile
import os
import json
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# Extract dataset
zip_file_path = 'archive.zip'
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall('extracted')

# Load and preprocess intents dataset
with open('extracted/intents.json') as file:
    data = json.load(file)

texts = []
intents = []
for intent in data['intents']:
    for text in intent['text']:
        texts.append(text)
        intents.append(intent['intent'])

# Tokenize texts
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
encoded_texts = tokenizer.texts_to_sequences(texts)
max_len = max([len(x) for x in encoded_texts])
padded_texts = pad_sequences(encoded_texts, maxlen=max_len, padding='post')

# Encode intents
le = LabelEncoder()
encoded_intents = le.fit_transform(intents)
num_intents = len(le.classes_)
encoded_intents = tf.one_hot(encoded_intents, depth=num_intents)

# Build and train the model
input_layer = Input(shape=(max_len,))
embedding_layer = Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_len)(input_layer)
lstm_layer = LSTM(128)(embedding_layer)
output_layer = Dense(num_intents, activation='softmax')(lstm_layer)
model = Model(inputs=input_layer, outputs=output_layer)

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(padded_texts, encoded_intents, epochs=50, batch_size=16)

# Save the model and tokenizer
model.save('chatbot_model34.keras')
with open('tokenizer.json', 'w') as f:
    json.dump(tokenizer.to_json(), f)

with open('label_encoder.json', 'w') as f:
    json.dump(le.classes_.tolist(), f)

print("Model training complete and saved.")
