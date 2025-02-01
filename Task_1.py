import random
from math import gcd
from typing import Tuple, Optional

def is_probable_prime(n: int, k: int = 5) -> bool:
    """
    Perform the Miller-Rabin primality test to check if a number is prime with high probability.

    :param n: The number to test for primality.
    :param k: The number of rounds of testing to improve accuracy.
    :return: True if the number is probably prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as d * 2^r + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform Miller-Rabin test
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Compute the greatest common divisor (GCD) of two numbers and their coefficients 
    in the extended Euclidean algorithm.

    :param a: First integer.
    :param b: Second integer.
    :return: A tuple (gcd, x, y) where gcd is the greatest common divisor of a and b,
             and x, y satisfy the equation ax + by = gcd.
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def pollards_rho(n: int) -> Optional[int]:
    """
    Perform Pollard's Rho algorithm to find a non-trivial factor of a composite number.

    :param n: The integer to be factored.
    :return: A factor of n if found, otherwise None.
    """
    def f(x: int) -> int:
        return (x**2 + 1) % n

    x, y, d = 2, 2, 1
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    return None if d == n else d

# a) Check if p and q are prime
p: int = 2903
q: int = 4091

print(f"Is p={p} probably prime? {is_probable_prime(p)}")
print(f"Is q={q} probably prime? {is_probable_prime(q)}")

# b) Compute n, Euler's totient function phi(n), and private exponent d
n: int = p * q
phi: int = (p - 1) * (q - 1)
e: int = 4097

if gcd(e, phi) != 1:
    raise ValueError("e and phi(n) are not coprime.")

# Compute modular inverse d (private exponent)
_, d, _ = extended_gcd(e, phi)
d = d % phi if d > 0 else d + phi  # Ensure d is positive

print(f"Computed private exponent d={d}")

# c) Encrypt the message "Att"
message: str = "Att"
m: int = ord('A') * 256**2 + ord('t') * 256 + ord('t')  # Convert to integer
c: int = pow(m, e, n)  # Encrypt

print(f"Message '{message}' encrypted as: c={c}")

# d) Decrypt the message
decrypted_m: int = pow(c, d, n)  # Decrypt
z1: int = decrypted_m // 256**2
z2: int = (decrypted_m % 256**2) // 256
z3: int = decrypted_m % 256
decrypted_message: str = chr(z1) + chr(z2) + chr(z3)  # Convert back to string

print(f"Decrypted message: {decrypted_message}")

# e) Factorize n using Pollard's Rho algorithm
n_to_factor: int = 11876173
factor: Optional[int] = pollards_rho(n_to_factor)

if factor:
    print(f"Found factor: {factor}, other factor: {n_to_factor // factor}")
else:
    print("Failed to find a factor using Pollard's Rho.")
