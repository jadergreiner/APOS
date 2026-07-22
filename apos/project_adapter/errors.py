class DetectorExecutionError(Exception):
    """Erro durante execucao de um detector."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
