import qrcode
import cv2
from pyzbar.pyzbar import decode
import numpy as np

from Models.Aluno import Aluno
from Models.Chave import Chave
from Models.Funcionario import Funcionario
from flask import Blueprint
from flask import render_template

from Models.Gerente import Gerente
from Models.Professor import Professor

QRCode_bp = Blueprint('QRCode', __name__, template_folder='../Templates',url_prefix='/QRcode')
from flask import session, send_file
from api.AdapterDB import AdapterDB

adapter = AdapterDB(host="localhost", user="manager", password="K@qr0208", database="keycode")

class QRCode:
#     def __init__(self, cod):
#         self.codigo = cod
#
    def __init__(self):
            pass

    def setCodigo(self, cod):
      self.codigo = cod

    def getCod(self):
      return self.codigo

    def gerarQRCode(self, cod, name):
        img = qrcode.make(cod)
        img_path = name + ".jpg"
        img.save(img_path)
        return img_path
        if os.path.exists(img_path):
            return img_path
        else:
            return None

@QRCode_bp.route("/gerar_qrcode/<cod>/<name>", methods=["POST"])
def gerar_qrcode(cod, name):
    gerador = QRCode()
    img_path = gerador.gerarQRCode(cod, name)
    print('code', cod)
    print('name', name)
    if img_path:
        return send_file(img_path, mimetype='image/jpeg', as_attachment=True)
    else:
        return "Falha ao gerar o QR Code", 500

@QRCode_bp.route("/home.html", methods = ["GET", "POST"])
def lerQRCODE(mirror=False):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    myData = None
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        cv2.imshow('Leitor', img)
        for barcode in decode(img):
            # print(barcode.data)
            myData = barcode.data.decode('utf-8')
            print(myData, flush=True)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165, 0), 2)
            if myData:
                break

        if cv2.waitKey(1) == 27 or myData:
            break
    cv2.destroyAllWindows()
    cam.release()
    chave = Chave("", "", myData, "")

    user_id = session.get('user_id')  # Obtém o ID do usuário armazenado na sessão
    usertype = session.get('user_type')
    chave = adapter.buscar_chave_por_qrcode(chave.getQrCode()) #Pega obj completo

    #Lembrete: mudar para a forma mais eficiente a questap  do tipoUser
    if usertype == 'aluno':
        aluno = Aluno("", "", "", "")
        result = adapter.pegarChave(chave, user_id)

        if result== 2:
            return render_template('chavePega.html', nome_sala=chave.getNomeSala(), tipoUser='/tela-inicial3')
        elif result==1:
            return render_template('sem-acesso-chave.html')
        elif result==3:
            return render_template('erro-geral.html')

    elif usertype == 'professor':
        professor = Professor("", "", "", "", "")
        result = adapter.pegarChave(chave, user_id)
        if result:
            return render_template('chavePega.html', nome_sala=chave.getNomeSala(), tipoUser='/tela-inicial2')

    elif usertype == 'gerente':
        gerente = Gerente("", "", "")
        result = adapter.pegarChave(chave, user_id)
        if result:
            return render_template('chavePega.html', nome_sala=chave.getNomeSala(), tipoUser='/tela-inicial')
    else:
        return "Tipo de usuário inválido."