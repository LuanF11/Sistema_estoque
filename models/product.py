from dataclasses import dataclass
from datetime import date
from typing import Optional

# Modelo de dados para um produto no sistema
@dataclass
class Product:
    id: int | None
    nome: str
    quantidade: int
    valor_compra: float
    valor_venda: float
    data_validade: Optional[date]
    ativo: bool = True
