from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI


class GenericAgentWithTools:
    """
    Classe para criação de agentes genéricos com ferramentas configuráveis para interagir com LLMs.

    Esta classe permite a criação de agentes flexíveis, incluindo suporte a ferramentas personalizadas e integração com modelos Azure OpenAI.

    Attributes:
        agent (object): Instância do agente criado pelo LangChain.
        tools (list): Lista de ferramentas configuráveis para o agente.

    Methods:
        invoke(question: str, memory: list = [], verbose: bool = False) -> dict:
            Executa o agente passando uma pergunta e retorna a resposta.

    Parameters:
        api_key (str): Chave de API para acesso ao Azure OpenAI.
        azure_endpoint (str): Endpoint do Azure para chamadas ao Azure OpenAI.
        system (str): Descrição do sistema que define o comportamento do agente.
        tools (list): Lista de ferramentas para o agente.
        openai_api_version (str, opcional): Versão da API Azure OpenAI. Padrão é '2024-02-15-preview'.
        azure_deployment (str, opcional): Nome do deployment no Azure. Padrão é 'gpt-4o-mini'.
        temperature (float, opcional): Configuração da temperatura para respostas. Padrão é 0.1.
        max_tokens (int, opcional): Número máximo de tokens na resposta. Padrão é None.
        timeout (int, opcional): Tempo limite para requisições. Padrão é None.
        max_retries (int, opcional): Número máximo de tentativas em caso de falha. Padrão é 15.
        streaming (bool, opcional): Habilita respostas em streaming. Padrão é False.
    """

    agent = None
    tools = []

    def __init__(
        self,
        api_key,
        azure_endpoint,
        system,
        tools,
        openai_api_version='2024-02-15-preview',
        azure_deployment='gpt-4o-mini',
        temperature=0.1,
        max_tokens=None,
        timeout=None,
        max_retries=15,
        streaming=False,
    ):
        self.tools = tools

        llm = AzureChatOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            openai_api_version=openai_api_version,
            azure_deployment=azure_deployment,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            max_retries=max_retries,
            streaming=streaming,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ('system', system),
                MessagesPlaceholder('history'),
                ('human', '{input}'),
                ('placeholder', '{agent_scratchpad}'),
            ]
        )

        # Constrói o agente com ferramentas
        self.agent = create_tool_calling_agent(llm, self.tools, prompt)

    def invoke(self, question, memory=None, verbose=False):
        """
        Executa o agente passando uma pergunta e um histórico de conversas.

        Parameters:
            question (str): Pergunta a ser respondida pelo agente.
            memory (list, opcional): Histórico da conversa (mensagens anteriores).
                                     Padrão é uma lista vazia.
            verbose (bool, opcional): Habilita logs detalhados durante a execução. Padrão é False.

        Returns:
            str: Resposta gerada pelo agente.

        Example:
            >>> agent = GenericAgentWithTools(api_key, azure_endpoint, "Hello!", tools)
            >>> response = agent.invoke("Qual é a previsão do tempo?", memory=["Olá, quem é você?"])
            >>> print(response)
        """
        if memory is None:
            memory = []

        agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=verbose
        )
        response = agent_executor.invoke(
            {'input': question, 'history': memory}
        )
        return response['output']
