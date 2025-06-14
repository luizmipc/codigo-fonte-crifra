# crypto_core.py
import struct

BLOCK_SIZE = 4  # bytes (32 bits)
N_ROUNDS = 3

# S-box e inversa
SBOX = [0xE, 0x4, 0xD, 0x1,
        0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC,
        0x5, 0x9, 0x0, 0x7]
SBOX_INV = [0]*16
for i, v in enumerate(SBOX): SBOX_INV[v] = i

# P-box e inversa
PBOX = [16, 25, 12, 11,
        3, 20, 4, 15,
        31, 17, 9, 6,
        27, 14, 1, 22,
        30, 24, 8, 18,
        0, 5, 29, 10,
        2, 21, 26, 19,
        13, 28, 23, 7]
PBOX_INV = [0]*32
for src, dst in enumerate(PBOX): PBOX_INV[dst] = src

def generate_subkeys(master_key: int) -> list[int]:
    sub = []
    for i in range(N_ROUNDS):
        sk = ((master_key << (i+1)) & 0xFFFFFFFF) | (master_key >> (32-(i+1)))
        sk ^= 0xA5A5A5A5 ^ i
        sub.append(sk & 0xFFFFFFFF)
    return sub

def substitute(word: int) -> int:
    out = 0
    for i in range(8):
        nib = (word >> (4*i)) & 0xF
        out |= (SBOX[nib] << (4*i))
    return out

def substitute_inv(word: int) -> int:
    out = 0
    for i in range(8):
        nib = (word >> (4*i)) & 0xF
        out |= (SBOX_INV[nib] << (4*i))
    return out

def permute(word: int) -> int:
    out = 0
    for src, dst in enumerate(PBOX):
        out |= (((word >> src)&1) << dst)
    return out

def permute_inv(word: int) -> int:
    out = 0
    for dst, src in enumerate(PBOX_INV):
        out |= (((word >> dst)&1) << src)
    return out

def encrypt_block(block: bytes, subkeys: list[int]) -> bytes:
    if len(block) < BLOCK_SIZE:
        block = block.ljust(BLOCK_SIZE, b'\0')
    w, = struct.unpack('>I', block)
    for sk in subkeys:
        w = substitute(w)
        w = permute(w)
        w ^= sk
    return struct.pack('>I', w)

def decrypt_block(block: bytes, subkeys: list[int]) -> bytes:
    if len(block) < BLOCK_SIZE:
        block = block.ljust(BLOCK_SIZE, b'\0')
    w, = struct.unpack('>I', block)
    for sk in subkeys:
        w ^= sk
        w = permute_inv(w)
        w = substitute_inv(w)
    return struct.pack('>I', w)
