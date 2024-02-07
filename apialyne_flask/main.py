import cursor as cursor
from db_config import mysql
from app import app
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
import random
import requests
import xml.etree.ElementTree as ET
import base64


@app.route('/getHWAuto')
def getHWAuto():
    try:
        # ObtÃ©m uma conexÃ£o e cursor usando a extensÃ£o flask_mysqldb
        conn = mysql.connection
        cursor = conn.cursor()

        # Ajusta a consulta SQL
        query = """
	SELECT id as id_smartgears, linha_turno as centro_de_trabalho,
        ((SELECT cad_empresa_linha.cod_linha FROM cad_empresa_linha WHERE cad_empresa_linha.linha = sintetico_linha.linha) + 0) as cod_linha
        FROM sintetico_linha
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        resp = jsonify(error='Erro ao obter dados sintÃ©ticos')
        resp.status_code = 500
        return resp
    finally:
        cursor.close()

@app.route('/GetCentrosAuto')
def getCentrosAuto():
    try:
        # ObtÃ©m uma conexÃ£o e cursor usando a extensÃ£o flask_mysqldb
        conn = mysql.connection
        cursor = conn.cursor()

        # Ajusta a consulta SQL
        query = """
	SELECT cod_centro, centro, IFNULL(mac, '-') as mac, IFNULL(corrente1, 0) 
	as corrente1, IFNULL(temperatura, '-') as temperatura, 
	IFNULL(data_insert, CURRENT_TIMESTAMP()) as data_insert FROM view_auto_senai
	"""

        cursor.execute(query)

        rows = cursor.fetchall()

        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        resp = jsonify(error='Erro ao obter dados sintÃ©ticos')
        resp.status_code = 500
        return resp
    finally:
        cursor.close()

@app.route('/GetColetor')
def getColetor():
    try:
        # ObtÃ©m uma conexÃ£o e cursor usando a extensÃ£o flask_mysqldb
        conn = mysql.connection
        cursor = conn.cursor()

        # Ajusta a consulta SQL
        query = """
	SELECT * FROM coletor_senai ORDER BY id DESC LIMIT 20
	"""

        cursor.execute(query)

        rows = cursor.fetchall()

        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        resp = jsonify(error='Erro ao obter dados sintÃ©ticos')
        resp.status_code = 500
        return resp
    finally:
        cursor.close()

@app.route('/getIST2')
def getIST2():
    try:
        # ObtÃ©m uma conexÃ£o e cursor usando a extensÃ£o flask_mysqldb
        conn = mysql.connection
        cursor = conn.cursor()

        # Ajusta a consulta SQL
        query = """
SELECT * FROM coletor_senai2 ORDER BY id DESC LIMIT 20
	"""

        cursor.execute(query)

        rows = cursor.fetchall()

        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        resp = jsonify(error='Erro ao obter dados sintÃ©ticos')
        resp.status_code = 500
        return resp
    finally:
        cursor.close()

@app.route('/getIST3')
def getIST3():
    try:
        # ObtÃ©m uma conexÃ£o e cursor usando a extensÃ£o flask_mysqldb
        conn = mysql.connection
        cursor = conn.cursor()

        # Ajusta a consulta SQL
        query = """
	SELECT * FROM auto_senai ORDER BY id DESC LIMIT 20
	"""

        cursor.execute(query)

        rows = cursor.fetchall()

        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        resp = jsonify(error='Erro ao obter dados sintÃ©ticos')
        resp.status_code = 500
        return resp
    finally:
        cursor.close()

@app.route('/postIST2', methods=['POST'])
def post2():
    try:
        cursor = mysql.connection.cursor()
        json_data = request.get_json(force=True)
        _mac = json_data['mac']
        _di0 = json_data['di0']
        _di1 = json_data['di1']
        _di2 = json_data['di2']
        _di3 = json_data['di3']
        _di4 = json_data['di4']
        _di5 = json_data['di5']
        _di6 = json_data['di6']
        _di7 = json_data['di7']
        _data = json_data['data']
        insert_user_cmd = """INSERT INTO coletor_senai2 (mac, di0, di1, di2, di3, di4, di5, di6, di7, data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_user_cmd, (_mac, _di0, _di1, _di2, _di3, _di4, _di5, _di6, _di7, _data))
        mysql.connection.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        return response

