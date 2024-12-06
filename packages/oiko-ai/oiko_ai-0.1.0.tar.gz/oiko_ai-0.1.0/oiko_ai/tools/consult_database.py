import json
from typing import List

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from sqlalchemy import text

from ..utils.database_connection import DatabaseConnection


class QueryInput(BaseModel):
    query: str = Field(
        ...,
        description='A SQL SELECT query to be executed. Only read operations are allowed.',
    )


def create_consult_database_tool(
    db_connection: DatabaseConnection,
) -> StructuredTool:
    """
    Cria uma ferramenta para executar consultas SQL SELECT no banco de dados.

    Esta ferramenta permite executar consultas SQL SELECT no banco de dados encapsulado pela instância de `DatabaseConnection` fornecida.

    Garantimos que apenas operações de leitura são permitidas.

    Ela retorna uma string com os resultados da consulta.

    Args:
        db_connection (DatabaseConnection): Instância de conexão configurada com o banco de dados.

    Returns:
        StructuredTool: Uma ferramenta configurada para executar consultas SQL SELECT.

    Raises:
        ValueError: Se a consulta contiver operações proibidas (por exemplo, DELETE, ALTER).
        RuntimeError: Se ocorrer um erro durante a execução da consulta.

    Example:
        Criando uma ferramenta de consulta no banco de dados

        ```python
        from oikoai.utils.database_connection import DatabaseConnection
        from oikoai.tools.consult_database import create_consult_database_tool

        # Configurar a conexão com o banco de dados
        db_connection = DatabaseConnection(
            db_type="mysql",
            host="localhost",
            port=3306,
            username="root",
            password="password",
            database="example_db"
        )

        # Criar a ferramenta de consulta
        consult_tool = create_consult_database_tool(db_connection)

        # Adicione ela a uma lista de ferramentas
        tools = [consult_tool]
        ```
    """

    def consult_database(query: str) -> List[dict]:
        """
        Executa uma consulta SQL SELECT.

        Args:
            query (str): A consulta SQL SELECT a ser executada.

        Returns:
            str: Uma string representando os resultados da consulta em formato JSON.

        Raises:
            ValueError: Se a consulta contiver operações proibidas.
            RuntimeError: Se ocorrer um erro durante a execução da consulta.
        """
        forbidden_commands = [
            'DELETE',
            'ALTER',
            'CREATE',
            'DROP',
            'UPDATE',
            'INSERT',
            'TRUNCATE',
            'REPLACE',
        ]
        if any(command in query.upper() for command in forbidden_commands):
            raise ValueError(
                'Erro: Apenas operações de leitura são permitidas.'
            )

        try:
            # Executa a consulta usando a sessão encapsulada
            with db_connection.get_session() as session:
                result = session.execute(text(query))
                rows = [dict(row) for row in result.fetchall()]
                return json.dumps(rows, ensure_ascii=False, indent=4)
        except Exception as e:
            raise RuntimeError(f'Erro ao executar a consulta: {str(e)}')

    return StructuredTool.from_function(
        func=consult_database,
        name='ConsultDatabase',
        description='Executes a SQL SELECT query on the database.',
        args_schema=QueryInput,
    )
