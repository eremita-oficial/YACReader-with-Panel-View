# -*- coding: utf-8 -*-
import sys
import sqlite3
import subprocess
import os
from datetime import datetime
from tkinter import messagebox # Ainda usado para mensagens de erro, mas não para a seleção principal

# --- Constantes de Caminho e Nomes de Arquivo ---
LOG_PATH = r"C:\temp\YACRedirect_log.txt" # Caminho para o arquivo de log

# Nome do executável do seletor AutoIt
YACREADER_SELECTOR_NAME = 'YACReader_Selector.exe' 

# Variáveis que serão preenchidas pelos argumentos da linha de comando
COMICS_ROOT_FOLDER = None
DB_PATH = None
FULL_COMIC_PATH = None # O caminho completo do quadrinho a ser aberto

# --- Funções Auxiliares ---

def log_message(message):
    """Escreve mensagens no arquivo de log."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] {message}\n")

def get_comic_full_path_from_db(comic_id, library_id, comics_root_folder, db_path):
    """
    Busca o caminho completo do quadrinho no banco de dados do YACReader.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT path FROM folder WHERE id=?", (library_id,))
        folder_path_row = cursor.fetchone()
        if not folder_path_row:
            log_message(f"[ERRO_DB] Caminho da pasta (libraryId={library_id}) não encontrado no DB.")
            return None
        base_path = folder_path_row[0]
        
        cursor.execute("SELECT path FROM comic WHERE id=?", (comic_id,))
        comic_path_row = cursor.fetchone()
        if not comic_path_row:
            log_message(f"[ERRO_DB] Caminho do quadrinho (comicId={comic_id}) não encontrado no DB.")
            return None
        comic_rel_path = comic_path_row[0]
        
        conn.close()

        # Normaliza barras para o sistema operacional
        base_path = base_path.lstrip('/').replace('/', os.sep) 
        comic_rel_path = comic_rel_path.lstrip('/').replace('/', os.sep)

        full_path = os.path.join(comics_root_folder, base_path, comic_rel_path)
        full_path = os.path.normpath(full_path)

        return full_path
    except Exception as e:
        log_message(f"[SQL_ERRO] Erro ao acessar DB ou construir caminho: {e}")
        return None

# --- Função Principal ---
def main():
    global COMICS_ROOT_FOLDER, DB_PATH, FULL_COMIC_PATH

    # Configura o log no início
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    log_message(f"\n--- INICIO EXECUTAVEL PYTHON (CHAMADOR AUTOIT) --- {datetime.now()} ---")
    log_message(f"Argumentos recebidos: {sys.argv}")

    # 1. Parsear Argumentos da Linha de Comando
    comic_id = None
    library_id = None

    if len(sys.argv) > 1:
        if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
            COMICS_ROOT_FOLDER = os.path.normpath(sys.argv[1])
            DB_PATH = os.path.join(COMICS_ROOT_FOLDER, '.yacreaderlibrary', 'library.ydb')
            log_message(f"Pasta Raiz detectada: {COMICS_ROOT_FOLDER}")
            log_message(f"Caminho do DB construído: {DB_PATH}")
        else:
            log_message("[ERRO] Não foi possível detectar a Pasta Raiz das HQs como primeiro argumento após o executável.")
            messagebox.showerror(
                "Erro YACReader Redirecionador",
                "Não foi possível obter a pasta raiz da sua biblioteca de HQs.\n"
                "Verifique a configuração do YACReader Library ou o log."
            )
            sys.exit(1)

        for arg in sys.argv[1:]:
            if arg.startswith("--comicId="):
                comic_id = arg.split("=", 1)[1]
            elif arg.startswith("--libraryId="):
                library_id = arg.split("=", 1)[1]
    
    # 2. Validar Argumentos e Encontrar Caminho Completo
    if not (comic_id and library_id):
        log_message("[ERRO] Argumentos esperados '--comicId=' e '--libraryId=' não encontrados ou incompletos.")
        messagebox.showerror(
            "Erro YACReader Redirecionador",
            "Argumentos essenciais (comicId, libraryId) não foram encontrados.\n"
            "Verifique a configuração do YACReader Library ou o log."
        )
        sys.exit(1)

    if not COMICS_ROOT_FOLDER:
        log_message("[ERRO] COMICS_ROOT_FOLDER não definido. Não é possível continuar.")
        messagebox.showerror(
            "Erro YACReader Redirecionador",
            "A pasta raiz das suas HQs não foi detectada.\n"
            "Verifique a configuração do YACReader Library."
        )
        sys.exit(1)

    if not os.path.exists(DB_PATH):
        log_message(f"[ERRO] Arquivo de banco de dados não encontrado em: {DB_PATH}")
        messagebox.showerror(
            "Erro YACReader Redirecionador",
            f"O arquivo de banco de dados do YACReader não foi encontrado em:\n{DB_PATH}\n"
            "Por favor, verifique se a pasta raiz da sua biblioteca está correta no YACReader Library."
        )
        sys.exit(1)

    FULL_COMIC_PATH = get_comic_full_path_from_db(comic_id, library_id, COMICS_ROOT_FOLDER, DB_PATH)

    if not FULL_COMIC_PATH or not os.path.exists(FULL_COMIC_PATH):
        log_message(f"[ERRO] Caminho do quadrinho não encontrado ou não existe: {FULL_COMIC_PATH}")
        messagebox.showerror(
            "Erro YACReader Redirecionador",
            f"O arquivo do quadrinho não foi encontrado no caminho:\n{FULL_COMIC_PATH}\n"
            "Verifique se o arquivo existe e se as configurações do YACReader estão corretas."
        )
        sys.exit(1)

    log_message(f"Caminho completo do quadrinho: {FULL_COMIC_PATH}")

    # 3. Chamar o Seletor AutoIt com o caminho completo da HQ
    selector_path = os.path.join(os.path.dirname(sys.executable), YACREADER_SELECTOR_NAME)
    
    if not os.path.exists(selector_path):
        log_message(f"[ERRO] Seletor AutoIt '{YACREADER_SELECTOR_NAME}' não encontrado em: {selector_path}")
        messagebox.showerror(
            "Erro YACReader Redirecionador",
            f"O executável do seletor '{YACREADER_SELECTOR_NAME}' não foi encontrado em:\n{selector_path}\n"
            "Certifique-se de que o seletor AutoIt foi compilado e colocado na pasta correta."
        )
        sys.exit(1)

    try:
        # Passa o caminho completo do quadrinho como argumento para o seletor AutoIt
        # Assegura que o caminho esteja entre aspas para lidar com espaços
        subprocess.Popen([selector_path, FULL_COMIC_PATH])
        log_message(f"[INFO] Seletor AutoIt '{YACREADER_SELECTOR_NAME}' iniciado com sucesso.")
    except Exception as e:
        log_message(f"[FALHA] Erro ao iniciar o seletor AutoIt: {e}")
        messagebox.showerror(
            "Erro YACReader Redirecionador",
            f"Falha ao iniciar o seletor AutoIt:\n{e}\nVerifique se '{YACREADER_SELECTOR_NAME}' pode ser executado."
        )
        sys.exit(1)

    log_message("--- FIM EXECUTAVEL PYTHON (CHAMADOR AUTOIT) ---")

if __name__ == "__main__":
    main()