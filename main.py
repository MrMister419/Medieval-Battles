import os
x = 90
y = 0
s = os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
import pgzrun, random, threading, easygui, pygame
from tkinter.constants import *
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from pygame import mixer
from queue import Queue

##music player functions

def music_player():
    def prev_song():
        next_s = song_box.curselection()
        next_s = next_s[0] - 1
        song = song_box.get(next_s)
        mixer.music.load(song)
        mixer.music.play()
        song_box.selection_clear(0, END)
        song_box.activate(next_s)
        song_box.selection_set(next_s, last=None)

    def next_song():
        next_s = song_box.curselection()
        next_s = next_s[0] + 1
        song = song_box.get(next_s)
        mixer.music.load(song)
        mixer.music.play()
        song_box.selection_clear(0, END)
        song_box.activate(next_s)
        song_box.selection_set(next_s, last=None)

    def pause():
        if song_state['text'] == 'The song is playing.':
            mixer.music.pause()
            song_state['text'] = 'The song is paused.'
        else:
            mixer.music.unpause()
            song_state['text'] = 'The song is playing.'

    def openfolder():
        songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song!", filetypes=(("mp3 Files", "*.mp3"),))
        for song in songs:
            song = song.split('/')[len(song.split('/'))-1]
            song_box.insert(END, song)

    def openfile():
        song = filedialog.askopenfilename(initialdir='tracks/', title="Choose a Song!", filetypes=(("mp3 Files", "*.mp3"),))
        song = song.split('/')[len(song.split('/'))-1]
        song_box.insert(END, song)
        
    def play():
        song = song_box.get(ACTIVE)
        mixer.music.load(song)
        mixer.music.play()
        song_state['text'] = "The song is playing."

    def stop():
        mixer.music.stop()
        song_box.selection_clear(ACTIVE)
        song_state['text'] = "The song is stopped."
    
    mixer.init()
    root = Tk(className =  'Behold the Music Player :')
    root.geometry("+100+20")
    
    master_frame = Frame(root, bg = 'skyblue2')
    master_frame.pack()
    
    info_frame = Frame(master_frame, bg = 'skyblue2')
    info_frame.grid(row=0, column=0)
    
    controls_frame = Frame(master_frame, bg = 'skyblue2')
    controls_frame.grid(row=1, column=0)
    
    file_frame = Frame(master_frame, bg = 'skyblue2')
    file_frame.grid(row=0, column=5)
    
    song_state = Label(info_frame, bg = 'royal blue', width=25, text="Select a song", font = ('algerian',25))
    
    song_state.grid(row=0, column=0)
    
    song_box = Listbox(info_frame, bg = 'pale goldenrod', width=50, height = 15, fg = 'medium purple', font = ('algerian', 20), selectbackground="medium purple")
    song_box.grid(row=1, column=0)
    
    back_button = Button(controls_frame, bg = 'coral', text = 'previous', fg = 'grey25', font = ('castellar', 15, 'bold'), width = 9, command = prev_song)
    forward_button = Button(controls_frame, bg = 'coral', text = ' next', fg = 'grey25', font = ('castellar', 15, 'bold'), width = 9, command = next_song)
    play_button = Button(controls_frame, bg = 'coral', text = ' play ???', fg = 'grey25', font = ('castellar', 15, 'bold'), width = 9, command = play)
    pause_button = Button(controls_frame, bg = 'coral', text = ' pause', fg = 'grey25', font = ('castellar', 15, 'bold'), width = 9, command = pause)
    stop_button = Button(controls_frame, bg = 'coral', text = ' stop', fg = 'grey25', font = ('castellar', 15, 'bold'), width = 9, command = stop)
    
    openfile_button = Button(file_frame, bg = 'medium purple', text = 'Open File', fg = 'grey25', font = ('castellar', 15, 'bold', 'italic'), width = 15, command = openfile)
    openfolder_button = Button(file_frame, bg = 'medium purple', text = 'Open Folder', fg = 'grey25', font = ('castellar', 15, 'bold', 'italic'), width = 15, command = openfolder)
    quit_button = Button(file_frame, bg = 'medium purple', text = 'Quit', fg = 'grey25', font = ('castellar', 15, 'bold', 'italic'), width = 15, command = root.destroy)
    
    author_label = Label(file_frame, bg = 'skyblue2', text = 'Coded by the Andrei !', fg = 'black', font = (':)hhh', 17, 'bold', 'underline'), width = 19, relief = RAISED)
    
    openfile_button.grid(row=0, column=0)
    openfolder_button.grid(row=1, column=0)
    quit_button.grid(row=2, column=0)
    author_label.grid(row=3, column=0)
    
    back_button.grid(row = 0, column = 0)
    forward_button.grid(row = 0, column = 1)
    play_button.grid(row = 0, column = 2)
    pause_button.grid(row = 0, column = 3)
    stop_button.grid(row = 0, column = 4)
    
    root.mainloop()
    

