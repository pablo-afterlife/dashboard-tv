# Dashboard TV — Processo de Atualização Automática

Documentação completa do sistema que sincroniza a planilha Excel com o site automaticamente.

---

## Visão Geral do Fluxo

```
Você salva o Excel
       ↓  (até 30 segundos)
monitor_excel.py detecta a mudança
       ↓  (instantâneo)
gerar_dashboard_json.py lê a planilha e gera dashboard_tv_data.json
       ↓  (instantâneo)
git commit + push para o GitHub
       ↓  (~60 segundos — GitHub Pages republica)
Site detecta o novo JSON e atualiza automaticamente
       ↓  (até 20 segundos — polling do site)
Dados novos aparecem na TV sem precisar de F5
```

**Tempo total estimado:** 1 a 2 minutos após salvar o Excel.

---

## Arquivos do Sistema

### No PC (fora do repositório)

| Caminho | Função |
|---------|--------|
| `C:\Users\Consultor\Scripts\dashboard-monitor\monitor_excel.py` | Script principal — fica rodando em segundo plano |
| `C:\Users\Consultor\Scripts\dashboard-monitor\iniciar_monitor_oculto.vbs` | Launcher — inicia o monitor sem janela visível |
| `C:\Users\Consultor\Aquila\ADM - EGA - General\Arquivos Referencias\Escola\Andamento - Projetos.xlsx` | Planilha monitorada |

### No Repositório (GitHub)

| Arquivo | Função |
|---------|--------|
| `gerar_dashboard_json.py` | Converte Excel → JSON no formato correto |
| `dashboard_tv_data.json` | JSON gerado automaticamente (não editar manualmente) |
| `dashboard_tv_slides_auto.html` | Site do dashboard |
| `atualizar_dashboard.bat` | Alternativa manual para forçar atualização |
| `log_atualizacao.txt` | Registro de todas as operações |

---

## Configuração Inicial (fazer uma vez)

### 1. Copiar os scripts para o PC

Baixe do repositório GitHub e copie para:
```
C:\Users\Consultor\Scripts\dashboard-monitor\
├── monitor_excel.py
└── iniciar_monitor_oculto.vbs
```

### 2. Instalar dependências Python

Abra o Prompt de Comando e execute:
```
pip install openpyxl
```

### 3. Configurar inicialização automática com o Windows

1. Pressione `Win + R`, digite `shell:startup` e pressione Enter
2. Na pasta que abrir, crie um atalho apontando para:
   ```
   C:\Users\Consultor\Scripts\dashboard-monitor\iniciar_monitor_oculto.vbs
   ```
3. Pronto — o monitor vai iniciar sozinho toda vez que o Windows ligar

### 4. Verificar autenticação do Git

No repositório local, confirme que o Git está autenticado:
```
cd "C:\Users\Consultor\OneDrive - Aquila\SITE AQUILA\teste123\dashboard_tv_slides_pacote\dashboard_tv_slides_pacote"
git push origin main
```
Se pedir senha, configure as credenciais do GitHub uma vez só.

---

## Uso Diário

### Iniciar o monitor manualmente

Duplo clique em:
```
C:\Users\Consultor\Scripts\dashboard-monitor\iniciar_monitor_oculto.vbs
```

Nenhuma janela aparece — o monitor sobe completamente oculto.

### Verificar se o monitor está rodando

Abra o **Gerenciador de Tarefas** (`Ctrl + Shift + Esc`) → aba **Detalhes** → procure `pythonw.exe`.

### Encerrar o monitor

**Gerenciador de Tarefas** → aba **Detalhes** → clique com botão direito em `pythonw.exe` → **Finalizar tarefa**.

### Forçar atualização manual

Duplo clique em `atualizar_dashboard.bat` no repositório local.

### Ver o log de atualizações

Abra o arquivo:
```
C:\Users\Consultor\OneDrive - Aquila\SITE AQUILA\teste123\dashboard_tv_slides_pacote\dashboard_tv_slides_pacote\log_atualizacao.txt
```

