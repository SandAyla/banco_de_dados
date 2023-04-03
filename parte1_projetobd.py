from flask import Flask, jsonify, request

app = Flask(__name__)

class Clientes():
    def __init__(self, cpf, nome, data):
        self.cpf=cpf
        self.nome=nome
        self.data=data

def transform(classe):
    return {'cpf': classe.cpf,'nome':classe.nome, 'data': classe.data }

clientes = [Clientes(123, "Ayla", "22-10-2002")]

@app.route('/clientes', methods=['GET'])
def tds_clientes():
    lista=[]
    for cliente in clientes:
        lista.append(transform(cliente))
    return jsonify(lista)

@app.route('/clientes', methods=['POST'])
def add_clientes():
    novo_cliente= request.get_json()
    for cliente in clientes:
        if cliente.cpf == novo_cliente.get('cpf'):
            return 'Cliente já cadastrado'
    cl=Clientes(novo_cliente.get('cpf'), novo_cliente.get('nome'),novo_cliente.get('data'))
    clientes.append(cl)
    lista=[]
    for cliente in clientes:
        lista.append(transform(cliente))
    return jsonify(lista)

@app.route('/clientes/<int:cpf>', methods=['GET'])
def obter_clientes(cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return jsonify(transform(cliente))
    return 'Cliente não encontrado'

app.run(port=5000, host='0.0.0.0', debug=True)
