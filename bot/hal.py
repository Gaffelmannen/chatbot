import numpy as np
import random
import string
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Hal:

    GREET_INPUT = ("hello, hi, sup")
    GREET_RESPONSE = [
        "Hi",
        "Hello",
        "Howdy",
        "Wz up",
        "How is it going?"
    ]
    GREET_NOT_UNDERSTAND = "I am sorry! I don't understand you"

    def __init__(self):

        nltk.download('punkt')
        nltk.download('wordnet')

        self.lemmer = nltk.stem.WordNetLemmatizer()

        with open("input/chatbot.txt","r", errors = "ignore") as f:
            self.raw_doc = f.read()
            self.raw_doc = self.raw_doc.lower()


    def _remove_punct_dict(self):
        return {ord(punct): None for punct in string.punctuation}

    def _lem_token(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def _lem_normalize(self, text):
        return self._lem_token(
            nltk.word_tokenize(
                    text.lower().translate(self._remove_punct_dict())
                )
            )

    def greet(self, sentence):
        for word in sentence.split():
            if word.lower() in self.GREET_INPUT:
                return random.choice(self.GREET_RESPONSE)

    def response(self, user_response):

        sent_tokens = nltk.sent_tokenize(self.raw_doc) 
        word_tokens = nltk.word_tokenize(self.raw_doc)

        hal_response = ""
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(
            tokenizer = self._lem_normalize, 
            stop_words = "english"
        )
        
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf == 0):
            hal_response = f"{hal_response} {self.GREET_NOT_UNDERSTAND}"
            return hal_response
        else:
            hal_response_response = f"{hal_response}{sent_tokens[idx]}"
            return hal_response_response