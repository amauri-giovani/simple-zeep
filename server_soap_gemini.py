from flask import Flask, request, Response
from zeep import Client, xsd
from lxml import etree
import os

app = Flask(__name__)

# Caminho para o WSDL
wsdl_path = os.path.join(os.path.dirname(__file__), 'static', 'simple_service.wsdl')
client = Client(f'file://{wsdl_path}')  # Inicializa o cliente Zeep com o WSDL

def process_soap_request(request_xml):
    print("Requisição Recebida:")
    print(request_xml.decode())

    try:
        # Parse da requisição
        tree = etree.fromstring(request_xml)

        print("Recebido XML:")
        print(etree.tostring(tree, pretty_print=True).decode())

        namespaces = {
            "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
            "sim": "http://example.com/simple"
        }

        # Extrai o valor de 'name'
        name_element = tree.find(".//sim:name", namespaces=namespaces)
        if name_element is None or not name_element.text.strip():
            raise ValueError("Elemento 'name' não encontrado ou vazio")

        name = name_element.text.strip()

        # Usando o Zeep para criar a resposta (CORREÇÃO CRUCIAL)
        # CRUCIAL: Usando client.create_message para a resposta
        SimpleResponse = client.get_type("tns:SimpleResponse")  # Obtém o tipo do WSDL
        response_data = SimpleResponse(greeting=f"Hello, {name}!")  # Cria a instancia do objeto de resposta
        envelope = client.create_message(client.service, "SayHello", parameters=response_data)  # Cria o envelope SOAP

        response_xml = etree.tostring(envelope, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        return response_xml

    except Exception as e:
        # Tratamento de erro com namespaces
        fault = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Fault")
        faultcode = etree.SubElement(fault, "faultcode")
        faultstring = etree.SubElement(fault, "faultstring")
        faultstring.text = str(e)
        body = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Body")
        body.append(fault)
        envelope = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Envelope")
        envelope.append(body)

        response_xml = etree.tostring(envelope, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        return response_xml
    except Exception as e:
        # Em caso de erro, retorna o erro no formato SOAP (com namespaces corretos)
        fault = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Fault")
        faultcode = etree.SubElement(fault, "faultcode")
        faultstring = etree.SubElement(fault, "faultstring")
        faultstring.text = str(e)
        body = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Body")
        body.append(fault)
        envelope = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Envelope")
        envelope.append(body)

        response_xml = etree.tostring(envelope, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        return response_xml


@app.route("/service", methods=["POST"])
def soap_service():
    request_xml = request.data
    response_xml = process_soap_request(request_xml)
    return Response(response_xml, content_type="text/xml")


if __name__ == "__main__":
    app.run(debug=True, port=8000)