def draw_characters():
    for char in range(10):
        leftChars[char].draw()
    for char in range(10):
        rightChars[char].draw()

def on_mouse_down(pos):
    for i in range(10):
        if leftChars[i].collidepoint(pos):
            selected = leftChars[i]
            print(selected)

def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                border.left = border.width * j
                border.top = border.height * i
                border.draw()
            elif my_map[i][j] == 1:
                floor.left = floor.width * j
                floor.top = floor.height * i
                floor.draw()
            elif my_map[i][j] == 2:
                bones.left = floor.width * j
                bones.top = floor.height * i
                bones.draw()
            elif my_map[i][j] == 3:
                crack.left = floor.width * j
                crack.top = floor.height * i
                crack.draw()
    castle1.draw()
    castle2.draw()
    castle3.draw()
    tower1.draw()
    tower2.draw()

def draw():
    global names, player1, player2, counter, turn, turn_q, q1, q2, q3
    screen.clear()
    map_draw()
    draw_characters()
    
    for char in range(10):
        if leftChars[char].health < 1:
            leftChars[char].death = True
            leftChars[char].image = 'grave'
            leftChars[char].draw()
        if leftChars[char].health < 0:
            leftChars[char].health = 0
    
    if not q1.empty():
        player1 = q1.get()
        player2 = q1.get()
        names = 'defined'
        counter = 1
    if not q2.empty():
        turn = q2.get()
        turn_q = 'use'
    
    ##Text
    if names == 'defined':
        text = player1 + "'s troops"
        text2 = player2 + "'s troops"
        screen.draw.text(text, center=(180, 25), color='blue', fontsize=40)
        screen.draw.text(text2, center=(900, 25), color='red', fontsize=40)
    else:
        screen.draw.text("Player One's troops",
                         center=(180, 25),
                         color='blue',
                         fontsize=40)
        screen.draw.text("Player Two's troops",
                         center=(900, 25),
                         color='red',
                         fontsize=40)

    if turn == 'player1'and names == 'defined':
        screen.draw.text((player1 + "'s turn."), center=(530, 25), color='black', fontsize=40, underline = True)
    elif turn == 'player2'and names == 'defined':
            screen.draw.text((player2 + "'s turn."), center=(530, 25), color='black', fontsize=40, underline = True)
    
    if names == 'defined' and counter == 1:
        q1.task_done()
        q1.task_done()
        counter = 3.14
    if turn_q == 'use':
        q2.task_done()
        turn_q = 'used'

def update():
    for char in range(10):
        if leftChars[char].health < 1:
            leftChars[char].death = True
            leftChars[char].image = 'grave'
            leftChars[char].draw()
    for char in range(10):
        if rightChars[char].health < 1:
            rightChars[char].death = True
            rightChars[char].image = 'grave'
            rightChars[char].draw()
    
    if not q3.empty():
        game_over = q3.get()
        q3.task_done()
        if game_over:
            print('Goodbye!')
            exit()


##easygui functions

def name_selection():
    title = 'Medieval Battles'
    players = []
    
    msg = "Enter the first player's name below."
    player1 = easygui.enterbox(msg, title)
    while player1 is None or player1 == '':
        player1 = easygui.enterbox(msg, title)

    msg = "Enter the second player's name below."
    player2 = easygui.enterbox(msg, title)
    while player2 is None or player2 == '':
        player2 = easygui.enterbox(msg, title)

    with open('Saved Data.txt', 'w') as file:
        file.write(player1)
        file.write('\n')
        file.write(player2)
        file.close()
    easygui.msgbox('Your usernames have been saved.', title, 'Continue')

    players.append(player1)
    players.append(player2)
    return players

def start():
    file_name = 'Saved Data.txt'
    title = 'Medieval Battles'
    button_text = 'Next'
    players = []
    msg = "Welcome to the game! In this two-player game, you will both be leading your own army into battle against each other. Feel free to leave the music player on and minimised while you're playing. When you are ready, press Next to be amazed."
    easygui.msgbox(msg, title, button_text)

    file_size = os.stat(file_name).st_size
    if file_size != 0:
        name_choice = easygui.buttonbox('You have a file with saved usernames. Do you want to use these usernames or create new ones?', title, ['Use saved', 'Create new'])
        if name_choice == 'Use saved':
            with open('Saved Data.txt', 'r') as file:
                lines = file.readlines()
                player1 = lines[0].rstrip()
                player2 = lines[1]
                players.append(player1)
                players.append(player2)
                file.close()
        else:
            players = name_selection()
            player1 = players[0]
            player2 = players[1]
    else:
        players = name_selection()
        player1 = players[0]
        player2 = players[1]
    
    message = " ".join([player1 + ", you will be defending your citadel from", player2 + '.', player2 + ", you will be attacking", player1 + ". Each of you will be commanding your own army and the one who defeats his opponent first wins. May the odds be ever in your favour, and let the battle begin!"])
    easygui.msgbox(message, title, 'Play!')
    return players

