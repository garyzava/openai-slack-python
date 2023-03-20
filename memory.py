import sqlite3
import os.path

import logging
logging.basicConfig(level=logging.DEBUG)

import datetime;

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "events.db")
#with sqlite3.connect(db_path) as db:

# Connect to the SQLite database
conn = sqlite3.connect(db_path, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        data TEXT NOT NULL,
        user TEXT NOT NULL,
        channel TEXT NULL,
        user_type TEXT NOT NULL
    )
""")
conn.commit()

start_chat_log = '''Human: Hello, who are you? You are slack chatbot
AI: I am doing great. How can I help you today?
'''

# Define a function to store Slack events
def write_message(type, timestamp, data, user, channel, user_type):
    # Store the event in the database
    cur.execute("""
        INSERT INTO events (type, timestamp, data, user, channel, user_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (type, timestamp, data, user, channel, user_type))
    conn.commit()      
    #conn.close()  


# Define a function to retrieve messages from the database
def get_message(type, user, channel):
    cur.execute("""
        SELECT data, user_type
        FROM events
        WHERE type = ?
        and user = ?
        and channel = ?
        ORDER BY timestamp
    """,(type,user,channel))
    rows = cur.fetchall()
    #check if there are any returned rows before returning
    if len(rows) > 0:
        #messages = [eval(row[0]) for row in rows]
        messages = [row[1] + ': '+ row[0] for row in rows]
        chat_log = '\n'.join(messages)
    else:
        chat_log = None
    return chat_log

def get_chat_log(type, timestamp, data, user, channel):
    chat_log = get_message(type, user, channel)
    #Write the incoming message to the database
    write_message("message", timestamp, data, user, channel, "Human")
    return chat_log

def append_interaction_to_chat_log(question, answer, chat_log=None, user=None, channel=None):
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    if chat_log is None:
        chat_log = start_chat_log
    write_message("message", ts, answer, user, channel, "AI")
    return f'{chat_log}Human: {question}\nAI: {answer}\n'

#def append_interaction_to_chat_log(question, answer, chat_log=None):
#    if chat_log is None:
#        chat_log = start_chat_log
#    return f'{chat_log}Human: {question}\nAI: {answer}\n'






if __name__ == "__main__":
    # Create the events table if it doesn't exist
    pass


# Retrieve messages from the database and print them out
#messages = get_messages()
#for message in messages:
#    print(message)