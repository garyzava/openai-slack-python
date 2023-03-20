import os
from pathlib import Path
from dotenv import load_dotenv
import openai

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

openai.api_key = os.environ.get('OPENAI_API_KEY')
completion = openai.Completion()

start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.6, presence_penalty=0.6, best_of=1,
        max_tokens=2048)
    answer = response.choices[0].text.strip()
    return answer

def ask_chatgpt(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f'{prompt}'}],
            max_tokens=4000,
            #n=1,
            stop=['\nHuman'],
            temperature=0,
        )
        answer = response['choices'][0]['message']['content'].strip()
    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        answer = f"OpenAI API returned an API Error: {e}"
        print(answer)
        pass
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        answer = f"Failed to connect to OpenAI API: {e}"
        print(answer)
        pass
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        answer = f"OpenAI API request exceeded rate limit: {e}"
        print(answer)
        pass      
    return answer
