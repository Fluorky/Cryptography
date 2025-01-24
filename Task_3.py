import random

def rotate_left_4_bits(byte):
    """
    Rotate the bits of the byte to the left by 4 positions.
    """
    return ((byte << 4) | (byte >> 4)) & 0xFF

def encrypt_block_ecb(block, key):
    """
    Encrypt a single block using the ECB mode:
    1. XOR the plaintext block with the key.
    2. Rotate the result left by 4 bits.
    """
    step1 = block ^ key
    encrypted = rotate_left_4_bits(step1)
    return encrypted

def ecb_mode_encrypt(plaintext, key):
    """
    Encrypt plaintext using ECB mode.
    """
    ciphertext = []
    for char in plaintext:
        ciphertext.append(encrypt_block_ecb(ord(char), key))
    return ciphertext

def encrypt_block_cbc(block, key, iv):
    """
    Encrypt a single block using the CBC mode:
    1. XOR the plaintext block with the IV.
    2. XOR the result with the key.
    3. Rotate the result left by 4 bits.
    """
    step1 = block ^ iv
    step2 = step1 ^ key
    encrypted = rotate_left_4_bits(step2)
    return encrypted

def cbc_mode_encrypt(plaintext, key, iv):
    """
    Encrypt plaintext using CBC mode.
    """
    ciphertext = []
    prev_block = iv
    for char in plaintext:
        encrypted = encrypt_block_cbc(ord(char), key, prev_block)
        ciphertext.append(encrypted)
        prev_block = encrypted  # The ciphertext of the current block becomes IV for the next
    return ciphertext

def format_as_hex(ciphertext):
    """
    Format ciphertext as a sequence of 2-digit hexadecimal numbers.
    """
    return " ".join(f"{byte:02X}" for byte in ciphertext)

# Given plaintext
plaintext = "attack at down"

# ECB encryption with two different keys
key1, key2 = random.randint(0, 255), random.randint(0, 255)
ciphertext_ecb1 = ecb_mode_encrypt(plaintext, key1)
ciphertext_ecb2 = ecb_mode_encrypt(plaintext, key2)

# CBC encryption with two different keys and IVs
key1, key2 = random.randint(0, 255), random.randint(0, 255)
iv1, iv2 = random.randint(0, 255), random.randint(0, 255)
ciphertext_cbc1 = cbc_mode_encrypt(plaintext, key1, iv1)
ciphertext_cbc2 = cbc_mode_encrypt(plaintext, key2, iv2)

# Print results
print("Plaintext:", plaintext)
print("Key 1:", key1)
print("Key 2:", key2)
print("IV 1:", iv1)
print("IV 2:", iv2)

print("ECB Ciphertext with Key 1:", format_as_hex(ciphertext_ecb1))
print("ECB Ciphertext with Key 2:", format_as_hex(ciphertext_ecb2))
print("CBC Ciphertext with Key 1 and IV 1:", format_as_hex(ciphertext_cbc1))
print("CBC Ciphertext with Key 2 and IV 2:", format_as_hex(ciphertext_cbc2))
