import json

from langchain.tools import StructuredTool
from sqlalchemy import text

from ..utils.database_connection import DatabaseConnection


def create_show_database_metadata_tool(
    db_connection: DatabaseConnection,
) -> StructuredTool:
    """
    Cria uma ferramenta para exibir metadados do banco de dados.

    Esta ferramenta recupera a estrutura do banco de dados, listando todas as tabelas
    e suas respectivas colunas em formato JSON.

    Args:
        db_connection (DatabaseConnection): Instância de conexão configurada com o banco de dados.

    Returns:
        StructuredTool: Uma ferramenta configurada para buscar e exibir metadados do banco.

    Example:
        >>> from oikoai.utils.database_connection import DatabaseConnection
        >>> from oikoai.tools import create_show_database_metadata_tool
        >>>
        >>> # Configurar a conexão com o banco de dados
        >>> db_connection = DatabaseConnection(
        >>>     db_type="mysql",
        >>>     host="localhost",
        >>>     port=3306,
        >>>     username="root",
        >>>     password="password",
        >>>     database="example_db"
        >>> )
        >>>
        >>> # Criar a ferramenta de metadados
        >>> metadata_tool = create_show_database_metadata_tool(db_connection)
        >>>
        >>> # Recuperar os metadados
        >>> metadata = metadata_tool.func()
        >>> print(metadata)
    """

    def show_database_metadata() -> str:
        """
        Recupera metadados do banco de dados, incluindo tabelas e colunas.

        Returns:
            str: Metadados do banco em formato JSON.

        Raises:
            RuntimeError: Se ocorrer um erro ao buscar os metadados.
        """
        try:
            with db_connection.get_session() as session:
                # Buscar nomes das tabelas
                result_tables = session.execute(text('SHOW TABLES;'))
                tables = [row[0] for row in result_tables.fetchall()]

                # Buscar colunas de cada tabela
                metadata = {}
                for table in tables:
                    columns_result = session.execute(
                        text(f'SHOW COLUMNS FROM `{table}`;')
                    )
                    columns = [
                        row['Field'] for row in columns_result.fetchall()
                    ]
                    metadata[table] = columns

                # Retornar metadados como JSON formatado
                return json.dumps(metadata, indent=2)

        except Exception as e:
            raise RuntimeError(f'Erro ao obter metadados: {str(e)}')

    return StructuredTool.from_function(
        func=show_database_metadata,
        name='ShowDatabaseMetadata',
        description='Recupera metadados do banco de dados, incluindo tabelas e colunas, e retorna em formato JSON.',
    )
