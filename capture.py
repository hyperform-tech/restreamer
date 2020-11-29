# importing the required packages
import pyautogui
import cv2
import numpy as np
import subprocess as sp
import win32gui


def screenshot(window_title=None):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            image = pyautogui.screenshot(region=(x, y, x1, y1))
            return image
        else:
            print('Window not found')
    else:
        image = pyautogui.screenshot()
        return image


# Specify resolution
resolution = (1920, 1080)

# Specify video codec
codec = cv2.VideoWriter_fourcc(*"XVID")

# Specify name of Output file
filename = "Recording.avi"

# Specify frames rate. We can choose any
# value and experiment with it
fps = 30.0


# Creating a VideoWriter object
out = cv2.VideoWriter(filename, codec, fps, resolution)

command = [
    'ffmpeg',

    '-r', str(fps),

    '-i', '-',
    '-c', 'copy',
    '-f', 'rtsp',
    'rtsp://localhost:8554/mystream'
]

process = sp.Popen(command, stdin=sp.PIPE)

while True:
    # Take screenshot using PyAutoGUI
    img = screenshot(window_title="Task Manager")

    # Convert the screenshot to a numpy array
    frame = np.array(img)

    # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Green, Blue)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Write it to the output file
    # out.write(frame)

    # Optional: Display the recording screen
    # cv2.imshow('Live', frame)

    # Stop recording when we press 'q'
    # if cv2.waitKey(1) == ord('q'):
    #    break
    ret, frame = cv2.imencode('.jpg', frame)
    process.stdin.write(frame.tobytes())

# Release the Video writer
out.release()

# Destroy all windows
cv2.destroyAllWindows()
