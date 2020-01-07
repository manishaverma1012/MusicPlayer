import os
import threading
import time
import tkinter.messagebox
from tkinter import *
import tkinter as tk
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as thk

from mutagen.mp3 import MP3
from pygame import mixer

screen = tk.Tk()

mixer.init()

screen.geometry("400x450")
screen.configure(background='turquoise')

screen.title("Acoustic") 
mylabel = tk.Label(screen,text="Rock n Roll!",font='Helvetica 60 bold',fg="blue",bg="turquoise")
mylabel.pack()



def Play_click():
	mixer.music.load("saki.mp3")
	mixer.music.play()


def stop_click():
	mixer.music.stop()


def set_vol(value):
	volume = int(value)/100
	mixer.music.set_volume(volume)






play_image = PhotoImage(file='play.png')
play_button= Button(screen,image = play_image ,command=Play_click)
play_button.pack()

stop_image = PhotoImage(file='stop.png')
stop_button = Button(screen,image = stop_image ,command=stop_click)
stop_button.pack()

scale = scale(screen,from_= 0, to=100, orient= HORIZONTAL,command = set_vol)
scale.set(70)
scale.pack()

	


#screen.iconbitmap('Home/Manisha/Project/Music-Player/acoustic.ico')
screen.mainloop()