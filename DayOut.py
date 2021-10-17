from tkinter import *
import random
import os
import pickle
import webbrowser

global score
global scoreboard
global username
global null
null = ""
not_null = False
global user_score
global value
global username
global wid
global choice

choice = 1  # default - space
# validates the username entry input


def get_username():
    global username
    global value
    global not_null
    global window_page1
    while not not_null:
        if username.get() != null:
            not_null = True
            value = username.get()
            page2()
        else:
            not_null = False
            window_page1.destroy()
            page1()


# opens the leaderboard file or, if not possible
# creats an empty list
def leaderboard_management():
    global scoreboard
    try:
        leaderboard_file = open("leaderboard", "rb")
        scoreboard = pickle.load(leaderboard_file)
        leaderboard_file.close()
    except FileNotFoundError:
        scoreboard = {}


# gets the value from entry
def get_value():
    global username
    global value
    value = username.get()


# finds the  score of the user
# if its the first time for that player
# it is set to 0
def get_user_score():
    global scoreboard
    global user_score
    global value
    try:
        leaderboard_file = open("leaderboard", "rb")
        scoreboard = pickle.load(leaderboard_file)
        if value in scoreboard:
            user_score = int(scoreboard[value])
        else:
            user_score = 0
        leaderboard_file.close()
    except:
        scoreboar = {}


