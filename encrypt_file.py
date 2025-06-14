# encrypt.py
import os
import sys
from crypto_core import BLOCK_SIZE, generate_subkeys, encrypt_block as _enc_block
from utils import list_local_archives

BASE_DIR = "files"


def encrypt_file(input_path: str, output_path: str, key_hex: str):
    """
    Encripta todo o arquivo de input_path em blocos de 32 bits,
    grava em output_path.
    """
    try:
        key = int(key_hex, 16) & 0xFFFFFFFF
    except ValueError:
        print("Chave inválida. Use 8 dígitos hex.")
        return

    subkeys = generate_subkeys(key)
    with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
        while chunk := fin.read(BLOCK_SIZE):
            fout.write(_enc_block(chunk, subkeys))
    print(f"Encrypt concluído: {output_path}")


def encrypt_menu(key_hex: str):
    """
    Exibe lista de arquivos em 'files/', permite escolher um para encriptar.
    """
    files = list_local_archives(return_list=True)
    if not files:
        print("Nenhum arquivo disponível para encriptar.")
        return

    print("\n=== Arquivos disponíveis para encriptar ===")
    for idx, fname in enumerate(files, 1):
        print(f"{idx}. {fname}")
    try:
        choice = int(input("Selecione o número do arquivo: "))
        filename = files[choice - 1]
    except Exception:
        print("Seleção inválida.")
        return

    input_path = os.path.join(BASE_DIR, filename)
    output_filename = filename + ".enc"
    output_path = os.path.join(BASE_DIR, output_filename)

    encrypt_file(input_path, output_path, key_hex)
    print(f"Arquivo salvo em: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python encrypt.py <key_hex>")
        sys.exit(1)
    _, key = sys.argv
    encrypt_menu(key)
