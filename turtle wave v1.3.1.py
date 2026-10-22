import turtle as tr
import tkinter as tk
import random
import pygame as pg
import json
import os
import sys
from time import perf_counter
from datetime import datetime

highscore = 0
if getattr(sys, "_MEIPASS", None):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
savefile = os.path.join(base_dir, "scores.json")
scores = []
timer_id = None
pg.mixer.init()
bgmlist = ["Phobos.mp3", "The Prototype.mp3", "Nuke Powder.mp3"]

root = tk.Tk()

def load_data():
    global highscore
    global scores
    if not os.path.exists(savefile):
        highscore = 0
        return
    try:
        with open(savefile, "r") as file:
            scores = json.load(file)
            if not scores:
                highscore = 0
                return
            highscore = scores[0]["score"]
    except (json.JSONDecodeError, KeyError, IndexError):
        highscore = 0
        return

load_data()

stat = tk.Label(root, text="0", font=("Arial", 20))
hsl = tk.Label(root, text="High Score: {}".format(highscore), font=("Arial", 20))
cps = tk.Label(root, text="NA", font=("Arial", 20))
colrr = tk.Label(root, text="Invalid Color, Loser!", font=("Arial", 35), fg="red")
colrrdes = tk.Label(root, text="Please stop being a delulu and think of colors\nthat doesnt exist(or at least in python)to continue playing\n(nullscapes cbf blocker ahh error message)", font=("Arial", 11), fg="red")

def save(score):
    global scores
    global highscore
    entry = {
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    scores.append(entry)
    scores.sort(key=lambda x: x["score"], reverse=True)
    top_scores = scores[:100]
    with open(savefile, "w") as file:
        json.dump(top_scores, file, indent=4)
    print("DEBUG: SCORES SAVED")

def game(icon, colour, bgm):
    global timer_id
    bgmi=pg.mixer.Sound(bgm)
    di=pg.mixer.Sound(r"audios\\death.mp3")
    channel = bgmi.play()

    begintime=perf_counter()
    def on_close():
        global timer_id
        print("DEBUG: PLAYER HAVE A SKILL ISSUE")
        channel.stop()

        if timer_id is not None:
            try:
                screen.getcanvas().after_cancel(timer_id)
            except Exception:
                pass
        try:
            tr.bye()
        except Exception:
            pass

    seconds = 0
    screen = tr.Screen()
    space_pressed = False
    gameover = False
    screen.tracer(5)
    screen.setup(width=600, height=600)
    t = tr.Turtle()
    tra = tr.Turtle()
    s1 = tr.Turtle()
    s2 = tr.Turtle()
    t.speed(0)
    tra.speed(0)
    size = 200
    s1y = size - 50
    s2y = -size + 50

    def up():
        nonlocal space_pressed
        space_pressed = True
    def down():
        nonlocal space_pressed
        space_pressed = False

    def move():
        global highscore, timer_id
        nonlocal s1y, s2y
        nonlocal seconds
        nonlocal gameover

        try:
            x, y = t.position()
        except (tr.Terminator, tk.TclError):
            return

        if gameover:
            return

        def centerv():
            try:
                screen.setworldcoordinates(x - size, -size, x + size, size)
            except (tr.Terminator, tk.TclError):
                pass

        if space_pressed:
            t.setheading(45)
            tra.setheading(45)
            if y >= size:
                t.sety(size)
                tra.sety(size)
                t.setheading(0)
                tra.setheading(0)
        else:
            handled = False
            if y <= -size:
                t.sety(-size)
                tra.sety(-size)
                t.setheading(0)
                tra.setheading(0)
                handled = True
            if not handled:
                t.setheading(315)
                tra.setheading(315)

        t.forward(5)
        tra.forward(5)
        s1.setx(x)
        s2.setx(x)
        centerv()

        t.shape(icon)
        t.color(colour, colour)
        t.pensize(7)
        tra.shape(icon)
        tra.color("white", colour)
        tra.pensize(3)
        s1.shape("triangle")
        s2.shape("triangle")
        s1.setheading(270)
        s2.setheading(90)
        s1.sety(s1y)
        s2.sety(s2y)
        s1y -= .1
        s2y += .1
        s1.pu()
        s2.pu()

        if not gameover:
            try:
                timer_id = screen.getcanvas().after(10, move)
            except (tr.Terminator, tk.TclError):
                return

        try:
            endtime=perf_counter()
            seconds=endtime-begintime
            stat.config(text=str(round(seconds, 2)))
            if highscore > 0:
                hsl.config(text="High Score: {}".format(highscore))
            else:
                hsl.config(text="High Score: 0")

            if t.distance(s1) <= 20 or t.distance(s2) <= 20:
                t.hideturtle()
                tra.hideturtle()
                t.clear()
                save(seconds)
                highscore = max(highscore, seconds)
                hsl.config(text="High Score: {}".format(highscore))
                gameover = True
            screen.update()
        except (tr.Terminator, tk.TclError):
            pass

    screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", on_close)
    screen.listen()
    screen.onkeypress(up, "space")
    screen.onkeyrelease(down, "space")
    move()
    try:
        screen.mainloop()
    except (tr.Terminator, tk.TclError):
        pass

def launch(icon, colour):
    def randomBGM():
        return r"audios\\{}".format(random.choice(bgmlist))
    def randomCol():
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return "#{:02X}{:02X}{:02X}".format(red, green, blue)
    launched = tk.Label(root, text="Game Launched!", font=("Arial", 40))
    sub = tk.Label(root, text="Time survived", font=("Arial", 15))
    tit.pack_forget()
    des.pack_forget()
    ins.pack_forget()
    option_menu.pack_forget()
    col.pack_forget()
    coldes.pack_forget()
    lb.pack_forget()
    try:
        if colour == "":
            launched.pack()
            sub.pack()
            stat.pack()
            cps.pack()
            hsl.pack()
            game(icon, randomCol(), randomBGM())
        else:
            launched.pack()
            sub.pack()
            stat.pack()
            cps.pack()
            hsl.pack()
            game(icon, colour, randomBGM())
    except tr.TurtleGraphicsError as e:
        if "bad color string" in str(e):
            colrr.pack()
            colrrdes.pack()
            try:
                tr.bye()
            except Exception:
                pass
            launched.pack_forget()
            sub.pack_forget()
            stat.pack_forget()
            cps.pack_forget()
            hsl.pack_forget()

titleso = ["turtle", "arrow", "triangle", "circle", "square"]
root.geometry("500x200")
root.title("GD wave on turtle graphics")
tit = tk.Label(root, text="GD wave on turtle graphics launcher", font=("Arial", 20))
des = tk.Label(root, text="The wave gamemode from geometry dash on turtle graphics by FullYellow", font=("Arial", 11))
ins = tk.Label(root, text="Click s to start,use space to control the wave,select icon below", font=("Arial", 11))
selected = tk.StringVar(value=titleso[0])
option_menu = tk.OptionMenu(root, selected, *titleso)
coldes = tk.Label(root, text="Color here (if left empty a random color will be used)", font=("Arial", 10))
col = tk.Entry(root, font=("Arial", 10))
lb = tk.Button(root, text="Launch", font=("Arial", 30), bg="red", command=lambda: launch(selected.get(), col.get()))

tit.pack()
des.pack()
ins.pack()
option_menu.pack()
coldes.pack()
col.pack()
lb.pack()
root.mainloop()
