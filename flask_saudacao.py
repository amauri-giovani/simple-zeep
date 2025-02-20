from flask import Flask, request, make_response
from lxml import etree

app = Flask(__name__)

@app.route('/saudacao', methods=['POST'])
def saudacao():
    try:
        xml_request = etree.fromstring(request.data)
        nome = xml_request.find('.//nome').text

        mensagem = f"Olá, {nome}!"

        # response_xml = f"""
        # <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        #     <soapenv:Body>
        #         <SaudacaoResponse xmlns="http://exemplo.com/saudacao">
        #             <mensagem>{mensagem}</mensagem>
        #         </SaudacaoResponse>
        #     </soapenv:Body>
        # </soapenv:Envelope>
        # """

        # Usando lxml para construir o XML com namespaces corretamente
        ns = {"tns": "http://exemplo.com/saudacao", "soapenv": "http://schemas.xmlsoap.org/soap/envelope/"}
        envelope = etree.Element("{%s}Envelope" % ns['soapenv'], nsmap=ns)
        body = etree.SubElement(envelope, "{%s}Body" % ns['soapenv'])
        saudacao_response = etree.SubElement(body, "{%s}SaudacaoResponse" % ns['tns'])
        mensagem_element = etree.SubElement(saudacao_response, "{%s}mensagem" % ns['tns'])
        mensagem_element.text = mensagem

        response_xml = etree.tostring(envelope, encoding="UTF-8", xml_declaration=True)

        response = make_response(response_xml)
        response.headers['Content-Type'] = 'application/soap+xml; charset=utf-8' # Content-Type correto
        return response

    except Exception as e:
        return f"Erro: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
