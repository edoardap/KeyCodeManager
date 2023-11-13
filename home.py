import cv2
import numpy as np
from pyzbar.pyzbar import decode
import keyboard

from flask import Flask, render_template, request
app=Flask(__name__,template_folder='Templates')

@app.route("/", methods = ["GET", "POST"])
def login():
    nome = ''
    senha = ''
    if request.method == "GET":
        return render_template('login/index.html')
    else:
        nome = request.form.get("email")
        senha = request.form.get("senha")
        if(nome == 'maria' and senha == '123'):
            return render_template('home.html')
        else:
            return '<h1> BURRO </h1>'

# @app.route("/PaginaInicial")
# def PaginaInicial():
#     return render_template('home.html')
@app.route("/home.html", methods = ["GET", "POST"])
def lerQRCODE():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while True:
        success, img = cap.read()
        for barcode in decode(img):
            # print(barcode.data)
            myData = barcode.data.decode('utf-8')
            print(myData, flush=True)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255,0,255), 5)
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165,0), 2)   
        cv2.imshow('Scan QR Code - https://laptrinhvb.net', img)
        cv2.waitKey(1)
        codigo_acesso = myData
        if keyboard.is_pressed('q'): 
            return codigo_acesso
            break  
