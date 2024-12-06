def format_prompt(
    question: str, language: str = None, file_text: str = None
) -> str:
    """
    Formata um prompt para interação com um modelo LLM.

    Args:
        question (str): Pergunta ou tarefa para o modelo responder.
        language (str | None): Linguagem desejada para a resposta do modelo. Pode ser None.
        file_text (str | None): Conteúdo adicional de um arquivo de texto. Pode ser None.

    Returns:
        str: Prompt formatado para envio ao LLM.
    """
    # Validar e normalizar o idioma
    language = language.capitalize() if language else 'English'

    # Criar a seção de conteúdo do arquivo se fornecido
    file_text_section = (
        f'\n### FILE TEXT ###\n{file_text.strip()}' if file_text else ''
    )

    # Criar o prompt estruturado
    prompt = f"""
### USER QUESTION ###
{question.strip()}

{file_text_section}

### RESPONSE REQUIREMENTS ###
The response should be in {language}. It must be clear, concise, and contextually relevant, adhering to the user's language preference.
"""
    return prompt.strip()
