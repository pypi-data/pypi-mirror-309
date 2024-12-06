# models.py

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """
    Modelo para a tabela `users`, que armazena informações dos usuários.

    Colunas:
        id (int): Identificador único do usuário.
        username (str): Nome de usuário, obrigatório.
        password (str): Senha do usuário, obrigatório.
        email (str): Email único do usuário, obrigatório.
        organization (str): Nome da organização associada ao usuário (opcional).
        organization_user_id (str): ID do usuário na organização (opcional).
        access_level (str): Nível de acesso do usuário (padrão: 'user').
        created_at (TIMESTAMP): Data/hora de criação do registro (preenchida automaticamente).
        updated_at (TIMESTAMP): Data/hora da última atualização do registro (preenchida automaticamente).
        deleted_at (TIMESTAMP): Data/hora de exclusão lógica do registro (opcional).

    Relacionamentos:
        chats: Relacionamento com a tabela `chats` (1:N).
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    organization = Column(String(255), nullable=True)
    organization_user_id = Column(String(255), nullable=True)
    access_level = Column(String(50), nullable=False, default='user')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)

    chats = relationship('Chat', back_populates='user')


class Chat(Base):
    """
    Modelo para a tabela `chats`, que armazena informações sobre as conversas.

    Colunas:
        id (int): Identificador único da conversa.
        user_id (int): ID do usuário associado à conversa.
        title (str): Título da conversa.
        thread (str): Conteúdo ou resumo da conversa.
        created_at (TIMESTAMP): Data/hora de criação do registro (preenchida automaticamente).
        updated_at (TIMESTAMP): Data/hora da última atualização do registro (preenchida automaticamente).
        deleted_at (TIMESTAMP): Data/hora de exclusão lógica do registro (opcional).

    Relacionamentos:
        user: Relacionamento com a tabela `users` (N:1).
        messages: Relacionamento com a tabela `messages` (1:N).
    """

    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(40), nullable=False)
    thread = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)

    user = relationship('User', back_populates='chats')
    messages = relationship('Message', back_populates='chat')


class Message(Base):
    """
    Modelo para a tabela `messages`, que armazena as mensagens trocadas em uma conversa.

    Colunas:
        id (int): Identificador único da mensagem.
        chat_id (int): ID da conversa à qual a mensagem pertence.
        user_message (str): Mensagem enviada pelo usuário.
        agent_message (str): Resposta enviada pelo agente (sistema).
        created_at (TIMESTAMP): Data/hora de criação do registro (preenchida automaticamente).

    Relacionamentos:
        chat: Relacionamento com a tabela `chats` (N:1).
    """

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_message = Column(Text, nullable=False)
    agent_message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    chat = relationship('Chat', back_populates='messages')


class Config(Base):
    """
    Modelo para a tabela `config`, que armazena configurações do banco de dados.

    Colunas:
        id (int): Identificador único da configuração.
        description_db (str): Descrição sobre o propósito do banco de dados.
        database_url (str): URL de conexão com o banco de dados.
        updated_at (TIMESTAMP): Data/hora da última atualização do registro (preenchida automaticamente).
    """

    __tablename__ = 'config'

    id = Column(Integer, primary_key=True, index=True)
    description_db = Column(Text, nullable=False)
    database_url = Column(String(255), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now())
