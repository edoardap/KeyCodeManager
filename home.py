import cv2
import numpy as np
from pyzbar.pyzbar import decode
import keyboard

from flask import Flask, render_template, request
app=Flask(__name__,template_folder='Templates')

from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

supabaseUrl = 'https://xisosulvxhowoxbcpkuo.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhpc29zdWx2eGhvd294YmNwa3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODg3NzQwNSwiZXhwIjoyMDE0NDUzNDA1fQ.IisZMCnX8ZVTVkpxMu_H9PZ8lIST0fI6QfsVDu1qMUA'
supabase = create_client(supabaseUrl, supabaseKey)

#Metodo para validar login
@app.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    emailp = request.form.get("email")
    senhap = request.form.get("senha")
    amostra = supabase.table("usuarios").select('email', 'senha').eq("email", emailp).eq("senha", senhap).execute()
    if amostra.data != []:
        return render_template('tela-inicial.html')
    else:
        return '<h1> email ou senha incorretos </h1>'

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
