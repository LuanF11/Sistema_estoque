# Backup e Restauração do Banco de Dados

## Como Usar

### Exportar Banco de Dados

1. Acesse o menu **Ferramentas** → **Backup e Restauração**
2. Na aba **Exportar Backup**:
   - Clique em "Escolher Pasta e Exportar"
   - Selecione a pasta onde deseja salvar o backup
   - O arquivo será salvo com o padrão: `estoque_backup_YYYYMMDD_HHMMSS.db`

**Benefícios:**
- Seu banco de dados está seguro em uma pasta de sua escolha
- Timestamp automático permite manter múltiplas versões
- Ideal para backup em nuvem (Google Drive, OneDrive, etc.)

### Restaurar Banco de Dados

1. Acesse o menu **Ferramentas** → **Backup e Restauração**
2. Na aba **Restaurar Backup**:
   - Clique em "Escolher Arquivo e Restaurar"
   - Selecione o arquivo de backup (*.db)
   - Confirme a restauração
   - Um backup de segurança será criado automaticamente
   - Reinicie a aplicação para recarregar os dados

**Segurança:**
- Um backup de segurança é criado automaticamente antes de restaurar
- Se houver erro, o banco original será preservado
- Você pode reverter a qualquer momento usando um backup anterior

## Localização do Banco de Dados

**Quando executando como script Python:**
- Local: `Sistema_estoque/estoque.db`

**Quando executando como executável (.exe):**
- Local: `C:\Users\{seu_usuario}\.estoque\estoque.db`

## Dicas de Segurança

1. **Faça backups regularmente** - Defina uma rotina (diária/semanal)
2. **Mantenha múltiplas cópias** - Não dependa de um único backup
3. **Teste restaurações** - Verifique se os backups funcionam ocasionalmente
4. **Use armazenamento em nuvem** - Backup para Google Drive, OneDrive, etc.
5. **Backup externo** - Considere backup em dispositivo USB para casos extremos

## Estrutura do Arquivo de Backup

Os arquivos de backup são bancos de dados SQLite válidos contendo:
- Produtos e informações de estoque
- Movimentações de caixa
- Relatórios e análises
- Tags de produtos
- Dados de "fiado" (débitos)
- Dados de prejuízos registrados

## Troubleshooting

### Erro: "Arquivo não encontrado"
- Verifique se o arquivo de backup ainda existe
- O arquivo pode ter sido movido ou deletado

### Erro: "Arquivo selecionado não é um banco de dados válido"
- Certifique-se de que selecionou um arquivo criado pelo Sistema de Estoque
- Tente usar um backup anterior

### A restauração falhou
- Um backup de segurança foi criado (.estoque_safety_backup.db)
- Entre em contato com o administrador do sistema

