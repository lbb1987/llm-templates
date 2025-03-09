#Código Python para interação via chat com modelos huggingface executando localmente na etação de trabalho

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Verificar se uma GPU está disponível e usar se possível
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Carregar o modelo e o tokenizer a partir do diretório local
model_name = "caminho/para/seu/modelo"  # Substitua pelo caminho do seu modelo local
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# Função para gerar resposta
def generate_response(prompt):
    inputs = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt').to(device)
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Loop de interação
print("Você pode começar a conversar! (Digite 'sair' para encerrar)")
while True:
    user_input = input("Você: ")
    if user_input.lower() == 'sair':
        break
    response = generate_response(user_input)
    print("Modelo:", response)
