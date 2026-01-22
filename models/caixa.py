from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Caixa:
    id: int | None
    data: str
    valor_abertura: float
    status: str = "ABERTO"
    valor_fechamento: Optional[float] = None
    data_abertura: Optional[datetime] = None
    data_fechamento: Optional[datetime] = None
