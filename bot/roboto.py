import nltk
from nltk.chat.util import Chat, reflections
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag, ne_chunk
from nltk.probability import FreqDist
from nltk.cluster.util import cosine_distance

import re

import wikipedia

from chatlog import Chatlog

class Roboto:

    def __init__(self):
        nltk.download("punkt")
        nltk.download("punkt_tab")
        nltk.download("stopwords")
        nltk.download("averaged_perceptron_tagger")

        self.pairs = [
            [r"hi|hello|hey", ["Hello! How can I help you today?", "Hi there! How may I assist you?"]],
            [r"my name is (.*)", ["Hello %1! How can I assist you today?"]],
            [r"(.*) your name?", ["I am your friendly chatbot!"]],
            [r"how are you?", ["I'm just a bot, but I'm doing well. How about you?"]],
            [r"tell me a joke", ["Why don't skeletons fight each other? They don't have the guts!"]],
            [r"(.*) (help|assist) (.*)", ["Sure! How can I assist you with %3?"]],
            [r"bye|exit", ["Goodbye! Have a great day!", "See you later!"]],
            [r"(.*)", ["I'm sorry, I didn't understand that. Could you rephrase?", "Could you please elaborate?"]]
        ]

        self.wikiword = "wiki "
        self.historyword = "history "

        self.chat = Chat(self.pairs, reflections)
        self.stop_words = set(stopwords.words("english"))

    def _summarize(self, text: str) -> str:
        sentences = sent_tokenize(text)
        preprocessed_sentences = [self._preprocess_text(sentence) for sentence in sentences]
        flat_preprocessed_words = [word for sentence in preprocessed_sentences for word in sentence]
        
        word_freq = FreqDist(flat_preprocessed_words)
        sentence_scores = self._score_sentences(preprocessed_sentences, word_freq)

        summary_sentences = []
        if sentence_scores:
            sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
            top_sentences = sorted_scores[:3]
            
            for index, _ in top_sentences:
                summary_sentences.append(sentences[index])
        summary = " ".join(summary_sentences)

        return summary

    def _score_sentences(self, sentences: list, word_freq: list) -> dict:
        sentence_scores = {}
        
        for i, sentence in enumerate(sentences):
            for word in sentence:
                if word in word_freq:
                    if i in sentence_scores:
                        sentence_scores[i] += word_freq[word]
                    else:
                        sentence_scores[i] = word_freq[word]
        
        return sentence_scores

    def _preprocess_text(self, sentence: str) -> str:
        sentence = re.sub(r"[^a-zA-Z0-9]", " ", sentence)
        
        words = word_tokenize(sentence)
        
        filtered_words = [w for w in words if w.lower() not in self.stop_words]
        
        stemmer = PorterStemmer()
        stemmed = [stemmer.stem(w) for w in filtered_words]
        
        return stemmed

    def _investigate_subject(self, query: str) -> str:
        try:
            return wikipedia.summary(query)
        except Exception:
            for new_query in wikipedia.search(query):
                try:
                    return wikipedia.summary(new_query)
                except Exception:
                    pass
        return f"I have not got the slightest clue about {query}."

    def _check_history_for_user(self, username: str) -> str:
        cl = Chatlog()
        data = cl.get_log_entry_by_user(username)
        return data

    def talk(self, query: str) -> str:
        response = ""
        if query.startswith(self.wikiword):
            query = (query[len(self.wikiword):]).lstrip()
            subject_details = self._investigate_subject(query)
            response = self._summarize(subject_details)
        elif query.startswith(self.historyword):
            query = (query[len(self.historyword):]).lstrip()
            history_details = self._check_history_for_user("gaffelmannen")
            print(history_details)
            #response = self._summarize(history_details)
        else:
            response = self.chat.respond(query)
        
        return response