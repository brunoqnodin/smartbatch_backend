import cursor as cursor
import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
import random
import requests
import xml.etree.ElementTree as ET
import base64


@app.route('/getFunc')
def getFunc():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, codigo, nome, cargo FROM funcionarios")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/getHWAuto')
def getHWAuto():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT cod_centro, centro, IFNULL(mac, '-') as mac, IFNULL(corrente1, 0) as corrente1, IFNULL(temperatura, '-') as temperatura,IFNULL(data_insert, CURRENT_TIMESTAMP()) as data_insert FROM view_auto_senai")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/GetCentrosAuto')
def getcentrosauto():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT cod_centro, centro, IFNULL(mac, '-') as mac, IFNULL(corrente1, 0) as corrente1, IFNULL(temperatura, '-') as temperatura, IFNULL(data_insert, CURRENT_TIMESTAMP()) as data_insert FROM view_auto_senai")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/brindes')
def getBrindes():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM brindes")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/sortear', methods=['POST'])
def sortear_brinde():
    # Crie uma conexão e obtenha um cursor
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM brindes WHERE quantidade_disponivel > 0')
    brindes_disponiveis = cursor.fetchall()

    if not brindes_disponiveis:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Nenhum brinde disponível para sorteio'})

    brinde_sorteado = random.choice(brindes_disponiveis)
    cursor.execute('UPDATE brindes SET quantidade_disponivel = quantidade_disponivel - 1 WHERE id = %s', (brinde_sorteado['id'],))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify(brinde_sorteado)


@app.route('/getIST')
def getColetor():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM coletor_senai ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/getIST2')
def getColetor2():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM coletor_senai2 ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/getIST3')
def getColetor3():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM auto_senai ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/postIST2', methods=['POST'])
def post2():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
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
        conn.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        # response.data = cursor.lastrowid
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()
        return (response)

@app.route('/postIST3', methods=['POST'])
def post3():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
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
        conn.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        # response.data = cursor.lastrowid
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()
        return (response)

@app.route('/postLead', methods=['POST'])
def lead():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        json_data = request.get_json(force=True)
        _nome = json_data['nome']
        _empresa = json_data['empresa']
        _telefone = json_data['telefone']
        _email = json_data['email']
        insert_user_cmd = """INSERT INTO cad_leads (nome, empresa, telefone, email) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_user_cmd, (_nome, _empresa, _telefone, _email))
        conn.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        # response.data = cursor.lastrowid
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()
        return (response)

@app.route('/postParada', methods=['POST'])
def parada():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        json_data = request.get_json(force=True)
        _cod_centro = json_data['cod_centro']
        _cod_ordem = json_data['cod_ordem']
        _operador = json_data['operador']
        _motivo = json_data['motivo']
        _tim = json_data['tim']
        _etapa = json_data['etapa']
        insert_user_cmd = """INSERT INTO alerta_parada (cod_centro, cod_ordem, operador, motivo, tim, etapa) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_user_cmd, (_cod_centro, _cod_ordem, _operador, _motivo, _tim, _etapa))
        conn.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        # response.data = cursor.lastrowid
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()
        return (response)

