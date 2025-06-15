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
    SBOX_INV[v] = i  # Calcula a inversa de cada entrada da SBOX

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
    Realiza um shift rotacional e uma operação XOR com uma constante para cada rodada.
    """
    sub = []
    for i in range(N_ROUNDS):
        # Rotaciona bits da chave para a esquerda
        sk = ((master_key << (i+1)) & 0xFFFFFFFF) | (master_key >> (32 - (i+1)))
        # Mistura com constante XOR
        sk ^= 0xA5A5A5A5 ^ i
        # Garante 32 bits com máscara
        sub.append(sk & 0xFFFFFFFF)
    return sub

def substitute(word: int) -> int:
    """
    Aplica substituição S-Box em cada nibble (4 bits) do valor de 32 bits.
    """
    out = 0
    for i in range(8):  # 32 bits = 8 nibbles de 4 bits
        nib = (word >> (4 * i)) & 0xF  # Extrai nibble
        out |= (SBOX[nib] << (4 * i))  # Substitui e posiciona no lugar
    return out

def substitute_inv(word: int) -> int:
    """
    Aplica substituição inversa (SBOX_INV) para decriptação.
    """
    out = 0
    for i in range(8):
        nib = (word >> (4 * i)) & 0xF
        out |= (SBOX_INV[nib] << (4 * i))
    return out

def permute(word: int) -> int:
    """
    Aplica a permutação de bits (P-Box).
    Cada bit da entrada é movido para a posição indicada na tabela PBOX.
    """
    out = 0
    for src, dst in enumerate(PBOX):
        out |= (((word >> src) & 1) << dst)
    return out

def permute_inv(word: int) -> int:
    """
    Aplica a permutação inversa de bits (PBOX_INV).
    Restaura a ordem original dos bits.
    """
    out = 0
    for dst, src in enumerate(PBOX_INV):
        out |= (((word >> dst) & 1) << src)
    return out

def encrypt_block(block: bytes, subkeys: list[int]) -> bytes:
    """
    Encripta um bloco de 4 bytes usando as subchaves fornecidas.
    Operações por rodada: substituição → permutação → XOR com subchave.
    """
    # Preenche com zeros se o bloco for menor que 4 bytes
    if len(block) < BLOCK_SIZE:
        block = block.ljust(BLOCK_SIZE, b'\0')

    # Converte de bytes para inteiro (big endian)
    w, = struct.unpack('>I', block)

    # Executa N_ROUNDS rodadas de cifra
    for sk in subkeys:
        w = substitute(w)
        w = permute(w)
        w ^= sk  # Mistura com subchave

    # Retorna o inteiro cifrado como bytes (big endian)
    return struct.pack('>I', w)

def decrypt_block(block: bytes, subkeys: list[int]) -> bytes:
    """
    Decripta um bloco de 4 bytes usando as subchaves fornecidas (em ordem reversa).
    Operações por rodada: XOR com subchave → permutação inversa → substituição inversa.
    """
    if len(block) < BLOCK_SIZE:
        block = block.ljust(BLOCK_SIZE, b'\0')

    w, = struct.unpack('>I', block)

    # Executa as rodadas em ordem inversa
    for sk in subkeys:
        w ^= sk
        w = permute_inv(w)
        w = substitute_inv(w)

    return struct.pack('>I', w)
