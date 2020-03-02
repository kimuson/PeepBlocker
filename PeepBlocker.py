#!/usr/bin/env python
# -*- coding: utf8 -*-
import tkinter
import tkinter.filedialog
from tkinter import messagebox
import threading
import cv2
import sys, os
import numpy as np
import datetime

#テストの際はコメントを外す
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#fpath='path.txt'

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
fpath = 'path.txt'
path =""

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
path=data1
ext='jpg'
os.makedirs(path, exist_ok=True)

root = tkinter.Tk()
root.title(u" ")
root.attributes("-topmost", True)
root.geometry("150x300")

flg = "off"
dispflg = "off"
closing_main_flg = "off"

text1 = tkinter.StringVar()
text1.set("Stopped")

buttontext = tkinter.StringVar()
buttontext.set("開始")

newWindow = None

def on_closing():
    global newWindow
    global dispflg
    newWindow.destroy()
    dispflg = "off"
    flg = "on"
    changeText()
    
def runRecgnition():
    while(True):
        global newWindow
        global dispflg
        global flg
        global closing_main_flg
        if flg == "on" and dispflg == "off" or closing_main_flg == "on":
            cap = cv2.VideoCapture(0)
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            '''
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                    cv2.imshow('img', img)
                    print('検出された人数: {}'.format(len(faces)))
            '''

            if len(faces) > 1:
                if dispflg == "off":
                    print("テスト２")
                    cv2.imwrite('{}/{}.{}'.format(path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext), img)
                    print('{}_{}.{}'.format(path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext))
                    newWindow = tkinter.Toplevel(root)
                    newWindow.attributes("-topmost", True)
                    newWindow.configure(bg="black")
                    newWindow.title("注意：画面が覗き込まれています")
                    tyuimongon = tkinter.Label(newWindow,font = ("",30),text='覗き込まれている可能性があります')
                    tyuimongon.pack(padx=10,pady=5)
                    btn = tkinter.Button(newWindow, text='閉じる',width=10,command=on_closing)
                    btn.pack(padx=2,pady=2)
                    w, h = newWindow.winfo_screenwidth(), newWindow.winfo_screenheight()
                    newWindow.geometry("%dx%d+0+0" % (w, h))
                    newWindow.protocol("WM_DELETE_WINDOW", on_closing)
                    dispflg = "on"
                    

        if flg == "off" and closing_main_flg == "on":
            dispflg = "off"
            break
        
        if flg == "off" and closing_main_flg == "off":
            newWindow.destroy()
            dispflg = "off"
            break

def changeText():
    global flg
    if (flg == "off"):
        text1.set("Runnig")
        buttontext.set("停止")
        flg = "on"
        print("テスト1")
        thread1 = threading.Thread(target=runRecgnition)
        thread1.start()
        
    else:
        text1.set("Stopped")
        buttontext.set("再開")
        flg = "off"

#フレーム配置
frame = tkinter.Frame(root,relief="ridge",bd=3)
frame.pack(padx=10,pady=10)

#ラベル2
label2 = tkinter.Label(frame,font = ("",15),text='PeepBlocker') #ラベルを生成する。
label2.pack(padx=10,pady=5) #ウインドウにラベルを配置する。

# ラベル
lbl_2 = tkinter.Label(root, text='■ 監視起動状態 ■')
lbl_2.pack()

#ボタン
lbl_1 = tkinter.Label(root,textvariable=text1)
lbl_1.pack()

Button = tkinter.Button(root,textvariable=buttontext, width=10,command=changeText)
Button.pack(padx=5,pady=5)

# clickイベント
def btn_click():
    global path
    root_test=tkinter.Tk()
    root_test.withdraw()
    iDir = os.path.abspath(os.path.dirname(__file__))
    path = tkinter.filedialog.askdirectory(initialdir = iDir)

    if len(path) > 0:
        path_w = 'path.txt'
        with open(path_w, mode='w') as f:
            f.write(path)
            messagebox.showinfo('Info', '保存先の設定が完了しました\n保存先：'+path)
    
# ラベル
lbl_2 = tkinter.Label(root, text='■ 画像の保存先設定 ■')
lbl_2.pack()

# ボタン作成
btn = tkinter.Button(root, text='設定する',width=10,command=btn_click)

# 配置
btn.pack(padx=2,pady=2)

def closing_main():
    global flg
    global closing_main_flg
    flg = "off"
    closing_main_flg = "on"
    root.destroy()
    sys.exit()
    print("成功")

root.protocol("WM_DELETE_WINDOW", closing_main)
root.mainloop()