# runs the game
def play_game():
    global frame_rate
    global score
    global user_score
    global window_game
    global scoreboard
    frame_rate = 20
    score = -1
    global wid
    global window_page2
    global window_game
    global airplane
    global airplane_y
    global pause
    global up_count
    global pipe_x
    global end_replay
    global best_score
    global pipe_hole
    global end_rectangle
    global end_score
    global choice
    global end_menu
    global score_pause
    global pause_now
    pause_now = False
    window_page2.destroy()
    pause_score = 0

    def center(top):
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split("+")[0].split("x"))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2 - 35
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

    window_game = Tk()
    window_game.title("Day Out")
    window_game.geometry("550x700")
    center(window_game)

    airplane_y = 200
    pipe_x = 550
    pipe_hole = 0
    pause = False

    best_score = 0

    wid = Canvas(window_game, width=550, height=700,
                 background="#87CEEB", bd=0)
    wid.pack()

    airplane_img = PhotoImage(file="planeV1.png")
    airplane = wid.create_image(100, 200, image=airplane_img)

    up_count = 0
    end_rectangle = end_score = None

    pipe_up = wid.create_rectangle(
        pipe_x, 0, pipe_x + 100, pipe_hole, fill="#A9A9A9", outline="#A9A9A9"
    )
    pipe_down = wid.create_rectangle(
        pipe_x, pipe_hole + 200, pipe_x + 100, 700,
        fill="#A9A9A9", outline="#A9A9A9"
    )
    score_w = wid.create_text(
        15, 45, text="0", font="Times 50", fill="#FFFFFF", anchor=W
    )

    def display_pipe_hole():
        global pipe_hole
        global score
        global frame_rate
        global user_score
        global pause_score
        score += 1
        user_score = score
        pause_score = score
        wid.itemconfig(score_w, text=str(score))
        pipe_hole = random.randint(50, 500)
        if score + 1 % 7 == 0 and score != 0:
            frame_rate -= 1

    display_pipe_hole()

    def airplane_up(event=None):
        global airplane_y
        global up_count
        global pause

        if not pause:
            airplane_y -= 20
            if airplane_y <= 0:
                airplane_y = 0
            wid.coords(airplane, 100, airplane_y)
            if up_count < 5:
                up_count += 1
                window_game.after(frame_rate, airplane_up)
            else:
                up_count = 0
        else:
            restart_game()

    def airplane_down():
        global airplane_y
        global pause

        airplane_y += 8
        if airplane_y >= 700:
            airplane_y = 700
        wid.coords(airplane, 100, airplane_y)
        if not pause:
            window_game.after(frame_rate, airplane_down)

    def pipes():
        global pipe_x
        global pipe_hole
        global pause
        pipe_x -= 5
        wid.coords(pipe_up, pipe_x, 0, pipe_x + 100, pipe_hole)
        wid.coords(pipe_down, pipe_x, pipe_hole + 200, pipe_x + 100, 700)

        if pipe_x < -100:
            pipe_x = 550
            display_pipe_hole()

        if not pause:
            window_game.after(frame_rate, pipes)

    def end_screen():
        global end_rectangle
        global end_score
        global end_best
        global end_replay
        global end_your_best
        global end_menu
        global scoreboard
        global button_back_end
        global window_game
        end_rectangle = wid.create_rectangle(0, 0, 550, 700, fill="#4E82CA")
        end_score = wid.create_text(
            15,
            260,
            text="Your score: " + str(score),
            font="Times 45",
            fill="#FFFFFF",
            anchor=W,
        )
        end_your_best = wid.create_text(
            15,
            340,
            text="Your best score: " + str(best_score),
            font="Times 45",
            fill="#FFFFFF",
            anchor=W,
        )
        end_replay = wid.create_text(
            0,
            40,
            text="*Press <chosen key>/<space> if default to play again*",
            font="Times 19",
            fill="#FFFFFF",
            anchor=W,
        )
        end_menu = wid.create_text(
            85,
            600,
            text="*Press <m> to go back to the menu*",
            font="Times 19",
            fill="#FFFFFF",
            anchor=W,
        )
        try:
            if user_score > scoreboard[value]:
                scoreboard[value] = user_score
        except KeyError:
            scoreboard[value] = user_score
        window_game.bind("m", back_to_menu)
        scoreboard = dict(sorted(scoreboard.items(),
                                 key=lambda x: x[1], reverse=True))
        leaderboard_file = open("leaderboard", "wb")
        pickle.dump(scoreboard, leaderboard_file)
        leaderboard_file.close()

    def back_to_menu(event):
        window_game.destroy()
        page2V2()

    def collision():
        global pause
        global best_score

        if (pipe_x < 150 and pipe_x + 100 >= 55) and (
            airplane_y < pipe_hole + 45 or airplane_y > pipe_hole + 175
        ):
            pause = True
            if score > best_score:
                best_score = score
            end_screen()
        if not pause:
            window_game.after(frame_rate, collision)

    def restart_game():
        global pipe_x
        global airplane_y
        global score
        global pause
        global frame_rate
        airplane_y = 200
        pipe_x = 550
        score = -1
        frame_rate = 20
        pause = False
        wid.delete(end_score)
        wid.delete(end_rectangle)
        wid.delete(end_your_best)
        wid.delete(end_replay)
        wid.delete(end_menu)
        display_pipe_hole()
        window_game.bind("q", cheat_code)
        window_game.bind("w", cheat_code2)
        window_game.after(frame_rate, airplane_down)
        window_game.after(frame_rate, pipes)
        window_game.after(frame_rate, collision)

    def resume_after_pause():
        global score_pause
        global score
        global frame_rate
        global pipe_x
        global airplane_y
        global pause
        score -= 1
        airplane_y = 200
        pipe_x = 550
        frame_rate = 20
        pause = False
        display_pipe_hole()
        window_game.bind("q", cheat_code)
        window_game.after(frame_rate, airplane_down)
        window_game.after(frame_rate, pipes)
        window_game.after(frame_rate, collision)

    def cheat_code(event):
        global score
        global user_score
        global score_pause
        score += 5
        user_score = score
        score_pause = score

    def cheat_code2(event):
        global score
        global user_score
        global score_pause
        score += 10
        user_score = score
        score_pause = score

    def boss_key(event):
        global pause
        global pause_now
        pause_game(event)
        webbrowser.open("https://bit.ly/2YEHQIa")

    def countdown(parameter):
        global text_countdown
        global wid
        global window_game
        try:
            wid.delete(text_countdown)
        except:
            pass
        text_countdown = wid.create_text(
            275, 350, fill="#FF0000", font="Times 50 bold", text=str(parameter)
        )
        if parameter != 0:
            window_game.after(1000, lambda: countdown(parameter - 1))
        else:
            window_game.after(1000, lambda: wid.delete(text_countdown))
            window_game.after(1000, resume_game)

    def resume_game():
        global pause
        pause = False
        resume_after_pause()

    def pause_game(event):
        global pause_now
        global wid
        global pauseText1
        global pauseText2
        global pause
        if not pause_now:
            pause_now = True
            pause = True
            pauseText1 = wid.create_text(
                (280, 320), text="GAME PAUSED",
                fill="#FF0000", font="Times 50 bold"
            )
            pauseText2 = wid.create_text(
                (280, 100),
                text="*Press 'p' to resune*",
                fill="#FF0000",
                font="Times 20 italic bold",
            )
            wid.pack()
        else:
            pause_now = False
            wid.delete(pauseText1)
            wid.delete(pauseText2)
            countdown(3)

    window_game.bind("b", boss_key)
    window_game.bind("p", pause_game)
    window_game.after(frame_rate, airplane_down)
    window_game.after(frame_rate, pipes)
    window_game.after(frame_rate, collision)
    if choice == 1:
        window_game.bind("<space>", airplane_up)
    elif choice == 2:
        window_game.bind("<Up>  ", airplane_up)
    elif choice == 3:
        window_game.bind("<Button-1>", airplane_up)

    window_game.mainloop()


