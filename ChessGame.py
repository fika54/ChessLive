import chess
import chess.svg
import dontleak
import obsws_python as obs
import time
import threading
import json
import pygame

try:
        winOBS = obs.ReqClient(host='localhost', port=dontleak.obs_server_port, password=dontleak.obs_server_password)
        print('Connected to OBS')
except:
        print('Failed to connect to OBS')
        quit()



#variables to help run the game

#the players
player1 = ''
player2 = ''

#the board
playerboard = chess.Board()

#player turn
current_player = ''

#total moves done in the game
move_counter = 0

#current url for obs
currentURL = 'chessbackup'

#check if the game is active
game_started = False


#initialise pygame
pygame.mixer.init()


#print(playerboard.is_check())
def lobby_timer():
    global player1
    global player2
    while True:
        time.sleep(1)
        if player1 != '' or player2 != '':
            if game_started == False:
                timer = 15
                winOBS.set_input_settings(
                    "LobbyClock",
                    {'opacity': 100},
                    True
                )
                while player1 != '' or player2 != '':
                    winOBS.set_input_settings(
                        "LobbyClock",
                        {'text': f'{timer}'},
                        True
                    )
                    time.sleep(1)
                    timer = timer-1
                    
                    if game_started == True:
                        break

                    if timer <= 5:
                        pygame.mixer.Sound('timerunningout.mp3').play()

                    if timer <= 0:
                        player1 = ''
                        player2 = ''
                        winOBS.set_input_settings(
                            "Player 1",
                            {'text': 'Player 1'},
                            True
                        )
                        winOBS.set_input_settings(
                            "Player 2",
                            {'text': 'Player 2'},
                            True
                        )
                        winOBS.set_input_settings(
                            '!join info',
                            {'text': ' !join to Enter  '},
                            True
                        )
                        break
                winOBS.set_input_settings(
                    "LobbyClock",
                    {'opacity': 0},
                    True
                )
                
thread = threading.Thread(target=lobby_timer)
thread.start()

#background music
def background_music():
    while True:
        sound = pygame.mixer.Sound('Background.mp3')
        sound.set_volume(0.5)
        sound.play()
        time.sleep(3688)

thread2 = threading.Thread(target=background_music)
thread2.start()

#functions to facilitate the game

#helper functions
def switch_player():
    global current_player
    if current_player == player1:
        current_player = player2
        winOBS.set_input_settings(
            'Player 2',
            {'opacity': 100},
            True
        )
        winOBS.set_input_settings(
            'Player 1',
            {'opacity': 60},
            True
        )
    else:
        if current_player == player2:
            current_player = player1
            winOBS.set_input_settings(
                'Player 1',
                {'opacity': 100},
                True
            )
            winOBS.set_input_settings(
                'Player 2',
                {'opacity': 60},
                True
            )



#player attempts to joins the game
def join_game(username: str):
      global game_started
      global player1
      global player2
      if game_started == False:
            
            if winOBS.get_current_program_scene() != 'Starter Screen':
                 winOBS.set_current_program_scene('Starter Screen')
                
            if player1 == '' and username != player2:
                player1 = username
                print('p1 join')
                winOBS.set_input_settings(
                    "Player 1",
                    {'text': player1,
                     'opacity': 100},
                    True
                )
                pygame.mixer.Sound('notify.mp3').play()
            else:
                  if player2 == '' and username != player1:
                        player2 = username
                        print('p2 join')
                        winOBS.set_input_settings(
                            "Player 2",
                            {'text': player2,
                             'opacity': 100},
                            True
                        )
                        pygame.mixer.Sound('notify.mp3').play()

            if player1 != '' and player2 != '':
                winOBS.set_input_settings(
                    '!join info',
                    {'text': ' !start   '},
                    True
                )
            else:
                winOBS.set_input_settings(
                    '!join info',
                    {'text': ' !join to Enter  '},
                    True
                )
            


def forfeit_game(username: str):
    if username == player1:
        end_game(player2, 'forfeit')
    else:
        if username != player2:
            end_game(player1, 'forfeit')


    
def leave_game(username: str):
    global player1
    global player2
    if username == player1:
        if game_started == False:
            player1 = ''
            print('p1 leave')
            winOBS.set_input_settings(
                    "Player 1",
                    {'text': 'Player 1'},
                    True
            )
            winOBS.set_input_settings(
                    '!join info',
                    {'text': ' !join to Enter  '},
                    True
            )
            pygame.mixer.Sound('notify.mp3').play()
        else:
             #game end function
             end_game(player2, 'forfeit')
    else:
         if username == player2:
            if game_started == False:
                player2 = ''
                print('p2 leave')
                winOBS.set_input_settings(
                    "Player 2",
                    {'text': 'Player 2'},
                    True
                )
                winOBS.set_input_settings(
                    '!join info',
                    {'text': ' !join to Enter  '},
                    True
                )
                pygame.mixer.Sound('notify.mp3').play()
            else:
                 end_game(player1, 'forfeit')
     

#starts the game
def start_game(username: str):
      global game_started
      global current_player
      if player1 != '' and player2 != '':
        if player1 == username or player2 == username:
            game_started = True
            update_board()
            current_player = player1
            pygame.mixer.Sound('game-start.mp3').play()
            winOBS.set_input_settings(
                'Player 2',
                {'opacity': 60},
                True
            )
            winOBS.set_current_program_scene('Chess Live')
            thread = threading.Thread(target=move_timer)
            thread.start()
            
            
            #obs things to start the game

