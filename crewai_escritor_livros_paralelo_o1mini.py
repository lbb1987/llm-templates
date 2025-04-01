import os
import concurrent.futures
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# Configuração das chaves da API
os.environ["SERPER_API_KEY"] = "chave"
os.environ["OPENAI_API_KEY"] = "chave"

# Definição do modelo de linguagem (LLM)
llm_gemini = LLM(
    model="openai/o1-mini",
    temperature=0.5,
)

# Instancia a ferramenta de pesquisa
search_tool = SerperDevTool(n_results=30)

# 🔎 Agente Pesquisador
pesquisador = Agent(
    role="Especialista em Pesquisa",
    goal="Identificar os 10 subtemas mais relevantes sobre {tema}",
    backstory="Pesquisador experiente, encontra e organiza conhecimento de forma clara.",
    tools=[search_tool],
    llm="gpt-4o-mini",
    verbose=True,
    memory=True
)

# 📖 Agente Planejador
planejador = Agent(
    role="Estrategista de Conteúdo",
    goal="Criar um esqueleto detalhado do livro",
    backstory="Especialista em estruturação de conteúdo e progressão lógica.",
    verbose=True,
    llm="gpt-4o-mini",
    memory=True
)

# ✍️ Agente Escritor
escritor = Agent(
    role="Escritor Profissional",
    goal="Escrever um livro completo sobre o tema {tema}, seguindo a estrutura definida",
    backstory="Transforma conhecimento complexo sobre {tema} em um material profundo, fluido e bem formatado.",
    verbose=True,
    llm=llm_gemini,
    memory=True
)

# 🛠️ Tarefas

# 1️⃣ Pesquisa de Subtemas (Executada primeiro)
pesquisa_task = Task(
    description=(
        "Pesquisar na internet e identificar os 10 subtemas mais relevantes para o livro sobre {tema}. "
        "Criar um mapa conceitual conectando os subtemas."
    ),
    expected_output="Relatório detalhado com os 10 subtemas e um mapa conceitual.",
    agent=pesquisador
)

# 2️⃣ Estruturação do Conteúdo (Executada após a pesquisa)
estrutura_task = Task(
    description=(
        "Criar um esqueleto detalhado do livro com título e capítulos:"
        "\n- Título principal"
        "\n- 10 capítulos sequenciais"
        "\n- Descrição de 1000-1500 palavras para cada capítulo"
    ),
    expected_output="Plano detalhado do livro com estrutura organizada.",
    agent=planejador
)

# Criando a equipe para pesquisa e estruturação (Execução sequencial)
etapas_iniciais = Crew(
    agents=[pesquisador, planejador],
    tasks=[pesquisa_task, estrutura_task],
    process=Process.sequential
)


# 🚀 Função para executar a escrita de um capítulo individualmente
def escrever_capitulo(numero, tema):
    """Cria uma Crew específica para escrever um capítulo e executa."""
    capitulo_task = Task(
        description=(
            f"Escrever o capítulo {numero} do livro sobre {tema} com base na estrutura planejada."
            "\nCada capítulo deve conter:"
            "\n- Introdução"
            "\n- Desenvolvimento com no mínimo 5 seções"
            "\n- Exemplos de código e prática de implementação"
            "\n- Explicação para leigos no tema"
            "\n- Conclusão conectando ao próximo capítulo"
        ),
        expected_output=f"Documento Markdown com o conteúdo do capítulo {numero}.",
        agent=escritor,
        output_file=f"capitulo_{numero}.md"
    )

    # Criando uma Crew individual para cada capítulo
    crew_capitulo = Crew(
        agents=[escritor],
        tasks=[capitulo_task],
        process=Process.sequential  # Mantemos sequencial dentro de cada capítulo
    )

    print(f"\n✍️ Iniciando escrita do Capítulo {numero}...")
    crew_capitulo.kickoff(inputs={"tema": tema})
    print(f"✅ Capítulo {numero} finalizado e salvo como 'capitulo_{numero}.md'.")


# 🚀 Execução do Projeto
if __name__ == "__main__":
    tema = input("Digite o tema do livro: ")

    print("\n🔍 Iniciando pesquisa e estruturação do livro sobre:", tema)
    etapas_iniciais.kickoff(inputs={"tema": tema})

    print("\n✍️ Iniciando escrita dos capítulos em paralelo...")

    # Criando um pool de threads para executar os capítulos simultaneamente
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futuros = {executor.submit(escrever_capitulo, i, tema): i for i in range(1, 11)}
        for futuro in concurrent.futures.as_completed(futuros):
            numero_capitulo = futuros[futuro]
            try:
                futuro.result()
            except Exception as e:
                print(f"❌ Erro ao processar o Capítulo {numero_capitulo}: {e}")

    print("\n✅ Livro gerado com sucesso! Os capítulos foram salvos separadamente.")