# Username page
def page1():
    global window_page1
    global value
    window_page1 = Tk()
    window_page1.title("Day out - Username")
    window_page1.geometry("350x200")
    window_page1.configure(background="#4E82CA")

    global username
    username = StringVar()
    username_label = Label(
        window_page1, text="Enter username here:",
        bg="#4E82CA", font="Times 20"
    ).pack()
    entry = Entry(window_page1, textvariable=username).place(x=90, y=65)
    button_ok = Button(
        window_page1,
        text="OK",
        bg="#FFFF9D",
        command=get_username,
        height="1",
        width="10",
    ).place(x=40, y=130)
    button_exit = Button(
        window_page1,
        text="Exit",
        bg="#FF4C4C",
        command=window_page1.destroy,
        height="1",
        width="10",
    ).place(x=200, y=130)

    window_page1.mainloop()


# Menu page
def page2():
    global window_page1
    global window_page2
    global window_play
    global scoreboard
    window_page2 = Tk()
    window_page2.title("Day Out")
    window_page2.geometry("550x700")
    window_page2.configure(background="#4E82CA")
    leaderboard_management()
    title_page = Label(
        window_page2, text="Day Out", bg="#4E82CA", font="Times 60 bold italic"
    ).pack()
    button_play = Button(
        window_page2,
        text="Play",
        bg="#7CFC00",
        command=lambda: [leaderboard_management(), play_game()],
        height="2",
        width="20",
    ).place(x=180, y=200)
    button_leaderboard = Button(
        window_page2,
        text="Leaderboard",
        bg="#FFFF9D",
        command=lambda: [leaderboard_management(), display_leaderboard()],
        height="2",
        width="20",
    ).place(x=180, y=300)
    button_change_user = Button(
        window_page2,
        text="Change User",
        bg="#FFFF9D",
        command=change_user,
        height="2",
        width="20",
    ).place(x=180, y=400)
    button_settings = Button(
        window_page2,
        text="Change key",
        bg="#FFFF9D",
        command=change_key,
        height="2",
        width="20",
    ).place(x=180, y=500)
    button_exit = Button(
        window_page2,
        text="Exit",
        bg="#FF4C4C",
        command=window_page2.destroy,
        height="2",
        width="20",
    ).place(x=180, y=600)
    button_info = Button(
        window_page2, text="i", bg="#FFFFFF",
        command=give_info, height="1", width="1",
    ).place(x=500, y=20)

    get_username()
    get_user_score()

    window_page1.destroy()
    window_page2.mainloop()


# Also menu page changed a little
def page2V2():
    global window_page2
    global window_play
    window_page2 = Tk()
    window_page2.title("Day Out")
    window_page2.geometry("550x700")
    window_page2.configure(background="#4E82CA")

    title_page = Label(
        window_page2, text="Day Out", bg="#4E82CA", font="Times 60 bold italic"
    ).pack()
    button_play = Button(
        window_page2,
        text="Play",
        bg="#7CFC00",
        command=play_game,
        height="2",
        width="20",
    ).place(x=180, y=200)
    button_leaderboard = Button(
        window_page2,
        text="Leaderboard",
        bg="#FFFF9D",
        command=display_leaderboard,
        height="2",
        width="20",
    ).place(x=180, y=300)
    button_change_user = Button(
        window_page2,
        text="Change User",
        bg="#FFFF9D",
        command=change_user,
        height="2",
        width="20",
    ).place(x=180, y=400)
    button_settings = Button(
        window_page2,
        text="Change key",
        bg="#FFFF9D",
        command=change_key,
        height="2",
        width="20",
    ).place(x=180, y=500)
    button_exit = Button(
        window_page2,
        text="Exit",
        bg="#FF4C4C",
        command=window_page2.destroy,
        height="2",
        width="20",
    ).place(x=180, y=600)
    button_info = Button(
        window_page2, text="i", bg="#FFFFFF",
        command=give_info, height="1", width="1",
    ).place(x=500, y=20)

    window_page2.mainloop()


