#Import the required libraries
from tkinter import *
import pygame
from DoublyLinkedList import *
import time
import tkinter.ttk as ttk
import os

#Create the root window
root = Tk()
pygame.mixer.init()

window = None

#Readimages
back_btn_img = PhotoImage(file="images/back50.png")
forward_btn_img = PhotoImage(file="images/forward50.png")
play_btn_img = PhotoImage(file="images/play50.png")
pause_btn_img = PhotoImage(file="images/pause50.png")
stop_btn_img = PhotoImage(file="images/stop50.png")



def make_table(frame_pa, music, bg, fg, leave_colo, row_x):
    #Function to create a table with the song's information
    def on_enter(
        event,
        music_info,
        index_framee,
        index,
        music_player_subtitle,
        music_title,
        music_artist,
        music_time,
    ):
        music_info.config(background=leave_colo)
        index_framee.config(background=leave_colo)
        index.config(text="  ▶", background=leave_colo, foreground=fg)
        music_player_subtitle.config(background=leave_colo)
        music_title.config(background=leave_colo)
        music_artist.config(background=leave_colo)
        music_time.config(background=leave_colo)
        
    #Function to change the color of the table when the mouse leaves
    def on_leave(
        event,
        music_info,
        index_framee,
        index,
        music_player_subtitle,
        music_title,
        music_artist,
        music_time,
    ):
        music_info.config(background=bg)
        index_framee.config(background=bg)
        index.config(text="", background=bg, foreground=bg)
        music_player_subtitle.config(background=bg)
        music_title.config(background=bg)
        music_artist.config(background=bg)
        music_time.config(background=bg)

    music_info = Frame(frame_pa, bg=bg, width=400, height=74.6)
    music_info.grid_propagate(False)
    music_info.grid(row=row_x, column=0)

    index_framee = Frame(music_info, bg=bg, width=40, height=74.6)
    index_framee.propagate(False)
    index_framee.grid(row=0, column=0, padx=2, pady=10)
    index = Label(index_framee, bg=bg)
    index.config(font=("Yu Gothic UI Semibold", 20))
    index.pack()

    music_player_subtitle = Frame(music_info, bg=bg, width=200, height=74.6)
    music_player_subtitle.grid_propagate(False)
    music_player_subtitle.grid(row=0, column=1, padx=0, pady=10)

    music_title = Label(music_player_subtitle, text=f"{music.data.title}", fg=fg, bg=bg)
    music_title.config(font=("Lobster", 15))
    music_title.grid(row=0, column=0, padx=5, pady=0)

    music_artist = Label(music_player_subtitle, text=music.data.artist, fg=fg, bg=bg)
    music_artist.config(font=("Lobster", 11))
    music_artist.grid(row=1, column=0, padx=5, sticky="w")

    music_time = Label(
        music_info,
        text=time.strftime("%M:%S", time.gmtime(music.data.duration)),
        fg="white",
        bg=bg,
        height=1,
    )
    music_time.config(font=("AG_Souvenir Bold Italic", 10))
    music_time.grid(row=0, column=2, pady=(10, 0))

    index.bind(
        "<Button-1>",
        lambda event, current_song_info=music: play(event, current_song_info),
    )

    music_info.bind(
        "<Enter>",
        lambda event, music_info=music_info, index_framee=index_framee, index=index, music_player_subtitle=music_player_subtitle, music_title=music_title, music_artist=music_artist, music_time=music_time: on_enter(
            event,
            music_info,
            index_framee,
            index,
            music_player_subtitle,
            music_title,
            music_artist,
            music_time,
        ),
    )
    music_info.bind(
        "<Leave>",
        lambda event, music_info=music_info, index_framee=index_framee, index=index, music_player_subtitle=music_player_subtitle, music_title=music_title, music_artist=music_artist, music_time=music_time: on_leave(
            event,
            music_info,
            index_framee,
            index,
            music_player_subtitle,
            music_title,
            music_artist,
            music_time,
        ),
    )

#Function to play the song
def play(event=None, now=None):
    global paused
    global current_song
    if now:
        current_song = now
        pygame.mixer.music.load(current_song.data.path)
        pygame.mixer.music.play(loops=0)
        time_start.config(text="00:00")
        my_slider.config(value=0)

        time_start.config(text="00:00")
        my_slider.config(value=0)

        play_button.config(image=pause_btn_img)
        paused = False
        play_time()
        return

    try:
        paused
    except NameError:
        pygame.mixer.music.load(current_song.data.path)
        pygame.mixer.music.play(loops=0)

        play_button.config(image=pause_btn_img)
        paused = False
        play_time()
        return
    else:
        if paused:
            pygame.mixer.music.unpause()
            paused = False
            play_button.config(image=pause_btn_img)
            play_time()
        else:
            pygame.mixer.music.pause()
            play_button.config(image=play_btn_img)
            play_time()
            paused = True

