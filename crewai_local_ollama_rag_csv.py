from crewai import Agent, Task, Crew, LLM
from crewai_tools import CSVSearchTool
import os

os.environ["OPENAI_API_KEY"] = "NA"

ollama = LLM(
    model="ollama/llama3.1:latest",
    base_url="http://192.168.0.53:11434"
)


tool = CSVSearchTool(csv='projetos_python/ollama_crewai/dre_banco_site_ri.csv')

# Agent 1: 
researcher = Agent(
    role="Analista de Dados Especialista", 
    goal="Extrair dados relevantes do arquivo CSV e estruturá-los conforme as instruções", 
    backstory="Você é um analista de dados especialista em extrair informações de arquivos CSV conforme as instruções fornecidas na descrição da tarefa. O resultado de sua tarefa deve ser em pt-BR português brasileiro",
    allow_delegation=False,
    verbose=True,
    tool=tool,
    llm=ollama
)

# Agent 2: 
contador = Agent(
    role="Especialista em Contabilidade", 
    goal="Analisar uma DRE (Demonstração do Resultado do Exercício) de uma empresas brasileiras, aferindo o desempenho financeiro do período dos 3 últimos anos (2022, 2023, 2024), aferindo a saúde financeira no período analisado, detalhando as receitas, custos, despesas e outros resultados que impactaram o patrimônio da empresa", 
    backstory="Você é um contato especialista em realizar análises de DRE em CSV com profundo conhecimento nas normas contábeis brasileiras, incluindo as Normas Brasileiras de Contabilidade (NBC) e os Pronunciamentos do Comitê de Pronunciamentos Contábeis (CPC). O resultado de sua tarefa deve ser em pt-BR português brasileiro",
    allow_delegation=False,
    verbose=True,
    tool=tool,
    llm=ollama
)

# Agent 3: 
writer = Agent(
    role="Analista Financeiro de Mercado",
    goal="avaliar a DRE (Demonstração do Resultado do Exercício) é fornecer uma análise detalhada e crítica sobre o desempenho financeiro da empresa, identificando pontos fortes, fraquezas, tendências e riscos.",
    backstory="Você é um especialista em análise da saúde financeira da empresa por meio de seus dados históricos da DRE. O resultado de sua tarefa deve ser em pt-BR português brasileiro",
    allow_delegation=False,
    verbose=True,
    llm=ollama
)

# Create tasks
task1 = Task(
    description="Usando o arquivo CSV chamado 'dre.bradesco.csv', extraia as informações necessárias para que o agente contador realize as seguintes análises contábeis: Rentabilidade, Margem Operacional, Margem Líquida, Crescimento da Receita Líquida, Crescimento do Lucro Líquido, Despesas Operacionais em Relação à Receita, Redução de Custos, , Análise de Resultados Não Operacionais, Resultados Financeiros, Ganhos ou Perdas com Venda de Ativos, Análise de Tributação, Aumento ou redução consistente da receita líquida, Melhoria ou deterioração das margens (bruta, operacional e líquida), Crescimento ou redução do lucro líquido, Retorno sobre o Patrimônio Líquido (ROE), Retorno sobre o Ativo Total (ROA), Avalia a eficiência da empresa em gerar lucro a partir de seus ativos, Calcular o ponto de equilíbrio (onde as receitas se igualam aos custos e despesas) para entender quanto a empresa precisa vender para cobrir seus custos fixos e variáveis, Simular cenários de aumento ou redução de receitas, custos e despesas para avaliar o impacto no lucro líquido",
    expected_output="Relação dos dados para que o agente contador realize suas análises",
    agent=researcher
)

task2 = Task(
    description="Usando os dados estruturados e os insights fornecidos pelo agente Analista de Dados Especialista, desenvolva um relatório técnico com as análises contábeis sobre a DRE avaliando os seguintes critério: Rentabilidade, Margem Operacional, Margem Líquida, Crescimento da Receita Líquida, Crescimento do Lucro Líquido, Despesas Operacionais em Relação à Receita, Redução de Custos, , Análise de Resultados Não Operacionais, Resultados Financeiros, Ganhos ou Perdas com Venda de Ativos, Análise de Tributação, Aumento ou redução consistente da receita líquida, Melhoria ou deterioração das margens (bruta, operacional e líquida), Crescimento ou redução do lucro líquido, Retorno sobre o Patrimônio Líquido (ROE), Retorno sobre o Ativo Total (ROA), Avalia a eficiência da empresa em gerar lucro a partir de seus ativos, Calcular o ponto de equilíbrio (onde as receitas se igualam aos custos e despesas) para entender quanto a empresa precisa vender para cobrir seus custos fixos e variáveis, Simular cenários de aumento ou redução de receitas, custos e despesas para avaliar o impacto no lucro líquido. Suas respostas deve conter formularas e referencias de quais celulas da planilha DRE você utilizou para que seu raciocinio lógico seja explicavel",
    expected_output="Relatório técnico e explicação de pelo menos 1000 palavras",
    agent=contador
)

task3 = Task(
    description="Usando os dados estruturados e os insights fornecidos pelo agente Especialista em Contabilidade, desenvolva um relatório técnico preciso que destaque as análises contábeis da DRE e um parecer sobre a saúde financeira da empresa.",
    expected_output="Relatório técnico e explicação de pelo menos 1000 palavras",
    agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, contador, writer],
    tasks=[task1, task2, task3],
    verbose=True,  # Corrigido: substituído 2 por True
)

result = crew.kickoff()
