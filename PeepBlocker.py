#!/usr/bin/env python
# -*- coding: utf8 -*-
import tkinter
import tkinter.filedialog
from tkinter import messagebox
import threading
import cv2
import sys
import os
import numpy as np
import datetime

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
fpath = 'path.txt'
path = ""

# Check for the existence of a configuration file
if not os.path.exists(fpath):
    textdata = "/usr/local/"
    writed = open('path.txt', 'w')
    writed.write(textdata)
    writed.close()

if os.path.getsize(fpath) == 0:
    textdata = "/usr/local/"
    writed = open('path.txt', 'w')
    writed.write(textdata)
    writed.close()

f = open(fpath)
data1 = f.read()
f.close()
path = data1
ext = 'jpg'
os.makedirs(path, exist_ok=True)


# ------------------------------------------------------------------
# Processing when the close button on the warning screen is pressed
# ------------------------------------------------------------------


def on_closing():
    global warningScreen
    global warningScreenDispFlg
    global startUpFlg
    warningScreen.destroy()
    warningScreenDispFlg = "off"
    startUpFlg = "on"
    changeText()


# ------------------------------------------------------------------
# Peep detection
# ------------------------------------------------------------------


def runRecgnition():
    while(True):
        global warningScreen
        global warningScreenDispFlg
        global startUpFlg
        global shutdownFlg
        if startUpFlg == "on" and warningScreenDispFlg == "off" or shutdownFlg == "on":
            cap = cv2.VideoCapture(0)
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 1:
                if warningScreenDispFlg == "off":

                    # Save detection results
                    cv2.imwrite(
                        '{}/{}.{}'.format(path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext), img)

                    # Display warning screen
                    warningScreen = tkinter.Toplevel(root)
                    warningScreen.attributes("-topmost", True)
                    warningScreen.configure(bg="black")
                    warningScreen.title("Caution：Being secretly peeped")
                    tyuimongon = tkinter.Label(
                        warningScreen, font=("", 30), text='Caution：Being secretly peeped')
                    tyuimongon.pack(padx=10, pady=5)
                    btn = tkinter.Button(
                        warningScreen, text='close', width=10, command=on_closing)
                    btn.pack(padx=2, pady=2)
                    w, h = warningScreen.winfo_screenwidth(), warningScreen.winfo_screenheight()
                    warningScreen.geometry("%dx%d+0+0" % (w, h))
                    warningScreen.protocol("WM_DELETE_WINDOW", on_closing)
                    warningScreenDispFlg = "on"

        if startUpFlg == "off" and shutdownFlg == "on":
            warningScreenDispFlg = "off"
            break

        if startUpFlg == "off" and shutdownFlg == "off":
            warningScreen.destroy()
            warningScreenDispFlg = "off"
            break


# ------------------------------------------------------------------
# Start status change processing
# ------------------------------------------------------------------


def changeText():
    global startUpFlg
    if (startUpFlg == "off"):
        statusText.set("Runnig")
        startButtonText.set("Stop")
        startUpFlg = "on"
        thread1 = threading.Thread(target=runRecgnition)
        thread1.start()

    else:
        statusText.set("Stopped")
        startButtonText.set("Run")
        startUpFlg = "off"

# ------------------------------------------------------------------
# set SavePath
# ------------------------------------------------------------------


def setSavePath():
    global path
    root_test = tkinter.Tk()
    root_test.withdraw()
    iDir = os.path.abspath(os.path.dirname(__file__))
    path = tkinter.filedialog.askdirectory(initialdir=iDir)

    if len(path) > 0:
        path_w = 'path.txt'
        with open(path_w, mode='w') as f:
            f.write(path)
            messagebox.showinfo(
                'Info', 'Save destination setting completed\nDestination：'+path)

# ------------------------------------------------------------------
# Shutdown processing
# ------------------------------------------------------------------


def shutdown():
    global startUpFlg
    global shutdownFlg
    startUpFlg = "off"
    shutdownFlg = "on"
    root.destroy()
    sys.exit()


# ------------------------------------------------------------------
# GUI parts
# ------------------------------------------------------------------

# base GUI parts
root = tkinter.Tk()
root.title(u" ")
root.attributes("-topmost", True)
root.geometry("180x300")
statusText = tkinter.StringVar()
statusText.set("Stopped")
startButtonText = tkinter.StringVar()
startButtonText.set("開始")
warningScreen = None

# Initialize flags
startUpFlg = "off"
warningScreenDispFlg = "off"
shutdownFlg = "off"


# GUI parts: Title
frame = tkinter.Frame(root, relief="ridge", bd=3)
frame.pack(padx=10, pady=10)

titleLabel = tkinter.Label(frame, font=("", 15), text='PeepBlocker')
titleLabel.pack(padx=10, pady=5)

# GUI parts: SubTitle
subTitleLabel1 = tkinter.Label(root, text='■ Monitoring Status ■')
subTitleLabel1.pack()

# GUI parts: statusLabel1
statusLabel = tkinter.Label(root, textvariable=statusText)
statusLabel.pack()

# GUI parts: startButton
startButton = tkinter.Button(root, textvariable=startButtonText,
                             width=10, command=changeText)
startButton.pack(padx=5, pady=5)

# GUI parts: subTitleLabel2
subTitleLabel2 = tkinter.Label(root, text='■ Set save destination ■')
subTitleLabel2.pack()

# GUI parts: setSavePathButton
setSavePathButton = tkinter.Button(
    root, text='Set', width=10, command=setSavePath)
setSavePathButton.pack(padx=2, pady=2)

root.protocol("WM_DELETE_WINDOW", shutdown)
root.mainloop()
