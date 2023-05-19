import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from tensorflow.keras.preprocessing.sequence import pad_sequences

import re

stopwords = [i.lower() for i in nltk.corpus.stopwords.words('english') + [chr(i) for i in range(97, 123)]]

def clean_text(text):
    return str(re.sub("\s+", " ", ' '.join([i for i in re.sub("[^9A-Za-z ]", "" , re.sub("\\n", "", re.sub("\s+", " ", re.sub(r'http\S+', '', text.lower())))).split(" ") if i not in stopwords])))

def clean_texts(texts, tokenizer):
    return pad_sequences(tokenizer.texts_to_sequences([
        clean_text(text) for text in texts
    ]), maxlen=100, padding='post', truncating='post')