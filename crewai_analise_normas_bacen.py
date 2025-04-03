import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool
#import litellm

#litellm._turn_on_debug()

os.environ["OPENAI_API_KEY"] = "chave"

# Definição do modelo de linguagem (LLM)
llm_gemini = LLM(
    model="openai/o1-mini",
    temperature=0.5,
)

# Definição ferramenta para leitura da norma
file_read_tool = FileReadTool(file_path='/home/leo/projetos_python/bacen_normas/resolucao_4949.txt')


# Definição dos agentes especializados
analista_juridico = Agent(
    role="Analista Jurídico-Regulatório",
    goal="Interpretar normas do BACEN e extrair obrigações regulatórias.",
    backstory="Especialista em legislação financeira, com foco em compliance bancário.",
    verbose=True,
    tools=[file_read_tool],
    llm="gpt-4o-mini",
    memory=True
)

engenheiro_requisitos = Agent(
    role="Engenheiro de Requisitos Financeiros",
    goal="Converter normas regulatórias em requisitos operacionais detalhados.",
    backstory="Profundo conhecedor dos impactos das regulações no setor financeiro.",
    verbose=True,
    llm=llm_gemini,
    memory=True
)

arquiteto_processos = Agent(
    role="Arquiteto de Processos Bancários",
    goal="Criar fluxogramas e definir subprocessos para garantir a conformidade.",
    backstory="Experiente em modelagem BPMN para operações financeiras.",
    verbose=True,
    llm=llm_gemini,
    memory=True
)

projetista_solucoes = Agent(
    role="Projetista de Soluções Financeiras",
    goal="Gerar documentos de implementação técnica para os processos desenhados.",
    backstory="Responsável pela especificação técnica e integração com sistemas bancários.",
    verbose=True,
    llm=llm_gemini,
    memory=True
)

gestor_conformidade = Agent(
    role="Gestor de Conformidade",
    goal="Consolidar saídas em um pacote de conformidade para auditoria.",
    backstory="Experiente em controles internos e auditoria regulatória.",
    verbose=True,
    llm=llm_gemini,
    memory=True
)

# Definição das tarefas
tarefa_analise_norma = Task(
    description="Interpretar a norma e gerar um mapa categorizado dos dispositivos legais.",
    expected_output="Markdown estruturado com artigos e obrigações categorizadas.",
    agent=analista_juridico
)

tarefa_extracao_requisitos = Task(
    description="Converter os dispositivos legais extraídos em requisitos operacionais estruturados.",
    expected_output="Lista JSON de requisitos formatados com impacto e área responsável.",
    agent=engenheiro_requisitos
)

tarefa_desenho_processos = Task(
    description="Criar fluxogramas BPMN e definir subprocessos, stakeholders e KPIs.",
    expected_output="Diagramas e tabelas detalhando os processos operacionais.",
    agent=arquiteto_processos
)

tarefa_detalhamento_implementacao = Task(
    description="Gerar documentos técnicos como matrizes RACI e especificações de sistemas.",
    expected_output="Documentação estruturada para implementação em projetos.",
    agent=projetista_solucoes
)

tarefa_pacote_conformidade = Task(
    description="Consolidar outputs anteriores em um pacote completo de conformidade.",
    expected_output="Pacote final contendo matriz de aderência, cronograma e checklist de auditoria.",
    agent=gestor_conformidade
)

# Criando a equipe com execução sequencial
crew = Crew(
    agents=[analista_juridico, engenheiro_requisitos, arquiteto_processos, projetista_solucoes, gestor_conformidade],
    tasks=[tarefa_analise_norma, tarefa_extracao_requisitos, tarefa_desenho_processos, tarefa_detalhamento_implementacao, tarefa_pacote_conformidade],
    process=Process.sequential
)

# Executando o fluxo com uma norma específica
resultado = crew.kickoff()
print(resultado)
