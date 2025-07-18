# decrypt_file.py
import os
import sys
sys.dont_write_bytecode = True
from crypto_core import BLOCK_SIZE, generate_subkeys, decrypt_block as _dec_block
from utils import list_local_archives

BASE_DIR = "files"


def decrypt_file(input_path: str, output_path: str, key_hex: str):
    """
    Decripta todo o arquivo de input_path em blocos de 32 bits,
    e remove zeros finais (caso tenha sido feito padding).
    Grava em output_path.
    """
    try:
        key = int(key_hex, 16) & 0xFFFFFFFF
    except ValueError:
        print("Chave inválida. Use 8 dígitos hex.")
        return

    subkeys = generate_subkeys(key)[::-1]  # inversão para decriptação

    decrypted = bytearray()
    with open(input_path, 'rb') as fin:
        while chunk := fin.read(BLOCK_SIZE):
            if len(chunk) < BLOCK_SIZE:
                print("Arquivo criptografado corrompido ou incompleto.")
                return
            decrypted += _dec_block(chunk, subkeys)

    # Optional: strip trailing zeros if you know that's safe
    decrypted = decrypted.rstrip(b'\x00')

    with open(output_path, 'wb') as fout:
        fout.write(decrypted)

    print(f"Decrypt concluído: {output_path}")



def decrypt_menu(key_hex: str):
    """
    Exibe lista de arquivos em 'files/', permite escolher um para decriptar.
    """
    files = list_local_archives(return_list=True)
    enc_files = [f for f in files if f.endswith(".enc")]

    if not enc_files:
        print("Nenhum arquivo '.enc' disponível para decriptar.")
        return

    print("\n=== Arquivos disponíveis para decriptar ===")
    for idx, fname in enumerate(enc_files, 1):
        print(f"{idx}. {fname}")

    try:
        choice = int(input("Selecione o número do arquivo: "))
        filename = enc_files[choice - 1]
    except Exception:
        print("Seleção inválida.")
        return

    input_path = os.path.join(BASE_DIR, filename)
    output_filename = filename.removesuffix(".enc") + ".dec"
    output_path = os.path.join(BASE_DIR, output_filename)

    decrypt_file(input_path, output_path, key_hex)
    print(f"Arquivo salvo em: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python decrypt.py <key_hex>")
        sys.exit(1)
    _, key = sys.argv
    decrypt_menu(key)
