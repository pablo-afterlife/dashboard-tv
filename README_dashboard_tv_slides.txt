PACOTE TV - MODO SLIDES AUTOMÁTICO

Arquivo principal:
- dashboard_tv_slides_auto.html

Como funciona:
- O painel roda em tela cheia como uma sequência de slides.
- Troca automaticamente a cada 12 segundos.
- Atualiza os dados a cada 60 segundos se o arquivo dashboard_tv_data.json estiver na mesma pasta.

Foco desta versão:
- Mais destaque para projetos em PREVISÃO.
- Mais visibilidade para projetos próximos de começar.
- Alertas visuais para previsões com data vencida.
- Leitura rápida para TV.

Arquivos recomendados na mesma pasta:
- dashboard_tv_slides_auto.html
- dashboard_tv_data.json
- gerar_dashboard_json.py

Para atualizar a base:
python gerar_dashboard_json.py "Andamento - Projetos.xlsx" filtrada dashboard_tv_data.json