@app.route('/postIST', methods=['POST'])
def post():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        json_data = request.get_json(force=True)
        _mac = json_data['mac']
        _identificador = json_data['identificador']
        _valor = json_data['valor']
        _data = json_data['data']
        insert_user_cmd = """INSERT INTO coletor_senai (mac, identificador, valor, data) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_user_cmd, (_mac, _identificador, _valor, _data))
        conn.commit()
        response = jsonify(message='Valor Inserido com Sucesso', id=cursor.lastrowid)
        # response.data = cursor.lastrowid
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Erro Brabissimo Senai')
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()
        return (response)

@app.route('/sintetico_data/<string:data>')
def user(data):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id as id_SMARTgears, linha_turno as centro_de_trabalho, cod_produto, descricao_produto, turno, programado_linha as programado, cod_ordem as cod_ordem_sap, refugo, IF(status = 2, ((((hist+valor_temp)*multiplos)+manual)-refugo), ((((hist)*multiplos)+manual)-refugo)) as produzido, data_inicio as data FROM view_total_hist WHERE empresa = '00153282000167' AND data_inicio = %s ORDER BY data_inicio DESC, linha_turno ASC", data)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/detalhe/<string:data>')
def detalhe(data):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT `view_total_hist`.`id` AS `id`, `view_total_hist`.`cod_ordem` AS `cod_ordem`, `view_total_hist`.`id_linha` AS `id_linha`, `view_total_hist`.`linha_turno` AS `linha_turno`, `view_total_hist`.`cod_produto` AS `cod_produto`, `view_total_hist`.`descricao_produto` AS `desc_produto`, `view_total_hist`.`programado_linha` AS `meta_hora`, round(`view_total_hist`.`programado_linha` * 7.33,0) AS `meta_total`, `view_total_hist`.`valor_temp` AS `valor_temp`, `view_total_hist`.`manual` AS `manual`, `view_total_hist`.`refugo` AS `refugo`, (SELECT tipo FROM status_ordem WHERE id = `view_total_hist`.`status`) as `status`, `view_total_hist`.`empresa` AS `empresa`, ((`view_total_hist`.`valor_temp` + `view_total_hist`.`manual`) * `view_total_hist`.`multiplos` - `view_total_hist`.`refugo`) as total, IF((timestampdiff(HOUR,(select `mudanca_status_meta`.`data` from `mudanca_status_meta` where `mudanca_status_meta`.`id_meta` = `view_total_hist`.`id` and `mudanca_status_meta`.`id_status` = 2 order by `mudanca_status_meta`.`id` limit 1),current_timestamp())) = 0 ,1, (timestampdiff(HOUR,(select `mudanca_status_meta`.`data` from `mudanca_status_meta` where `mudanca_status_meta`.`id_meta` = `view_total_hist`.`id` and `mudanca_status_meta`.`id_status` = 2 order by `mudanca_status_meta`.`id` limit 1),current_timestamp()))) as fer, (((`view_total_hist`.`valor_temp` + `view_total_hist`.`manual`) * `view_total_hist`.`multiplos` - `view_total_hist`.`refugo`)/(if(current_timestamp() > concat(`view_total_hist`.`data_final`,' ',(select `cad_turno`.`hora_fim` from `cad_turno` where `cad_turno`.`turno` = `view_total_hist`.`turno` and `cad_turno`.`empresa` = `view_total_hist`.`empresa`)),round(`view_total_hist`.`programado_linha` * 7.33,0),round(`view_total_hist`.`programado_linha` * IF((timestampdiff(HOUR,(select `mudanca_status_meta`.`data` from `mudanca_status_meta` where `mudanca_status_meta`.`id_meta` = `view_total_hist`.`id` and `mudanca_status_meta`.`id_status` = 2 order by `mudanca_status_meta`.`id` limit 1),current_timestamp())) = 0 ,1, (timestampdiff(HOUR,(select `mudanca_status_meta`.`data` from `mudanca_status_meta` where `mudanca_status_meta`.`id_meta` = `view_total_hist`.`id` and `mudanca_status_meta`.`id_status` = 2 order by `mudanca_status_meta`.`id` limit 1),current_timestamp()))),0))))as performance, IFNULL((if(`view_total_hist`.`valor_temp` + `view_total_hist`.`manual` + `view_total_hist`.`hist` - `view_total_hist`.`refugo` = 0,(`view_total_hist`.`valor_temp` + `view_total_hist`.`manual` + `view_total_hist`.`hist` - `view_total_hist`.`refugo`) / 1 * 100,(`view_total_hist`.`valor_temp` + `view_total_hist`.`manual` + `view_total_hist`.`hist` - `view_total_hist`.`refugo`) / (`view_total_hist`.`valor_temp` + `view_total_hist`.`manual` + `view_total_hist`.`hist`))),0) AS `qualidade`, 1 as disponibilidade from `view_total_hist` WHERE (`view_total_hist`.`data_inicio` = CURRENT_DATE() OR `view_total_hist`.`data_final` = CURRENT_DATE()) AND id_linha = %s AND `view_total_hist`.`status` = 2 ORDER BY hora_inicio DESC LIMIT 1", data)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



@app.route('/centros_trabalho', methods=['GET'])
def get_centros_trabalho():
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
        return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400

    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
    

@app.route('/motivo_paradas', methods=['GET'])
def get_motivo_paradas():
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
        return jsonify({"error": "O parâmetro 'codseq' é obrigatório"}), 400
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
        return jsonify({"error": "O parâmetro 'codcentro' é obrigatório"}), 400
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
        return jsonify({"error": "O parâmetro 'centro' é obrigatório"}), 400
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
    # Obtendo o parâmetro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.continuarInstanciaAtividades&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    # Corpo da segunda requisição com o parâmetro da URL
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

    # Extraindo informações do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)


@app.route('/post_iniciarop', methods=['GET'])
def post_iniciarop():
    # Obtendo o parâmetro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv', default='1')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.iniciarInstanciaAtividades&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    # Corpo da segunda requisição com o parâmetro da URL
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

    # Extraindo informações do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)


@app.route('/post_parar_maquina', methods=['GET'])
def post_parar_maquina():
    # Obtendo o parâmetro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')
    codmtp_param = request.args.get('codmtp')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?application=OperacaoProducao&mgeSession={jsessionid}&serviceName=OperacaoProducaoSP.pararInstanciaAtividades"

    # Corpo da segunda requisição com o parâmetro da URL
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

    # Extraindo informações do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_finalizarop', methods=['GET'])
def post_finalizarop():
    # Obtendo o parâmetro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')
    idefx_param = request.args.get('idefx')
    idiproc_param = request.args.get('idiproc')
    idproc_param = request.args.get('idproc')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.finalizarInstanciaAtividades&mgeSession={jsessionid}"

    # Corpo da segunda requisição com o parâmetro da URL
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

    # Extraindo informações do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_realocacentro', methods=['GET'])
def post_realocacentro():
    # Obtendo o parâmetro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')
    idiproc_param = request.args.get('idiproc')
    codwcp_param = request.args.get('codwcp')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?application=OperacaoProducao&mgeSession={jsessionid}&serviceName=OperacaoProducaoSP.realocarCentroDeTrabalhoPorCategoria"

    # Corpo da segunda requisição com o parâmetro da URL
    body_post = f"""
        <serviceRequest serviceName="OperacaoProducaoSP.realocarCentroDeTrabalhoPorCategoria">
            <requestBody>
                <params idiproc="{idiproc_param}" idiatv="{idiatv_param}" codwcp="{codwcp_param}" isWorkCenterPadrao="true"/>
            </requestBody>
        </serviceRequest>
    """

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informações do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)


@app.route('/post_criaapontamento', methods=['GET'])
def post_criaapontamento():
    # Obtendo o parâmetro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.criarApontamento&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    # Corpo da segunda requisição com o parâmetro da URL
    body_post = f"""
    <serviceRequest serviceName="OperacaoProducaoSP.criarApontamento">
    <requestBody>
        <params IDIATV="{idiatv_param}" QTDAPONTADA="1"/>
    </requestBody>
    </serviceRequest>
    """

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informações do XML retornado
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

    # Criando um dicionário com os resultados
    result_dict = {
        'status': status,
        'statusMessage': status_message,
        'NUAPO': nuapo,
        'LISTAPENDENTES': listapendentes
    }

    return jsonify(result_dict)

@app.route('/post_salvarapontamento3', methods=['GET'])
def post_salvarapontamento3():
    # Obtendo o parâmetro da URL para a tag IDIATV
    qnt_param = request.args.get('qnt')
    nuapo_param = request.args.get('nuapo')
    seqapa_param = request.args.get('seqapa')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mge/service.sbr?serviceName=CRUDServiceProvider.saveRecord&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"
    
    # Corpo da segunda requisição com o parâmetro da URL
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

    # Extraindo informações do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_confirmarapontamento', methods=['GET'])
def post_confirmarapontamento():
    # Obtendo o parâmetro da URL para a tag IDIATV
    idiatv_param = request.args.get('idiatv')
    nuapo_param = request.args.get('nuapo')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')

    # Realizando o segundo POST
    url_post = f"http://179.185.45.146:8280/mgeprod/service.sbr?serviceName=OperacaoProducaoSP.confirmarApontamento&application=OperacaoProducao&mgeSession={jsessionid}&resourceID=br.com.sankhya.producao.cad.OperacaoProducao"

    # Corpo da segunda requisição com o parâmetro da URL
    body_post = f"""
        <serviceRequest serviceName="mgeprod@OperacaoProducaoSP.confirmarApontamento">
            <requestBody>
                <params NUAPO="{nuapo_param}" IDIATV="{idiatv_param}" ACEITARQTDMAIOR="false" ULTIMOAPONTAMENTO="false" RESPOSTA_ULTIMO_APONTAMENTO="false"/>
            </requestBody>
        </serviceRequest>
    """
    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informações do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_salvarapontamento2', methods=['GET'])
def post_salvarapontamento2():
    # Obtendo o parâmetro da URL para a tag IDIATV
    #qnt_param = request.args.get('qnt')
    #nuapo_param = request.args.get('nuapo')
    #seqapa_param = request.args.get('seqapa')

    url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json"
    headers = {'Content-Type': 'application/json'}

    # Corpo da requisição
    body = {
        "serviceName": "MobileLoginSP.login",
        "requestBody": {
            "NOMUSU": {"$": "IRANILDO"},
            "INTERNO": {"$": "123456"},
            "KEEPCONNECTED": {"$": "S"}
        }
    }

    # Fazendo a requisição
    response = requests.post(url, json=body, headers=headers)
    
    # Obtendo o jsessionid da resposta
    jsessionid = response.json().get('responseBody', {}).get('jsessionid', {}).get('$', '')
    print(jsessionid)
    # Realizando o segundo POST
    #url_post = f"http://179.185.45.146:8280/mge/service.sbr?serviceName=CRUDServiceProvider.saveRecord&application=OperacaoProducao&resourceID=br.com.sankhya.producao.cad.OperacaoProducao&mgeSession={jsessionid}"
    url_post = f"http://179.185.45.146:8280/mge/service.sbr?serviceName=CRUDServiceProvider.saveRecord&application=OperacaoProducao&resourceID=br.com.sankhya.producao.cad.OperacaoProducao&mgeSession={jsessionid}"
    print(url_post)
    # Corpo da segunda requisição com o parâmetro da URL
    body_post = f'''
    <serviceRequest serviceName=\"CRUDServiceProvider.saveRecord\" ><requestBody>\r\n    <dataSet rootEntity=\"ApontamentoPA\" includePresentationFields=\"S\" datasetid=\"1658322435343_10\">\r\n    <entity path=\"\"><fieldset list=\"*\"/><field name=\"CONTROLEPA\"/></entity>\r\n    <entity path=\"Produto\"><fieldset list=\"DECQTD,TIPCONTEST\"/></entity>\r\n    <entity path=\"MotivosPerda\"><field name=\"DESCRICAO\"/></entity>\r\n        <dataRow>\r\n            <localFields>\r\n                <QTDAPONTADA>10</QTDAPONTADA>\r\n            </localFields>\r\n            <key>\r\n                <NUAPO>92959</NUAPO>\r\n                <SEQAPA>1</SEQAPA>\r\n            </key>\r\n        </dataRow>\r\n    </dataSet>\r\n        </requestBody></serviceRequest>
    '''
    print(body_post)

    # Fazendo o segundo POST
    response_post = requests.post(url_post, data=body_post, headers={'Content-Type': 'application/xml'})

    # Extraindo informações do XML retornado
    info_from_xml = extract_info_from_xml(response_post.text)

    return jsonify(info_from_xml)

@app.route('/post_salvarapontamento', methods=['GET'])
def post_salvarapontamento():
    # Configuração da primeira solicitação HTTP
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

        # Configuração da segunda solicitação usando o cookie da primeira API
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
