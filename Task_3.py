import random

def rotate_left_4_bits(byte):
    """
    Rotate the bits of an 8-bit byte to the left by 4 positions.

    Args:
        byte (int): An 8-bit integer to be rotated.

    Returns:
        int: The result of the rotation as an 8-bit integer.
    """
    return ((byte << 4) | (byte >> 4)) & 0xFF

def encrypt_block_ecb(block, key):
    """
    Encrypt a single block using ECB mode by XOR-ing with the key
    and rotating the result left by 4 bits.

    Args:
        block (int): A single 8-bit plaintext block (ASCII character).
        key (int): An 8-bit encryption key.

    Returns:
        int: The encrypted 8-bit block.
    """
    step1 = block ^ key
    return rotate_left_4_bits(step1)

def ecb_mode_encrypt(plaintext, key):
    """
    Encrypt plaintext using ECB mode. Each block (character) is encrypted independently.

    Args:
        plaintext (str): The plaintext string to be encrypted.
        key (int): An 8-bit encryption key.

    Returns:
        list[int]: A list of encrypted blocks as 8-bit integers.
    """
    return [encrypt_block_ecb(ord(char), key) for char in plaintext]

def encrypt_block_cbc(block, key, iv):
    """
    Encrypt a single block using CBC mode by XOR-ing with the IV, 
    then the key, followed by rotating left by 4 bits.

    Args:
        block (int): A single 8-bit plaintext block (ASCII character).
        key (int): An 8-bit encryption key.
        iv (int): An 8-bit initialization vector.

    Returns:
        int: The encrypted 8-bit block.
    """
    step1 = block ^ iv
    step2 = step1 ^ key
    return rotate_left_4_bits(step2)

def cbc_mode_encrypt(plaintext, key, iv):
    """
    Encrypt plaintext using CBC mode. Each block is XOR-ed with the previous
    ciphertext block before encryption.

    Args:
        plaintext (str): The plaintext string to be encrypted.
        key (int): An 8-bit encryption key.
        iv (int): An 8-bit initialization vector.

    Returns:
        list[int]: A list of encrypted blocks as 8-bit integers.
    """
    ciphertext = []
    prev_block = iv
    for char in plaintext:
        encrypted = encrypt_block_cbc(ord(char), key, prev_block)
        ciphertext.append(encrypted)
        prev_block = encrypted
    return ciphertext

def format_as_hex(ciphertext):
    """
    Convert a list of encrypted blocks to a space-separated hexadecimal string.

    Args:
        ciphertext (list[int]): A list of encrypted blocks as integers.

    Returns:
        str: A formatted hexadecimal string.
    """
    return " ".join(f"{byte:02X}" for byte in ciphertext)

def analyze_ecb_same_plaintext(plaintext, key1, key2):
    """
    Check if two ECB-encrypted ciphertexts for the same plaintext are identical
    when encrypted with different keys.

    Args:
        plaintext (str): The plaintext string to be encrypted.
        key1 (int): The first 8-bit encryption key.
        key2 (int): The second 8-bit encryption key.

    Returns:
        bool: True if the ciphertexts are identical, False otherwise.
    """
    ciphertext1 = ecb_mode_encrypt(plaintext, key1)
    ciphertext2 = ecb_mode_encrypt(plaintext, key2)
    return ciphertext1 == ciphertext2

def analyze_cbc_same_plaintext(plaintext, key1, iv1, key2, iv2):
    """
    Check if two CBC-encrypted ciphertexts for the same plaintext are identical
    when encrypted with different keys and IVs.

    Args:
        plaintext (str): The plaintext string to be encrypted.
        key1 (int): The first 8-bit encryption key.
        iv1 (int): The first 8-bit initialization vector.
        key2 (int): The second 8-bit encryption key.
        iv2 (int): The second 8-bit initialization vector.

    Returns:
        bool: True if the ciphertexts are identical, False otherwise.
    """
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
