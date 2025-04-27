import pandas as pd

df = pd.read_csv("MovieReview.csv")
try:
    display(df.head())  # Works in Jupyter
except NameError:
    print(df.head())  # Works in standard Python scripts
print(df.shape)

df = df.drop('sentiment', axis=1)

import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK datasets (only needs to be done once)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
stop_words = set(stopwords.words('english'))
print("Stopwords loaded successfully!")

# Converts the unicode file to ascii
def unicode_to_ascii(s):
    # ''.join(...) This reconstructs the string using only the characters that are not nonspacing marks (effectively removing accents).
    return ''.join(c for c in unicodedata.normalize('NFD', s) #characters with diacritical marks (like é) are split into base character (e) and diacritical mark (´)
        if unicodedata.category(c) != 'Mn') #filters out characters whose Unicode category is 'Mn' (Mark, Nonspacing) - usually accent marks and other diacritics.

def preprocess_sentence(w):
    w = unicode_to_ascii(w.lower().strip())
    # creating a space between a word and the punctuation following it
    # eg: "he is a boy." => "he is a boy ."
    w = re.sub(r"([?.!,¿])", r" \1 ", w) #Separate punctuation from words
    w = re.sub(r'[" "]+', " ", w) #Replace multiple spaces with a single space
    # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
    w = re.sub(r"[^a-zA-Z?.!]+", " ", w) #Remove all characters except letters and certain punctuation. Keeps only: Letters (a-z, A-Z). Allowed punctuation: ?.!
    w = re.sub(r'\b\w{0,2}\b', '', w) #Remove short words (0 to 2 characters long). "I am happy" → "happy".

    # remove stopword
    mots = word_tokenize(w.strip())
    mots = [mot for mot in mots if mot not in stop_words]
    return ' '.join(mots).strip()

df.review = df.review.apply(lambda x :preprocess_sentence(x)) #applies preprocess_sentence() to each row in the review column of a DataFrame
df.head()

import tensorflow as tf
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000) #defining a tokenizer with a vocabulary size of 10,000 words.
tokenizer.fit_on_texts(df.review) #Update the tokenizer dictionary using the fit_on_texts method

word2idx = tokenizer.word_index #Store the word-index matching dictionary in the variable word2idx
idx2word = tokenizer.index_word #Store the index-word matching dictionary in the variable idx2word
vocab_size = tokenizer.num_words #Store the size of the vocabulary in the variable vocab_size

# Creatomg Dataset X, Y
import numpy as np

def sentenceToData(tokens, WINDOW_SIZE):
    window = np.concatenate((np.arange(-WINDOW_SIZE,0),np.arange(1,WINDOW_SIZE+1)))
    X,Y=([],[])
    for word_index, word in enumerate(tokens) :
        if ((word_index - WINDOW_SIZE >= 0) and (word_index + WINDOW_SIZE <= len(tokens) - 1)) :
            X.append(word)
            Y.append([tokens[word_index-i] for i in window])
    return X, Y


WINDOW_SIZE = 5

X, Y = ([], [])
for review in df.review:
    for sentence in review.split("."):
        word_list = tokenizer.texts_to_sequences([sentence])[0]
        if len(word_list) >= WINDOW_SIZE:
            Y1, X1 = sentenceToData(word_list, WINDOW_SIZE//2)
            X.extend(X1)
            Y.extend(Y1)
    
X = np.array(X).astype(int)
y = np.array(Y).astype(int).reshape([-1,1])

#Creating the model. The Embedding layer will take the imput size 10K and output size 300. The Dense layer will cinsist of 10K neurons and a SoftMax activation function
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, Dense, GlobalAveragePooling1D

embedding_dim = 300
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(GlobalAveragePooling1D())
model.add(Dense(vocab_size, activation='softmax'))

#Compile the model and train it during 50 epochs - here only 2 because models runs too long
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, batch_size = 128, epochs=2)

#Saved in H5 format
model.save("word2vec.h5") 