def end(q3, winner, loser):
    global restart
    message = " ".join(["  The battle is over.", winner + ', you have prevailed over your opponent,', loser + ". Congratulations on your exemplary strategy and combat skills. You have proved yourself to be an exeptional tactician and a promising future lies ahead for you.", loser + ", you have allowed yourself to be defeated and you will live with your shameful, unwise decisions for eternity.                                                   Farewell, combatants, and may the force be with you always."])
    easygui.msgbox(message, 'Medieval Battles', 'Continue')
    easygui.msgbox("   This work (of art) was developed by Andrei Durbaca. Author's note:            I deem that special thanks should be awarded to Marius, Mihaela and Ramona for their support and invaluable debugging tips. Also, thank you to Mr.Weston, Robert Watkin and Kodland for their remarkable lessons: I could not have programmed this without you. Last but not least, I would like to dedicate this game and all the hours I put into it, to my sister. Cati, this is for you.                                                 Yours Sincerely, Andre??.", 'Medieval Battles: Credits + Acknowledgements', 'Finish')
    restart = easygui.ynbox('Thank you for playing! Do you want to play again?', 'Medieval Battles')
    if restart == False:
        easygui.msgbox("The notable sound tracks that have been implemented in this game were sourced from 'Bensound.com'.                                                                     This is a work of fiction. Names, characters, business, events and incidents are the products of the author's imagination. Any resemblance to actual persons, living or dead, or actual events is purely coincidental.                           All rights reserved.", 'Legal + Disclaimer', 'Continue')
        easygui.msgbox('See you next time.  ;-) ', 'Medieval Battles', 'END')
        game_over = True
        q3.put(game_over)
        q3.put(game_over)

def left_selection_function(left_options, player1, left_options_mod):
    msg = " ".join(["Choose which troop you wish to use in your attack, Commander", player1 + '.'])
    title = player1 + "'s " 'Command Centre'
    choice = easygui.choicebox(msg, title, choices=left_options)

    for char in range(10):
        if choice == left_options[char]:
            selected_char1 = leftChars[char]
            selected_char_name1 = left_options_mod[char]
    
    while choice is None or selected_char1.death == True or selected_char1.uses < 1:
        if choice is None:
            easygui.msgbox("Make a choice, Commander.", title, 'Continue')
        elif selected_char1.death == True:
            message = " ".join(["The", selected_char_name1, 'has been defeated. Choose a different troop, Commander.'])
            easygui.msgbox(message, title, 'Continue')
        else:
            easygui.msgbox("The Wizard is exhausted and cannot cast any more spells. You must choose a different troop, Commander.", title, 'Continue')

        choice = easygui.choicebox(msg, title, choices=left_options)
        for char in range(10):
            if choice == left_options[char]:
                selected_char1 = leftChars[char]
                selected_char_name1 = left_options_mod[char]

    msg = " ".join(["You selected the", selected_char_name1 + '.'])
    easygui.msgbox(msg, title, 'Continue')
    arguments = [selected_char1, selected_char_name1]
    return arguments

def left_target_function(right_options, player1, right_options_mod):
    msg = " ".join(["Choose which of the opponent's troops you wish to attack, Commander", player1 + '.'])
    title = player1 + "'s " 'Command Centre'
    choice = easygui.choicebox(msg, title, choices=right_options)

    for char in range(10):
        if choice == right_options[char]:
            selected_target1 = rightChars[char]
            selected_target_name1 = right_options_mod[char]
    
    while choice is None or selected_target1.death == True:
        if choice is None:
            easygui.msgbox("Make a choice, Commander.", title, 'Continue')
        else:
            easygui.msgbox("You have already defeated this troop. Choose a different opponent.", title, 'Continue')

        choice = easygui.choicebox(msg, title, choices=right_options)
        for char in range(10):
            if choice == right_options[char]:
                selected_target1 = rightChars[char]
                selected_target_name1 = right_options_mod[char]

    msg = " ".join(["You selected the", selected_target_name1 + '.'])
    easygui.msgbox(msg, title, 'Continue')
    arguments = [selected_target1, selected_target_name1]
    return arguments

