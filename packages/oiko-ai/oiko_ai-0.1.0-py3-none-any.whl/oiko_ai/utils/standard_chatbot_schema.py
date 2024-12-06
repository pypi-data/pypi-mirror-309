from standard_models import Base

from ..utils.database_connection import DatabaseConnection


def create_chatbot_schema(db_connection: DatabaseConnection) -> None:
    """
    Cria as tabelas necessárias para o chatbot no banco de dados existente.

    Esta função cria automaticamente as tabelas `users`, `chats`, `messages` e `config`
    no banco de dados configurado via `DatabaseConnection`.

    Nota:
        O banco de dados (`database`) já deve existir no MySQL antes de executar esta função.
        Esta funcionalidade apenas cria as tabelas dentro do banco especificado.

    Args:
        db_connection (DatabaseConnection): Instância da classe
            `DatabaseConnection` configurada para o banco de dados.

    Raises:
        RuntimeError: Se ocorrer algum erro ao tentar criar as tabelas.

    Example:
        Cria as tabelas no banco de dados existente:

            from oikoai.utils.database_connection import DatabaseConnection
            from create_schema import create_chatbot_schema

            # Configurar conexão com o banco de dados existente
            db_connection = DatabaseConnection(
                db_type="mysql",
                host="localhost",
                port=3306,
                username="root",
                password="password",
                database="chatbot_db"  # Banco já deve existir
            )

            # Criar as tabelas
            create_chatbot_schema(db_connection)
    """
    try:
        # Obtém o engine da conexão
        engine = db_connection.get_engine()

        # Cria as tabelas no banco de dados
        Base.metadata.create_all(bind=engine)
        print('Tabelas criadas com sucesso!')
    except Exception as e:
        print(f'Erro ao criar o schema do chatbot: {str(e)}')
        raise RuntimeError(f'Erro ao criar o schema do chatbot: {str(e)}')