#Function to update the real time playing of the song
def play_time():
    global current_song
    global paused
    current_time = pygame.mixer.music.get_pos() / 1000
    if current_time < 0:
        next_song()
    converted_song_length = time.strftime(
        "%M:%S", time.gmtime(current_song.data.duration)
    )
    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))
    current_time += 1

    if int(my_slider.get()) == int(current_song.data.duration):
        time_start.config(text=f"{converted_current_time}")
        time_lenght.config(text=f"{converted_song_length}")
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        slider_position = int(current_song.data.duration)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(current_song.data.duration)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime(
            "%M:%S", time.gmtime(int(my_slider.get()))
        )
        time_start.config(text=f"{converted_current_time}")
        time_lenght.config(text=f"{converted_song_length}")
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    time_start.after(1000, play_time)

#Function to play the next song
def next_song():
    time_start.config(text="00:00")
    my_slider.config(value=0)
    global current_song
    if not current_song.next:
        current_song = playlist.head
    else:
        current_song = current_song.next
    pygame.mixer.music.load(current_song.data.path)
    pygame.mixer.music.play(loops=0)

#Function to play the previous song
def prev_song():
    global current_song
    if not current_song.prev:
        current_song = listsong.tail
    else:
        current_song = current_song.prev
    time_start.config(text="00:00")
    my_slider.config(value=0)
    pygame.mixer.music.load(current_song.data.path)
    pygame.mixer.music.play(loops=0)

#Function to slide the song
def slide(x):
    global current_song
    global paused
    pygame.mixer.music.load(current_song.data.path)
    if not paused:
        pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
    else:
        pygame.mixer.music.pause()


gray = "#121212"
fg_str = "#f3f3f3"
leave_colo = "#2a2a2a"

#To show the songs in the list
def cr(lit, frame_pa, bg, fg_str, leave_colo, canvas=None, scrollbar=None):
    current_song_info = lit.head
    row_x = 0
    while current_song_info:
        make_table(frame_pa, current_song_info, bg, fg_str, leave_colo, row_x)
        row_x += 1
        current_song_info = current_song_info.next

    if canvas and scrollbar:
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=canvas.yview)

#Create the list of songs
listsong = DoublyLinkedList()
for file in os.listdir("Music"):
    full_path = os.path.join("Music", file)
    _, file_extension = os.path.splitext(full_path)
    if os.path.isfile(full_path) and file_extension == ".mp3":
        listsong.addToTail(full_path)

playlist = listsong.copy()
current_song = playlist.head

#Create the root window
root.title(" MP3 Player")
root.geometry("600x450")
root.resizable(False, False)

master_frame = Frame(root)
master_frame.pack(pady=20)

song_box = Frame(master_frame, bg="red", width=335, height=274)
song_box.grid_propagate(False)
song_box.grid(row=0, column=0)

canvas = Canvas(song_box)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(song_box, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

interior = Frame(canvas)
interior_id = canvas.create_window((0, 0), window=interior, anchor=NW)

cr(playlist, interior, gray, fg_str, leave_colo, canvas, scrollbar)

time_frame = Frame(master_frame)
time_frame.grid(row=1, column=0, pady=10)

time_start = Label(time_frame, text="00:00", bd=1, relief=GROOVE, anchor=E)
time_start.grid(row=0, column=0, padx=10, pady=10)

my_slider = ttk.Scale(
    time_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360
)
my_slider.grid(row=0, column=1, padx=10)
my_slider.bind("<ButtonRelease-1>", slide)

time_lenght = Label(time_frame, text="00:00", bd=1, relief=GROOVE, anchor=E)
time_lenght.grid(row=0, column=3, padx=10)

controls_frame = Frame(master_frame)
controls_frame.grid(row=2, column=0)

volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=30)

#Create the buttons
def open_window():
    global window
    if window and window.winfo_exists():
        window.deiconify()
    else:
        window = Toplevel(root)
        window.title("List Song")
        gray = "#121212"
        fg_str = "#f3f3f3"
        leave_colo = "#2a2a2a"
        cr(listsong, window, gray, fg_str, leave_colo)
        window.resizable(False, False)


back_button = Button(
    controls_frame, image=back_btn_img, borderwidth=0, command=prev_song
)
forward_button = Button(
    controls_frame, image=forward_btn_img, borderwidth=0, command=next_song
)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=2, padx=10)
play_button.grid(row=0, column=1, padx=10)

#Create the volume slider
def volume_(vol):
    volume = float(vol) / 100
    pygame.mixer.music.set_volume(volume)


volume_slider = ttk.Scale(
    volume_frame, from_=100, to=0, orient=VERTICAL, length=120, command=volume_
)
volume_slider.set(30)
volume_slider.pack(pady=10)

root.mainloop()