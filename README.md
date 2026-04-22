# Dashboard TV — v2

Painel de monitoramento de projetos e treinamentos para exibição contínua em TVs corporativas.  
Os dados saem direto da planilha Excel e chegam ao site automaticamente — sem copiar arquivos, sem abrir terminais, sem pressionar F5.

---

## Como funciona

```
Você salva o Excel
      ↓  até 30 s
Monitor detecta a mudança
      ↓  instantâneo
Planilha convertida em JSON
      ↓  instantâneo
Git commit + push → GitHub
      ↓  ~60 s  (GitHub Pages publica)
Site detecta o JSON novo
      ↓  até 20 s  (polling automático)
TV exibe os dados atualizados
```

**Tempo total:** 1 a 2 minutos após salvar o Excel.  
Nenhuma ação manual necessária além de salvar a planilha.

---

## Slides

| # | Título | O que exibe |
|---|--------|-------------|
| 0 | O que está mais perto de começar | Projeto prioritário, dias restantes, radar de inícios, alertas |
| 1 | Próximos Treinamentos | Sessões confirmadas, datas, instrutor |
| 2 | Agenda Operacional | Projetos em andamento e fila de início |
| 3 | Envios e Materiais | Livros, kits, certificados por projeto |
| 4 | Resumo Executivo | KPIs da carteira, ranking por valor, gestor, UF, produto |

Troca automática a cada **30 segundos** · barra de progresso · navegação por dots ou setas do teclado.

---

## Estrutura de arquivos

```
Repositório GitHub (dashboard-tv)
├── dashboard_tv_slides_auto.html   → Site completo (HTML + CSS + JS)
├── dashboard_tv_data.json          → Dados gerados automaticamente (não editar)
├── gerar_dashboard_json.py         → Converte Excel → JSON (chamado pelo monitor)
├── atualizar_dashboard.bat         → Atualização manual forçada
├── monitor_excel.py                → Script do monitor (copiar para pasta Scripts)
├── iniciar_monitor_oculto.vbs      → Launcher sem janela (copiar para pasta Scripts)
├── processo.md                     → Documentação técnica detalhada do fluxo
└── log_atualizacao.txt             → Registro de todas as sincronizações

Fora do repositório — PC local
C:\Users\Consultor\Scripts\dashboard-monitor\
├── monitor_excel.py                → Cópia do repositório
└── iniciar_monitor_oculto.vbs      → Cópia do repositório
```

---

## Configuração inicial (fazer uma vez)

### 1. Dependência Python

```
pip install openpyxl
```

### 2. Copiar os scripts do monitor

Após clonar o repositório, copie estes dois arquivos para a pasta do monitor:

```
monitor_excel.py          →  C:\Users\Consultor\Scripts\dashboard-monitor\
iniciar_monitor_oculto.vbs →  C:\Users\Consultor\Scripts\dashboard-monitor\
```

### 3. Configurar inicialização automática com o Windows

1. `Win + R` → digite `shell:startup` → Enter
2. Na pasta que abrir, crie um atalho apontando para:
   ```
   C:\Users\Consultor\Scripts\dashboard-monitor\iniciar_monitor_oculto.vbs
   ```
3. Pronto — o monitor inicia sozinho toda vez que o Windows ligar.

### 4. Autenticação Git

No repositório local, confirme que o push funciona:

```
git push origin main
```

Se pedir credenciais, configure uma vez:

```
git config --global credential.helper manager
```

---

## Uso diário

### Iniciar o monitor agora

Duplo clique em:
```
C:\Users\Consultor\Scripts\dashboard-monitor\iniciar_monitor_oculto.vbs
```

Nenhuma janela aparece — o processo sobe oculto.

### Verificar se está rodando

**Gerenciador de Tarefas** (`Ctrl + Shift + Esc`) → aba **Detalhes** → procure `pythonw.exe`.

### Encerrar o monitor

**Gerenciador de Tarefas** → clique com botão direito em `pythonw.exe` → **Finalizar tarefa**.

### Forçar atualização manual

Duplo clique em `atualizar_dashboard.bat` no repositório local.

### Ver o log

```
[repositório]\log_atualizacao.txt
```

---

## Exibição na TV

1. Abra `dashboard_tv_slides_auto.html` no navegador
2. `F11` para tela cheia
3. Os slides rotacionam automaticamente — nenhuma interação necessária

O site verifica o JSON a cada **20 segundos**. Quando há dados novos, atualiza todos os slides automaticamente, sem F5.

---

## Componentes técnicos

### `monitor_excel.py`

- Loop a cada **30 s**, calcula hash MD5 do Excel
- Se o hash mudou → chama `gerar_dashboard_json.py` → git commit + push
- Retry automático no push (4 tentativas, backoff exponencial: 2s / 4s / 8s / 16s)
- Usa `pythonw.exe` quando iniciado pelo `.vbs` → sem janela, sem ícone na taskbar

### `gerar_dashboard_json.py`

Converte a aba `filtrada` do Excel em JSON válido:

- Células vazias, `""`, `-` → `null`
- `NaN` / `Infinity` → `null`  
- Datas → `YYYY-MM-DD` (sem hora)
- Inteiros sem casas decimais (`80.0` → `80`)
- Nomes das colunas preservados exatamente como estão no Excel

Saída:

```json
{
  "source_file": "Andamento - Projetos.xlsx",
  "source_sheet": "filtrada",
  "generated_at": "2026-04-22T10:30:00-03:00",
  "row_count": 39,
  "records": [ { "Proposta": "...", "Cliente": "...", ... } ]
}
```

### `dashboard_tv_slides_auto.html`

- `fetch()` com `cache: 'no-store'` a cada 20 s
- Cache local automático — se o fetch falhar, mantém os últimos dados
- Fallback em dados embutidos no HTML — funciona offline
- Reinício completo a cada 6 horas (evita memory leak em exibição 24/7)
- Timezone São Paulo em todos os cálculos de data

---

## Requisitos

| Item | Detalhe |
|------|---------|
| Python 3.10+ | `pip install openpyxl` |
| Git autenticado | `credential.helper manager` |
| Aba `filtrada` no Excel | Com cabeçalhos na primeira linha |
| PC ligado | Monitor precisa estar rodando |
| Internet | Para o push ao GitHub |

---

## Solução de problemas

**Site mostra dados antigos (de março)**  
→ O monitor não está rodando ou o push está falhando. Verifique `log_atualizacao.txt` e confirme `pythonw.exe` no Gerenciador de Tarefas.

**Monitor não inicia pelo VBS**  
→ Execute `python monitor_excel.py` direto no terminal para ver o erro completo.

**Push falha — autenticação**  
→ `git config --global credential.helper manager` e faça um push manual para salvar as credenciais.

**Aba `filtrada` não encontrada**  
→ O Excel precisa ter uma aba com exatamente esse nome (minúsculas).

**`openpyxl` não instalado**  
→ `pip install openpyxl`

---

Documentação técnica completa do fluxo: [`processo.md`](processo.md)