# Leaderboad page
def display_leaderboard():
    global window_page2
    global window_leaderboard
    global scoreboard
    window_leaderboard = Tk()
    window_leaderboard.title("Day Out - Leaderboard")
    window_leaderboard.geometry("550x700")
    window_leaderboard.configure(background="#4E82CA")

    canvas = Canvas(window_leaderboard, bg="#4E82CA", width=450, height=550)

    Label(window_leaderboard,
          text="Leaderboard:",
          font="Times 30", bg="#4E82CA").pack()

    place = 1
    y = 0

    for x in scoreboard:
        playerX = str(place) + "." + str(x) + " : " + str(scoreboard[x])
        canvas.create_text(
            220, 50 + y, fill="#FFFFFF", font="Times 20", text=str(playerX)
        )
        y += 30
        place += 1
    canvas.pack()

    button_back = Button(
        window_leaderboard,
        text="Back",
        bg="#FF9DCE",
        command=back_fleaderboard,
        height="2",
        width="20",
    ).place(x=180, y=600)

    window_page2.destroy()
    window_leaderboard.mainloop()


# Info page
def give_info():
    global window_info
    window_info = Tk()
    window_info.geometry("550x700")
    window_info.configure(background="#4E82CA")
    window_info.title("Day Out - Info")

    Label(window_info, text="Keys", bg="#4E82CA", font="Times 30").pack()

    canvas3 = Canvas(window_info, bg="#4E82CA", width=450, height=550)
    canvas3.create_text(220, 100, fill="#FFFFFF",
                        font="Times 20",
                        text="<p> - pause")
    canvas3.create_text(
        220, 170, fill="#FFFFFF", font="Times 20", text="<b> - boss key"
    )
    canvas3.create_text(
        220,
        240,
        fill="#FFFFFF",
        font="Times 20",
        text="<q> - cheat-5 points each press",
    )
    canvas3.create_text(
        220,
        310,
        fill="#FFFFFF",
        font="Times 20",
        text="<w> - cheat-10 points each press",
    )
    canvas3.create_text(
        220,
        380,
        fill="#FFFFFF",
        font="Times 20",
        text="In end screen, <m> - back to menu",
    )
    canvas3.create_text(
        220,
        450,
        fill="#FFFFFF",
        font="Times 20",
        text="The first attempt is always fair!!",
    )
    canvas3.pack()

    button_back = Button(
        window_info,
        text="Back",
        bg="#FF9DCE",
        command=back_finfo,
        height="2",
        width="20",
    ).place(x=180, y=600)

    window_page2.destroy()
    window_info.mainloop()


def back_finfo():
    global window_info
    window_info.destroy()
    page2V2()


def back_fleaderboard():
    global window_leaderboard
    window_leaderboard.destroy()
    page2V2()


def back_fchkey():
    global window_chkey
    window_chkey.destroy()
    page2V2()


# Back to first page
def change_user():
    global window_page2
    global not_null
    not_null = False
    window_page2.destroy()
    page1()


# Change key page
def change_key():
    global window_chkey
    window_chkey = Tk()
    window_chkey.geometry("550x700")
    window_chkey.configure(background="#4E82CA")
    window_chkey.title("Day Out - Change key")

    button_Space = Button(
        window_chkey,
        text="Space",
        bg="#FFFF9D",
        command=choose_space,
        height="2",
        width="20",
    ).place(x=180, y=200)
    button_up = Button(
        window_chkey, text="Up", bg="#FFFF9D",
        command=choose_up,
        height="2", width="20"
    ).place(x=180, y=300)
    button_click = Button(
        window_chkey,
        text="Click",
        bg="#FFFF9D",
        command=choose_click,
        height="2",
        width="20",
    ).place(x=180, y=400)

    button_back = Button(
        window_chkey,
        text="Back",
        bg="#FF9DCE",
        command=back_fchkey,
        height="2",
        width="20",
    ).place(x=180, y=600)

    window_page2.destroy()
    window_chkey.mainloop()


def choose_space():
    global choice
    choice = 1


def choose_up():
    global choice
    choice = 2


def choose_click():
    global choice
    choice = 3


page1()