def right_selection_function(right_options, player2, right_options_mod):
    msg = " ".join(["Choose which troop you wish to use in your attack, Commander", player2 + '.'])
    title = player2 + "'s " 'Command Centre'
    choice = easygui.choicebox(msg, title, choices=right_options)

    for char in range(10):
        if choice == right_options[char]:
            selected_char2 = rightChars[char]
            selected_char_name2 = right_options_mod[char]
    
    while choice is None or selected_char2.death == True or selected_char2.uses < 1:
        if choice is None:
            easygui.msgbox("Make a choice, Commander.", title, 'Continue')
        elif selected_char2.death == True:
            message = " ".join(["The", selected_char_name2, 'has been defeated. Choose a different troop, Commander.'])
            easygui.msgbox(message, title, 'Continue')
        else:
            message = " ".join(["The Sorcerer is exhausted and cannot cast any more spells. You must choose a different troop, Commander."])
            easygui.msgbox(message, title, 'Continue')

        choice = easygui.choicebox(msg, title, choices = right_options)
        for char in range(10):
            if choice == right_options[char]:
                selected_char2 = rightChars[char]
                selected_char_name2 = right_options_mod[char]
    
    msg = " ".join(["You selected the", selected_char_name2 + '.'])
    easygui.msgbox(msg, title, 'Continue')
    arguments = [selected_char2, selected_char_name2]
    return arguments

def right_target_function(left_options, player2, left_options_mod):
    msg = " ".join(["Choose which of the opponent's troops you wish to attack, Commander", player2 + '.'])
    title = player2 + "'s Command Centre"
    choice = easygui.choicebox(msg, title, choices=left_options)

    for char in range(10):
        if choice == left_options[char]:
            selected_target2 = leftChars[char]
            selected_target_name2 = left_options_mod[char]
    
    while choice is None or selected_target2.death == True:
        if choice is None:
            easygui.msgbox("Make a choice, Commander.", title, 'Continue')
        else:
            easygui.msgbox("You have already defeated this troop. Choose a different opponent.", title, 'Continue')

        choice = easygui.choicebox(msg, title, choices = left_options)
        for char in range(10):
            if choice == left_options[char]:
                selected_target2 = leftChars[char]
                selected_target_name2 = left_options_mod[char]
    
    msg = " ".join(["You selected the", selected_target_name2 + '.'])
    easygui.msgbox(msg, title, 'Continue')
    arguments = [selected_target2, selected_target_name2]
    return arguments


def player1_attack(spell_mesg1, player1_spell, selected_char1, selected_target1, player1, player2, right_options, left_options, selected_char_name1, selected_target_name1):
    storm_effect1 = 0
    storm_random1 = random.randint(1, 10)
    if storm_random1 > 9:
        storm_effect1 = 2
    
    if selected_char_name1 == 'Wizard':
        wizard.uses -= 1
        player1_spell = 'on'
        message = " ".join([player1, "has used his", selected_char_name1, 'to cast a spell on his army. Next time it is', player1 + "'s turn, his army will deal more damage. The damage dealt will be random. Press OK to continue to", player2 + "'s turn."])
    elif selected_char_name1 == 'Healing Potion':
        healer_left.uses -= 1
        added_health1 = random.randint(1, 3)
        for char in range(10):
            if leftChars[char].death == False:
                leftChars[char].health = leftChars[char].health + added_health1
            if leftChars[char].health > 10:
                leftChars[char].health = 10
        message = " ".join([player1, "has used his", selected_char_name1, 'to heal his army. All of', player1 + "'s troops have been given back", str(added_health1 * 10), "healthpoints each, to a maximum of 100. Press OK to continue to", player2 + "'s turn."])
    elif player1_spell == 'off':
        selected_target1.health = selected_target1.health - (selected_char1.damage - storm_effect1)
        message = " ".join([player1, "has used his", selected_char_name1, 'to do', str(selected_char1.damage * 10), "damage to", player2 + "'s", selected_target_name1 + '. The', selected_target_name1, 'now has', str(selected_target1.health * 10), 'health. Press Ok to continue to', player2 + "'s turn."])
    else:
        added_damage1 = random.randint(1, 7)
        selected_target1.health = selected_target1.health - ((selected_char1.damage + added_damage1) - storm_effect1)
        player1_spell = 'off'
        spell_mesg1 = 'on'
        message = " ".join(["Because of the spell his wizard cast last turn,", player1, "was able to deal extra damage this round. He has used his", selected_char_name1, 'to do', str((selected_char1.damage + added_damage1) * 10), "damage to", player2 + "'s", selected_target_name1 + '. The', selected_target_name1, 'now has', str(selected_target1.health * 10), 'health. Press Ok to continue to', player2 + "'s turn."])
    
    if storm_random1 > 9:
        if spell_mesg1 == 'on':
            message = " ".join(['A huge thunderstorm has swept over the battlefield and', player1, 'has not been able to be so damaging in his attack: his damage has been decreased by 20 healthpoints in this round. However, the spell that his wizard cast last round has assisted him, increasing the damage he has dealt.', player1, "has used his", selected_char_name1, 'to do', str(((selected_char1.damage + added_damage1) - 2)* 10), "damage to", player2 + "'s", selected_target_name1 + '. The', selected_target_name1, 'now has', str(selected_target1.health * 10), 'health. Press Ok to continue to', player2 + "'s turn."])
            spell_mesg1 = 'off'
        else:
            message = " ".join(['A huge thunderstorm has swept over the battlefield and', player1, 'has not been able to be so damaging in his attack: his damage has been decreased by 20 healthpoints in this round.', player1, "has used his", selected_char_name1, 'to do', str((selected_char1.damage - 2) * 10), "damage to", player2 + "'s", selected_target_name1 + '. The', selected_target_name1, 'now has', str(selected_target1.health * 10), 'health. Press Ok to continue to', player2 + "'s turn."])
    
    for char in range(10):
        if leftChars[char].health < 0:
            leftChars[char].health = 0
    
    message = message
    storm_effect1 = 0
    title = 'Battle Report'
    turn = 'player2'
    easygui.msgbox(message, title, 'Continue')
    arguments = [turn, player1_spell]
    return arguments

