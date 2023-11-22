from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/consulta-soap', methods=['GET'])
def consulta_soap():
    try:
        url = 'http://ws.kplcloud.onclick.com.br/AbacosWserp.asmx'
        headers = {
            'Content-Type': 'application/soap+xml; charset=utf-8',
            'SOAPAction': 'http://www.kplsolucoes.com.br/ABACOSWebService/PedidosDisponiveis',
        }
        xml_body = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:kpl="http://www.kplsolucoes.com.br/ABACOSWebService">
                        <soapenv:Header/>
                        <soapenv:Body>
                            <kpl:PedidosDisponiveis>
                                <kpl:ChaveIdentificacao>3923D08F-6069-42CE-979A-D62B9D7AA60B</kpl:ChaveIdentificacao>
                            </kpl:PedidosDisponiveis>
                        </soapenv:Body>
                    </soapenv:Envelope>'''
        
        response = requests.post(url, data=xml_body, headers=headers)
        
        # Analisar a resposta XML
        root = ET.fromstring(response.content)
        namespace = {'kpl': 'http://www.kplsolucoes.com.br/ABACOSWebService'}
        resultado = root.find('.//kpl:PedidosDisponiveisResult', namespaces=namespace).text
        
        return jsonify({'resultado': resultado})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)