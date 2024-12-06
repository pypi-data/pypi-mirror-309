from typing import List

from langchain.schema import AIMessage, HumanMessage
from sqlalchemy.sql import text

from ..utils.database_connection import DatabaseConnection


def get_last_k_messages(
    chat_id: int, k: int, db_connection: DatabaseConnection
) -> List:
    """
    Recupera as últimas `k` mensagens de um chat específico a partir do banco de dados mysql e as formata utilizando as classes de mensagens do LangChain.

    Necessidades mínimas do banco de dados:
        Para que a função opere corretamente, é necessário que existam (as tabelas podem conter outros campos, porém necessariamente precisarão conter esses):

        - Tabela de chats (nome pode variar, como `chat`, `chats`, etc.):

            - id (int): Identificador único do chat

        - Tabela de mensagens (`messages`):

            - id (int): Identificador único da mensagem.

            - chat_id (int): Chave estrangeira referenciando o `id` da tabela de chats.

            - user_message (str): Mensagem enviada pelo usuário.

            - agent_message (str): Mensagem enviada pelo agente/IA.

    ### Caso queira
    Você pode utilizar o [Standard ChatBot Schema](../utils/standard_chatbot_schema.md) para criar um banco de dados com nosso esquema padrão de tabelas

    Args:
        chat_id (int): Identificador único do chat cujas mensagens serão recuperadas.
        k (int): Número de mensagens a serem retornadas. Deve ser maior que zero.
        db_connection (DatabaseConnection): Instância da classe `DatabaseConnection` para gerenciar a conexão ao banco de dados.

    Returns:
        List[Union[HumanMessage, AIMessage]]:
            Lista de mensagens formatadas em ordem cronológica:
            - `HumanMessage`: Representa uma mensagem enviada pelo usuário.
            - `AIMessage`: Representa uma mensagem enviada pelo agente/IA.

    Raises:
        ValueError: Se o valor de `k` for menor ou igual a zero.
        RuntimeError: Se a conexão com o banco de dados não estiver configurada corretamente.

    Example:
        Recuperar as últimas 5 mensagens de um chat com ID 1:

        ```python
        from oikoai.utils.database_connection import DatabaseConnection

        # Configurar a conexão com o banco de dados
        db_connection = DatabaseConnection(
            db_type="mysql",
            host="localhost",
            port=3306,
            username="root",
            password="password",
            database="chatbot_db"
        )

        # Obter as últimas 5 mensagens
        messages = get_last_k_messages(chat_id=1, k=5, db_connection=db_connection)

        # Exibir as mensagens formatadas
        for message in messages:
            print(message)
        ```
    """
    if k <= 0:
        raise ValueError("O valor de 'k' deve ser maior que zero.")

    # Inicia uma sessão com o banco de dados
    with db_connection.get_session() as session:
        # Recupera as últimas k mensagens em ordem decrescente
        query = text(
            """
            SELECT id, chat_id, user_message, agent_message 
            FROM messages 
            WHERE chat_id = :chat_id 
            ORDER BY id DESC 
            LIMIT :limit
        """
        )
        results = session.execute(query, {'chat_id': chat_id, 'limit': k})

        # Converte os resultados para dicionários
        rows = results.mappings().all()  # Retorna uma lista de dicionários

        # Reverte para manter a ordem cronológica
        rows.reverse()

        # Formata as mensagens utilizando as classes do LangChain
        formatted_messages = []
        for row in rows:
            if row['user_message']:
                formatted_messages.append(
                    HumanMessage(content=row['user_message'])
                )
            if row['agent_message']:
                formatted_messages.append(
                    AIMessage(content=row['agent_message'])
                )

    return formatted_messages
