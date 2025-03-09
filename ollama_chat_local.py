#Código de exemplo para interação local com modelos LLM executados no ollama

from ollama import Client
client = Client(
  host='http://45.71.195.113:11434',
  headers={'x-some-header': 'some-value'}
)
response = client.chat(model='llama2:latest', messages=[
  {
    'role': 'user',
    'content': 'responde em pt-BR português do Brasil: defina o que é risco inerente?',
  },
])

print(response)
