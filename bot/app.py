#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openai import OpenAI
import irc.client
import os
from roboto import Roboto

SERVER = os.getenv("IRC_SERVER", "inspircd")
PORT = int(os.getenv("IRC_PORT", 6667))
NICK = os.getenv("IRC_NICK", "God")
CHANNEL = os.getenv("IRC_CHANNEL", "#local")
API_KEY = os.getenv("OPENAI_API_KEY")

OpenAI.api_key = API_KEY
client = OpenAI(api_key=API_KEY)

use_chat_gpt = True
rob = Roboto()

def ask_rob(query):
    return rob.talk(query=query)

def ask_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except:
        return "Error"

def on_connect(connection, event):
    connection.join(CHANNEL)
    connection.privmsg(CHANNEL, "Walk in the light my son.")

def on_message(connection, event):
    user_msg = event.arguments[0]
    if NICK.lower() in user_msg.lower():
        prompt = f"{event.source.nick} says: {user_msg}"

        if use_chat_gpt:
            reply = ask_gpt(user_msg)
        else:
            reply = ask_rob(user_msg)
        
        connection.privmsg(CHANNEL, f"{event.source.nick}: {reply}")
        print(prompt)

def main():
    reactor = irc.client.Reactor()
    conn = reactor.server().connect(SERVER, PORT, NICK)
    conn.add_global_handler("welcome", on_connect)
    conn.add_global_handler("privmsg", on_message)
    conn.add_global_handler("pubmsg", on_message)
    reactor.process_forever()

if __name__ == "__main__":
    print("Das boot is a bot.")
    print(f"API_KEY={API_KEY}")
    if ask_gpt("test") != "Error":
        use_chat_gpt = True
    else:
        use_chat_gpt = False
    main()