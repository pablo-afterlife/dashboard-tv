# Dashboard TV — v2

Painel de monitoramento de projetos e treinamentos para exibição contínua em TVs corporativas.  
Os dados saem direto da planilha Excel e chegam ao site automaticamente — sem copiar arquivos, sem abrir terminais, sem pressionar F5.

---

## Como funciona

```
Você salva o Excel
      ↓  até 30 s
monitor_excel.py detecta a mudança (hash MD5)
      ↓  instantâneo
gerar_dashboard_json.py converte a planilha em JSON
      ↓  instantâneo
git commit + push → GitHub
      ↓  ~60 s  (GitHub Pages republica o site)
Site detecta o JSON novo via fetch()
      ↓  até 20 s  (polling automático)
TV exibe os dados atualizados — sem F5
```

**Tempo total:** 1 a 2 minutos após salvar o Excel.

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

## Arquivos do sistema

### Repositório GitHub

| Arquivo | Função |
|---------|--------|
| `dashboard_tv_slides_auto.html` | Site completo (HTML + CSS + JS) |
| `dashboard_tv_data.json` | Dados gerados automaticamente — não editar manualmente |
| `gerar_dashboard_json.py` | Converte Excel → JSON com formato correto |
| `atualizar_dashboard.bat` | Atualização manual forçada |
| `monitor_excel.py` | Script do monitor — copiar para a pasta Scripts |
| `iniciar_monitor_oculto.vbs` | Launcher sem janela — copiar para a pasta Scripts |
| `log_atualizacao.txt` | Registro gerado automaticamente de todas as sincronizações |

### PC local (fora do repositório)

| Caminho | Função |
|---------|--------|
| `C:\Users\Consultor\Scripts\dashboard-monitor\monitor_excel.py` | Monitor rodando em segundo plano |
| `C:\Users\Consultor\Scripts\dashboard-monitor\iniciar_monitor_oculto.vbs` | Launcher — duplo clique para iniciar oculto |
| `C:\Users\Consultor\Aquila\ADM - EGA - General\Arquivos Referencias\Escola\Andamento - Projetos.xlsx` | Planilha monitorada |

---

## Configuração inicial (fazer uma vez)

### 1. Instalar dependência Python

```
pip install openpyxl
```

### 2. Copiar os scripts do monitor

Após clonar o repositório, copie para a pasta do monitor:

```
monitor_excel.py           →  C:\Users\Consultor\Scripts\dashboard-monitor\
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

**Iniciar o monitor agora** — duplo clique em `iniciar_monitor_oculto.vbs`.  
Nenhuma janela aparece. O processo sobe completamente oculto.

**Verificar se está rodando** — Gerenciador de Tarefas (`Ctrl + Shift + Esc`) → aba **Detalhes** → procure `pythonw.exe`.

**Encerrar o monitor** — Gerenciador de Tarefas → botão direito em `pythonw.exe` → **Finalizar tarefa**.

**Forçar atualização manual** — duplo clique em `atualizar_dashboard.bat` no repositório local.

**Ver o log** — abra `log_atualizacao.txt` na raiz do repositório local.

---

## Exibição na TV

1. Abra `dashboard_tv_slides_auto.html` no navegador
2. `F11` para tela cheia
3. Os slides rotacionam automaticamente — nenhuma interação necessária

O site verifica o JSON a cada **20 segundos** com `cache: 'no-store'` (ignora cache do navegador). Quando detecta dados novos, atualiza todos os slides automaticamente e exibe o badge **"Modo dinâmico · JSON atualizado"**. Se o fetch falhar (sem internet, GitHub fora do ar), mantém os últimos dados com o badge **"usando cache local"**.

---

## Detalhes técnicos

### Por que o monitor usa MD5 e não data de modificação?

O Excel atualiza a data de modificação do arquivo mesmo em saves automáticos sem alteração de conteúdo. O hash MD5 garante que a sincronização só dispara quando os dados realmente mudam.

### Formato do JSON gerado

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
      "Valor Total": 2800.0
    }
  ]
}
```

**Regras aplicadas automaticamente pelo `gerar_dashboard_json.py`:**

| Entrada | Saída |
|---------|-------|
| Célula vazia, `""`, `-` | `null` |
| `NaN`, `Infinity` | `null` |
| Data/hora (`datetime`) | `"YYYY-MM-DD"` |
| Float inteiro (`80.0`) | `80` |
| Texto com `_x000D_` | Texto limpo |
| Nomes das colunas | Preservados exatamente como no Excel |

### Retry no push

O monitor tenta o push até **4 vezes** com backoff exponencial (2 s → 4 s → 8 s → 16 s) antes de registrar falha no log.

---

## Requisitos

| Item | Detalhe |
|------|---------|
| Python 3.10+ | `pip install openpyxl` |
| Git instalado e autenticado | `credential.helper manager` |
| Aba `filtrada` no Excel | Com cabeçalhos na primeira linha |
| PC ligado com monitor rodando | Necessário para sincronização automática |
| Conexão com a internet | Para git push ao GitHub |

---

## Solução de problemas

**Site mostra dados antigos**  
Verifique se `pythonw.exe` aparece no Gerenciador de Tarefas. Se não, inicie o monitor. Abra `log_atualizacao.txt` para ver o último erro registrado.

**Monitor não inicia pelo VBS**  
Abra um terminal e rode `python monitor_excel.py` diretamente para ver a mensagem de erro completa.

**Push falha — erro de autenticação**  
Execute `git config --global credential.helper manager` e faça um push manual para salvar as credenciais.

**Aba `filtrada` não encontrada**  
O Excel precisa ter uma aba com exatamente esse nome (minúsculas, sem espaços).

**`openpyxl` não instalado**  
`pip install openpyxl`

**Planilha não encontrada pelo monitor**  
Confirme que o caminho no `monitor_excel.py` está correto:
```python
EXCEL_PATH = Path(r"C:\Users\Consultor\Aquila\ADM - EGA - General\Arquivos Referencias\Escola\Andamento - Projetos.xlsx")
```
