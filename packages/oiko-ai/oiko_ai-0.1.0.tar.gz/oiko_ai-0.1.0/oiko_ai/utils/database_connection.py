from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseConnection:
    """
    Classe para gerenciar conexões com diferentes tipos de bancos de dados usando o SQLAlchemy.

    Suporta os seguintes tipos de banco:
      - MySQL
      - PostgreSQL
      - SQL Server
      - SQLite

    Args:
        db_type (str): Tipo do banco de dados. Pode ser 'mysql', 'postgresql', 'sqlserver' ou 'sqlite'.
        host (str, optional): Host do banco de dados. Necessário para todos os tipos, exceto SQLite.
        port (int, optional): Porta do banco de dados. Necessário para todos os tipos, exceto SQLite.
        username (str, optional): Nome de usuário para autenticação. Necessário para todos os tipos, exceto SQLite.
        password (str, optional): Senha para autenticação. Necessário para todos os tipos, exceto SQLite.
        database (str, optional): Nome do banco de dados. Necessário para todos os tipos, exceto SQLite.
        sqlite_path (str, optional): Caminho para o arquivo SQLite. Necessário apenas para SQLite.

    Raises:
        ValueError: Se os parâmetros necessários para o tipo de banco de dados não forem fornecidos.
    """

    def __init__(
        self,
        db_type: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        sqlite_path: Optional[str] = None,
    ):
        self.db_type = db_type.lower()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.sqlite_path = sqlite_path
        self.engine: Optional[Engine] = None
        self.session_maker = None

        self._validate_params()
        self._create_engine()

    def _validate_params(self):
        if self.db_type == 'sqlite':
            if not self.sqlite_path:
                raise ValueError(
                    'Para SQLite, o caminho do arquivo (sqlite_path) deve ser fornecido.'
                )
        elif self.db_type in ['mysql', 'postgresql', 'sqlserver']:
            if not (
                self.host
                and self.port
                and self.username
                and self.password
                and self.database
            ):
                raise ValueError(
                    f'Para {self.db_type}, é necessário fornecer host, port, username, password e database.'
                )
        else:
            raise ValueError(
                f"Tipo de banco de dados '{self.db_type}' não suportado."
            )

    def _create_engine(self):
        """
        Cria o objeto `Engine` do SQLAlchemy com base nos parâmetros fornecidos.

        Raises:
            ValueError: Se o tipo de banco de dados não for suportado.
        """
        if self.db_type == 'sqlite':
            self.engine = create_engine(f'sqlite:///{self.sqlite_path}')
        elif self.db_type == 'mysql':
            self.engine = create_engine(
                f'mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
            )
        elif self.db_type == 'postgresql':
            self.engine = create_engine(
                f'postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
            )
        elif self.db_type == 'sqlserver':
            self.engine = create_engine(
                f'mssql+pyodbc://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server'
            )
        else:
            raise ValueError(
                f"Tipo de banco de dados '{self.db_type}' não suportado."
            )

        # Criar a factory para sessões
        self.session_maker = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """
        Retorna uma nova sessão de banco de dados.

        Returns:
            Session: Uma nova sessão vinculada ao engine configurado.

        Raises:
            RuntimeError: Se o engine não foi inicializado corretamente.
        """
        if not self.session_maker:
            raise RuntimeError('O engine não foi inicializado corretamente.')
        return self.session_maker()

    def get_engine(self) -> Engine:
        """
        Retorna o engine SQLAlchemy configurado.

        Returns:
            Engine: O engine configurado para o banco de dados.

        Raises:
            RuntimeError: Se o engine não foi inicializado corretamente.
        """
        if not self.engine:
            raise RuntimeError('O engine não foi inicializado corretamente.')
        return self.engine

    def close(self):
        """
        Fecha o engine do SQLAlchemy, liberando recursos.
        """
        if self.engine:
            self.engine.dispose()
