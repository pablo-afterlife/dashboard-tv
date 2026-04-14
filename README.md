# Dashboard TV Slides - v1

Painel de monitoramento de projetos e treinamentos para exibição contínua em TVs e monitores. Desenvolvido para rodar em modo tela cheia com troca automática de slides, permitindo que equipes acompanhem o status da carteira de projetos sem intervenção manual.

![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Licença](https://img.shields.io/badge/licença-privado-lightgrey)

---

## Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura dos Slides](#estrutura-dos-slides)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Atualização dos Dados](#atualização-dos-dados)
- [Configuração](#configuração)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Tecnologias](#tecnologias)
- [Solução de Problemas](#solução-de-problemas)
- [Suporte](#suporte)

---

## Visão Geral

Este dashboard transforma dados de uma planilha Excel de acompanhamento de projetos em uma experiência visual de slides automáticos. Ideal para exibir em TVs de escritório, monitores de equipe ou salas de reunião, oferecendo uma visão clara e atualizada de:

- Projetos em andamento e seus prazos
- Próximos treinamentos e sessões confirmadas
- Materiais, livros e kits previstos
- Resumo executivo da carteira de projetos
- Alertas visuais para projetos atrasados ou prestes a iniciar

---

## Funcionalidades

- **Troca automática de slides** — rotação a cada 12 segundos, sem necessidade de interação
- **Atualização automática dos dados** — lê o arquivo `dashboard_tv_data.json` a cada 60 segundos
- **Interface responsiva** — adapta-se a qualquer resolução de tela (Full HD, 4K, etc.)
- **Alertas visuais** — destaque para projetos com data vencida, previsão próxima e prioridade máxima
- **KPIs em tempo real** — total de projetos, valor da carteira, treinamentos pendentes
- **Design profissional** — gradientes, glassmorphism e animações suaves
- **Relógio integrado** — exibe data e hora atuais no topo do painel
- **Indicadores de progresso** — barra e dots mostrando o slide atual
- **Zero dependência de servidor** — roda 100% no navegador, sem backend

---

## Estrutura dos Slides

| Slide | Conteúdo | Descrição |
|-------|----------|-----------|
| **0** | O que está mais perto de começar | Projeto prioridade máxima, dias restantes, radar de inícios e alertas |
| **1** | Próximos Treinamentos | Sessões confirmadas, datas previstas, instrutor por projeto |
| **2** | Agenda Operacional | Projetos em andamento com prazos próximos e fila de início |
| **3** | Envios e Materiais | Livros, kits, certificados e projetos com maior demanda |
| **4** | Resumo Executivo | Status da carteira, maiores propostas, distribuição por gestor/UF/produto |

---

## Instalação

### Pré-requisitos

- Python 3.8+ (para geração do JSON)
- Navegador moderno (Chrome, Edge, Firefox)
- Arquivo Excel com a base de projetos

### Passos

1. **Clone ou baixe** este repositório para uma pasta local
2. **Instale a dependência** do Python:

```bash
pip install openpyxl
```

3. **Gere o JSON** a partir da planilha:

```bash
python gerar_dashboard_json.py "Andamento - Projetos.xlsx" filtrada dashboard_tv_data.json
```

4. **Abra o dashboard** no navegador:

```
dashboard_tv_slides_auto.html
```

5. Pressione **F11** para tela cheia

---

## Como Usar

### Exibição em TV

1. Abra o arquivo `dashboard_tv_slides_auto.html` no navegador da TV ou dispositivo conectado
2. Pressione `F11` (ou equivalente) para ativar o modo tela cheia
3. Os slides começam a rotacionar automaticamente a cada 12 segundos
4. A barra de progresso na parte inferior mostra o tempo restante do slide

### Controles Manuais

- **Clique nos dots** na parte inferior para navegar entre slides
- **Barra de progresso** indica visualmente o slide atual e o tempo restante

### Atualização dos Dados

O painel verifica o arquivo `dashboard_tv_data.json` a cada 60 segundos. Se o arquivo for atualizado, o dashboard carrega os novos dados automaticamente, sem precisar recarregar a página.

---

## Atualização dos Dados

### Via Linha de Comando

```bash
python gerar_dashboard_json.py "Andamento - Projetos.xlsx" filtrada dashboard_tv_data.json
```

### Parâmetros do Script

| Argumento | Descrição | Padrão |
|-----------|-----------|--------|
| `INPUT_XLSX` | Caminho para o arquivo Excel | `Andamento - Projetos.xlsx` |
| `SHEET_NAME` | Nome da aba da planilha | `filtrada` |
| `OUTPUT_JSON` | Caminho do JSON de saída | `dashboard_tv_data.json` |

### Exemplos

```bash
# Usando padrões
python gerar_dashboard_json.py

# Caminho personalizado
python gerar_dashboard_json.py "C:\dados\projetos.xlsx" base dashboard_data.json

# Com caminho relativo
python gerar_dashboard_json.py ../dados/andamento.xlsx filtrada data.json
```

### Atualização Automatizada (Opcional)

Para atualizar automaticamente a cada hora no Windows, use o **Agendador de Tarefas**:

1. Crie um arquivo `.bat`:

```bat
@echo off
cd /d "C:\caminho\do\projeto"
python gerar_dashboard_json.py "Andamento - Projetos.xlsx" filtrada dashboard_tv_data.json
```

2. Agende a execução no **Task Scheduler** do Windows

---

## Configuração

### Intervalo dos Slides

No arquivo `dashboard_tv_slides_auto.html`, localize e ajuste:

```javascript
const SLIDE_INTERVAL = 12000; // 12 segundos (em milissegundos)
```

### Frequência de Atualização dos Dados

```javascript
const DATA_REFRESH_INTERVAL = 60000; // 60 segundos (em milissegundos)
```

### Cores e Tema

As variáveis CSS no topo do arquivo HTML permitem personalizar:

```css
:root {
  --bg1: #07111f;
  --accent: #57a4ff;
  --accent2: #8a7dff;
  --ok: #3ddc97;
  --warn: #f4c75b;
  --danger: #ff6b6b;
  /* ... */
}
```

---

## Estrutura de Arquivos

```
dashboard_tv_slides_pacote/
├── dashboard_tv_slides_auto.html   # Painel principal (HTML + CSS + JS)
├── dashboard_tv_data.json          # Dados dos projetos (gerado pelo script)
├── gerar_dashboard_json.py         # Script Python para gerar o JSON
└── README.md                       # Esta documentação
```

### Descrição dos Arquivos

| Arquivo | Função |
|---------|--------|
| `dashboard_tv_slides_auto.html` | Interface completa do dashboard com HTML, CSS e JavaScript integrados |
| `dashboard_tv_data.json` | Dados estruturados extraídos da planilha Excel |
| `gerar_dashboard_json.py` | Script Python que converte a planilha em JSON |
| `README.md` | Documentação do projeto |

---

## Tecnologias

- **HTML5** — estrutura semântica do painel
- **CSS3** — Grid, Flexbox, variáveis CSS, animações, glassmorphism, gradientes
- **JavaScript (vanilla)** — lógica de slides, atualização de dados, relógio, KPIs
- **Python 3** — geração do JSON via `openpyxl`
- **openpyxl** — leitura de arquivos Excel `.xlsx`

---

## Solução de Problemas

### O dashboard não carrega os dados

1. Verifique se `dashboard_tv_data.json` está na **mesma pasta** que o HTML
2. Abra o console do navegador (`F12`) e verifique erros
3. Valide o JSON em um validador online (ex: jsonlint.com)

### Os dados não atualizam

1. Certifique-se de que o JSON foi gerado corretamente pelo script Python
2. O navegador pode estar com cache — force recarregamento com `Ctrl + Shift + R`
3. Verifique as permissões de leitura do arquivo JSON

### O slide não troca automaticamente

1. Verifique se o JavaScript não está bloqueado no navegador
2. Abra o console (`F12 > Console`) para identificar erros
3. Teste em outro navegador (Chrome ou Edge recomendado)

### Layout desconfigurado

1. Certifique-se de que o navegador está em **tela cheia** (`F11`)
2. Resoluções abaixo de 1280x720 podem apresentar problemas de layout
3. Recomendado: Full HD (1920x1080) ou 4K

### Script Python falha

1. Instale a dependência: `pip install openpyxl`
2. Verifique se o arquivo Excel existe e a aba `filtrada` está presente
3. Execute com verbose: `python gerar_dashboard_json.py 2>&1`

---

## Suporte

Em caso de dúvidas ou problemas, entre em contato com a equipe de desenvolvimento.

---

**Dashboard TV Slides v1** — Desenvolvido para exibição contínua em ambiente corporativo.
