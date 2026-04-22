#!/usr/bin/env python3
"""
Monitor de alterações no Excel e sincronização automática com GitHub Pages.

A cada 60 segundos verifica se o arquivo Excel foi modificado (via hash MD5).
Quando há mudança, delega a conversão para gerar_dashboard_json.py (openpyxl)
e faz commit + push para o GitHub.

Uso:
    python monitor_excel.py
    python monitor_excel.py --intervalo 120   # checar a cada 2 minutos
"""

import argparse
import hashlib
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Configurações ──────────────────────────────────────────────────────────────
EXCEL_PATH = Path(
    r"C:\Users\Consultor\Aquila\ADM - EGA - General"
    r"\Arquivos Referencias\Escola\Andamento - Projetos.xlsx"
)
REPO_DIR = Path(__file__).resolve().parent
JSON_FILE = REPO_DIR / "dashboard_tv_data.json"
GERADOR   = REPO_DIR / "gerar_dashboard_json.py"
SHEET     = "filtrada"
INTERVALO = 60  # segundos


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    log_path = REPO_DIR / "log_atualizacao.txt"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def gerar_json() -> bool:
    """Chama gerar_dashboard_json.py via subprocess. Retorna True se OK."""
    result = subprocess.run(
        [sys.executable, str(GERADOR), str(EXCEL_PATH), SHEET, str(JSON_FILE)],
        capture_output=True,
        text=True,
        cwd=str(REPO_DIR),
    )
    if result.returncode != 0:
        log(f"ERRO ao gerar JSON:\n{result.stderr.strip()}")
        return False
    log(result.stdout.strip())
    return True


def git(*args: str) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_DIR),
    )
    return result.returncode, (result.stdout + result.stderr).strip()


def sincronizar() -> None:
    log("Mudança detectada — iniciando sincronização.")

    if not gerar_json():
        return

    # Verifica se o JSON realmente mudou antes de commitar
    rc, diff = git("diff", "--quiet", "dashboard_tv_data.json")
    if rc == 0:
        log("JSON gerado é idêntico ao anterior — nenhum commit necessário.")
        return

    ts = datetime.now().strftime("%d/%m/%Y %H:%M")
    rc, out = git("add", "dashboard_tv_data.json")
    if rc != 0:
        log(f"ERRO git add: {out}")
        return

    rc, out = git("commit", "-m", f"dados: atualizar JSON {ts}")
    if rc != 0:
        log(f"ERRO git commit: {out}")
        return
    log(f"Commit criado: dados: atualizar JSON {ts}")

    for tentativa in range(1, 5):
        rc, out = git("push", "origin", "main")
        if rc == 0:
            log("Push enviado ao GitHub com sucesso.")
            return
        log(f"AVISO push (tentativa {tentativa}/4): {out}")
        time.sleep(2 ** tentativa)  # backoff: 2s, 4s, 8s, 16s

    log("ERRO: push falhou após 4 tentativas.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor Excel → GitHub Pages")
    parser.add_argument("--intervalo", type=int, default=INTERVALO,
                        help="Intervalo de verificação em segundos (padrão: 60)")
    args = parser.parse_args()

    log("=" * 60)
    log("Monitor iniciado.")
    log(f"Excel:     {EXCEL_PATH}")
    log(f"Repo:      {REPO_DIR}")
    log(f"JSON:      {JSON_FILE}")
    log(f"Intervalo: {args.intervalo}s")
    log("=" * 60)

    if not EXCEL_PATH.exists():
        log(f"ERRO: arquivo Excel não encontrado: {EXCEL_PATH}")
        sys.exit(1)

    if not GERADOR.exists():
        log(f"ERRO: gerar_dashboard_json.py não encontrado em {GERADOR}")
        sys.exit(1)

    hash_anterior = ""

    while True:
        try:
            hash_atual = md5(EXCEL_PATH)
            if hash_atual != hash_anterior:
                if hash_anterior:  # ignora a primeira leitura (inicialização)
                    sincronizar()
                else:
                    log("Hash inicial registrado — monitorando alterações.")
                hash_anterior = hash_atual
        except PermissionError:
            # Excel pode estar travado enquanto salva; tenta na próxima rodada
            log("Arquivo em uso (Excel salvando?) — tentará novamente.")
        except Exception as exc:
            log(f"Erro inesperado: {exc}")

        time.sleep(args.intervalo)


if __name__ == "__main__":
    main()
