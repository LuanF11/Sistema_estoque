# 🚀 Como Gerar Executável do Sistema de Estoque

## Resumo Executivo
Este guia explica como transformar seu projeto Python em um **arquivo `.exe`** que funciona com 2 cliques, sem precisa de Python instalado no PC da cliente.

---

## 📋 O QUE VAI ACONTECER?

Seu projeto será transformado assim:

```
Antes: Pasta com arquivos Python (.py)
  ↓
Depois: Arquivo único (Sistema_Estoque.exe)
  ↓
Cliente dá 2 cliques → Sistema abre!
```

---

## 🔧 PASSO A PASSO COMPLETO

### **PASSO 1: Preparação (1 vez)**

1. Abra a pasta do projeto: `c:\Users\Luan\Desktop\Sistema_estoque`
2. Veja os arquivos criados:
   - `build.spec` - Arquivo de configuração
   - `BUILD_EXECUTABLE.bat` - Script para gerar o .exe

### **PASSO 2: Gerar o Executável (5-15 minutos)**

**Windows:**
1. Entre na pasta `c:\Users\Luan\Desktop\Sistema_estoque`
2. Dê dois cliques em `BUILD_EXECUTABLE.bat`
3. Uma janela OpenShell vai abrir e processar (pode levar 5-15 minutos)
4. Quando terminar, verá a mensagem: `SUCESSO!`
5. O arquivo `Sistema_Estoque.exe` foi criado em `dist\Sistema_Estoque.exe`

**Linha de comando (alternativa):**
```bash
cd c:\Users\Luan\Desktop\Sistema_estoque
pyinstaller build.spec
```

### **PASSO 3: Testar Localmente**

1. Abra a pasta `dist`
2. Dê dois cliques em `Sistema_Estoque.exe`
3. O sistema deve abrir normalmente!
4. Se abrir, sucesso! ✅

### **PASSO 4: Entregar para Cliente**

**Opção A - Arquivo único (recomendado):**
```
Sistema_Estoque.exe (arquivo único)
```
- Copie apenas o arquivo `.exe` de `dist\Sistema_Estoque.exe`
- Envie para cliente
- Cliente dá 2 cliques e pronto!

**Opção B - Pasta completa (mais segura):**
```
dist/
├── Sistema_Estoque.exe
├── _internal/
├── ... (arquivos de suporte)
```
- Copie a pasta `dist` inteira
- Envie em um .ZIP
- Cliente extrai e dá 2 cliques no `.exe`

---

## ⚙️ CONFIGURAÇÕES IMPORTANTES

### **Se quiser adicionar um ícone:**
1. Salve uma imagem `.ico` em `ui/resources/icon.ico`
2. O arquivo `build.spec` já tenta usar este ícone
3. Gere novamente com `BUILD_EXECUTABLE.bat`

### **Se o sistema não abrir:**
- Verifique se `schema.sql` exists em `database/`
- Verifique se todas as pastas estão presentes
- Rode manualmente: `python main.py` para testar

---

## 📁 ESTRUTURA FINAL

Depois de rodar `BUILD_EXECUTABLE.bat`, terá:

```
Sistema_estoque/
├── main.py
├── config.py
├── requirements.txt
├── build.spec                  ← Arquivo de configuração
├── BUILD_EXECUTABLE.bat        ← Script para gerar .exe
├── GUIA_EXECUTAVEL.md          ← Este arquivo
├── database/
│   └── schema.sql
├── dist/                       ← Pasta com o executável!
│   ├── Sistema_Estoque.exe     ← O arquivo para enviar!
│   └── _internal/              ← Bibliotecas necessárias
├── build/                      ← Pasta temporária (pode deletar)
└── ... (resto do projeto)
```

---

## 🎯 RESUMO DO QUE FAZER PARA CLIENTE

Sua cliente vai receber:
```
Sistema_Estoque.exe
```

E fazer:
1. **Dois cliques no arquivo**
2. Sistema abre automaticamente
3. Sem precisar de nada instalado!

---

## ❓ PERGUNTAS COMUNS

**P: O cliente precisa de Python instalado?**
R: NÃO! O executável já contém tudo necessário.

**P: Preciso gerar novamente o .exe depois de mudanças?**
R: SIM. Sempre que mudar algum código, rode `BUILD_EXECUTABLE.bat` novamente.

**P: Dá para distribuir como instalador (.MSI)?**
R: SIM! Use INNO Setup ou Advanced Installer (após ter o .exe).

**P: Que tamanho vai ter o .exe?**
R: Aproximadamente 200-300 MB (PySide6 é pesado).

**P: Pode rodar em Mac/Linux?**
R: Precisa gerar para cada sistema operacional. Este guia é para Windows.

---

## 🚀 PRÓXIMOS PASSOS (OPCIONAL)

### Criar um Instalador (.MSI ou .EXE Installer)
Use **INNO Setup** (grátis) para criar um instalador profissional:
1. Baixe em: https://jrsoftware.org/isdl.php
2. Aponte para a pasta `dist\`
3. Gera um `Setup.exe` que o cliente executa
4. Sistema é instalado no PC dela

### Otimizar Tamanho
Se quiser reduzir o tamanho do `.exe`:
1. Remova dependências não usadas em `requirements.txt`
2. Use `--onefile` no `build.spec`

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique se `python main.py` funciona
2. Verifique se todas as dependências em `requirements.txt` estão instaladas
3. Verifique o arquivo `build.spec` - pode precisar ajustar os `datas`

Boa sorte! 🎉