def player2_attack(spell_mesg2, player2_spell, selected_char2, selected_target2, player1, player2, right_options, left_options, selected_char_name2, selected_target_name2):
    storm_effect2 = 0
    storm_random2 = random.randint(1, 10)
    if storm_random2 > 9:
        storm_effect2 = 2
    
    if selected_char_name2 == 'Sorcerer':
        sorcerer.uses -= 1
        player2_spell = 'on'
        message = " ".join([player2, "has used his", selected_char_name2, 'to cast a spell on his army. Next time it is', player2 + "'s turn, his army will deal more damage. The damage dealt will be random. Press OK to continue to", player1 + "'s turn."])
    elif selected_char_name2 == 'Healing Potion':
        healer_right.uses -= 1
        added_health2 = random.randint(1, 3)
        for char in range(10):
            if leftChars[char].death == False:
                rightChars[char].health = rightChars[char].health + added_health2
            if rightChars[char].health > 10:
                rightChars[char].health = 10
        message = " ".join([player2, "has used his", selected_char_name2, 'to heal his army. All of', player2 + "'s troops have been given back", str(added_health2 * 10), "healthpoints each, to a maximum of 100. Press OK to continue to", player1 + "'s turn."])
    elif player2_spell == 'off':
        selected_target2.health = selected_target2.health - (selected_char2.damage - storm_effect2)
        message = " ".join([player2, "has used his", selected_char_name2, 'to do', str(selected_char2.damage * 10), "damage to", player1 + "'s", selected_target_name2 + '. The', selected_target_name2, 'now has', str(selected_target2.health * 10), 'health. Press Ok to continue to', player1 + "'s turn."])
    else:
        added_damage2 = random.randint(1, 7)
        selected_target2.health = selected_target2.health - ((selected_char2.damage + added_damage2) - storm_effect2)
        player2_spell = 'off'
        spell_mesg1 = 'on'
        message = " ".join(["Because of the spell his wizard cast last turn,", player2, "was able to deal extra damage this round. He has used his", selected_char_name2, 'to do', str((selected_char2.damage + added_damage2) * 10), "damage to", player1 + "'s", selected_target_name2 + '. The', selected_target_name2, 'now has', str(selected_target2.health * 10), 'health. Press Ok to continue to', player1 + "'s turn."])
    
    if storm_random2 > 9:
        if spell_mesg2 == 'on':
            message = " ".join(['A huge thunderstorm has swept over the battlefield and', player2, 'has not been able to be so damaging in his attack: his damage has been decreased by 20 healthpoints in this round. However, the spell that his wizard cast last round has assisted him, increasing the damage he has dealt.', player2, "has used his", selected_char_name2, 'to do', str(((selected_char2.damage + added_damage2) - 2)* 10), "damage to", player1 + "'s", selected_target_name2 + '. The', selected_target_name2, 'now has', str(selected_target2.health * 10), 'health. Press Ok to continue to', player1 + "'s turn."])
            spell_mesg2 = 'off'
        else:
            message = " ".join(['A huge thunderstorm has swept over the battlefield and', player2, 'has not been able to be so damaging in his attack: his damage has been decreased by 20 healthpoints in this round.', player2, "has used his", selected_char_name2, 'to do', str((selected_char2.damage - 2) * 10), "damage to", player1 + "'s", selected_target_name2 + '. The', selected_target_name2, 'now has', str(selected_target2.health * 10), 'health. Press Ok to continue to', player1 + "'s turn."])
    
    for char in range(10):
        if rightChars[char].health < 0:
            rightChars[char].health = 0
    
    message = message
    storm_effect2 = 0
    title = 'Battle Report'
    turn = 'player1'
    easygui.msgbox(message, title, 'Continue')
    arguments = [turn, player2_spell]
    return arguments


