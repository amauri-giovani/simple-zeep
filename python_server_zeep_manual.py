from lxml import etree
from flask import Flask, request, Response

app = Flask(__name__)

# Mapeamento de namespaces
NAMESPACES = {
    'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
    'simp': 'http://example.com/simple'
}

def process_soap_request(request_xml):
    try:
        print("Requisição Recebida:")
        print(request_xml.decode())

        # Parse da requisição recebida
        tree = etree.fromstring(request_xml)

        # Extração do nome do elemento usando namespaces
        name_element = tree.find(".//simp:name", namespaces=NAMESPACES)
        if name_element is None or not name_element.text:
            raise ValueError("Elemento 'name' não encontrado ou vazio")

        name = name_element.text.strip()

        # Construção programática da resposta conforme o WSDL
        envelope = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Envelope", nsmap=NAMESPACES)
        body = etree.SubElement(envelope, "{http://schemas.xmlsoap.org/soap/envelope/}Body")
        response = etree.SubElement(body, "{http://example.com/simple}SimpleResponse")
        greeting = etree.SubElement(response, "{http://example.com/simple}greeting")
        greeting.text = f"Hello, {name}!"

        # Serializa o XML para string
        response_xml = etree.tostring(envelope, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        print("Resposta Gerada:")
        print(response_xml.decode())
        return response_xml
    except Exception as e:
        # Tratamento de erro genérico
        error_message = f"<error>{str(e)}</error>"
        return error_message

@app.route("/service", methods=["POST"])
def soap_service():
    request_xml = request.data
    response_xml = process_soap_request(request_xml)
    return Response(response_xml, content_type="text/xml")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
