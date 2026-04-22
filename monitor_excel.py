#!/usr/bin/env python3
"""
Monitor de alterações no Excel → GitHub Pages (Dashboard TV)

Roda em segundo plano (use iniciar_monitor_oculto.vbs para executar sem janela).
A cada 30 segundos verifica se o Excel mudou (hash MD5).
Quando há mudança, delega a conversão ao gerar_dashboard_json.py e faz
commit + push para o GitHub, que republica o site automaticamente.

Uso direto (com janela, para debug):
    python monitor_excel.py
    python monitor_excel.py --intervalo 60

Uso oculto (sem janela, produção):
    iniciar_monitor_oculto.vbs  ← duplo clique
"""

import argparse
import hashlib
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Caminhos ───────────────────────────────────────────────────────────────────

# Planilha monitorada
EXCEL_PATH = Path(
    r"C:\Users\Consultor\Aquila\ADM - EGA - General"
    r"\Arquivos Referencias\Escola\Andamento - Projetos.xlsx"
)

# Repositório git local (onde ficam gerar_dashboard_json.py e dashboard_tv_data.json)
REPO_DIR = Path(
    r"C:\Users\Consultor\OneDrive - Aquila\SITE AQUILA\teste123"
    r"\dashboard_tv_slides_pacote\dashboard_tv_slides_pacote"
)

JSON_FILE = REPO_DIR / "dashboard_tv_data.json"
GERADOR   = REPO_DIR / "gerar_dashboard_json.py"
LOG_FILE  = REPO_DIR / "log_atualizacao.txt"
SHEET     = "filtrada"
INTERVALO = 30  # segundos entre cada verificação


# ── Utilitários ────────────────────────────────────────────────────────────────

def log(msg: str) -> None:
    ts   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # não deixa o log travar o monitor


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _python_exe() -> str:
    """Retorna o executável Python atual (pythonw.exe se disponível)."""
    return sys.executable


def git(*args: str) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_DIR),
    )
    return result.returncode, (result.stdout + result.stderr).strip()


# ── Geração e sincronização ────────────────────────────────────────────────────

def gerar_json() -> bool:
    """Chama gerar_dashboard_json.py. Retorna True se OK."""
    result = subprocess.run(
        [_python_exe(), str(GERADOR), str(EXCEL_PATH), SHEET, str(JSON_FILE)],
        capture_output=True,
        text=True,
        cwd=str(REPO_DIR),
    )
    if result.returncode != 0:
        log(f"ERRO ao gerar JSON:\n{result.stderr.strip()}")
        return False
    for linha in result.stdout.strip().splitlines():
        log(linha)
    return True


def sincronizar() -> None:
    log("Mudança detectada — iniciando sincronização.")

    if not gerar_json():
        return

    # Verifica se o JSON realmente mudou (evita commits desnecessários)
    rc, _ = git("diff", "--quiet", "dashboard_tv_data.json")
    if rc == 0:
        log("JSON idêntico ao anterior — nenhum commit necessário.")
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
    log(f"Commit criado.")

    # Push com retry e backoff exponencial
    for tentativa in range(1, 5):
        rc, out = git("push", "origin", "main")
        if rc == 0:
            log("Push enviado — site será atualizado em ~1 min.")
            return
        log(f"AVISO push (tentativa {tentativa}/4): {out}")
        time.sleep(2 ** tentativa)  # 2s, 4s, 8s, 16s

    log("ERRO: push falhou após 4 tentativas. Verifique internet/credenciais.")


# ── Loop principal ─────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor Excel → GitHub Pages")
    parser.add_argument("--intervalo", type=int, default=INTERVALO,
                        help=f"Intervalo em segundos (padrão: {INTERVALO})")
    args = parser.parse_args()

    log("=" * 60)
    log("Monitor iniciado.")
    log(f"Excel    : {EXCEL_PATH}")
    log(f"Repo     : {REPO_DIR}")
    log(f"Intervalo: {args.intervalo}s")
    log("=" * 60)

    if not EXCEL_PATH.exists():
        log(f"ERRO: Excel não encontrado: {EXCEL_PATH}")
        sys.exit(1)

    if not GERADOR.exists():
        log(f"ERRO: gerar_dashboard_json.py não encontrado em {GERADOR}")
        sys.exit(1)

    hash_anterior = ""

    while True:
        try:
            hash_atual = md5(EXCEL_PATH)
            if hash_atual != hash_anterior:
                if hash_anterior:
                    sincronizar()
                else:
                    log("Hash inicial registrado — aguardando alterações no Excel.")
                hash_anterior = hash_atual
        except PermissionError:
            # Excel salva em arquivo temporário antes de gravar — normal
            log("Arquivo em uso (Excel está salvando?) — aguardando próxima verificação.")
        except Exception as exc:
            log(f"Erro inesperado: {exc}")

        time.sleep(args.intervalo)


if __name__ == "__main__":
    main()
