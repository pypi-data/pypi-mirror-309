from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from sqlalchemy import text

from ..utils.database_connection import DatabaseConnection


class WriteQueryInput(BaseModel):
    query: str = Field(
        ...,
        description='A SQL query to be executed. Only DELETE, UPDATE, or INSERT commands are allowed.',
    )


def create_write_database_tool(
    db_connection: DatabaseConnection,
) -> StructuredTool:
    """
     Cria uma ferramenta para executar comandos SQL de escrita no banco de dados.

     Esta ferramenta permite executar comandos SQL de escrita, como `DELETE`, `UPDATE` e `INSERT`,
     no banco de dados encapsulado pela instância de `DatabaseConnection`.

     Args:
         db_connection (DatabaseConnection): Instância de conexão configurada com o banco de dados.

     Returns:
         StructuredTool: Uma ferramenta configurada para executar comandos SQL de escrita.

     Raises:
         ValueError: Se a consulta não for um comando `DELETE`, `UPDATE` ou `INSERT`.
         RuntimeError: Se ocorrer um erro durante a execução do comando.

    Example:
         Criando uma ferramenta de escrita no banco de dados

         ```python
         from oikoai.utils.database_connection import DatabaseConnection
         from oikoai.tools.write_database import create_write_database_tool

          # Configurar a conexão com o banco de dados
          db_connection = DatabaseConnection(
              db_type="mysql",
              host="localhost",
              port=3306,
              username="root",
              password="password",
              database="example_db"
          )

          # Criar a ferramenta de escrita
          write_tool = create_write_database_tool(db_connection)

          # Adicione ela a uma lista de ferramentas
          tools = [consult_tool]
         ```

    """

    def write_database(query: str) -> str:
        """
        Executa um comando SQL de escrita no banco de dados.

        Args:
            query (str): O comando SQL a ser executado.

        Returns:
            str: Uma mensagem de sucesso com o número de linhas afetadas.

        Raises:
            ValueError: Se o comando não for `DELETE`, `UPDATE` ou `INSERT`.
            RuntimeError: Se ocorrer um erro durante a execução do comando.
        """
        allowed_commands = ['DELETE', 'UPDATE', 'INSERT']
        command = query.strip().split()[0].upper()

        if command not in allowed_commands:
            raise ValueError(
                'Erro: Apenas comandos DELETE, UPDATE ou INSERT são permitidos.'
            )

        try:
            # Executa o comando usando a sessão encapsulada
            with db_connection.get_session() as session:
                result = session.execute(text(query))
                session.commit()
                return f'Operação {command} bem-sucedida. Linhas afetadas: {result.rowcount}'
        except Exception as e:
            raise RuntimeError(f'Erro ao executar {command}: {str(e)}')

    return StructuredTool.from_function(
        func=write_database,
        name='WriteDatabase',
        description='Executes SQL write commands on the database (DELETE, UPDATE, or INSERT).',
        args_schema=WriteQueryInput,
    )
