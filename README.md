# Keylogger

Keylogger written in Python. The script can run on Linux as well as Windows.
It also works as an executable on Windows. The file can be converted into an executable using **pyinstaller**

**Note**: Make sure to include the .env file while building the exe file.

Features:
- Key strokes Capture
- Microphone Capture
- Regular Screenshot Capture throughout the capture duration
- System Information Capture

All captured data is sent over gmail automatically at the end of the capture.
All files are deleted from target machine once data is sent over mail.

Pending Fixes:
- Script does not progress until any key is pressed at the end of the capture duration.
- Windows executable also fails due to above issue.
    - If target user is typing at the end of the capture duration, no error occurs. It is only if the target user is not typing at the end of the capture duration, that the issue occurs.