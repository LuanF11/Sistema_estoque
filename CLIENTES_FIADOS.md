# Gerenciamento de Clientes e Fiados

## Visão Geral

Este módulo implementa um sistema completo para gerenciar clientes e seus fiados (dívidas/crédito), com suporte a pagamentos parciais. Os clientes podem ter múltiplos fiados, e cada fiado pode ser pago aos poucos.

## Características Implementadas

### 1. **Modelo de Cliente**
- Registro de clientes com informações básicas
- Campos: Nome (obrigatório), Telefone, Email, Endereço
- Cada cliente tem um ID único
- Controle de ativo/inativo (soft delete)

### 2. **Fiados (Dívidas/Crédito)**
- Um cliente pode ter múltiplos fiados
- Cada fiado registra:
  - Produto vendido
  - Quantidade
  - Valor unitário e valor total
  - **Valor pendente** (permite pagamentos parciais)
  - Data do fiado
  - Data de vencimento (opcional)
  - Observações

### 3. **Pagamentos Parciais**
- Cada fiado pode receber múltiplos pagamentos
- Um pagamento é registrado com:
  - Valor pago
  - Data do pagamento
  - Observação (opcional)
- O valor pendente é automaticamente atualizado
- Validação para evitar pagamentos que excedam o saldo pendente

### 4. **Interface de Usuário - ClienteWindow**

#### Painel Esquerdo
- **Pesquisa de Clientes**: Campo de busca por nome (em tempo real)
- **Botão "Novo Cliente"**: Criar novo cliente
- **Tabela de Clientes**: Lista todos os clientes com seu saldo pendente total

#### Painel Direito
- **Detalhes do Cliente**: Informações completas do cliente selecionado
- **Buttons de Ação**:
  - Editar Cliente
  - Deletar Cliente
  - Novo Fiado
- **Tabela de Fiados**: Lista fiados do cliente selecionado
- **Buttons de Ação para Fiados**:
  - **Novo Fiado**: Criar novo fiado para o cliente
  - **Adicionar Pagamento**: Registrar um pagamento parcial
  - **Ver Pagamentos**: Visualizar histórico de pagamentos
  - **Deletar Fiado**: Remover um fiado

## Estrutura de Código

### Modelos (models/cliente.py)
```python
- Cliente: Dados do cliente
- Fiado: Dados de um fiado/dívida
- FiadoPagamento: Dados de um pagamento
```

### Repositórios
- **ClienteRepository** (repositories/cliente_repository.py)
  - CRUD de clientes
  - Busca por nome
  - Cálculo de saldo pendente
  
- **FiadoRepository** (repositories/fiado_repository.py)
  - CRUD de fiados
  - Gerenciamento de pagamentos
  - Listagem por cliente ou período

### Serviço (services/cliente_service.py)
- Lógica de negócio para clientes e fiados
- Validação de dados
- Gerenciamento de estoque ao criar fiados
- Reposição de estoque ao deletar fiados

### Controller (controllers/cliente_controller.py)
- Camada intermediária entre UI e Service
- Tratamento de erros
- Formatação de respostas

### Interface (ui/windows/cliente_window.py)
- **ClienteWindow**: Janela principal
- **NovoClienteDialog**: Criar novo cliente
- **EditarClienteDialog**: Editar cliente
- **NovoFiadoDialog**: Criar novo fiado
- **PagamentoFiadoDialog**: Adicionar pagamento
- **VisualizarPagamentosDialog**: Ver histórico de pagamentos

## Fluxo de Uso

### Criar um Cliente
1. Clique no botão "Novo Cliente"
2. Preencha os dados (nome é obrigatório)
3. Clique em "Salvar"

### Criar um Fiado
1. Selecione um cliente na lista
2. Clique em "Novo Fiado"
3. Selecione o produto, quantidade e data de vencimento (opcional)
4. Clique em "Salvar"
5. O estoque do produto é automaticamente reduzido

### Registrar um Pagamento
1. Selecione um cliente
2. Selecione um fiado da tabela
3. Clique em "Adicionar Pagamento"
4. Digite o valor a pagar (máximo = valor pendente)
5. Clique em "Confirmar Pagamento"
6. O valor pendente é automaticamente atualizado

### Ver Histórico de Pagamentos
1. Selecione um cliente
2. Selecione um fiado
3. Clique em "Ver Pagamentos"
4. Uma janela mostra todos os pagamentos do fiado

## Banco de Dados

### Tabelas Criadas/Modificadas

#### Tabela: clientes
```sql
id          - INTEGER PRIMARY KEY
nome        - TEXT UNIQUE (obrigatório)
telefone    - TEXT
email       - TEXT
endereco    - TEXT
ativo       - INTEGER (1 = ativo, 0 = inativo)
data_cadastro - DATETIME
```

#### Tabela: fiados
```sql
id              - INTEGER PRIMARY KEY
cliente_id      - INTEGER (FK para clientes)
produto_id      - INTEGER (FK para produtos)
quantidade      - INTEGER
valor_unitario  - REAL
valor_total     - REAL
valor_pendente  - REAL (chave principal para rastrear saldo)
observacao      - TEXT
data_fiado      - DATETIME
data_vencimento - DATE (opcional)
```

#### Tabela: fiado_pagamentos
```sql
id          - INTEGER PRIMARY KEY
fiado_id    - INTEGER (FK para fiados)
valor_pago  - REAL
data_pagamento - DATETIME
observacao  - TEXT
```

## Validações

1. **Cliente**: Nome obrigatório e único
2. **Fiado**: 
   - Quantidade > 0
   - Cliente deve existir
   - Produto deve existir
   - Estoque deve ser suficiente
3. **Pagamento**: 
   - Valor > 0
   - Valor não pode exceder saldo pendente
   - Fiado deve existir

## Integração no Menu Principal

O módulo foi integrado no menu principal da aplicação:
- Menu: **Clientes > Gerenciar Clientes e Fiados**
- Atalho: Acesso rápido via menu dropdown

## Exemplo de Uso Prático

1. **João chega à loja e leva produtos a prazo**
   - Crie cliente "João"
   - Crie fiado: Vaso (2 unid. x R$ 80 = R$ 160)
   - Estoque reduzido automaticamente

2. **João paga R$ 100 uma semana depois**
   - Selecione João
   - Selecione o fiado
   - Clique "Adicionar Pagamento"
   - Registre R$ 100
   - Saldo pendente agora é R$ 60

3. **João paga mais R$ 60 depois**
   - Registre mais um pagamento de R$ 60
   - Saldo pendente agora é R$ 0 (fiado quitado)

4. **Ver histórico de pagamentos**
   - Clique "Ver Pagamentos"
   - Veja todos os pagamentos registrados

## Melhorias Futuras

- Relatórios de fiados pendentes por cliente
- Notificações automáticas para fiados vencidos
- Integração com cálculo automatizado de juros
- Exportação de dados para relatórios
- Backup automático de dados de clientes
