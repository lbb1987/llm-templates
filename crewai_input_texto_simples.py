import os
from crewai import Agent, Task, Crew, Process, LLM

# Configuração das chaves de API
# Define a chave de API necessária para acessar o serviço do modelo de linguagem
os.environ["GEMINI_API_KEY"] = "sua chave google ai studio"

# Definição do modelo de linguagem (LLM) que os agentes irão utilizar
# O modelo é configurado com um parâmetro de temperatura que controla a aleatoriedade das respostas
llm_gemini = LLM(
    model="gemini/gemini-1.5-pro-latest",
    temperature=0.7,
)

# Criação dos agentes que irão realizar tarefas específicas
# Cada agente tem um papel, objetivo, histórico, e utiliza o modelo de linguagem definido

# Agente responsável por analisar processos tecnológicos
especialista_ti = Agent(
    role="Especialista de TI",
    goal="Analisar e mapear os processos tecnológicos do cenário descrito.",
    backstory=(
        "Você é um especialista altamente qualificado em tecnologia da informação. "
        "Seu papel é analisar o cenário descrito em {cenario} e identificar os principais processos "
        "tecnológicos envolvidos, garantindo um entendimento claro do ambiente de TI."
    ),
    verbose=True,
    memory=True,
    llm=llm_gemini,
)

# Agente responsável por identificar riscos tecnológicos
especialista_riscos = Agent(
    role="Especialista em Riscos de Tecnologia",
    goal="Identificar possíveis riscos associados aos processos mapeados.",
    backstory=(
        "Você é um especialista em riscos de tecnologia com anos de experiência. "
        "Com base nos processos descritos pelo Especialista de TI, sua missão é "
        "avaliar e detalhar possíveis vulnerabilidades e ameaças tecnológicas."
    ),
    verbose=True,
    memory=True,
    llm=llm_gemini,
)

# Agente responsável por planejar auditorias para mitigar riscos
auditor_ti = Agent(
    role="Auditor de TI",
    goal="Criar um planejamento de auditoria detalhado para mitigar os riscos identificados.",
    backstory=(
        "Você é um auditor de TI experiente e meticuloso. Seu papel é utilizar "
        "os riscos identificados pelo Especialista em Riscos e criar um planejamento "
        "detalhado de auditoria para avaliar e mitigar esses riscos."
    ),
    verbose=True,
    memory=True,
    llm=llm_gemini,
)

# Criação das tarefas que cada agente irá executar
# Cada tarefa tem uma descrição, uma saída esperada e é atribuída a um agente

# Tarefa para mapear processos tecnológicos
tarefa_mapeamento = Task(
    description=(
        "Analise o cenário de TI fornecido em {cenario} e identifique os principais processos tecnológicos envolvidos. "
        "Liste os processos de forma clara e objetiva."
    ),
    expected_output="Uma lista detalhada dos principais processos tecnológicos do cenário descrito. Sua resposta deve ser em pt-BR português do brasil",
    agent=especialista_ti
)

# Tarefa para identificar riscos tecnológicos
tarefa_riscos = Task(
    description=(
        "Com base nos processos tecnológicos mapeados, identifique os principais riscos envolvidos. "
        "Descreva os riscos e suas possíveis consequências para a organização."
    ),
    expected_output="Uma lista de riscos tecnológicos associados ao cenário, com explicação detalhada. Sua resposta deve ser em pt-BR português do brasil",
    agent=especialista_riscos
)

# Tarefa para planejar auditoria
tarefa_auditoria = Task(
    description=(
        "Com base nos riscos identificados, elabore um planejamento detalhado de auditoria para avaliar "
        "e mitigar esses riscos. Inclua metodologias, escopo e cronograma."
    ),
    expected_output="Um planejamento completo de auditoria em TI, pronto para implementação. Sua resposta deve ser em pt-BR português do brasil",
    agent=auditor_ti
)

# Criação do fluxo de trabalho (Crew) que organiza a execução das tarefas
# Os agentes trabalham em sequência, cada um completando sua tarefa antes do próximo começar
crew = Crew(
    agents=[especialista_ti, especialista_riscos, auditor_ti],
    tasks=[tarefa_mapeamento, tarefa_riscos, tarefa_auditoria],
    process=Process.sequential  # Os agentes trabalham em sequência
)

# Solicita ao usuário a descrição do cenário de TI para auditoria
cenario_ti = input("Descreva o cenário de TI para auditoria: ")

# Executa o fluxo de trabalho com o cenário fornecido
resultado = crew.kickoff(inputs={"cenario": cenario_ti})

# Exibe o resultado final do planejamento de auditoria
print("\n📌 PLANEJAMENTO FINAL DE AUDITORIA 📌\n")
print(resultado)



#==================================================================
#===========================documentação===========================
#==================================================================

#Documentação Detalhada
#Visão Geral
#Este programa é uma aplicação de orquestração de multiagentes de inteligência artificial utilizando o framework CrewAI. Ele simula um processo de auditoria de TI, onde diferentes agentes desempenham papéis específicos para analisar um cenário de TI, identificar riscos e planejar auditorias.
#Componentes do Código
#
#    Configuração de Ambiente:
#        O código começa configurando uma chave de API necessária para acessar o modelo de linguagem (LLM) que os agentes utilizarão.
#    Modelo de Linguagem (LLM):
#        Um modelo de linguagem chamado gemini/gemini-1.5-pro-latest é configurado. Este modelo é usado pelos agentes para processar informações e gerar respostas.
#    Agentes:
#        Três agentes são criados, cada um com um papel específico:
#            Especialista de TI: Analisa e mapeia processos tecnológicos.
#            Especialista em Riscos de Tecnologia: Identifica riscos associados aos processos mapeados.
#            Auditor de TI: Cria um planejamento de auditoria para mitigar os riscos identificados.
#    Tarefas:
#        Cada agente é responsável por uma tarefa específica:
#            Tarefa de Mapeamento: Executada pelo Especialista de TI.
#            Tarefa de Riscos: Executada pelo Especialista em Riscos.
#            Tarefa de Auditoria: Executada pelo Auditor de TI.
#    Fluxo de Trabalho (Crew):
#        Os agentes e suas tarefas são organizados em um fluxo de trabalho sequencial, onde cada agente completa sua tarefa antes do próximo começar.
#    Execução:
#        O usuário é solicitado a descrever um cenário de TI.
#        O fluxo de trabalho é executado com base no cenário fornecido, e o resultado final é exibido.

Como Executar

    Pré-requisitos:
        Certifique-se de ter o framework CrewAI instalado.
        Configure a chave de API correta para acessar o modelo de linguagem.
    Execução:
        Execute o script Python.
        Quando solicitado, insira uma descrição do cenário de TI que deseja auditar.
        O programa processará a entrada e exibirá um planejamento de auditoria detalhado.



