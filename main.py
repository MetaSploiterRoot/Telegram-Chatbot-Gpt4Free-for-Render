from telethon import TelegramClient
from telethon.events import NewMessage
from dotenv import load_dotenv
from os import getenv
import theb

load_dotenv()

api_id = getenv('API_ID')
api_hash = getenv('API_HASH')
bot_token = getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash)

@client.on(NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hey! Write something and I will answer you using the gpt-3 model or add me to a group and I will answer you when you mention me.')

@client.on(NewMessage())
async def handler(e):
    my_id = await client.get_me()
    my_id = my_id.id
    my_username = await client.get_me()
    my_username = my_username.username
    if e.text.startswith('/'):
        return
    if e.sender_id == my_id:
        return
    if e.is_private:
        prompt = e.text
    else:
        if not e.text.startswith(f'@{my_username}'):
            return
        prompt = e.text.replace(f'@{my_username}', '')
    msg = await e.respond('Thinking...')
    full_text = ""
    for token in theb.Completion.create(prompt=prompt):
        full_text += token
    await msg.edit(full_text)

client.start(bot_token=bot_token)
client.run_until_disconnected()