import re
import gensim
import numpy as np
import pandas as pd
import math
import keras
import nltk
import pickle
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords # Stop word like: the a an
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer # Root word like: loved->love
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

max_words = 5000
max_len = 200

# Use to cleaning data.
def depure_data(data):

  # Replace puntuation
    data = re.sub('[^a-zA-Z]',' ', data)

    # #Removing URLs with a regular expression
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    data = url_pattern.sub(r'', data)

    # Remove Emails
    data = re.sub('\S*@\S*\s?', '', data)

    # Remove new line characters
    data = re.sub('\s+', ' ', data)

    # Remove distracting single quotes
    data = re.sub("\'", "", data)

    # Make it lowercase
    data = data.lower()

    # Split the word
    data = data.split()

    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    data = [ps.stem(word) for word in data if not word in set(all_stopwords)]
    data = " ".join(data)

    return data

# Sent a sentence to word.
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

# combine the word back to sentence
def detokenize(text):
    return TreebankWordDetokenizer().detokenize(text)

def sentiment_analysis(tokenizer, text, best_model):
    sentiment_2 = ['Neutral', 'Positive', 'Negative']
    # text = "This vaccine is not good like another vaccine"
    sequence = tokenizer.texts_to_sequences(sent_to_words([depure_data(text)]))
    test = pad_sequences(sequence, maxlen=max_len)
    percent = best_model.predict(test)*100
    list_percent = []
    for i in range(len(percent[0])):
        list_percent.append(percent[0][i])
    result = sentiment_2[list_percent.index(max(list_percent))]
    return result, list_percent

def analysis(inputtext):
    # load tokenizer
    with open('tokenizer/tokenizer2_mix.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    best_model = keras.models.load_model("model/best_model5_mix_suff.hdf5")
    text = inputtext
    result, percentage = sentiment_analysis(tokenizer, text, best_model)
    neutralpercentage = str(percentage[0])
    positivepercentage = str(percentage[1])
    negativepercentage = str(percentage[2])
    return "Neutral: " + neutralpercentage + "       "+"Positive: " + positivepercentage + "       " +"Negative: " + negativepercentage + "          "+ "Result: " + result 
