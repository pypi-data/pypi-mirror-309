from langchain.tools import StructuredTool

from ..tools.consult_database import create_consult_database_tool
from ..tools.show_database import create_show_database_metadata_tool
from ..tools.write_database import create_write_database_tool
from ..utils.database_connection import DatabaseConnection


def create_database_toolkit(
    db_connection: DatabaseConnection,
) -> StructuredTool:
    """
    Cria um conjunto de ferramentas para interagir com o banco de dados.

    Este método retorna ferramentas estruturadas que permitem a interação com o banco de dados,
    incluindo operações de consulta  (SELECT), escrita (INSERT, UPDATE, DELETE) e visualização de estrutura do banco (nomenclatura das tabelas e nomes de colunas).

    Args:
        db_connection (DatabaseConnection):
            Instância da classe `DatabaseConnection` configurada para conectar-se ao banco de dados.

    Returns:
        List[StructuredTool]:
            Uma lista contendo as ferramentas estruturadas para interagir com o banco de dados.

    Raises:
        RuntimeError: Se ocorrer algum erro ao criar as ferramentas de banco de dados.

    Example:
        ```python
        from oikoai.utils.database_connection import DatabaseConnection
        from oikoai.toolkits.database_toolkit import create_database_toolkit

        # Configurar a conexão com o banco de dados
        db_connection = DatabaseConnection(
            db_type="mysql",
            host="localhost",
            port=3306,
            username="root",
            password="password",
            database="chatbot_db"
        )

        # Criar o conjunto de ferramentas
        database_toolkit = create_database_toolkit(db_connection)
        ```
    """
    consult_database_tool = create_consult_database_tool(db_connection)
    write_database_tool = create_write_database_tool(db_connection)
    show_database_metadata_tool = create_show_database_metadata_tool(
        db_connection
    )
    tools = [
        consult_database_tool,
        write_database_tool,
        show_database_metadata_tool,
    ]
    return tools
