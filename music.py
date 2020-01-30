import os
import threading
import time
import tkinter.messagebox
from tkinter import *
import tkinter as tk
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer

screen = tk.ThemedTk()
screen.get_themes()                 
screen.set_theme("radiance")


statusbar = ttk.Label(screen,text="Enjoy The Beats!",font='Times 50 italic', relief=SUNKEN ,anchor=W)
statusbar.pack(side=BOTTOM,fill=X)




#to set the  menubar 
toolbar = Menu(screen)
screen.config(menu=toolbar)
subMenu = Menu(toolbar,tearoff=0)
playlist =[]



def browse_file():
	global filename_path
	filename_path = filedialog.askopenfilename()
	add_to_playlist(filename_path)

	mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


toolbar.add_cascade(label="Playlist",menu=subMenu)
subMenu.add_command(label="Open",command=browse_file)
subMenu.add_command(label="Exit",command = screen.destroy)



def about_us():
	tkinter.messagebox.showinfo("About Acoustic","This is music  player,you can use it very comfortably")


subMenu = Menu(toolbar,tearoff=0)
toolbar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us",command = about_us)


mixer.init()  #intialize the mixer
#work on the main screen
screen.geometry("400x450")
screen.configure(background='turquoise')

screen.title("Acoustic") 
mylabel = Label(screen,text="Rock n Roll!",font='Helvetica 60 bold',fg="blue",bg="turquoise")
mylabel.pack()


leftframe = Frame(screen)
leftframe.pack(side=LEFT, padx=50, pady=50)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(screen)
rightframe.pack(pady=50)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()    


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1



def play_click():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_click()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Acoustic could not find the file. Please check again.')



def stop_click():
	mixer.music.stop()
	statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_click():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_click():
    play_click()
    statusbar['text'] = "Music Rewinded"


def set_vol(value):
	volume = float(value)/100
	mixer.music.set_volume(volume)


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volume_button.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volume_button.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE



middleframe = Frame(rightframe)
middleframe.pack(pady=50, padx=50)      



play_image = PhotoImage(file='play.png')
play_button= ttk.Button(middleframe,image = play_image ,command=play_click)
play_button.grid(row=0, column=0, padx=10)

stop_image = PhotoImage(file='stop.png')
stop_button = Button(middleframe,image = stop_image ,command=stop_click)
stop_button.grid(row=0, column=1, padx=10)


pause_image = PhotoImage(file='pause.png')
pause_button = ttk.Button(middleframe, image=pause_image, command=pause_click)
pause_button.grid(row=0, column=2, padx=10)


bottomframe = Frame(rightframe)
bottomframe.pack()

rewind_image = PhotoImage(file='rewind.png')
rewind_button = ttk.Button(bottomframe, image=rewind_image, command=rewind_click)
rewind_button.grid(row=0, column=0,padx=10)

mute_image = PhotoImage(file='mute.png')
volume_image = PhotoImage(file='volume.png')
volume_button = ttk.Button(bottomframe, image=volume_image, command=mute_music)
volume_button.grid(row=0, column=1,padx=10)



scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)







def on_closing():
    stop_click()
    screen.destroy()
	

screen.protocol("WM_DELETE_WINDOW", on_closing)
screen.mainloop()