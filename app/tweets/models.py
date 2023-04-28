class Tweet:
    """Clase fundamental con el contenido del tweet sin procesar"""

    def __init__(self,tweet:str) -> None:
        self.value = tweet

    def __str__(self) -> str:
        return f'El tweet original es: {self.value}'
        