from flask_restx import Api, Resource, fields
from flask import Flask, jsonify, request
import datetime
app = Flask(__name__)


class Clientes():
    def __init__(self, cpf, nome, data):
        self.cpf = cpf
        self.nome = nome
        self.data = data


def transform(classe):
    return {'cpf': classe.cpf, 'nome': classe.nome, 'data': classe.data}


def checa_data(data):
    if data['ano'] <= 0:
        return False
    elif data['mes'] < 1 or data['mes'] > 12:
        return False
    elif data['dia'] < 1 or data['dia'] > 31:
        return False
    return True


clientes = [Clientes(123, "Ayla", datetime.date(2002,10,22))]

########################################################################
# Swagger

api = Api(app, version='ayla 2.0', title='Ayla BD', doc='/doc',
          description='Esse é o banco de dados de Ayla', contact='Ayla Florencio')


data_model = api.model('Date', {'ano': fields.Integer(required=True),
                                'mes': fields.Integer(required=True),
                                'dia': fields.Integer(required=True)})

cliente_model = api.model('Cliente', {'cpf': fields.Integer(required=True),
                                      'nome': fields.String(required=True),
                                      'data': fields.Nested(data_model, required=True)})

us = api.namespace('Primeiras Funções', description='cadastro de usuário')


@us.route('/clientes/<int:cpf>')
class Encontrar_cliente(Resource):
    @api.doc(responses={200: 'OK', 404: 'Erro de acesso.'},
             params={
                 'cpf': {'description': 'Insirir CPF do cliente', 'example': 123}},
             description='Busca o cliente no banco de dados')
    def get(self, cpf):
        for cliente in clientes:
            if cliente.cpf == cpf:
                return jsonify(transform(cliente))
        return 'Cliente não encontrado'


@us.route('/clientes/cadastrar')
class Cadastrar_cliente(Resource):
    @api.doc(responses={201: 'OK', 400: 'Inválido.'},
             params={'cpf': {'description': 'Inserir CPF do cliente', 'example': 123},
                     'nome': {'description': 'Inserir nome do cliente', 'example': "André Silva"},
                     'data': {'description': 'Inserir data de nascimento', 'example': {'dia': 11, 'mes': 5, 'ano': 2001}}},
             description='Cadastra o cliente no banco de dados')
    @api.expect(cliente_model)
    def post(self):
        novo_cliente = request.get_json()
        for cliente in clientes:
            if cliente.cpf == novo_cliente['cpf']:
                return 'Cliente já existente.', 400
        data_nascimento = (novo_cliente['data'])
        if checa_data(data_nascimento) == False:
            return 'Data inválida.', 400

        data_checada = datetime.date(data_nascimento["ano"], data_nascimento["mes"], data_nascimento["dia"])

        cl = Clientes(novo_cliente.get('cpf'),
                      novo_cliente.get('nome'), data_checada)
        clientes.append(cl)
        lista = []
        for cliente in clientes:
            lista.append(transform(cliente))
        return jsonify(lista)

app.run(port=5000, host='localhost', debug=True)
