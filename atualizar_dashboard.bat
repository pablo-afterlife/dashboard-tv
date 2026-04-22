@echo off
cd /d "C:\Users\Consultor\OneDrive - Aquila\SITE AQUILA\teste123\dashboard_tv_slides_pacote\dashboard_tv_slides_pacote"

python gerar_dashboard_json.py ^
  "C:\Users\Consultor\Aquila\ADM - EGA - General\Arquivos Referencias\Escola\Andamento - Projetos.xlsx" ^
  filtrada ^
  dashboard_tv_data.json

git add dashboard_tv_data.json
git commit -m "Atualizar dados %date% %time%"
git push origin main

echo %date% %time% - JSON atualizado e enviado >> log_atualizacao.txt
