# Código para validação do quanto uma crew criada por prompt pode ser eficiente

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Configurar as chaves de API (se necessário)
os.environ["SERPER_API_KEY"] = "sua_chave_serper"
os.environ["OPENAI_API_KEY"] = "sua_chave_openai"

# Ferramenta de pesquisa para buscar CVEs e informações adicionais
search_tool = SerperDevTool(
    n_results=30,
)

# Criar os agentes
pesquisador_internet = Agent(
    role="Pesquisa e Análise de Dados",
    goal="realizar buscas profundas na internet utilizando técnicas de SEO, dorks, coletando dados relevantes sobre o tema {tema}.",
    backstory=(
        "expertise em análise de dados possibilitando que ela identifique informações críticas e tendências sobre o tema alta experiência em consultoria análise de dados e metodologias de pesquisa."
    ),
    verbose=True,
    memory=True,
    tools=[search_tool],
)

especialista_risco = Agent(
    role="Análise de Riscos Corporativos",
    goal="realizar uma análise detalhada dos possíveis riscos e impactos corporativos identificados nas informações coletadas utilizando-se dos frameworks COSO ERM (Enterprise Risk Management), ISO 31000, COBIT2019. Sua expertise em gestão de riscos permitirá que avalie a gravidade e a probabilidade dos riscos, contribuindo para um planejamento de auditoria mais eficaz.",
    backstory=(
        "especialização em Gestão de Riscos, experiência em análise de riscos em empresas de diversos setores"
    ),
    verbose=True,
    memory=True,
)

especialista_auditoria = Agent(
    role="Planejar Auditorias",
    goal="utilizar as informações pesquisador_internet e especialista_risco para desenvolver um planejamento de auditoria que aborde as análises e os riscos identificados.",
    backstory=(
        "Auditor certificado pelo instituto de auditoria interna com mais de 15 anos de experiência em auditorias de Negócio, Tecnologia, e operacionais. Formado Gestão de Riscos, sua experiência em auditoria garantirá que o planejamento seja robusto e eficaz."
    ),
    verbose=True,
    memory=True,
)

especialista_compliance = Agent(
    role="Aferir planejamento de auditoria",
    goal="assegurar que o planejamento de auditoria esteja em conformidade com as normas e regulamentos aplicáveis. Sua experiência em compliance ajudará a identificar requisitos que devem ser considerados dos frameworks COSO ERM (Enterprise Risk Management), ISO 31000, COBIT2019.",
    backstory=(
        "experiência em compliance e auditoria. Consultor de empresas em questões regulatórias, compliance, análise de riscos e já atuou como auditor interno em grandes corporações."
    ),
    verbose=True,
    memory=True,
)

# Criar as tarefas
task_analisar_busca = Task(
    description=(
        "Conduzir uma pesquisa abrangente, utilizando técnicas avançadas de busca e análise de dados, compilar informações de fontes confiáveis e relevantes delimitado pelas tags <tema_final></tema_final>: "
        "<tema_final>\n"
        "{tema}\n"
        "</tema_final>"
    ),
    expected_output="Um relatório detalhado contendo uma análise das informações coletadas, identificação de riscos inerentes e recomendações preliminares. Este relatório servirá como base para o planejamento da auditoria.",
    agent=pesquisador_internet,
)

tarefa_aferir_risco = Task(
    description=(
        "Conduzir uma análise de riscos detalhada, utilizando metodologias reconhecidas, como a Análise SWOT e a Matriz de Risco, classificar os riscos identificados em termos de impacto e probabilidade, além de sugerir estratégias de mitigação."
    ),
    expected_output="Um relatório de análise de riscos que incluirá descrição dos riscos identificados, uma matriz de riscos, classificações dos riscos e recomendações de mitigação. Este relatório será essencial para que especialista_auditoria interaja com as informações de risco no planejamento da auditoria.",
    agent=especialista_risco
)

tarefa_planejamento_auditoria = Task(
    description=(
        "Criar um planejamento de auditoria que inclua objetivos claros, escopo definido e uma lista detalhada de 10 testes a serem executados. Ele irá garantir que todos os riscos identificados sejam abordados no planejamento."
    ),
    expected_output="Um planejamento de auditoria, que incluirá os riscos inerentes a serem auditados, objetivo da auditoria, escopo, metodologia e a lista de testes. Este documento será utilizado por toda a equipe para guiar a execução da auditoria.",
    agent=especialista_auditoria
)

tarefa_aferir_compliance = Task(
    description=(
        "Revisar o planejamento de auditoria elaborado por especialista_auditoria, garantindo que todas as normas e regulamentos sejam atendidos. Também deve fornecer insights sobre riscos que podem impactar a auditoria."
    ),
    expected_output="Um parecer técnico que incluirá recomendações e ajustes necessários no planejamento de auditoria",
    agent=especialista_compliance
)

# Criar a equipe
equipe_auditoria = Crew(
    agents=[pesquisador_internet, especialista_risco, especialista_auditoria, especialista_compliance],
    tasks=[task_analisar_busca, tarefa_aferir_risco, tarefa_planejamento_auditoria, tarefa_aferir_compliance],
    process=Process.sequential  # Execução ordenada das tarefas
)

# Executar a auditoria com um tema específico
resultado = equipe_auditoria.kickoff(inputs={"tema": "estratégias, riscos, direcionadores e previsões futuras sobre ESG - Environmental, Social and Governance"})
print(resultado)
