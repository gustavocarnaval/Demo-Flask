from flask import Flask, request
from main import insertusuario


app = Flask("Demo_Carnaval")


@app.route("/olamundo", methods=["GET"])
def olaMundo():
    return{"ola": "mundo2"}


@app.route("/cadastra/usuario", methods=["POST"])
def cadastra_usuario():
    body = request.get_json()

    if("nome" not in body):
        return geraResponse(400, "O parametro nome é obrigatorio")

    if("email" not in body):
        return geraResponse(400, "O parametro email é obrigatorio")

    if("senha" not in body):
        return geraResponse(400, "O parametro senha é obrigatorio")

    usuario = insertusuario(body["nome"], body["email"], body["senha"])

    return geraResponse(200, "Usuario Criado", "user", usuario)


def geraResponse(status, mensagem, nome_do_conteudo=False, conteudo=False):
    response = {}
    response["status"] = status
    response["mensagem"] = mensagem

    if(nome_do_conteudo and conteudo):
        response[nome_do_conteudo] = conteudo

    return response


app.run()
