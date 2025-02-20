from zeep import Client, Settings
from lxml import etree  # Opcional, para manipulação de XML (se necessário)

# Caminho do WSDL (ajuste conforme necessário)
caminho_wsdl = '/home/amauri/Amauri/projects/simple-zeep/static/simple_service.wsdl'

# Crie um cliente Zeep com configurações apropriadas
configuracoes = Settings(xml_huge_tree=True)  # Recomendado para WSDLs grandes
cliente = Client(caminho_wsdl, settings=configuracoes)

def enviar_requisicao_soap(nome):
  """Envia uma requisição SOAP para o serviço com o nome fornecido.

  Args:
      nome: O nome a ser usado na requisição.

  Returns:
      A resposta SOAP como uma string.
  """

  # Crie a mensagem de requisição SOAP
  mensagem_requisicao = cliente.create_message(cliente.service, "SayHello", name=nome)

  # Envie a requisição e obtenha a resposta
  resposta = cliente.service.SayHello(mensagem_requisicao)

  # Converta a resposta em uma string (opcional, para processamento posterior)
  resposta_xml = etree.tostring(resposta, pretty_print=True, encoding='utf-8', xml_declaration=True)

  return resposta_xml

# Exemplo de uso
nome = "Bard"
resposta_xml = enviar_requisicao_soap(nome)
print(resposta_xml)
