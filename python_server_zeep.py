from flask import Flask, request, Response
from zeep import Client, Settings
from lxml import etree
import os

app = Flask(__name__)

# Ensure correct WSDL path (adjust as needed)
wsdl_path = os.path.join(os.path.dirname(__file__), 'static', 'simple_service.wsdl')

# Load WSDL with appropriate settings
try:
    client = Client(f'file://{wsdl_path}', settings=Settings(xml_huge_tree=True))
except Exception as e:
    print(f"Error loading WSDL: {e}")
    exit()

def process_soap_request(request_xml):
    try:
        tree = etree.fromstring(request_xml)
        namespaces = {"ns0": "http://example.com/simple"}  # Match WSDL namespace

        name_element = tree.find(".//ns0:name", namespaces=namespaces)
        if name_element is None:
            raise ValueError("Elemento 'name' não encontrado.")
        name = name_element.text

        # **Robust Type Access (using namespace):**
        SimpleResponse = client.get_type("{http://example.com/simple}SimpleResponse")
        response = SimpleResponse(greeting=f"Hello, {name}!")

        envelope = client.create_message(client.service, "SayHello", parameters=response)
        response_xml = etree.tostring(envelope, pretty_print=True, encoding="utf-8", xml_declaration=True)
        return response_xml

    except Exception as e:
        # Trata erros e retorna uma resposta SOAP de Fault
        fault_xml = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Body>
                <soapenv:Fault>
                    <faultcode>soapenv:Server</faultcode>
                    <faultstring>{str(e)}</faultstring>
                </soapenv:Fault>
            </soapenv:Body>
        </soapenv:Envelope>
        """.encode('utf-8')  # Codifica para bytes
        return fault_xml

@app.route('/service', methods=['POST'])
def soap_service():
    request_xml = request.data
    response_xml = process_soap_request(request_xml)
    return Response(response_xml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