@app.route('/postIST3', methods=['POST'])
def post3():
    try:
        cursor = mysql.connection.cursor()
        json_data = request.get_json(force=True)
        _mac = json_data['mac']
        _di0 = json_data['di0']
        _di1 = json_data['di1']
        _di2 = json_data['di2']
        _di3 = json_data['di3']
        _peso = json_data['peso']
        _temperatura = json_data['temperatura']
        _corrente1 = json_data['corrente1']
        _corrente2 = json_data['corrente2']
        _corrente3 = json_data['corrente3']
        _tim = json_data['tim']
        insert_user_cmd = """INSERT INTO auto_senai (mac, di0, di1, di2, di3, peso, temperatura, corrente1, corrente2, corrente3, tim) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_user_cmd, (_mac, _di0, _di1, _di2, _di3, _peso, _temperatura, _corrente1, _corrente2, _corrente3, _tim))
        mysql.connection.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        return response

@app.route('/postParada', methods=['POST'])
def parada():
    try:
        cursor = mysql.connection.cursor()
        json_data = request.get_json(force=True)
        _cod_centro = json_data['cod_centro']
        _cod_ordem = json_data['cod_ordem']
        _operador = json_data['operador']
        _motivo = json_data['motivo']
        _tim = json_data['tim']
        _etapa = json_data['etapa']
        insert_user_cmd = """INSERT INTO alerta_parada (cod_centro, cod_ordem, operador, motivo, tim, etapa) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_user_cmd, (_cod_centro, _cod_ordem, _operador, _motivo, _tim, _etapa))
        mysql.connection.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        return response

