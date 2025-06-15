# utils.py
import sys
sys.dont_write_bytecode = True
import os
import secrets

# Diretório base para arquivos de entrada/saída
BASE_DIR = "files"
# Arquivo de chave dentro de BASE_DIR
KEY_FILE = os.path.join(BASE_DIR, "key.txt")

# Garante que exista o diretório BASE_DIR
os.makedirs(BASE_DIR, exist_ok=True)


import os
import secrets

BASE_DIR = 'files'  # ajuste conforme seu contexto
KEY_FILE = os.path.join('files/key.txt')

def ensure_key_file(provided_key: str = None) -> str | None:
    """
    Garante que o arquivo de chave em 'files/key.txt' exista.
    Se `provided_key` for fornecida, valida e grava esta chave no arquivo, substituindo o conteúdo.
    Se não for fornecida, gera uma chave aleatória se o arquivo não existir,
    ou lê e valida o arquivo existente.
    Retorna a chave em formato hexadecimal (8 dígitos maiúsculos) ou None em caso de erro.
    """
    def is_valid_key(k: str) -> bool:
        return len(k) == 8 and all(c in "0123456789ABCDEF" for c in k.upper())
    
    if provided_key is not None:
        key_hex = provided_key.strip().upper()
        if not is_valid_key(key_hex):
            print(f"Chave fornecida inválida: '{provided_key}'. Deve ter 8 dígitos hexadecimais.")
            return None
        # grava a chave fornecida no arquivo (sobrescreve se existir)
        try:
            os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
            with open(KEY_FILE, 'w') as f:
                f.write(key_hex)
            print(f"Chave fornecida gravada em '{KEY_FILE}'.")
            return key_hex
        except Exception as e:
            print(f"Erro ao gravar arquivo de chave: {e}")
            return None

    # Se não passou chave, garante que o arquivo exista
    if not os.path.exists(KEY_FILE):
        key_int = secrets.randbits(32)
        key_hex = f"{key_int:08X}"
        try:
            os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
            with open(KEY_FILE, 'w') as f:
                f.write(key_hex)
            print(f"Arquivo de chave não encontrado. Nova chave gerada em '{KEY_FILE}'.")
        except Exception as e:
            print(f"Erro ao criar arquivo de chave: {e}")
            return None
    else:
        try:
            with open(KEY_FILE, 'r') as f:
                key_hex = f.read().strip().upper()
        except Exception as e:
            print(f"Erro ao ler arquivo de chave: {e}")
            return None

    if not is_valid_key(key_hex):
        print(f"Chave em formato inválido no arquivo '{KEY_FILE}'.")
        return None

    return key_hex


def list_local_archives(return_list=False) -> list[str] | None:
    """
    Lista todos os arquivos no diretório 'files/'.
    Se 'return_list' for True, retorna a lista de nomes; caso contrário, imprime numerada.
    """
    files = os.listdir(BASE_DIR)
    if return_list:
        return files
    print("\n=== LISTA DE ARQUIVOS LOCAIS ===")
    for index, fname in enumerate(files, 1):
        print(f"{index}. {fname}")


def show_file():
    """
    Lista os arquivos no diretório 'files/', permite a escolha por número e exibe o conteúdo como texto UTF-8.
    """
    files = list_local_archives(return_list=True)

    if not files:
        print("Nenhum arquivo encontrado.")
        return

    print("\n=== SELECIONE O ARQUIVO PARA EXIBIR ===")
    for index, fname in enumerate(files, 1):
        print(f"{index}. {fname}")

    try:
        choice = int(input("\nDigite o número do arquivo: ").strip())
        if choice < 1 or choice > len(files):
            print("Número inválido.")
            return
        filename_target = files[choice - 1]
        full_path = os.path.join(BASE_DIR, filename_target)
        with open(full_path, 'rb') as f:
            data = f.read()
        print("\n=== CONTEÚDO DO ARQUIVO ===")
        print(data.decode('utf-8', errors='replace'))
    except ValueError:
        print("Entrada inválida. Digite um número.")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")

