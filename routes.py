from flask import Flask, request, jsonify, make_response, Response
import datetime
import json
import jwt
from main import insertusuario, listusuario, check_login, check_password_hash
from functools import wraps
import config as cfg

app = Flask("Demo_API_JWT")
app.config['SECRET_KEY'] = cfg.SECRET_KEY
app.config['JSON_AS_ASCII'] = cfg.JSON_AS_ASCII


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Token na rota: http://127.0.0.1:5000/route?token=aslasdjasd
        # token = request.args.get('token')
        
        # Token no header
        #token = request.headers['x-access-tokens']

        # Token bearer
        bearer = request.headers.get('Authorization')    # Bearer YourTokenHere
        
        if not bearer:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            token = bearer.split()[1]  # YourTokenHere
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/olamundo", methods=["GET"])
def olaMundo():
    return{"ola": "mundo"}


@app.route("/login", methods=["GET"])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        # Ou usuário ou senha ou ambos não preenchidos
        return make_response('Could not verify!',
                             401,
                             {'WWW.Authentication': 'Basic realm: "Login and Pass Required"'})
    else:
        # Usuário e senha preenchidos
        chk_user = check_login(auth.username)
        if chk_user['sucesso']:
            # Encontrou o usuário no cadastro
            # Procura pela senha
            snh = chk_user['resultado']
            chk_pass = check_password_hash(snh, auth.password)
            if chk_pass:
                # Senha certa

                # Controle de resposta:
                codigo = 0
                mensagem = 'Operação efetuada com sucesso.'
                sucesso = True
                # Datas de Criação e Validade:
                dtCriacao = datetime.datetime.utcnow()
                dtCriacaostr = dtCriacao.strftime('%Y-%m-%d %H:%M:%S')
                dtValidade = dtCriacao + datetime.timedelta(hours=24)
                dtValidadestr = dtValidade.strftime('%Y-%m-%d %H:%M:%S')
                # Geração do Token:
                token = jwt.encode(
                    {'user': auth.username, 'exp': dtValidade}, app.config['SECRET_KEY'])
                # Montagem do JSON de resposta:
                jtoken = dict(accessToken=token, dtCriacao=dtCriacaostr,
                              dtValidade=dtValidadestr)
                resp = dict(codigo=codigo, mensagem=mensagem,
                            sucesso=sucesso, resultado=jtoken)
                # Resposta:
                return Response(json.dumps(resp, ensure_ascii=False).encode('utf8'),  mimetype='application/json')

            else:
                # Senha errada
                return make_response('Could not verify!',
                                     401,
                                     {'WWW.Authentication': 'Basic realm: "Password dont match"'})

        else:
            # Não Encontrou o usuário no cadastro ou múltiplos
            return make_response('Could not verify!',
                                 401,
                                 {'WWW.Authentication': 'Basic realm: "Login não encontrado ou multiplos Logins"'})


@ app.route("/usuario/quantidade", methods=["GET"])
@ token_required
def quantifica_usuario():
    lt = listusuario(False,False,False)
    return jsonify(len(lt))


@ app.route("/usuario", methods=["GET"])
@ token_required
def lista_usuario():
    inicio = request.args.get('inicio')
    quantidade = request.args.get('quantidade')
    ident = request.args.get('id')
    if not ident:
        if not inicio:
            inicio = 1
        else:
            inicio = int(inicio)
        if not quantidade:
            quantidade = 300
        else:
            quantidade = int(quantidade)
        fim = inicio + quantidade - 1
        lt = listusuario(False,inicio,fim)
    else:
        ident = int(ident)
        lt = listusuario(ident,False,False)
    return jsonify(lt)


@ app.route("/usuario", methods=["POST"])
@ token_required
def cadastra_usuario():
    body = request.get_json()

    if("nome" not in body):
        return make_response('O parametro nome é obrigatorio', 400) 

    if("email" not in body):
        return make_response('O parametro email é obrigatorio', 400)

    if("senha" not in body):
        return make_response('O parametro senha é obrigatorio', 400)

    usuario = insertusuario(body["nome"], body["email"], body["senha"])
    retorno = dict(status=200, mensagem='Usuário Criado com Sucesso', user=usuario)
    return jsonify(retorno)


app.run()
