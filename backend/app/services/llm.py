import os
import requests
from app.services import prompt_builder
import re

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mistral")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")

REGEX_USER = re.compile(r'[Uu]ser:\s')
REGEX_BREAK_LINE = re.compile(r'\n+')

conversation_history = []

def formart_conversation(character, user_reply, bot_reply):

    user_reply['content'] = re.sub(REGEX_USER, '', user_reply['content'])
    bot_reply['content'] = re.sub(rf'{character}:\s', '', bot_reply['content'])
    bot_reply['content'] = re.sub(REGEX_BREAK_LINE, ' ', bot_reply['content'])

    return user_reply, bot_reply

def start_conversation(name):
    greeting = prompt_builder.get_greeting(name)
    
    conversation_history.clear()
    conversation_history.append({"role": "assistant", "content": greeting})
    return greeting

def get_response(request):
    if LLM_PROVIDER == "mistral":
        return call_mistral(request)
    elif LLM_PROVIDER == "deepseek":
        return call_deepseek(request)
    
def call_mistral(request):

    messages = [
        {"role": "system", "content": prompt_builder.build_system_prompt(request.character)},
        *conversation_history,
        {"role": "user", "content": request.prompt}
    ]

    payload = {
        "model": "mistral:latest",
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": 80,
            "stop": ["User:"]
        }
    }

    response = requests.post(MISTRAL_API_URL, json=payload)
    reply = response.json()["message"]["content"].strip()

    user_reply = {"role": "user", "content": request.prompt.strip()}
    bot_reply = {"role": "assistant", "content": reply}

    user_reply, bot_reply = formart_conversation(request.character, user_reply, bot_reply)

    conversation_history.append(user_reply)
    conversation_history.append(bot_reply)
    print(conversation_history)

    return bot_reply['content']

def call_deepseek(request):
    return "TBD"