def easygui_function(q1, q2, q3, spell_mesg1, spell_mesg2, turn, selection, count, game, names, player1_spell, player2_spell, right_options, left_options, right_options_mod, left_options_mod, rightChars, leftChars):
    loser = None
    players = start()
    player1 = players[0]
    player2 = players[1]
    q1.put(player1)
    q1.put(player2)
    while loser == None:  #change this line to:'     while loser != None:'
        if turn == 'player1':
            arguments = left_selection_function(left_options, player1, left_options_mod)
            selected_char1 = arguments[0]
            selected_char_name1 = arguments[1]
            arguments = left_target_function(right_options, player1, right_options_mod)
            selected_target1 = arguments[0]
            selected_target_name1 = arguments[1]
            arguments = player1_attack(spell_mesg1, player1_spell, selected_char1, selected_target1, player1, player2, right_options, left_options, selected_char_name1, selected_target_name1)
            turn = arguments[0]
            player1_spell = arguments[1]
            q2.put(turn)
            
            right_options = [' '.join(("1. Archer                               | Health:", str(rightChars[0].health * 10), "           | Damage:", str(rightChars[0].damage * 10))), ' '.join(("2. Ballista                              | Health:", str(rightChars[1].health * 10), "           | Damage:", str(rightChars[1].damage * 10))), ' '.join(("3. Spearman                         | Health:", str(rightChars[2].health * 10), "           | Damage:", str(rightChars[2].damage * 10))), ' '.join(("4. Soldier                               | Health:", str(rightChars[3].health * 10), "           | Damage:", str(rightChars[3].damage * 10))), ' '.join(("5. Healing Potion                    | Health:", str(rightChars[4].health * 10), "           | Healing: 10 to 30 (random)")), ' '.join(("6. sorcerer                      | Health:", str(rightChars[5].health * 10), "           | Damage increase: 10 to 70 (random)")), ' '.join(("7. Reaper                               | Health:", str(rightChars[6].health * 10), "           | Damage:", str(rightChars[6].damage * 10))), ' '.join(("8. Spearman                          | Health:", str(rightChars[7].health * 10), "           | Damage:", str(rightChars[7].damage * 10))), ' '.join(("9. Ballista                              | Health:", str(rightChars[8].health * 10), "           | Damage:", str(rightChars[8].damage * 10))), ' '.join(("10. Archer                             | Health:", str(rightChars[9].health * 10), "           | Damage:", str(rightChars[9].damage * 10)))]
            
        elif turn == 'player2':
            arguments = right_selection_function(right_options, player2, right_options_mod)
            selected_char2 = arguments[0]
            selected_char_name2 = arguments[1]
            arguments = right_target_function(left_options, player2, left_options_mod)
            selected_target2 = arguments[0]
            selected_target_name2 = arguments[1]
            arguments = player2_attack(spell_mesg2, player2_spell, selected_char2, selected_target2, player1, player2, right_options, left_options, selected_char_name2, selected_target_name2)
            turn = arguments[0]
            player2_spell = arguments[1]
            q2.put(turn)

            left_options = [' '.join(("1. Archer                               | Health:", str(leftChars[0].health * 10), "          | Damage:", str(leftChars[0].damage * 10))), ' '.join(("2. Catapult                            | Health:", str(leftChars[1].health * 10), "          | Damage:", str(leftChars[1].damage * 10))), ' '.join(("3. Spearman                          | Health:", str(leftChars[2].health * 10), "          | Damage:", str(leftChars[2].damage * 10))), ' '.join(("4. Soldier                               | Health:", str(leftChars[3].health * 10), "          | Damage:", str(leftChars[3].damage * 10))), ' '.join(("5. Healing Potion                    | Health:", str(leftChars[4].health * 10), "          | Healing: 10 to 30 (random)")), ' '.join(("6. Wizard                       | Health:", str(leftChars[5].health * 10), "          | Damage increase: 10 to 70 (random)")), ' '.join(("7. Paladin                               | Health:", str(leftChars[6].health * 10), "          | Damage:", str(leftChars[6].damage * 10))), ' '.join(("8. Spearman                          | Health:", str(leftChars[7].health * 10), "          | Damage:", str(leftChars[7].damage * 10))), ' '.join(("9. Catapult                            | Health:", str(leftChars[8].health * 10), "          | Damage:", str(leftChars[8].damage * 10))), ' '.join(("10. Archer                             | Health:", str(leftChars[9].health * 10), "          | Damage:", str(leftChars[9].damage * 10)))]

        result1 = all(x.death == True for x in leftChars)
        result2 = all(x.death == True for x in rightChars)

        if result1 == True:
            loser = 'player1'
        if result2 == True:
            loser = 'player2'
        if loser =='player1':
            winner = player2
        else:
            winner = player1
    
    #loser = player2  # remove hashtag on this line
    #winner = player1  # remove hashtag on this line
    restart = end(q3, winner, loser)
    
    if restart != False:
        turn = 'player1'
        selection = 'player'
        count = 'new'
        game = ':-)'
        names = 'undefined'
        player1_spell = 'off'
        player2_spell = 'off'
        easygui_function(q1, q2, q3, spell_mesg1, spell_mesg2, turn, selection, count, game, names, player1_spell, player2_spell, right_options, left_options, right_options_mod, left_options_mod, rightChars, leftChars)

