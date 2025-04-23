import nltk
import re
import wikipedia
from nltk.chat.util import Chat, reflections
#from chatbot import Chat, reflections

class Roboto:

    def __init__(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

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

        self.chat = Chat(self.pairs, reflections)

        pass

    def _investigate_subject(self, query):
        try:
            return wikipedia.summary(query)
        except Exception:
            for new_query in wikipedia.search(query):
                try:
                    return wikipedia.summary(new_query)
                except Exception:
                    pass
        return f"I have not got the slightest clue about {query}."
    
    def talk(self, query):
        subject_details = self._investigate_subject(query)
        return self.chat.respond(query)