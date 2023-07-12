from flask import Flask, flash, jsonify, request, send_file, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import datetime
from flask_marshmallow import Marshmallow
import os
from werkzeug.utils import secure_filename


# files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def save_file(arquivo):
    if 'file' not in arquivo:
        flash('No file part')
        return redirect(request.url)
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if arquivo.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if arquivo and allowed_file(arquivo.filename):
        filename = secure_filename( arquivo.filename)
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', name=filename))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/alfa_bots'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/uploads'
app.config['MAX_CONTENT_LENGTH'] = 15 * 1000 * 1000
ALLOWED_EXTENSIONS = {'csv'}


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Execucoes(db.Model):
    __tablename__ = 'execucoes'
    id = db.Column(db.Integer, primary_key=True)
    tipo_bot = db.Column(db.Text())
    status = db.Column(db.Text())
    usuario_acionador = db.Column(db.Text())
    arquivo = db.Column(db.Text())
    observacoes = db.Column(db.Text())
    data = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, tipo_bot, status, usuario_acionador, arquivo, observacoes):
        self.tipo_bot = tipo_bot
        self.status = status
        self.usuario_acionador = usuario_acionador
        self.arquivo = arquivo
        self.observacoes = observacoes


class ExecucaoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tipo_bot', 'status', 'usuario_acionador', 'arquivo', 'data', 'observacoes')


execucao_schema = ExecucaoSchema()
execucoes_schema = ExecucaoSchema(many=True)


# with app.app_context():
    # db.create_all()

@app.get('/')
def index():
    return jsonify({"Hello":"World"})
    # send_file('../frontend/public/index.html')

@app.get('/alterar_status_aulas')
def exibir_pagina_alterar_status_aulas():
    return "<h1>Aqui será exibido a página de Alterar Status das Aulas</h1>"

@app.post('/alterar_status_aulas/executar_bot')
def alterar_status_aulas_executar():
    tipo_bot = request.form['tipo_bot']
    status = request.form['status']
    usuario_acionador = request.form['usuario_acionador']
    arquivo = request.files['arquivo_bot_alterar_status_aulas']
    observacoes = request.form['observacoes']
    
    save_file(arquivo)
    # aulas.definir_nova_situacao_aulas(aulas.site_login, aulas.email, aulas.password, nova_situacao, )


    execucoes = Execucoes(tipo_bot, status, usuario_acionador, arquivo.filename, observacoes)
    db.session.add(execucoes)
    db.session.commit()
    return '<h2>Sucesso, <a href="http://127.0.0.1:5000/uploads/">Uploads</a></h2>'
    # execucao_schema.jsonify(execucoes)

    # id, tipo_bot, status, usuario_acionador, arquivo, data
    # define_nova_situacao.definir_nova_situacao_aulas("url", "email", "senha", "novo_status")

@app.get('/execucoes')
def get_execucoes():
    all_execucoes = Execucoes.query.all()
    results = execucoes_schema.dump(all_execucoes)
    return jsonify(results)

@app.get('/execucoes/<id>')
def get_execucao(id):
    execucao = Execucoes.query.get(id)
    return execucao_schema.jsonify(execucao)

@app.get('/execucoes/alterar_status_aulas')
def query_by_tipo_bot():
    all_execucoes = Execucoes.query.filter_by(tipo_bot='alterar_status_aulas').all()
    results = execucoes_schema.dump(all_execucoes)
    return results

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)