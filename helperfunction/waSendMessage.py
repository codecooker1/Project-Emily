import os
import sys
import emoji
# and formatting them as :emoji_name:
import openai
import json

from twilio.rest import Client

from dotenv import load_dotenv
load_dotenv()

# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

openai.api_key = os.getenv("OPENAI_API_KEY")

lore = open("utils/emily-test.txt").read()
name = "Saminur"

messages = [
    {"role": "system", "content": lore}
]

conversation = []
# Create a dictionary to hold the message data
history = {"history": conversation}

ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
FROM = os.environ.get('FROM')

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_message_simple(content):
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1
    )

    chat_response = completion.choices[0].message
    messages.append({"role": "assistant", "content": chat_response.content})
    print(chat_response['content'])
    conversation.append(messages)
    
    with open("conversation.json", "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)
        
    return chat_response

#Code To Be Cleaned
'''
def openai_answer(prompt):
    global total_characters, conversation

    total_characters = sum(len(d['content']) for d in conversation)

    while total_characters > 4000:
        try:
            # print(total_characters)
            # print(len(conversation))
            conversation.pop(2)
            total_characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error removing old messages: {0}".format(e))

    with open("conversation.json", "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

    prompt = getPrompt()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=128,
        temperature=1,
        top_p=0.9,
        frequency_penalty=.7,
        presence_penalty=.6,
    )
    message = response['choices'][0]['message']['content']
    conversation.append({'role': 'assistant', 'content': message})
    #conversation.append({'role': 'name', 'content': name})

    return message
'''


def sendMessage(senderId, message):

    print(senderId)
    print(message)
    
    answer = send_message_simple(message)
    
    res = client.messages.create(
        body=emoji.emojize(answer.content),
        from_=FROM,
        to=f'whatsapp:+{senderId}'
    )
    return res