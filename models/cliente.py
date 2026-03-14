from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Cliente:
    """Modelo de dados para um cliente no sistema"""
    id: int | None
    nome: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    ativo: bool = True
    data_cadastro: Optional[datetime] = None


@dataclass
class Fiado:
    """Modelo de dados para um fiado (dívida de um cliente)"""
    id: int | None
    cliente_id: int
    produto_id: int
    quantidade: int
    valor_unitario: float
    valor_total: float
    valor_pendente: float
    observacao: Optional[str] = None
    data_fiado: Optional[datetime] = None
    data_vencimento: Optional[str] = None


@dataclass
class FiadoPagamento:
    """Modelo de dados para um pagamento parcial de um fiado"""
    id: int | None
    fiado_id: int
    valor_pago: float
    data_pagamento: Optional[datetime] = None
    observacao: Optional[str] = None
