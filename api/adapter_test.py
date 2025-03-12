import AdapterDB as adb

from flask import Flask, jsonify

app = Flask(__name__)

# Configuração do banco de dados
db = adb.AdapterDB(host="localhost", user="manager", password="K@qr0208", database="keycode")

@app.route('/data', methods=['GET'])
def get_data():
    data = db.get_tempo_uso_chave()
    return jsonify(data)

@app.route('/')
def home():
    return "API Flask rodando!"

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