@app.route('/postIST', methods=['POST'])
def post():
    try:
        cursor = mysql.connection.cursor()
        json_data = request.get_json(force=True)
        _mac = json_data['mac']
        _identificador = json_data['identificador']
        _valor = json_data['valor']
        _data = json_data['data']
        insert_user_cmd = """INSERT INTO coletor_senai (mac, identificador, valor, data) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_user_cmd, (_mac, _identificador, _valor, _data))
        mysql.connection.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        return response

@app.route('/centros_trabalho', methods=['GET'])
def get_centros_trabalho():
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "select CODWCP, NOME, WCP.CODCWC, CWC.DESCRICAO FROM TPRWCP WCP JOIN TPRCWC CWC ON CWC.CODCWC = WCP.CODCWC WHERE CODWCP <> 0 AND WCP.CODCWC = 5"
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500
    

@app.route('/ordem_producao', methods=['GET'])
def get_ordem_producao():
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "SELECT * FROM SANKHYA_TEST.sankhya.AD_VAPP_OPS_SMART"
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500
    
    
@app.route('/materia_prima', methods=['GET'])
def get_materia_prima():
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "SELECT TOP 10 PROPA.REFERENCIA AS codEan, PROPA.DESCRPROD AS nomeMp, PROPA.CODPROD AS codProduto, PROPA.CODVOL AS unidade, 1 AS qtdPA, PROMP.CODPROD AS codMp, PROMP.DESCRPROD as nomeMp, MP.QTDMISTURA AS qtdMP FROM TPRLMP MP JOIN TGFPRO PROMP ON PROMP.CODPROD = MP.CODPRODMP JOIN TGFPRO PROPA ON PROPA.CODPROD = MP.CODPRODPA where PROPA.CODVOL = 'L'"
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500
    

@app.route('/produto', methods=['GET'])
def get_produto():
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "SELECT PRO.CODPROD AS codProduto, PRO.DESCRPROD AS nomeProduto, PRO.CODGRUPOPROD AS CodfamiliaProduto, GRU.DESCRGRUPOPROD AS familiaProduto, PRO.CODVOL AS unidMedida FROM TGFPRO PRO JOIN TGFGRU GRU ON GRU.CODGRUPOPROD = PRO.CODGRUPOPROD WHERE PRO.ATIVO <> 'N' AND GRU.DESCRGRUPOPROD in ('MP','EM','PI','PP','PA')"
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500
    

@app.route('/funcionarios', methods=['GET'])
def get_funcionarios():

    matricula = request.args.get('matricula')

    if matricula is None:
        return jsonify({"error": "O parÃ¢metro 'matricula' Ã© obrigatÃ³rio"}), 400

    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "SELECT ECD.CODIGO AS codFuncionario, USU.NOMEUSU AS nome, '' AS cargo, USU.CODGRUPO, GRU.NOMEGRUPO FROM TPRECD ECD JOIN TSIUSU USU ON USU.CODUSU = ECD.CODIGO JOIN TSIGRU GRU ON GRU.CODGRUPO = USU.CODGRUPO WHERE ISNULL(DTLIMACESSO,'') = '' AND ECD.CODIGO = %s GROUP BY ECD.CODIGO, USU.NOMEUSU, USU.CODGRUPO, GRU.NOMEGRUPO" % matricula
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500

@app.route('/apontamentos', methods=['GET'])
def get_apontamentos():

    idiatv = request.args.get('idiatv')

    if idiatv is None:
        return jsonify({"error": "O parÃ¢metro 'idiatv' Ã© obrigatÃ³rio"}), 400

    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "Select APO.NUAPO, APA.SEQAPA, isnull(APO.SITUACAO,'') from TPRAPO APO left join TPRAPA APA ON APA.NUAPO = APO.NUAPO WHERE IDIATV = %s AND SITUACAO = 'P'" % idiatv
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500
    

@app.route('/motivo_paradas', methods=['GET'])
def get_motivo_paradas():
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "select CODMTP as codParada, DESCRICAO AS motivoParada, '' AS tipoParada from TPRMTP WHERE ATIVO <> 'N'"
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500
    
    
@app.route('/fluxo', methods=['GET'])
def get_fluxo():
    codprod = request.args.get('codprod')
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": f"""SELECT PRO.CODPROD as codProduto, pre.descpre as etapa, PRE.SEQPRE as prioridade, pre.TEMPO as tempoAgitacao FROM AD_MODPRE PRE	LEFT JOIN TGFPRO PRO ON PRO.CODPROD = PRE.CODPROD WHERE PRO.CODPROD = {codprod}"""
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500



@app.route('/fluxo_detail', methods=['GET'])
def get_fluxo_detail():
    
    codseq = request.args.get('codseq')
    codprod = request.args.get('codprod')

    if codseq is None:
        return jsonify({"error": "O parÃ¢metro 'codseq' Ã© obrigatÃ³rio"}), 400
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": f"""SELECT PRO.CODPROD as codProduto, pre.descpre as etapa, PRE.SEQPRE as prioridade, isnull(pre.TEMPO,'00:00:00') as tempoAgitacao, isnull(PRE.TEMPERATURA,0) as temperatura FROM AD_MODPRE PRE join TGFPRO PRO ON PRO.CODPROD = PRE.CODPROD  WHERE PRO.CODPROD = {codprod} AND PRE.SEQPRE = {codseq} order by 1,3"""
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500


    
@app.route('/ordem_producao_detail', methods=['GET'])
def get_ordem_producao_detail():
    
    codordem = request.args.get('codordem')

    if codordem is None:
        return jsonify({"error": "O parÃ¢metro 'codcentro' Ã© obrigatÃ³rio"}), 400
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "SELECT codOrdem, codProduto, descProduto, codCentro, descCentro, processo, lote, localOrigem, localDestino, DHINICIO, DHFINAL, DATASEQ, QTD_APRODUZ, QTD_PRODUZ, STATUSOP, IDIATV, IDPROC, IDEFX FROM SANKHYA_TEST.sankhya.AD_VAPP_OPS_SMART WHERE STATUSOP <> 'Finalizado' AND codOrdem = %s" % codordem
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500

@app.route('/ordem_producao_centro', methods=['GET'])
def get_ordem_producao_centro():
    
    centro = request.args.get('centro')

    if centro is None:
        return jsonify({"error": "O parÃ¢metro 'centro' Ã© obrigatÃ³rio"}), 400
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = {
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": "SELECT * FROM SANKHYA_TEST.sankhya.AD_VAPP_OPS_SMART WHERE codCentro = %s" % centro
            }
        }

        response2 = requests.post(segunda_api_url, json=segunda_api_payload, headers=segunda_api_headers)

        if response2.status_code == 200:
            return response2.json()  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao acessar as APIs"}), 500




def extract_info_from_xml(xml_text):
    root = ET.fromstring(xml_text)
    status = root.attrib.get('status', '')
    transaction_id = root.attrib.get('transactionId', '')
    status_message_elem = root.find('.//statusMessage')
    status_message = base64.b64decode(status_message_elem.text).decode('ISO-8859-1') if status_message_elem is not None else ''
    return {'status': status, 'transactionId': transaction_id, 'statusMessage': status_message}

# Rota para a primeira consulta
@app.route('/post_continuar_op', methods=['GET'])
def post_continuar_op():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.continuarInstanciaAtividades&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f"""
    <serviceRequest serviceName="OperacaoProducaoSP.continuarInstanciaAtividades">
        <requestBody>
            <instancias>
                <instancia>
                    <IDIATV>{idiatv_param}</IDIATV>
                </instancia>
            </instancias>
        </requestBody>
    </serviceRequest>
    """

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)


@app.route('/post_iniciarop', methods=['GET'])
def post_iniciarop():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv', default='1')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.iniciarInstanciaAtividades&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f"""
    <serviceRequest serviceName="OperacaoProducaoSP.iniciarInstanciaAtividades">
        <requestBody>
            <instancias>
                <instancia>
                    <IDIATV>{idiatv_param}</IDIATV>
                </instancia>
            </instancias>
        </requestBody>
    </serviceRequest>
    """

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)


@app.route('/post_parar_maquina', methods=['GET'])
def post_parar_maquina():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')
    codmtp_param = request.args.get('codmtp')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?application=OperacaoProducao&mgeSession={jsessionid}&serviceName=OperacaoProducaoSP.pararInstanciaAtividades"

    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f"""
    <serviceRequest serviceName="OperacaoProducaoSP.pararInstanciaAtividades">
    <requestBody>
        <instancias tipoParada="P">
            <instancia>
                <IDIATV>{idiatv_param}</IDIATV>
                <CODMTP>{codmtp_param}</CODMTP>
                <OBSERVACAO/>
            </instancia>
        </instancias>
    </requestBody>
    </serviceRequest>
    """

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_finalizarop', methods=['GET'])
def post_finalizarop():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')
    idefx_param = request.args.get('idefx')
    idiproc_param = request.args.get('idiproc')
    idproc_param = request.args.get('idproc')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.finalizarInstanciaAtividades&mgeSession={jsessionid}"

    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f"""
    <serviceRequest serviceName="OperacaoProducaoSP.finalizarInstanciaAtividades">
    <requestBody>
        <instancias confirmarApontamentosDivergentes="false">
            <instancia>
                <IDIATV>{idiatv_param}</IDIATV>
                <IDEFX>{idefx_param}</IDEFX>
                <IDIPROC>{idiproc_param}</IDIPROC>
                <IDPROC>{idproc_param}</IDPROC>
            </instancia>
        </instancias>
    </requestBody>
    </serviceRequest>
    """

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_realocacentro', methods=['GET'])
def post_realocacentro():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')
    idiproc_param = request.args.get('idiproc')
    codwcp_param = request.args.get('codwcp')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?application=OperacaoProducao&mgeSession={jsessionid}&serviceName=OperacaoProducaoSP.realocarCentroDeTrabalhoPorCategoria"

    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f"""
        <serviceRequest serviceName="OperacaoProducaoSP.realocarCentroDeTrabalhoPorCategoria">
            <requestBody>
                <params idiproc="{idiproc_param}" idiatv="{idiatv_param}" codwcp="{codwcp_param}" isWorkCenterPadrao="true"/>
            </requestBody>
        </serviceRequest>
    """

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)


@app.route('/post_criaapontamento', methods=['GET'])
def post_criaapontamento():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.criarApontamento&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f"""
    <serviceRequest serviceName="OperacaoProducaoSP.criarApontamento">
    <requestBody>
        <params IDIATV="{idiatv_param}" QTDAPONTADA="1"/>
    </requestBody>
    </serviceRequest>
    """

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_apontar', methods=['GET'])
def post_apontars():
    
    idiatv_param = request.args.get('idiatv')
    
    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    response = requests.post(url, json=body, headers=headers)
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.criarApontamento&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    body_post = f"""
        <serviceRequest serviceName="OperacaoProducaoSP.criarApontamento">
            <requestBody>
                <params IDIATV="{idiatv_param}" QTDAPONTADA="1"/>
            </requestBody>
        </serviceRequest>
    """

    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Analisando o XML retornado
    root = ET.fromstring(response_post.text)

    # Extraindo os campos desejados
    status = root.attrib.get('status', '')
    status_message = ''
    nuapo = ''
    listapendentes = ''

    if status == '1':
        nuapo = root.find('.//apontamento').attrib.get('NUAPO', '')
        listapendentes = root.find('.//apontamento').attrib.get('LISTAPENDENTES', '')
    elif status == '0':
        encoded_status_message = root.find('.//statusMessage').text.strip()
        # Decodificando o statusMessage em base64
        status_message = base64.b64decode(encoded_status_message).decode('utf-8', errors='replace')

    # Criando um dicionÃ¡rio com os resultados
    result_dict = {
        'status': status,
        'statusMessage': status_message,
        'NUAPO': nuapo,
        'LISTAPENDENTES': listapendentes
    }

    return jsonify(result_dict)

@app.route('/post_salvarapontamento3', methods=['GET'])
def post_salvarapontamento3():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    qnt_param = request.args.get('qnt')
    nuapo_param = request.args.get('nuapo')
    seqapa_param = request.args.get('seqapa')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mge/service.sbr?serviceName=CRUDServiceProvider.saveRecord&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"
    
    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f"""
        serviceRequest serviceName="CRUDServiceProvider.saveRecord\" ><requestBody>
    <dataSet rootEntity="ApontamentoPA" includePresentationFields="S" datasetid="1658322435343_10">
    <entity path=""><fieldset list="*"/><field name="CONTROLEPA"/></entity>
    <entity path="Produto"><fieldset list="DECQTD,TIPCONTEST"/></entity>
    <entity path="MotivosPerda"><field name="DESCRICAO"/></entity>
        <dataRow>
            <localFields>
                <QTDAPONTADA>{qnt_param}</QTDAPONTADA>
            </localFields>
            <key>
                <NUAPO>{nuapo_param}</NUAPO>
                <SEQAPA>{seqapa_param}</SEQAPA>
            </key>
        </dataRow>
    </dataSet>
        </requestBody></serviceRequest>
    """
    #print(body_post)
    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_confirmarapontamento', methods=['GET'])
def post_confirmarapontamento():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')
    nuapo_param = request.args.get('nuapo')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.confirmarApontamento&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f"""
        <serviceRequest serviceName="mgeprod@OperacaoProducaoSP.confirmarApontamento">
            <requestBody>
                <params NUAPO="{nuapo_param}" IDIATV="{idiatv_param}" ACEITARQTDMAIOR="false" ULTIMOAPONTAMENTO="false" RESPOSTA_ULTIMO_APONTAMENTO="false"/>
            </requestBody>
        </serviceRequest>
    """
    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_salvarapontamento2', methods=['GET'])
def post_salvarapontamento2():
    # Obtendo o parÃ¢metro da URL para a tag IDIATV
    #qnt_param = request.args.get('qnt')
    #nuapo_param = request.args.get('nuapo')
    #seqapa_param = request.args.get('seqapa')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisiÃ§Ã£o
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisiÃ§Ã£o
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')
    print(jsessionid)
    # Realizando o segundo POST
    #url_post = f"http://179.185.45.146:8280/mge/service.sbr?serviceName=CRUDServiceProvider.saveRecord&application=OperacaoProducao&resourceID=br.com.sankhya.producao.cad.OperacaoProducao&mgeSession={jsessionid}"
    url_post = f"http://179.185.45.146:8280/mge/service.sbr?serviceName=CRUDServiceProvider.saveRecord&application=OperacaoProducao&resourceID=br.com.sankhya.producao.cad.OperacaoProducao&mgeSession={jsessionid}"
    print(url_post)
    # Corpo da segunda requisiÃ§Ã£o com o parÃ¢metro da URL
    body_post = f'''
    <serviceRequest serviceName=\"CRUDServiceProvider.saveRecord\" ><requestBody>\r\n    <dataSet rootEntity=\"ApontamentoPA\" includePresentationFields=\"S\" datasetid=\"1658322435343_10\">\r\n    <entity path=\"\"><fieldset list=\"*\"/><field name=\"CONTROLEPA\"/></entity>\r\n    <entity path=\"Produto\"><fieldset list=\"DECQTD,TIPCONTEST\"/></entity>\r\n    <entity path=\"MotivosPerda\"><field name=\"DESCRICAO\"/></entity>\r\n        <dataRow>\r\n            <localFields>\r\n                <QTDAPONTADA>10</QTDAPONTADA>\r\n            </localFields>\r\n            <key>\r\n                <NUAPO>92959</NUAPO>\r\n                <SEQAPA>1</SEQAPA>\r\n            </key>\r\n        </dataRow>\r\n    </dataSet>\r\n        </requestBody></serviceRequest>
    '''
    print(body_post)

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informaÃ§Ãµes do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_salvarapontamento', methods=['GET'])
def post_salvarapontamento():
    # ConfiguraÃ§Ã£o da primeira solicitaÃ§Ã£o HTTP
    qnt_param = request.args.get('qnt')
    nuapo_param = request.args.get('nuapo')
    seqapa_param = request.args.get('seqapa')
    
    login_url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": { "$": "IRANILDO" },
            "INTERNO": { "$": "123456" },
            "KEEPCONNECTED": { "$": "S" }
        }
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao acessar a primeira API"}), 500

        # Extrai o cookie JSESSIONID da resposta
        cookie = response.headers['set-cookie'].split(';')[0]
        jsessionid = cookie
        jsessionid2 = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')
        print(jsessionid)
        print(jsessionid2)

        # ConfiguraÃ§Ã£o da segunda solicitaÃ§Ã£o usando o cookie da primeira API
        segunda_api_url = f"http://179.185.45.146:8280/mge/service.sbr?serviceName=CRUDServiceProvider.saveRecord&application=OperacaoProducao&resourceID=br.com.sankhya.producao.cad.OperacaoProducao&mgeSession={jsessionid2}"
        segunda_api_headers = {
            "Content-Type": "application/json",
            "Cookie": jsessionid
        }
        segunda_api_payload = f""" 
        <serviceRequest serviceName="CRUDServiceProvider.saveRecord" ><requestBody>
    <dataSet rootEntity="ApontamentoPA" includePresentationFields="S" datasetid="1658322435343_10">
    <entity path=""><fieldset list="*"/><field name="CONTROLEPA"/></entity>
    <entity path="Produto"><fieldset list="DECQTD,TIPCONTEST"/></entity>
    <entity path="MotivosPerda"><field name="DESCRICAO"/></entity>
        <dataRow>
            <localFields>
                <QTDAPONTADA>{qnt_param}</QTDAPONTADA>
            </localFields>
            <key>
                <NUAPO>{nuapo_param}</NUAPO>
                <SEQAPA>{seqapa_param}</SEQAPA>
            </key>
        </dataRow>
    </dataSet>
        </requestBody></serviceRequest>
        """

        response2 = requests.post(segunda_api_url, data=segunda_api_payload, headers=segunda_api_headers)

        info_from_xml = extract_info_from_xml(response2.text)
        if response2.status_code == 200:
            
            return jsonify(info_from_xml)  # Retorna a resposta da segunda API
        else:
            return jsonify({"error": "Erro ao acessar a segunda API"}), 500

    except Exception as e:
        info_from_xml = extract_info_from_xml(response2.text)

        return jsonify(info_from_xml), 500

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