---

## Como o Monitor Funciona

O `monitor_excel.py` entra em loop infinito fazendo o seguinte a cada **30 segundos**:

1. Calcula o hash MD5 do arquivo Excel
2. Compara com o hash da verificação anterior
3. **Se for diferente** → arquivo foi salvo → inicia sincronização:
   - Chama `gerar_dashboard_json.py` para converter a planilha em JSON
   - Verifica se o JSON mudou (evita commits sem alteração real)
   - Faz `git commit` e `git push` para o GitHub
4. **Se for igual** → nenhuma ação, aguarda os próximos 30 segundos

### Por que MD5 e não `data de modificação`?

A data de modificação do arquivo muda mesmo quando o Excel faz saves automáticos sem alteração de conteúdo. O MD5 garante que só há sincronização quando os dados realmente mudam.

---

## Como o Site se Atualiza Sozinho

O site verifica o arquivo `dashboard_tv_data.json` a cada **20 segundos** via `fetch()` com `cache: 'no-store'` (ignora cache do navegador). Quando o JSON muda:

- O site detecta os novos dados na próxima verificação
- Atualiza todos os slides automaticamente (sem F5)
- Exibe o badge "Modo dinâmico · JSON atualizado" no canto superior

Se o fetch falhar (sem internet, GitHub fora do ar):
- O site mantém os últimos dados carregados com sucesso
- Exibe "Modo dinâmico · usando cache local"

---

## Formato do JSON Gerado

O `gerar_dashboard_json.py` produz um arquivo com esta estrutura:

```json
{
  "source_file": "Andamento - Projetos.xlsx",
  "source_sheet": "filtrada",
  "generated_at": "2026-04-22T10:30:00-03:00",
  "row_count": 39,
  "records": [
    {
      "Proposta": "0619/25 BNN A",
      "Cliente": "Empresa Exemplo",
      "Produto": "Formação de Gestores",
      "Status": "Em andamento",
      "Início": "2026-01-19",
      "Término": "2026-07-19",
      "Quantidade Livro": 80,
      "Valor Total": 2800.0,
      ...
    }
  ]
}
```

**Regras aplicadas automaticamente:**
- Células vazias, traços e `""` → `null`
- Números inteiros (ex: `80.0`) → `80`
- Datas → formato `YYYY-MM-DD` (sem hora)
- Textos → `_x000D_` removido, espaços nas bordas cortados
- `NaN` / `Infinity` → `null` (JSON válido)

---

## Requisitos

| Item | Status |
|------|--------|
| Python 3.10 ou superior | Necessário |
| Biblioteca `openpyxl` | `pip install openpyxl` |
| Git instalado e autenticado | Necessário |
| Planilha na aba `filtrada` | Necessário |
| PC ligado com monitor rodando | Necessário para sincronização |

---

## Solução de Problemas

### Site continua mostrando dados antigos

1. Verifique se o monitor está rodando (Gerenciador de Tarefas → `pythonw.exe`)
2. Abra o `log_atualizacao.txt` e procure erros
3. Execute `atualizar_dashboard.bat` manualmente para forçar sincronização

### Monitor não inicia com o VBS

1. Verifique se `monitor_excel.py` está em `C:\Users\Consultor\Scripts\dashboard-monitor\`
2. Abra o VBS em um editor de texto e confirme o caminho do script
3. Tente iniciar diretamente: `python monitor_excel.py` no terminal para ver o erro

### Erro "openpyxl not found"

```
pip install openpyxl
```

### Push falha (erro de autenticação)

```
git config --global credential.helper manager
git push origin main
```
Siga as instruções de autenticação do GitHub que aparecerem.

### Planilha não encontrada

Confirme que o caminho no `monitor_excel.py` está correto:
```python
EXCEL_PATH = Path(r"C:\Users\Consultor\Aquila\ADM - EGA - General\Arquivos Referencias\Escola\Andamento - Projetos.xlsx")
```
