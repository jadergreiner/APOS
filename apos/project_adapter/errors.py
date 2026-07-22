"""Exceções do módulo ProjectAdapter."""

from apos.errors import AposError


class DetectorExecutionError(AposError):
    """Erro durante execucao de um detector."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
