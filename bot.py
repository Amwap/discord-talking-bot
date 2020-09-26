import discord
from dora_client import Dora_client
import json

with open('config.json') as f:
    config = json.load(f)

TOKEN = config['token']
client = discord.Client()
bot = Dora_client()

bot.key = config['key']
last_message = {}
rating_stop = {}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    text = message.content.replace('d!', '')
    lowtext = text.lower().strip()
    if message.author == client.user:
        return
    elif message.content.startswith('d!'):
        if lowtext.startswith('add'):
            try:
                arg1, arg2 = text.replace('add', '').split('=')
                author = f'discord {message.author.id}'
                response = bot.learn(arg1, arg2, author)
                answer = response['answer']

            except IndexError:
                answer = 'Ошибочная команда. попробуй "d! add вопрос = ответ"'

        elif lowtext.startswith('r+') or lowtext.startswith('r-'):
            if rating_stop[message.author] == last_message[message.channel.id]:
                answer = 'Больше одного раза голосовать нельзя.'

            else:
                if lowtext.startswith('r+'): operator = 'rup'
                if lowtext.startswith('r-'): operator = 'rdown'
                response = bot.rating(operator, last_message[message.channel.id])
                answer = response['answer']
                rating_stop[message.author] = last_message[message.channel.id]
                print(message.author, response)

        else:
            response = bot.answer(text)
            last_message[message.channel.id] = response['response_id']
            rating_stop[message.author] = -1
            answer = f"{response['answer']} ({response['coefficient']})"
            print(message.author, response)


        await message.channel.send(answer)


client.run(TOKEN)