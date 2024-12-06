from typing import Callable, Type

from langchain.tools import StructuredTool
from pydantic import BaseModel


class GenericToolCreator:
    """
    Classe genérica para criar tools (ferramentas) de maneira flexível.

    **Recomendado**: Escrever o name, description e args_schema em inglês.

    Attributes:
        func (Callable): A função a ser associada à ferramenta.
        name (str): O nome da ferramenta.
        description (str): Uma descrição detalhada da ferramenta.
        args_schema (Type[BaseModel]): Classe Pydantic usada para validar os argumentos da ferramenta.
        return_direct (bool): Define se o retorno da função será enviado diretamente ao usuário ou processado posteriormente. Padrão é `False`.
    """

    def __init__(
        self,
        func: Callable,
        name: str,
        description: str,
        args_schema: Type[BaseModel],
        return_direct: bool = False,
    ):
        self.func = func
        self.name = name
        self.description = description
        self.args_schema = args_schema
        self.return_direct = return_direct

    def create_tool(self) -> dict:
        """
        Cria uma instância de ferramenta configurada.

        Returns:
            dict: Um dicionário contendo a configuração da ferramenta, incluindo:
                - name (str): O nome da ferramenta.
                - description (str): A descrição da ferramenta.
                - args_schema (Type[BaseModel]): O esquema de argumentos da ferramenta.
                - func (Callable): A função associada à ferramenta.
                - return_direct (bool): Se o retorno será enviado diretamente ao usuário.
        """
        return StructuredTool.from_function(
            func=self.func,
            name=self.name,
            description=self.description,
            args_schema=self.args_schema,
            return_direct=self.return_direct,
        )
