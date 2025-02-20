from flask import Flask, request, Response
from lxml import etree
from flask import send_from_directory
import os

app = Flask(__name__)

# Mapeamento de namespaces
NAMESPACES = {
    'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
    'simp': 'http://example.com/simple'
}


@app.route('/service?wsdl', methods=["GET"])
def serve_wsdl():
    wsdl_file = os.path.join(os.getcwd(), "static", "simple_service.wsdl")
    return send_from_directory(os.path.dirname(wsdl_file), os.path.basename(wsdl_file), mimetype='application/xml')


def process_soap_request(request_xml):
    print(request_xml.decode())

    try:
        # Parse da requisição
        tree = etree.fromstring(request_xml)

        # Extrair o valor de 'name' (considerando namespaces)
        name_element = tree.find(".//simp:name", namespaces=NAMESPACES)
        if name_element is None or name_element.text is None:
            return "<error>Element 'name' not found</error>"

        name = name_element.text

        # Criação da resposta SOAP
        response = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:simp="http://example.com/simple">
            <soapenv:Body>
                <simp:SimpleResponse>
                    <simp:greeting>Hello, {name}!</simp:greeting>
                </simp:SimpleResponse>
            </soapenv:Body>
        </soapenv:Envelope>
        """
        return response
    except Exception as e:
        return f"<error>{str(e)}</error>"

@app.route("/service", methods=["POST"])
def soap_service():
    request_xml = request.data
    response_xml = process_soap_request(request_xml)
    return Response(response_xml, content_type="text/xml")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
