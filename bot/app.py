#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openai import OpenAI
import irc.client
import os
import textwrap
import datetime
from roboto import Roboto
from hal import Hal

from chatlog import Chatlog

SERVER = os.getenv("IRC_SERVER", "inspircd")
PORT = int(os.getenv("IRC_PORT", 6667))
NICK = os.getenv("IRC_NICK", "God")
CHANNEL = os.getenv("IRC_CHANNEL", "#local")
API_KEY = os.getenv("OPENAI_API_KEY")

IRC_MAX_MESSAGE_LENGTH = 450

OpenAI.api_key = API_KEY
client = OpenAI(api_key=API_KEY)

use_chat_gpt = True
rob = Roboto()
hal = Hal()

def split_into_chunks(s):
    return textwrap.wrap(s, IRC_MAX_MESSAGE_LENGTH)

def ask_rob(input):
    print(f"ask_rob={input}")
    return rob.talk(query=input)

def ask_hal(input):
    print(f"ask_hal={ask_hal}")
    return hal.response(user_response=input)

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
    connection.privmsg(CHANNEL, "Walk in the light my children.")

def on_message(connection, event):
    user_msg = event.arguments[0]
    if NICK.lower() in user_msg.lower():
        cl = Chatlog()
        #prompt = f"{event.source.nick} says: {user_msg}"
        
        cl.insert_row(
            log_channel=CHANNEL,
            log_message=user_msg.replace(f"{event.source.nick}", ""),
            log_user=event.source.nick,
            log_timestamp=datetime.datetime.now()
        )

        user_msg = user_msg.lower()
        user_msg = user_msg.replace(NICK.lower(), "")
        user_msg = user_msg.strip()

        if use_chat_gpt:
            reply = ask_gpt(user_msg)
        else:
            reply = ask_hal(user_msg)
            #reply = ask_rob(user_msg)
        
        reply = reply.strip()
        
        messages = split_into_chunks(reply)
        for message in messages:
            connection.privmsg(CHANNEL, f"{event.source.nick}: {message}")
        
        cl.insert_row(
            log_channel=CHANNEL,
            log_message=reply,
            log_user=NICK,
            log_timestamp=datetime.datetime.now()
        )

def main():
    reactor = irc.client.Reactor()
    conn = reactor.server().connect(SERVER, PORT, NICK)
    conn.add_global_handler("welcome", on_connect)
    conn.add_global_handler("privmsg", on_message)
    conn.add_global_handler("pubmsg", on_message)
    reactor.process_forever()

if __name__ == "__main__":
    print("Das boot is a bot.")

    if ask_gpt("test") != "Error":
        use_chat_gpt = True
    else:
        use_chat_gpt = False
    
    main()