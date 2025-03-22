import os
from crewai import Agent, Task, Crew, Process
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI  # ✅ Correto

# Configurar chave OpenAI
os.environ["OPENAI_API_KEY"] = "sua_chave_api"

# Diretório dos arquivos
pdf_files = ["/home/leo/projetos_python/crewai_graphrag/arquivo_01.pdf", "/home/leo/projetos_python/crewai_graphrag/arquivo_02.pdf"]

# 🔹 1️⃣ Extração de Texto dos PDFs
documents = SimpleDirectoryReader(input_files=pdf_files).load_data()

# 🔹 2️⃣ Construção do Grafo de Conhecimento
graph_store = SimpleGraphStore()
parser = SimpleNodeParser.from_defaults()
index = KnowledgeGraphIndex.from_documents(documents, graph_store=graph_store, node_parser=parser)

# 🔹 3️⃣ Criando os Agentes CrewAI
extrator_temas = Agent(
    role="Extrator de Temas",
    goal="Identificar os principais tópicos em cada PDF",
    backstory="Você é um especialista em análise textual e extração de tópicos importantes.",
    verbose=True,
)

comparador_conceitos = Agent(
    role="Comparador de Conceitos",
    goal="Relacionar os temas entre os dois documentos utilizando GraphRAG",
    backstory="Você é um analista de conhecimento que encontra conexões entre conceitos em documentos.",
    verbose=True,
)

analista_correlacoes = Agent(
    role="Analista de Correlações",
    goal="Identificar e destacar trechos específicos onde há interseção entre os documentos",
    backstory="Você analisa os textos em detalhes para encontrar onde os temas convergem.",
    verbose=True,
)

formatador_relatorio = Agent(
    role="Formatador de Relatório",
    goal="Organizar os achados em um documento Markdown estruturado",
    backstory="Você é um especialista em formatação e organização de informações para gerar relatórios claros.",
    verbose=True,
)

# 🔹 4️⃣ Criando as Tarefas CrewAI
tarefa_extracao = Task(
    description="Leia os documentos e extraia os temas principais.",
    agent=extrator_temas,
    expected_output="Uma lista dos principais tópicos identificados em cada documento.",  # ✅ Adicionado
)

tarefa_comparacao = Task(
    description="Analise os temas extraídos e encontre conexões entre eles utilizando GraphRAG.",
    agent=comparador_conceitos,
    expected_output="Um relatório das conexões encontradas entre os temas dos documentos.",  # ✅ Adicionado
)

tarefa_correlacao = Task(
    description="Identifique trechos específicos onde os temas de ambos os documentos se conectam.",
    agent=analista_correlacoes,
    expected_output="Trechos específicos dos documentos onde há interseção entre os temas.",  # ✅ Adicionado
)

tarefa_formatacao = Task(
    description="Organize os achados em um arquivo Markdown estruturado.",
    agent=formatador_relatorio,
    expected_output="Um arquivo Markdown bem formatado com os resultados da análise.",  # ✅ Adicionado
    output_file="relatorio_correlacoes.md"
)

# 🔹 5️⃣ Criando o Crew
crew = Crew(
    agents=[extrator_temas, comparador_conceitos, analista_correlacoes, formatador_relatorio],
    tasks=[tarefa_extracao, tarefa_comparacao, tarefa_correlacao, tarefa_formatacao],
    process=Process.sequential  # Executar as tarefas em sequência
)

# 🔹 6️⃣ Executando a Análise
resultado = crew.kickoff()
print("✅ Análise concluída! Relatório salvo em 'relatorio_correlacoes.md'")
