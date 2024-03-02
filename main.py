# Import the required libraries
from tkinter import *
import pygame
from DoublyLinkedList import *
import time
import tkinter.ttk as ttk
import os

# Initialize Tkinter
root = Tk()
root.title(" MP3 Player")
root.geometry("600x450")
root.resizable(False, False)
# Initialize Pygame mixer
pygame.mixer.init()
window = None
# Load button images
back_btn_img = PhotoImage(file="images/back50.png")
forward_btn_img = PhotoImage(file="images/forward50.png")
play_btn_img = PhotoImage(file="images/play50.png")
pause_btn_img = PhotoImage(file="images/pause50.png")
stop_btn_img = PhotoImage(file="images/stop50.png")


# Function to create a single music entry in the playlist
def make_tale(
    frame_pa, music, row_x, la, bg="#121212", fg="#f3f3f3", leave_colo="#2a2a2a"
):
    # Function to handle mouse entering event
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
        # Change background color and appearance when mouse enters
        music_info.config(background=leave_colo)
        index_framee.config(background=leave_colo)
        index.config(text="  ▶", background=leave_colo, foreground=fg)
        music_player_subtitle.config(background=leave_colo)
        music_title.config(background=leave_colo)
        music_artist.config(background=leave_colo)
        music_time.config(background=leave_colo)
      

    # Function to handle mouse leaving event
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
        # Change background color and appearance when mouse leaves
        music_info.config(background=bg)
        index_framee.config(background=bg)
        index.config(text="", background=bg, foreground=bg)
        music_player_subtitle.config(background=bg)
        music_title.config(background=bg)
        music_artist.config(background=bg)
        music_time.config(background=bg)


    # Create frames and labels for displaying music information
    global current_song
    music_info = Frame(frame_pa, bg=bg, width=400, height=74.6)
    music_info.grid_propagate(False)
    music_info.grid(row=row_x, column=0)
    # Index frame
    index_framee = Frame(music_info, bg=bg, width=40, height=74.6)
    index_framee.propagate(False)
    index_framee.grid(row=0, column=0, padx=2, pady=10)
    index = Label(index_framee, bg=bg)
    index.config(font=("Yu Gothic UI Semibold", 20))
    index.pack()
    # Index frame
    music_player_subtitle = Frame(music_info, bg=bg, width=200, height=74.6)
    music_player_subtitle.grid_propagate(False)
    music_player_subtitle.grid(row=0, column=1, padx=0, pady=10)
    # Music title label
    music_title = Label(music_player_subtitle, text=f"{music.data.title}", fg=fg, bg=bg)
    music_title.config(font=("Lobster", 15))
    music_title.grid(row=0, column=0, padx=5, pady=0)
    # Music artist label
    music_artist = Label(music_player_subtitle, text=music.data.artist, fg=fg, bg=bg)
    music_artist.config(font=("Lobster", 11))
    music_artist.grid(row=1, column=0, padx=5, sticky="w")
    # Music duration label
    music_time = Label(
        music_info,
        text=time.strftime("%M:%S", time.gmtime(music.data.duration)),
        fg="white",
        bg=bg,
        height=1,
    )
    music_time.config(font=("AG_Souvenir Bold Italic", 10))
    music_time.grid(row=0, column=2, pady=(10, 0))
    # Check if the current song is being displayed and update its appearance accordingly
    if music is current_song:
        music_info.config(background=leave_colo)
        index_framee.config(background=leave_colo)
        index.config(text="  ", background=leave_colo, foreground=fg)
        music_player_subtitle.config(background=leave_colo)
        music_title.config(background=leave_colo)
        music_artist.config(background=leave_colo)
        music_time.config(background=leave_colo)
        return

    # Add button for each music entry

    index.bind("<Button-1>", lambda event, music=music: play(event, music))
 

        

    # Bind events for mouse entering and leaving
    
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
        lambda event, music_info=music_info, index_framee=index_framee, index=index, music_player_subtitle=music_player_subtitle, music_title=music_title, music_artist=music_artist, music_time=music_time : on_leave(
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


# Function to create and populate the playlist
def cre_listsong(list_s, frame_pa, la):
    current_song_info = list_s.head
    row_x = 0

    while current_song_info:
        make_tale(frame_pa, current_song_info, row_x, la)
        row_x += 1
        if current_song_info is list_s.tail:
            break
        current_song_info = current_song_info.next


# Function to clear all frames in a master frame
def clear_frames(master_frame):

    for widget in master_frame.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()


# Function to change song to next song
def change(song):
    global current_song
    global playlist
    clear_frames(interior)
    playlist.changenode(current_song, song)
    cre_listsong(playlist, interior, True)


# Function to add a song to next song the playlist
def add_song(event, song):
    global current_song
    global playlist
    global interior
    playlist.addAfter(current_song, song.data.path)
    clear_frames(interior)
    cre_listsong(playlist, interior, True)


# Function to delete a song from the playlist
def del_song(event, song):
    global current_song
    global playlist

    if song is current_song:
        next_song()
    playlist.delete(song)
    clear_frames(interior)
    cre_listsong(playlist, interior, True)


# Function to play a song


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
        cre_listsong(playlist, interior, True)
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


# Function to display the current time and update the slider
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


# Function to play the next song in the playlist
def next_song():
    time_start.config(text="00:00")
    my_slider.config(value=0)
    global current_song
    if not current_song.next:
        current_song = playlist.head
    else:
        current_song = current_song.next
    play_button.config(image=pause_btn_img)
    pygame.mixer.music.load(current_song.data.path)
    pygame.mixer.music.play(loops=0)
    cre_listsong(playlist, interior, True)
    play_time()


# Function to play the previous song in the playlist
def prev_song():
    global current_song
    if not current_song.prev:
        current_song = playlist.tail
    else:
        current_song = current_song.prev
    time_start.config(text="00:00")
    my_slider.config(value=0)
    pygame.mixer.music.load(current_song.data.path)
    pygame.mixer.music.play(loops=0)
    cre_listsong(playlist, interior, True)


# Function to handle slider movement
def slide(x):
    global current_song
    global paused
    pygame.mixer.music.load(current_song.data.path)
    if not paused:
        pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
    else:
        pygame.mixer.music.pause()

# Create a linked list to hold the playlist
listsong = DoublyLinkedList()
for file in os.listdir("Music"):
    full_path = os.path.join("Music", file)
    _, file_extension = os.path.splitext(full_path)
    if os.path.isfile(full_path) and file_extension == ".mp3":
        listsong.addToTail(full_path)


# Create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)
# Create frame to hold the song box
song_box = Frame(master_frame, bg="red", width=335, height=274)
song_box.grid_propagate(False)
song_box.grid(row=0, column=0)
# Create canvas and scrollbar for scrolling through the playlist
canvas = Canvas(song_box)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar = Scrollbar(song_box, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
# Create interior frame to hold the playlist items
interior = Frame(canvas)
interior_id = canvas.create_window((0, 0), window=interior, anchor=NW)


# Function to adjust canvas size
def configure_interior(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=335, height=274)


# Function to adjust canvas size on configuration change
def on_canvas_configure(event):
    canvas.itemconfig(interior_id, width=event.width)


canvas.bind("<Configure>", on_canvas_configure)
interior.bind("<Configure>", configure_interior)
# Create a copy of the playlist
playlist = listsong.copy()
# Set the current song to the first song in the playlist
current_song = playlist.head
# Create the list of songs in the GUI
cre_listsong(playlist, interior, True)

# Frame for displaying the current time and song duration
time_frame = Frame(master_frame)
time_frame.grid(row=1, column=0, pady=10)
# Label for displaying current time
time_start = Label(time_frame, text="00:00", bd=1, relief=GROOVE, anchor=E)
time_start.grid(row=0, column=0, padx=10, pady=10)
# Slider for changing playback position
my_slider = ttk.Scale(
    time_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360
)
my_slider.grid(row=0, column=1, padx=10)
my_slider.bind("<ButtonRelease-1>", slide)
# Label for displaying song duration
time_lenght = Label(time_frame, text="00:00", bd=1, relief=GROOVE, anchor=E)
time_lenght.grid(row=0, column=2, padx=10)

# Frame for playback controls
controls_frame = Frame(master_frame)
controls_frame.grid(row=2, column=0)
# Frame for volume control
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=30)
window_interior_id = None
# Function to open the list of songs window


# Buttons for playback control
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


def volume_(vol):
    volume = float(vol) / 100
    pygame.mixer.music.set_volume(volume)


# Slider for volume control
volume_slider = ttk.Scale(
    volume_frame, from_=100, to=0, orient=VERTICAL, length=120, command=volume_
)
volume_slider.set(30)
volume_slider.pack(pady=10)


# Start the GUI event loop
root.mainloop()