turn = 'player1'
selection = 'player'
count = 'new'
counter = 0
turn_q = 'unused'
game = ':-)'
names = 'Games take too long to program. :-('
player1_spell = 'off'
player2_spell = 'off'
spell_mesg1 = 'off'
spell_mesg2 = 'off'
game_over = False

WIDTH = 1100
HEIGHT = 600

leftChars = []
rightChars = []

left_options_mod = ["Archer", "Catapult", "Spearman", "Soldier", "Healing Potion",
    "Wizard", "Paladin", "Spearman", "Catapult", "Archer"]

right_options_mod = ["Archer", "Ballista", "Spearman", "Soldier", "Healing Potion",
    "Sorcerer", "Reaper", "Spearman", "Ballista", "Archer"]

##Floor
border = Actor('border')
floor = Actor('floor')
bones = Actor('bones')
crack = Actor('crack')
castle2 = Actor('castle1', (25, 300))
castle1 = Actor('castle', (25, 240))
castle3 = Actor('castle', (25, 360))
tower1 = Actor('tower', (25, 50))
tower2 = Actor('tower', (25, 550))

## Left Army
archer_left_top = Actor('archer_mod2', (75, 75))
catapult_top = Actor('catapult_resized', (75, 125))
spearman_left_top = Actor('spearman_right', (75, 175))
soldier = Actor('soldier', (75, 225))
healer_left = Actor('potion', (75, 275))
wizard = Actor('wizard2', (75, 325))
knight = Actor('knight', (75, 375))
spearman_left_bottom = Actor('spearman_right', (75, 425))
catapult_bottom = Actor('catapult_resized', (75, 475))
archer_left_bottom = Actor('archer_mod2', (75, 525))

## Right Army
archer_right_top = Actor('archer_mod', (1025, 75))
ballista_top = Actor('ballista', (1025, 125))
spearman_right_top = Actor('spearman_left', (1025, 175))
skeleton = Actor('skeleton', (1025, 225))
healer_right = Actor('potion', (1025, 275))
sorcerer = Actor('sorcerer', (1025, 325))
reaper = Actor('reaper', (1025, 375))
spearman_right_bottom = Actor('spearman_left', (1025, 425))
ballista_bottom = Actor('ballista', (1025, 475))
archer_right_bottom = Actor('archer_mod', (1025, 525))

leftChars.append(archer_left_top)
leftChars.append(catapult_top)
leftChars.append(spearman_left_top)
leftChars.append(soldier)
leftChars.append(healer_left)
leftChars.append(wizard)
leftChars.append(knight)
leftChars.append(spearman_left_bottom)
leftChars.append(catapult_bottom)
leftChars.append(archer_left_bottom)

rightChars.append(archer_right_top)
rightChars.append(ballista_top)
rightChars.append(spearman_right_top)
rightChars.append(skeleton)
rightChars.append(healer_right)
rightChars.append(sorcerer)
rightChars.append(reaper)
rightChars.append(spearman_right_bottom)
rightChars.append(ballista_bottom)
rightChars.append(archer_right_bottom)

##Sets damage for all chars
left_archers_damage = random.randint(2, 5)
left_catapult_damage = random.randint(5, 8)
left_spearman_damage = random.randint(3, 6)
left_knight_damage = random.randint(4, 7)
left_soldier_damage = random.randint(3, 7)

right_archers_damage = random.randint(2, 5)
right_catapult_damage = random.randint(5, 8)
right_spearman_damage = random.randint(3, 6)
right_knight_damage = random.randint(4, 7)
right_soldier_damage = random.randint(3, 7)

archer_left_top.damage = left_archers_damage
archer_left_bottom.damage = left_archers_damage
catapult_top.damage = left_catapult_damage
catapult_bottom.damage = left_catapult_damage
spearman_left_top.damage = left_spearman_damage
spearman_left_bottom.damage = left_spearman_damage
knight.damage = left_knight_damage
soldier.damage = left_soldier_damage
healer_left.damage = 0
wizard.damage = 0

archer_right_top.damage = right_archers_damage
archer_right_bottom.damage = right_archers_damage
spearman_right_top.damage = right_spearman_damage
spearman_right_bottom.damage = right_spearman_damage
ballista_top.damage = right_catapult_damage
ballista_bottom.damage = right_catapult_damage
reaper.damage = right_knight_damage
skeleton.damage = right_soldier_damage
healer_right.damage = 0
sorcerer.damage = 0

