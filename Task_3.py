import random

def rotate_left_4_bits(byte):
    return ((byte << 4) | (byte >> 4)) & 0xFF

def encrypt_block_ecb(block, key):
    step1 = block ^ key
    return rotate_left_4_bits(step1)

def ecb_mode_encrypt(plaintext, key):
    ciphertext = [encrypt_block_ecb(ord(char), key) for char in plaintext]
    return ciphertext

def encrypt_block_cbc(block, key, iv):
    step1 = block ^ iv
    step2 = step1 ^ key
    return rotate_left_4_bits(step2)

def cbc_mode_encrypt(plaintext, key, iv):
    ciphertext = []
    prev_block = iv
    for char in plaintext:
        encrypted = encrypt_block_cbc(ord(char), key, prev_block)
        ciphertext.append(encrypted)
        prev_block = encrypted
    return ciphertext

def format_as_hex(ciphertext):
    return " ".join(f"{byte:02X}" for byte in ciphertext)

def analyze_ecb_same_plaintext(plaintext, key1, key2):
    ciphertext1 = ecb_mode_encrypt(plaintext, key1)
    ciphertext2 = ecb_mode_encrypt(plaintext, key2)
    return ciphertext1 == ciphertext2

def analyze_cbc_same_plaintext(plaintext, key1, iv1, key2, iv2):
    ciphertext1 = cbc_mode_encrypt(plaintext, key1, iv1)
    ciphertext2 = cbc_mode_encrypt(plaintext, key2, iv2)
    return ciphertext1 == ciphertext2

# Given plaintext
plaintext = "attack at down"

# Keys and IVs
key1, key2 = random.randint(0, 255), random.randint(0, 255)
iv1, iv2 = random.randint(0, 255), random.randint(0, 255)

# Encrypt in ECB and CBC modes
ciphertext_ecb1 = ecb_mode_encrypt(plaintext, key1)
ciphertext_ecb2 = ecb_mode_encrypt(plaintext, key2)
ciphertext_cbc1 = cbc_mode_encrypt(plaintext, key1, iv1)
ciphertext_cbc2 = cbc_mode_encrypt(plaintext, key2, iv2)

# Analyze results
ecb_identical = analyze_ecb_same_plaintext(plaintext, key1, key2)
cbc_identical = analyze_cbc_same_plaintext(plaintext, key1, iv1, key2, iv2)

# Print results
print("Plaintext:", plaintext)
print("Key1:", key1, "Key2:", key2)
print("IV1:", iv1, "IV2:", iv2)
print("ECB Ciphertext with Key 1:", format_as_hex(ciphertext_ecb1))
print("ECB Ciphertext with Key 2:", format_as_hex(ciphertext_ecb2))
print("CBC Ciphertext with Key 1 and IV 1:", format_as_hex(ciphertext_cbc1))
print("CBC Ciphertext with Key 2 and IV 2:", format_as_hex(ciphertext_cbc2))
print(f"Are ECB ciphertexts identical? {'Yes' if ecb_identical else 'No'}")
print(f"Are CBC ciphertexts identical? {'Yes' if cbc_identical else 'No'}")
