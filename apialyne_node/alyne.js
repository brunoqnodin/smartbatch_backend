const express = require('express');
const request = require('request');
const app = express();

// Rota para consulta da primeira API
app.get('/consulta-api1', (req, res) => {
  const url = "http://179.185.45.146:8280/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json";
  const headers = {
    "Content-Type": "application/json"
  };
  const payload = {
    "serviceName": "MobileLoginSP.login",
    "requestBody": {
      "NOMUSU": { "$": "TESTE" },
      "INTERNO": { "$": "CIGEL@123" },
      "KEEPCONNECTED": { "$": "S" }
    }
  };

  request.post({ url, json: payload, headers }, (error, response, body) => {
    if (error) {
      res.status(500).json({ error: "Erro ao acessar a primeira API" });
    } else if (response.statusCode === 200) {
      // Extrai o cookie JSESSIONID da resposta
      const cookie = response.headers['set-cookie'][0];
      const jsessionid = cookie.split(';')[0];

      // Rota para consulta da segunda API usando o cookie
      const segundaApiUrl = "http://179.185.45.146:8280/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json";
      const segundaApiHeaders = {
        "Content-Type": "application/json",
        "Cookie": jsessionid  // Usando o cookie da primeira API
      };
      const segundaApiPayload = {
        "serviceName": "DbExplorerSP.executeQuery",
        "requestBody": {
          "sql": "select CODWCP, NOME, WCP.CODCWC, CWC.DESCRICAO FROM TPRWCP WCP JOIN TPRCWC CWC ON CWC.CODCWC = WCP.CODCWC WHERE CODWCP <> 0 AND WCP.CODCWC = 5"
        }
      };

      request.post({ url: segundaApiUrl, json: segundaApiPayload, headers: segundaApiHeaders }, (error2, response2, body2) => {
        if (error2) {
          res.status(500).json({ error: "Erro ao acessar a segunda API" });
        } else if (response2.statusCode === 200) {
          res.json({ api1Response: body, api2Response: body2 });
        } else {
          res.status(500).json({ error: "Erro ao acessar a segunda API" });
        }
      });
    } else {
      res.status(500).json({ error: "Erro ao acessar a primeira API" });
    }
  });
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
