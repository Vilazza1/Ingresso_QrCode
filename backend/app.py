from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import qrcode
import os

app = Flask(__name__, static_folder='frontend_build/static', static_url_path='/static')
CORS(app)

# Banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de ingresso
class Ingresso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_titular = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    cnpj = db.Column(db.String(20), nullable=True)
    nome_acompanhante = db.Column(db.String(120), nullable=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    codigo_acomp = db.Column(db.String(50), unique=True, nullable=True)
    usado_titular = db.Column(db.Boolean, default=False)
    usado_acomp = db.Column(db.Boolean, default=False)

# Função para gerar QR Code no diretório temporário
def gerar_qrcode(codigo):
    link = f"https://SEU_DOMINIO.onrender.com/validar/{codigo}"
    img = qrcode.make(link)
    caminho = f"/tmp/qrcodes/{codigo}.png"
    os.makedirs('/tmp/qrcodes', exist_ok=True)
    img.save(caminho)
    return caminho

@app.route('/')
def serve_index():
    # Serve o arquivo index.html da pasta frontend_build
    return send_from_directory('frontend_build', 'index.html')

@app.route('/<path:path>')
def serve_static_or_index(path):
    # Tenta servir arquivo estático, se não existir, serve o index.html (para SPA)
    if os.path.exists(os.path.join('frontend_build', path)):
        return send_from_directory('frontend_build', path)
    else:
        return send_from_directory('frontend_build', 'index.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.json
    nome = data.get('nome_titular')
    email = data.get('email')
    telefone = data.get('telefone')
    cnpj = data.get('cnpj')
    nome_acomp = data.get('nome_acompanhante')

    if not nome:
        return jsonify({"error": "Nome do titular é obrigatório"}), 400

    total = Ingresso.query.count() + 1
    codigo = f"ING{total:05d}T"
    codigo_acomp = f"ING{total:05d}A" if nome_acomp else None

    ingresso = Ingresso(
        nome_titular=nome,
        email=email,
        telefone=telefone,
        cnpj=cnpj,
        nome_acompanhante=nome_acomp,
        codigo=codigo,
        codigo_acomp=codigo_acomp
    )

    db.session.add(ingresso)
    db.session.commit()

    gerar_qrcode(codigo)
    if codigo_acomp:
        gerar_qrcode(codigo_acomp)

    return jsonify({
        "msg": "Cadastro realizado!",
        "codigo_titular": codigo,
        "qr_titular_url": f"/static/qrcodes/{codigo}.png",
        "codigo_acompanhante": codigo_acomp,
        "qr_acompanhante_url": f"/static/qrcodes/{codigo_acomp}.png" if codigo_acomp else None
    })

@app.route('/validar/<codigo>', methods=['GET'])
def validar(codigo):
    ingresso = Ingresso.query.filter(
        (Ingresso.codigo == codigo) | (Ingresso.codigo_acomp == codigo)
    ).first()

    if not ingresso:
        return "<h1>QR Code inválido!</h1>", 404

    if codigo == ingresso.codigo:
        if ingresso.usado_titular:
            return "<h1>Ingresso do titular já foi usado!</h1>", 400
        ingresso.usado_titular = True
        db.session.commit()
        return f"<h1>Ingresso válido do titular: {ingresso.nome_titular}</h1>"

    if codigo == ingresso.codigo_acomp:
        if ingresso.usado_acomp:
            return "<h1>Ingresso do acompanhante já foi usado!</h1>", 400
        ingresso.usado_acomp = True
        db.session.commit()
        return f"<h1>Ingresso válido do acompanhante: {ingresso.nome_acompanhante}</h1>"

    return "<h1>Erro desconhecido.</h1>", 500

# Rota para servir QR codes gerados em /tmp/qrcodes/
@app.route('/static/qrcodes/<filename>')
def get_qrcode(filename):
    caminho = f"/tmp/qrcodes/{filename}"
    if os.path.exists(caminho):
        return send_file(caminho, mimetype='image/png')
    return "<h1>QR não encontrado</h1>", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        os.makedirs('/tmp/qrcodes', exist_ok=True)
    app.run(host='0.0.0.0', port=10000)
