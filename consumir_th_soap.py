from zeep import Client, Settings


# url = 'https://th-soap.itmss.com.br/wsdl'
# url = 'https://www.argoit.com.br/th/ws/interface3.asmx?wsdl'
url = '/home/amauri/Amauri/projects/simple-zeep/static/simple_service.wsdl'
client = Client(url, settings=Settings(xml_huge_tree=True))

login = "ons.api"
senha = "On5@2024"
empresa = "onsorg"

xml = """
<xml>
<dataIni>2024-12-20</dataIni>
<dataFin>2024-12-25</dataFin>
</xml>
"""

# response = client.service.GetToken(login=login, senha=senha, empresa=empresa)

# print(response)
print()