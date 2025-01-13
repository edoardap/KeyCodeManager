import qrcode
import cv2
from pyzbar.pyzbar import decode
from flask import Blueprint
QRCode_bp = Blueprint('QRCode', __name__, template_folder='../Templates')

@QRCode_bp.route("/gerarQRCode/<cod>/<name>", methods = ["GET", "POST"])
class QRCode():
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
      img = qrcode.make(cod)
      img_path = name + ".jpg"
      img.save(img_path)
      return img_path
      if os.path.exists(img_path):
         return f"QR Code gerado com sucesso e salvo em {img_path}"
      else:
         return "Falha ao gerar o QR Code"

@QRCode_bp.route("/gerar_qrcode/<cod>/<name>", methods=["GET", "POST"])
def gerar_qrcode(cod, name):
    gerador = geradorQRCode()
    img_path = gerador.gerarQRCode(cod, name)
    return send_file(img_path, as_attachment=True)

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
    print('login', loginVariavel.getId())

    resposta = funcionario.pegarChave(chave, loginVariavel.getId())

    if resposta == 2:
        return '<h1>Chave não cadastrada</h1>'
    else:
        return '<h1>Você pegou a chave {}!</h1>'.format(chave.getNomeSala())
