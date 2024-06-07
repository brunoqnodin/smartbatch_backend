const express = require('express');
const request = require('request');
const iconv = require('iconv-lite');
const dotenv = require('dotenv');

// Carregar variáveis de ambiente do arquivo .env
dotenv.config();

const app = express();

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }

  next();
});

const loginAndGetSession = (callback) => {
  const url = `${process.env.API_URL}/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json`;
  const headers = { "Content-Type": "application/json" };
  const payload = {
    "serviceName": "MobileLoginSP.login",
    "requestBody": {
      "NOMUSU": { "$": process.env.NOMUSU },
      "INTERNO": { "$": process.env.INTERNO },
      "KEEPCONNECTED": { "$": process.env.KEEPCONNECTED }
    }
  };

  request.post({ url, json: payload, headers }, (error, response, body) => {
    if (error || response.statusCode !== 200) {
      return callback(error || new Error("Erro ao acessar a primeira API"));
    }
    const cookie = response.headers['set-cookie'][0];
    const jsessionid = cookie.split(';')[0];
    callback(null, jsessionid);
  });
};

const executeQuery = (jsessionid, sql, res) => {
  const url = `${process.env.API_URL}/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json`;
  const headers = {
    "Content-Type": "application/json",
    "Cookie": jsessionid
  };
  const payload = {
    "serviceName": "DbExplorerSP.executeQuery",
    "requestBody": { "sql": sql }
  };

  request.post({ url, json: payload, headers }, (error, response, body) => {
    if (error || response.statusCode !== 200) {
      res.status(500).json({ error: "Erro ao acessar a segunda API" });
    } else {
      res.json(body);
    }
  });
};

app.get('/centros_trabalho', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = "select CODWCP, NOME, WCP.CODCWC, CWC.DESCRICAO FROM TPRWCP WCP JOIN TPRCWC CWC ON CWC.CODCWC = WCP.CODCWC WHERE CODWCP <> 0 AND WCP.CODCWC = 5";
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/materia_prima', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = "SELECT TOP 10 PROPA.REFERENCIA AS codEan, PROPA.DESCRPROD AS nomeMp, PROPA.CODPROD AS codProduto, PROPA.CODVOL AS unidade, 1 AS qtdPA, PROMP.CODPROD AS codMp, PROMP.DESCRPROD as nomeMp, MP.QTDMISTURA AS qtdMP FROM TPRLMP MP JOIN TGFPRO PROMP ON PROMP.CODPROD = MP.CODPRODMP JOIN TGFPRO PROPA ON PROPA.CODPROD = MP.CODPRODPA where PROPA.CODVOL = 'L'";
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/materia_prima_produto', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = `SELECT TOP 1 PROPA.REFERENCIA AS codEan, PROPA.DESCRPROD AS nomeMp, PROPA.CODPROD AS codProduto, PROPA.CODVOL AS unidade, 1 AS qtdPA, PROMP.CODPROD AS codMp, PROMP.DESCRPROD as nomeMp, MP.QTDMISTURA AS qtdMP FROM TPRLMP MP JOIN TGFPRO PROMP ON PROMP.CODPROD = MP.CODPRODMP JOIN TGFPRO PROPA ON PROPA.CODPROD = MP.CODPRODPA where PROPA.CODVOL = 'L' AND PROPA.CODPROD = ${req.query.codProduto}`;
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/produto', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = "SELECT PRO.CODPROD AS codProduto, PRO.DESCRPROD AS nomeProduto, PRO.CODGRUPOPROD AS CodfamiliaProduto, GRU.DESCRGRUPOPROD AS familiaProduto, PRO.CODVOL AS unidMedida FROM TGFPRO PRO JOIN TGFGRU GRU ON GRU.CODGRUPOPROD = PRO.CODGRUPOPROD WHERE PRO.ATIVO <> 'N' AND GRU.DESCRGRUPOPROD in ('MP','EM','PI','PP','PA')";
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/funcionarios', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = "SELECT ECD.CODIGO AS codFuncionario, USU.NOMEUSU AS nome, '' AS cargo, USU.CODGRUPO, GRU.NOMEGRUPO FROM TPRECD ECD JOIN TSIUSU USU ON USU.CODUSU = ECD.CODIGO JOIN TSIGRU GRU ON GRU.CODGRUPO = USU.CODGRUPO WHERE ISNULL(DTLIMACESSO,'') = ''";
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/login', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = `SELECT ECD.CODIGO AS codFuncionario, USU.NOMEUSU AS nome, '' AS cargo, USU.CODGRUPO, GRU.NOMEGRUPO FROM TPRECD ECD JOIN TSIUSU USU ON USU.CODUSU = ECD.CODIGO JOIN TSIGRU GRU ON GRU.CODGRUPO = USU.CODGRUPO WHERE ISNULL(DTLIMACESSO,'') = '' AND ECD.CODIGO = ${req.query.matricula}`;
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/ordem_producao', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = "SELECT * FROM SANKHYA_TEST.sankhya.AD_VAPP_OPS_SMART WHERE codCentro <> 51";
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/ordem_producao_detail', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = `SELECT codOrdem, codProduto, descProduto, codCentro, descCentro, processo, lote, localOrigem, localDestino, DHINICIO, DHFINAL, DATASEQ, QTD_APRODUZ, QTD_PRODUZ, STATUSOP, CODMTP, MOTPARADA, IDIATV FROM SANKHYA_TEST.sankhya.AD_VAPP_OPS_SMART WHERE codOrdem = ${req.query.codOrdem}`;
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/ordem_producao_centro', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = `SELECT codOrdem, codProduto, descProduto, codCentro, descCentro, processo, lote, localOrigem, localDestino, DHINICIO, DHFINAL, DATASEQ, QTD_APRODUZ, QTD_PRODUZ, STATUSOP FROM SANKHYA_PROD.sankhya.AD_VAPP_OPS_SMART WHERE STATUSOP <> 'Finalizado' AND codCentro = ${req.query.codCentro}`;
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/motivo_paradas', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = "select CODMTP as codParada, DESCRICAO AS motivoParada, '' AS tipoParada from TPRMTP WHERE ATIVO <> 'N'";
    executeQuery(jsessionid, sql, res);
  });
});

