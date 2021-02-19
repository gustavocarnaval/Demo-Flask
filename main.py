import json
import hashlib


def check_login(username):
    # Verificar usuário no login
    # Read the logins and search for the username
    with open('data/logins.json') as f:
        df = json.load(f)
    lt = [x for x in df if x['Login'] == username]
    if len(lt) == 1:
        sucesso = True
        retorno = dict(sucesso=sucesso, resultado=lt[0]['Pass'])
    elif len(lt) > 1:
        sucesso = False
        retorno = dict(sucesso=sucesso, resultado='Multiple')
    else:
        sucesso = False
        retorno = dict(sucesso=sucesso, resultado='Not Found')
    return retorno


def check_password_hash(user_password, auth_password):
    # Verificar senha no login
    result = hashlib.md5(auth_password.encode())
    converted = result.hexdigest()
    if user_password == converted:
        sucesso = True
    else:
        sucesso = False
    return sucesso



def insertusuario(nome, email, senha):
    # Inserir usuário no cadastro
    # Read the users and pick de max ID
    with open('data/users.json') as f:
        df = json.load(f)
    idmaxlist = max(df, key=lambda ev: ev['id'])
    idmax = idmaxlist['id']
    idnovo = idmax + 1

    # Convert the inputs to a list with new id and append to data
    entry = {'id': idnovo, 'nome': nome, 'email': email, 'senha': senha}
    df.append(entry)

    # Write de new json file with new data
    with open('data/users.json', 'w') as json_file:
        json.dump(df, json_file)

    return {"id": idnovo, "nome": nome}


def listusuario(ident, inicio, fim):
    # Listar usuário no cadastro
    # Read the users file
    with open('data/users.json') as f:
        df = json.load(f)
    if ident:
        lt = [x for x in df if x['id'] == ident]
    elif not fim:
        lt = df
    else:
        lt = [x for x in df if x['id'] >= inicio and x['id'] <= fim]
    return lt


""" 
def geraResponse(status, mensagem, nome_do_conteudo=False, conteudo=False):
    response = {}
    response["status"] = status
    response["mensagem"] = mensagem

    if(nome_do_conteudo and conteudo):
        response[nome_do_conteudo] = conteudo

    return response
 """