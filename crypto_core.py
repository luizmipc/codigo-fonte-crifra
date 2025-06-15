import sys
sys.dont_write_bytecode = True
import struct

# Tamanho do bloco em bytes (4 bytes = 32 bits)
BLOCK_SIZE = 4  
# Número de rodadas de substituição/permutação/chave
N_ROUNDS = 3

# Tabela de substituição (S-Box) com 16 entradas (4 bits)
SBOX = [0xE, 0x4, 0xD, 0x1,
        0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC,
        0x5, 0x9, 0x0, 0x7]

# Inverso da S-Box (para decriptação)
SBOX_INV = [0]*16
for i, v in enumerate(SBOX):
    SBOX_INV[v] = i

# Tabela de permutação de bits (P-Box) para 32 bits
PBOX = [16, 25, 12, 11,
        3, 20, 4, 15,
        31, 17, 9, 6,
        27, 14, 1, 22,
        30, 24, 8, 18,
        0, 5, 29, 10,
        2, 21, 26, 19,
        13, 28, 23, 7]

# Inverso da P-Box (para desfazer a permutação na decriptação)
PBOX_INV = [0]*32
for src, dst in enumerate(PBOX):
    PBOX_INV[dst] = src


def generate_subkeys(master_key: int) -> list[int]:
    """
    Gera uma lista de subchaves a partir da chave mestra.
    """
    sub = []
    for i in range(N_ROUNDS):
        sk = ((master_key << (i+1)) & 0xFFFFFFFF) | (master_key >> (32 - (i+1)))
        sk ^= 0xA5A5A5A5 ^ i
        sub.append(sk & 0xFFFFFFFF)
    return sub


def substitute(word: int) -> int:
    out = 0
    for i in range(8):
        nib = (word >> (4 * i)) & 0xF
        out |= (SBOX[nib] << (4 * i))
    return out


def substitute_inv(word: int) -> int:
    out = 0
    for i in range(8):
        nib = (word >> (4 * i)) & 0xF
        out |= (SBOX_INV[nib] << (4 * i))
    return out


def permute(word: int) -> int:
    out = 0
    for src, dst in enumerate(PBOX):
        out |= (((word >> src) & 1) << dst)
    return out


def permute_inv(word: int) -> int:
    out = 0
    for dst, src in enumerate(PBOX_INV):
        out |= (((word >> dst) & 1) << src)
    return out


def encrypt_block(block: bytes, subkeys: list[int], verbose: bool = True) -> bytes:
    """
    Encripta um bloco de 4 bytes usando as subchaves fornecidas.
    Com verbose=True (padrão), mostra o estado parcial após cada sub-etapa para demonstração.
    """
    if len(block) < BLOCK_SIZE:
        block = block.ljust(BLOCK_SIZE, b'\0')

    w, = struct.unpack('>I', block)
    print(f"\n[ENCRYPT] Entrada : {w:032b}")

    for i, sk in enumerate(subkeys):
        before = w
        w = substitute(w)
        print(f"Round {i+1} Sub   : {before:032b} -> {w:032b}")
        before = w
        w = permute(w)
        print(f"Round {i+1} Perm  : {before:032b} -> {w:032b}")
        before = w
        w ^= sk
        print(f"Round {i+1} XOR   : {before:032b} -> {w:032b}  (subkey={sk:08X})")

    print(f"[ENCRYPT] Saida  : {w:032b}\n")
    return struct.pack('>I', w)


def decrypt_block(block: bytes, subkeys: list[int], verbose: bool = True) -> bytes:
    """
    Decripta um bloco de 4 bytes usando as subchaves (em ordem reversa).
    Com verbose=True (padrão), mostra o estado parcial após cada sub-etapa para demonstração.
    """
    if len(block) < BLOCK_SIZE:
        block = block.ljust(BLOCK_SIZE, b'\0')

    w, = struct.unpack('>I', block)
    print(f"\n[DECRYPT] Entrada : {w:032b}")

    for i, sk in enumerate(subkeys):
        before = w
        w ^= sk
        print(f"Round {i+1} XOR   : {before:032b} -> {w:032b}  (subkey={sk:08X})")
        before = w
        w = permute_inv(w)
        print(f"Round {i+1} Perm^-1: {before:032b} -> {w:032b}")
        before = w
        w = substitute_inv(w)
        print(f"Round {i+1} Sub^-1: {before:032b} -> {w:032b}")

    print(f"[DECRYPT] Saida  : {w:032b}\n")
    return struct.pack('>I', w)
