from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, JoinEvent, ConnectEvent, DisconnectEvent
import obsws_python as obs
import pygame
import dontleak
import time
import ChessGame

# Replace with your actual TikTok username (without @)
client = TikTokLiveClient(unique_id="@f1kayo54")

CHESS_GAME = ChessGame
ChessGame.update_board()



@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    username = event.user.nickname

    if event.comment == '!join':
        CHESS_GAME.join_game(username)

    if event.comment.lower() == '!leave':
        CHESS_GAME.leave_game(username)

    if event.comment.lower() == '!start':
        CHESS_GAME.start_game(username)
    
    if event.comment.startswith('!move'):
        parts = event.comment.split(' ')
        CHESS_GAME.piece_move(username, parts[1])

    if event.comment.lower() == '!forfeit':
        CHESS_GAME.forfeit_game(username)

@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    print('someone joined')


@client.on(DisconnectEvent)
async def on_disconnect(event: DisconnectEvent):
    client.run()

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print('Connected!')

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()