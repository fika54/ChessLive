from twitchAPI.chat import Chat, EventData,ChatMessage, ChatSub, ChatCommand
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
import asyncio
import dontleak
import random
import time
import obsws_python as obs
import pygame
import ChessGame

#set up constants
APP_ID = dontleak.client_id
APP_SECRET = dontleak.client_secret
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]
TARGET_CHANNEL = 'fika54'
RANDOM_NUMBER = 624
CHESS_GAME = ChessGame
ChessGame.update_board()




# #listen for message
# async def on_message(msg: ChatMessage):
#     #print username and chat message
#     print(f'{msg.user.display_name} - {msg.text}')





# Keep track of users we've seenS
seen_users = set()
number_guessed = False


async def on_message(msg: ChatMessage):
    username = msg.user.display_name

    if msg.text == '!join':
        CHESS_GAME.join_game(username)

    if msg.text == '!leave':
        CHESS_GAME.leave_game(username)

    if msg.text == '!start':
        CHESS_GAME.start_game(username)
    
    if msg.text.startswith('!move'):
        parts = msg.text.split(' ')
        CHESS_GAME.piece_move(username, parts[1])

    if msg.text == '!forfeit':
        CHESS_GAME.forfeit_game(username)
        


    
    



#bot connected successfully
async def on_ready(ready_event: EventData):
    #connect to TARGET_CHANNEL
    await ready_event.chat.join_room(TARGET_CHANNEL)

    #print ready message
    print('Bot Ready')


#guess command
async def on_guess(cmd: ChatCommand):
    await cmd.reply(cmd.text)


#lurk command
async def lurk_command(cmd: ChatCommand):
    chance = random.randint(0,4)

    name = cmd.user.display_name

    responses = [
        f"See you soon, {name}!",
        f"{name} is now lurking in the shadows 👀",
        f"Thanks for hanging out, {name}. Enjoy your lurk!",
        f"{name} just activated stealth mode 🕶️",
        f"Lurk mode engaged. Catch you later, {name}!"
    ]

    await cmd.reply(responses[chance])

#bot setupfunction
async def run_bot():
    bot = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(bot, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await bot.set_user_authentication(token, USER_SCOPE, refresh_token)


    #initialize chat class
    chat = await Chat(bot)

    #register events
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)

    #register commands
    chat.register_command('lurk', lurk_command)

    #start the chatbot
    chat.start()

    try:
        input('press ENTER to stop \\n')
    finally:
        chat.stop()
        await bot.close()


asyncio.run(run_bot())