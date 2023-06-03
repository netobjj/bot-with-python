from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import datetime
from flask_marshmallow import Marshmallow
# import funcoes.define_nova_situacao

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/alfa_bots'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Execucoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_bot = db.Column(db.Text())
    status = db.Column(db.Text())
    usuario_acionador = db.Column(db.Text())
    arquivo = db.Column(db.Text())
    data = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, tipo_bot, status, usuario_acionador, arquivo):
        self.tipo_bot = tipo_bot
        self.status = status
        self.usuario_acionador = usuario_acionador
        self.arquivo = arquivo


class ExecucaoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tipo_bot', 'status', 'usuario_acionador', 'arquivo', 'data')


execucao_schema = ExecucaoSchema()
execucoes_schema = ExecucaoSchema(many=True)


# with app.app_context():
    # db.create_all()


@app.get('/')
def index():
    return jsonify({"Hello":"World"})
    # send_file('../frontend/public/index.html')

@app.get('/alterar_status_aula')
def exibir_pagina_alterar_status_aula():
    return "<h1>Aqui será exibido a página de Alterar Status da Aula</h1>"

@app.post('/alterar_status_aula/executar_bot')
def alterar_status_aula_executar():
    tipo_bot = request.json['tipo_bot']
    status = request.json['status']
    usuario_acionador = request.json['usuario_acionador']
    arquivo = request.json['arquivo']

    execucoes = Execucoes(tipo_bot, status, usuario_acionador, arquivo)
    db.session.add(execucoes)
    db.session.commit()
    return execucao_schema.jsonify(execucoes)

    # id, tipo_bot, status, usuario_acionador, arquivo, data
    # define_nova_situacao.definir_nova_situacao_aula("url", "email", "senha", "novo_status")

@app.get('/execucoes')
def get_execucoes():
    all_execucoes = Execucoes.query.all()
    results = execucoes_schema.dump(all_execucoes)
    return jsonify(results)

@app.get('/execucoes/<id>')
def get_execucao(id):
    execucao = Execucoes.query.get(id)
    return execucao_schema.jsonify(execucao)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)