def end_game(winner: str, type_of_win):
    global game_started
    global current_player
    global player1
    global player2
    global playerboard
    global move_counter


    update_board()
    game_started = False
    current_player = ''
    player1 = ''
    player2 = ''
    move_counter = 0
    playerboard = chess.Board()

    winOBS.set_input_settings(
        '!join info',
        {'text': '  !join to Enter  '},
        True
    )

    winOBS.set_input_settings(
            'Player 2',
            {'opacity': 100},
            True
    )
    winOBS.set_input_settings(
        'Player 1',
        {'opacity': 100},
        True
    )

    winOBS.set_input_settings(
        'Check',
        {'opacity': 0},
        True
    )

    pygame.mixer.Sound('game-end.mp3').play()

    if type_of_win != 'stalemate':
        record_win(winner)
        #obs things to end the game
        winOBS.set_input_settings(
             'Win condition',
             {'text': f"Won by {type_of_win}!"},
             True
        )
        winOBS.set_input_settings(
             'win',
             {'text': f"{winner}"},
             True
        )
        print(f"{winner} won by {type_of_win}!")
        
    else:
         winOBS.set_input_settings(
             'win',
             {'text': "Stalemate!"},
             True
        )
         print('Stalemate!')
         update_board()

    if any(name == winner for name, _ in get_top(5)):
        display_top_5()
    
    winOBS.set_current_program_scene('Game end')
    winOBS.set_input_settings(
             'Player 1',
             {'text': 'Player 1'},
             True
        )
    winOBS.set_input_settings(
             'Player 2',
             {'text': 'Player 2'},
             True
        )
    time.sleep(1)

#the current person whos turn it is moves their piece
def piece_move(username:  str, move: str):
    global move_counter
    print('tryna move')
    global current_player
    #checks if the game has started or not
    if game_started != True:
        print('game not started')
        return False
    #checks if command comes from the relevant player
    if username != current_player:
        return False
    
    

    try:
        boardMove = chess.Move.from_uci(move)
        if boardMove in playerboard.legal_moves:
            castle = playerboard.is_castling(boardMove)
            capture = playerboard.is_capture(boardMove)

        
        playerboard.push_uci(move)
        winOBS.set_input_settings(
            "Last move input",
            {'text': move},
            True
        )
        move_counter = move_counter + 1
        print(f'new move counter: {move_counter}')
        #edit to show an overlay on obs
        #end the game
        #update a leaderboard
        if playerboard.is_checkmate():
            end_game(current_player, 'checkmate')
            return

        #flips the current player
        switch_player()


        

        #edit later for obs overlay
        if playerboard.is_check():
            print(f"{current_player} is in check!")
            winOBS.set_input_settings(
                'Check',
                {'opacity': 100},
                True
            )
        else:
            winOBS.set_input_settings(
                'Check',
                {'opacity': 0},
                True
            )


        if playerboard.is_stalemate():
            end_game('', 'stalemate')
            return
        
        #sounds for the move
        print('sounds')
        if playerboard.is_check():
            print('check')
            pygame.mixer.Sound('move-check.mp3').play()
        else:
            if castle:
                print('castle')
                pygame.mixer.Sound('castle.mp3').play()
            else:
                if capture:
                    print('capture')
                    pygame.mixer.Sound('capture.mp3').play()
                else:
                    print('move')
                    pygame.mixer.Sound('move.mp3').play()
        
        update_board()
        #update move counter
        return
        
    except:
        #change to a comment of ('invalid move') in tiktok chat
        print('invalid move')
        pygame.mixer.Sound('illegal.mp3').play()
        return

#timer for the game

def move_timer():
    timer = 30
    movecheck = move_counter
    while timer != 0 and game_started == True:
        winOBS.set_input_settings(
            "Timer",
            {'text': f'{timer}'},
            True
        )
        #display to obs
        time.sleep(1)
        timer = timer - 1

        if timer <= 10:
            pygame.mixer.Sound('timerunningout.mp3').play()

        if movecheck != move_counter:
            movecheck = move_counter
            timer = 30
    if game_started == True:
        if current_player == player1:
            winner = player2
        else:
            winner = player1
        end_game(winner, 'Timeout')


        

        
    

#updates the board for the live
def update_board():
    global currentURL
    URL = f"file:///C:/Users/jajay/OneDrive/Documents/Chessbot/{currentURL}.html"
    #creates an svg for the board
    board_svg = chess.svg.board(playerboard, size=480)

    #saved that svg as an image
    with open("last_position.svg", "w") as svg_file:
        svg_file.write(board_svg)

    #updates obs with that new image
    winOBS.set_input_settings(
       "chess",
       {'url': URL},
       True
    )

    if currentURL == 'chess':
          currentURL = 'chessbackup'
          print('switched to chessbackup')
    else:
          if currentURL == 'chessbackup':
                currentURL = 'chess'
                print('switched to chess')

#leaderboard commands
FILENAME = "leaderboard.json"

def load_leaderboard():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_leaderboard(lb):
    with open(FILENAME, "w") as f:
        json.dump(lb, f, indent=2)

def record_win(player):
    lb = load_leaderboard()
    lb[player] = lb.get(player, 0) + 1
    save_leaderboard(lb)

def get_top(n=None):
    lb = load_leaderboard()
    # Sort by win count descending
    ranked = sorted(lb.items(), key=lambda item: item[1], reverse=True)
    return ranked if n is None else ranked[:n]

def get_wins(username: str):
     lb = load_leaderboard()
     return lb[username]

def display_top_5():
    records = get_top(5)

    with open("leaderboard.txt", "w", encoding="utf-8") as f:
    # 3) Write a header (optional)
        f.write("LeaderBoard:\n")

        # 4) Loop through records and write each in your desired format.
        for rec in records:
            # Example: fixed-width columns, name left-aligned in 14 chars, score right-aligned in 5
            line = f"{rec[1]:>5} | {rec[0]:<14}\n"
            f.write(line)

