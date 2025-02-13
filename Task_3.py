import random

### (a) Block Cipher: XOR + Left Rotation ###
def rotate_left_4_bits(byte: int) -> int:
    """
    Rotate the bits of an 8-bit byte to the left by 4 positions.
    """
    return ((byte << 4) | (byte >> 4)) & 0xFF

def encrypt_block(block: int, key: int) -> int:
    """
    Encrypt a single 8-bit block using XOR and left rotation.

    Step 1: XOR the plaintext byte with the key.
    Step 2: Rotate the result left by 4 bits.

    Returns:
        The encrypted 8-bit block.
    """
    step1 = block ^ key
    return rotate_left_4_bits(step1)

### (b) ECB Mode Encryption ###
def ecb_mode_encrypt(plaintext: str, key: int) -> list[int]:
    """
    Encrypt plaintext using ECB mode. Each character is encrypted independently.

    Args:
        plaintext (str): The plaintext string to be encrypted.
        key (int): An 8-bit encryption key.

    Returns:
        list[int]: A list of encrypted blocks as 8-bit integers.
    """
    return [encrypt_block(ord(char), key) for char in plaintext]

### (c) CBC Mode Encryption ###
def encrypt_block_cbc(block: int, key: int, iv: int) -> int:
    """
    Encrypt a single block using CBC mode by XOR-ing with IV,
    then XOR-ing with the key, followed by a left bit rotation.

    Returns:
        The encrypted 8-bit block.
    """
    step1 = block ^ iv
    step2 = step1 ^ key
    return rotate_left_4_bits(step2)

def cbc_mode_encrypt(plaintext: str, key: int, iv: int) -> list[int]:
    """
    Encrypt plaintext using CBC mode. Each block is XOR-ed with the previous
    ciphertext block before encryption.

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

### (d) Probability Analysis ###
def analyze_ecb_same_plaintext(plaintext: str, key1: int, key2: int) -> bool:
    """
    Check if two ECB-encrypted ciphertexts for the same plaintext are identical
    when encrypted with different keys.

    Returns:
        bool: True if the ciphertexts are identical, False otherwise.
    """
    ciphertext1 = ecb_mode_encrypt(plaintext, key1)
    ciphertext2 = ecb_mode_encrypt(plaintext, key2)
    return ciphertext1 == ciphertext2  # Should be False (low probability)

def analyze_cbc_same_plaintext(plaintext: str, key1: int, iv1: int, key2: int, iv2: int) -> bool:
    """
    Check if two CBC-encrypted ciphertexts for the same plaintext are identical
    when encrypted with different keys and IVs.

    Returns:
        bool: True if the ciphertexts are identical, False otherwise.
    """
    ciphertext1 = cbc_mode_encrypt(plaintext, key1, iv1)
    ciphertext2 = cbc_mode_encrypt(plaintext, key2, iv2)
    return ciphertext1 == ciphertext2  # Should always be False

### Helper Function to Format Output ###
def format_as_hex(ciphertext: list[int]) -> str:
    """
    Convert a list of encrypted blocks to a space-separated hexadecimal string.
    """
    return " ".join(f"{byte:02X}" for byte in ciphertext)

### (Main Execution) ###
if __name__ == "__main__":
    # Given plaintext
    plaintext = "attack at down"

    # Generate random keys and IVs
    key1, key2 = random.randint(0, 255), random.randint(0, 255)
    iv1, iv2 = random.randint(0, 255), random.randint(0, 255)

    print("\n=== (a) Block Cipher Encryption ===")
    example_char = 'A'
    example_encrypted = encrypt_block(ord(example_char), key1)
    print(f"Example: Encrypting '{example_char}' (ASCII {ord(example_char)}) with Key {key1:02X}")
    print(f"Encrypted result: {example_encrypted:02X}")

    print("\n=== (b) ECB Mode Encryption ===")
    ciphertext_ecb1 = ecb_mode_encrypt(plaintext, key1)
    ciphertext_ecb2 = ecb_mode_encrypt(plaintext, key2)
    print(f"ECB Ciphertext with Key 1: {format_as_hex(ciphertext_ecb1)}")
    print(f"ECB Ciphertext with Key 2: {format_as_hex(ciphertext_ecb2)}")

    print("\n=== (c) CBC Mode Encryption ===")
    ciphertext_cbc1 = cbc_mode_encrypt(plaintext, key1, iv1)
    ciphertext_cbc2 = cbc_mode_encrypt(plaintext, key2, iv2)
    print(f"CBC Ciphertext with Key 1 and IV 1: {format_as_hex(ciphertext_cbc1)}")
    print(f"CBC Ciphertext with Key 2 and IV 2: {format_as_hex(ciphertext_cbc2)}")

    print("\n=== (d) Probability Analysis ===")
    ecb_identical = analyze_ecb_same_plaintext(plaintext, key1, key2)
    cbc_identical = analyze_cbc_same_plaintext(plaintext, key1, iv1, key2, iv2)
    print(f"Are ECB ciphertexts identical? {'Yes' if ecb_identical else 'No'} (Expected: No)")
    print(f"Are CBC ciphertexts identical? {'Yes' if cbc_identical else 'No'} (Expected: No)")
