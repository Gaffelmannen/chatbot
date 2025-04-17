#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openai
import irc.client
import os

SERVER = os.getenv("IRC_SERVER", "inspircd")
PORT = int(os.getenv("IRC_PORT", 6667))
NICK = os.getenv("IRC_NICK", "God")
CHANNEL = os.getenv("IRC_CHANNEL", "#local")
API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = API_KEY
client = openai.OpenAI(api_key=API_KEY)

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def on_connect(connection, event):
    connection.join(CHANNEL)

def on_message(connection, event):
    user_msg = event.arguments[0]
    if NICK.lower() in user_msg.lower():
        prompt = f"{event.source.nick} says: {user_msg}"
        reply = ask_gpt(user_msg)
        connection.privmsg(CHANNEL, f"{event.source.nick}: {reply}")

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
    main()