app.get('/fluxo2', (req, res) => {
  const loginUrl = `${process.env.API_URL}/mge/service.sbr?serviceName=MobileLoginSP.login`;
  const loginHeaders = {
    "Content-Type": "application/json"
  };
  const loginPayload = {
    "serviceName": "MobileLoginSP.login",
    "requestBody": {
      "NOMUSU": { "$": process.env.NOMUSU },
      "INTERNO": { "$": process.env.INTERNO },
      "KEEPCONNECTED": { "$": process.env.KEEPCONNECTED }
    }
  };

  request.post({ url: loginUrl, json: loginPayload, headers: loginHeaders, encoding: null }, (error, response, body) => {
    if (error) {
      res.status(500).json({ error: "Erro ao acessar a primeira API" });
    } else if (response.statusCode === 200) {
      const cookie = response.headers['set-cookie'][0];
      const jsessionid = cookie.split(';')[0];

      const segundaApiUrl = `${process.env.API_URL}/mge/service.sbr?serviceName=DbExplorerSP.executeQuery`;
      const segundaApiHeaders = {
        "Content-Type": "application/json",
        "Cookie": jsessionid
      };
      const segundaApiPayload = {
        "serviceName": "DbExplorerSP.executeQuery",
        "requestBody": {
          "sql": "SELECT PRO.CODPROD as codProduto, pre.descpre as etapa, PRE.SEQPRE as prioridade, pre.TEMPO as tempoAgitacao FROM AD_MODPRE PRE LEFT JOIN TGFPRO PRO ON PRO.CODPROD = PRE.CODPROD WHERE PRO.CODPROD = '1130289'"
        }
      };

      request.post({ url: segundaApiUrl, json: segundaApiPayload, headers: segundaApiHeaders, encoding: null }, (error2, response2, body2) => {
        if (error2) {
          res.status(500).json({ error: "Erro ao acessar a segunda API" });
        } else if (response2.statusCode === 200) {
          const responseBody = iconv.decode(Buffer.from(body2, 'utf-8'), 'utf-8');
          res.json(responseBody);
        } else {
          res.status(500).json({ error: "Erro ao acessar a segunda API" });
        }
      });
    } else {
      res.status(500).json({ error: "Erro ao acessar a primeira API" });
    }
  });
});

app.get('/fluxo', (req, res) => {
  loginAndGetSession((err, jsessionid) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    const sql = "SELECT PRO.CODPROD as codProduto, pre.descpre as etapa, PRE.SEQPRE as prioridade, pre.TEMPO as tempoAgitacao FROM AD_MODPRE PRE LEFT JOIN TGFPRO PRO ON PRO.CODPROD = PRE.CODPROD WHERE PRO.CODPROD = '1130289'";
    executeQuery(jsessionid, sql, res);
  });
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
