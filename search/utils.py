import string

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from dotFoods.settings import MAX_LEN_KEYWORD, MIN_LEN_KEYWORD

def tokenize(data):
    # tokenize text and remove stopwords
    stemmer = SnowballStemmer('english')
    text = ''.join([ch for ch in str(data)
                    if ch not in string.punctuation])
    words = word_tokenize(text)
    normalized = [stemmer.stem(word) for word in words]
    return [word for word in normalized
            if word and word not in stopwords.words('english')
            and MAX_LEN_KEYWORD >= len(word) >= MIN_LEN_KEYWORD]