##sets number of uses available for each char
for i in range(10):
    leftChars[i].uses = 6969
for i in range(10):
    rightChars[i].uses = 6969

wizard.uses = 3
sorcerer.uses = 3
healer_left.uses = 2
healer_right.uses = 2

##sets health for all chars
archer_left_top.health = 5
archer_left_bottom.health = 5
catapult_top.health = 7
catapult_bottom.health = 7
spearman_left_top.health = 6
spearman_left_bottom.health = 6
knight.health = 9
soldier.health = 8
healer_left.health = 4
wizard.health = 6

archer_right_top.health = 5
archer_right_bottom.health = 5
spearman_right_top.health = 7
spearman_right_bottom.health = 7
ballista_top.health = 6
ballista_bottom.health = 6
reaper.health = 9
skeleton.health = 8
healer_right.health = 4
sorcerer.health = 6

##sets death status for all chars
for i in range(10):
    leftChars[i].death = False
for i in range(10):
    rightChars[i].death = False
    
left_options = [' '.join(("1. Archer                               | Health:", str(leftChars[0].health * 10), "          | Damage:", str(leftChars[0].damage * 10))), ' '.join(("2. Catapult                            | Health:", str(leftChars[1].health * 10), "          | Damage:", str(leftChars[1].damage * 10))), ' '.join(("3. Spearman                          | Health:", str(leftChars[2].health * 10), "          | Damage:", str(leftChars[2].damage * 10))), ' '.join(("4. Soldier                               | Health:", str(leftChars[3].health * 10), "          | Damage:", str(leftChars[3].damage * 10))), ' '.join(("5. Healing Potion                    | Health:", str(leftChars[4].health * 10), "          | Healing: 10 to 30 (random)")), ' '.join(("6. Wizard                       | Health:", str(leftChars[5].health * 10), "          | Damage increase: 10 to 70 (random)")), ' '.join(("7. Paladin                               | Health:", str(leftChars[6].health * 10), "          | Damage:", str(leftChars[6].damage * 10))), ' '.join(("8. Spearman                          | Health:", str(leftChars[7].health * 10), "          | Damage:", str(leftChars[7].damage * 10))), ' '.join(("9. Catapult                            | Health:", str(leftChars[8].health * 10), "          | Damage:", str(leftChars[8].damage * 10))), ' '.join(("10. Archer                             | Health:", str(leftChars[9].health * 10), "          | Damage:", str(leftChars[9].damage * 10)))]

right_options = [' '.join(("1. Archer                               | Health:", str(rightChars[0].health * 10), "           | Damage:", str(rightChars[0].damage * 10))), ' '.join(("2. Ballista                             | Health:", str(rightChars[1].health * 10), "           | Damage:", str(rightChars[1].damage * 10))), ' '.join(("3. Spearman                         | Health:", str(rightChars[2].health * 10), "           | Damage:", str(rightChars[2].damage * 10))), ' '.join(("4. Soldier                               | Health:", str(rightChars[3].health * 10), "           | Damage:", str(rightChars[3].damage * 10))), ' '.join(("5. Healing Potion                    | Health:", str(rightChars[4].health * 10), "           | Healing: 10 to 30 (random)")), ' '.join(("6. sorcerer                      | Health:", str(rightChars[5].health * 10), "           | Damage increase: 10 to 70 (random)")), ' '.join(("7. Reaper                               | Health:", str(rightChars[6].health * 10), "           | Damage:", str(rightChars[6].damage * 10))), ' '.join(("8. Spearman                          | Health:", str(rightChars[7].health * 10), "           | Damage:", str(rightChars[7].damage * 10))), ' '.join(("9. Ballista                           | Health:", str(rightChars[8].health * 10), "           | Damage:", str(rightChars[8].damage * 10))), ' '.join(("10. Archer                             | Health:", str(rightChars[9].health * 10), "           | Damage:", str(rightChars[9].damage * 10)))]

my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0],
          [0, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0],
          [0, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 0],
          [0, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 0],
          [0, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

q1 = Queue()
q2 = Queue()
q3 = Queue()
easygui_thread = threading.Thread(target=easygui_function, args = (q1, q2, q3, spell_mesg1, spell_mesg2, turn, selection, count, game, names, player1_spell, player2_spell, right_options, left_options, right_options_mod, left_options_mod, rightChars, leftChars))
easygui_thread.daemon = True

music_thread = threading.Thread(target = music_player)

try:
    easygui_thread.start()
    music_thread.start()
    pgzrun.go()
except:
    print('    An error has occurred. :( Please try again or contact Developer Durbaca for help.')