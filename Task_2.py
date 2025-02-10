import random
from sympy import primerange, gcd
from math import isqrt
from typing import Optional, Tuple

def is_probably_prime(n: int, k: int = 10) -> bool:
    """
    Perform the Miller-Rabin primality test to check if a number is prime with high probability.

    :param n: The number to test for primality.
    :param k: The number of rounds of testing.
    :return: True if the number is probably prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n as 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_parameters(p: int) -> int:
    """
    Generate a generator g for the group Z*_p with order p-1.

    :param p: The prime modulus.
    :return: The generator g.
    """
    if not is_probably_prime(p):
        raise ValueError("p must be prime.")
    
    phi = p - 1
    factors = [23, 29, 101, 179]  # Given prime factorization of 4194328
    
    g = 2
    while True:
        if all(pow(g, phi // q, p) != 1 for q in factors):
            break
        g += 1
    return g

def generate_keys(p: int, g: int) -> Tuple[int, int, int, int]:
    """
    Generate private and public keys for two participants A and B.

    :param p: The prime modulus.
    :param g: The generator.
    :return: (a, b, A, B) where:
             - a is the private key for A,
             - b is the private key for B,
             - A is the public key for A,
             - B is the public key for B.
    """
    a = random.randint(1, p - 1)
    b = random.randint(1, p - 1)
    A = pow(g, a, p)
    B = pow(g, b, p)
    return a, b, A, B

def compute_shared_key(a: int, b: int, A: int, B: int, p: int) -> Optional[int]:
    """
    Compute the shared secret key in the Diffie-Hellman key exchange.

    :param a: Private key of A.
    :param b: Private key of B.
    :param A: Public key of A.
    :param B: Public key of B.
    :param p: The prime modulus.
    :return: The shared secret key if both computed keys match, otherwise None.
    """
    key1 = pow(B, a, p)  # A computes key using B's public key
    key2 = pow(A, b, p)  # B computes key using A's public key
    return key1 if key1 == key2 else None

def baby_step_giant_step(g: int, h: int, p: int) -> Optional[int]:
    """
    Solve the discrete logarithm problem using Baby-Step Giant-Step algorithm.

    :param g: The generator.
    :param h: The public key (A or B).
    :param p: The prime modulus.
    :return: The exact private exponent (a or b) used in key generation.
    """
    n = isqrt(p - 1) + 1  # sqrt(p-1) rounded up
    p_minus_1 = p - 1  # The order of the group

    # Compute baby steps
    baby_steps = {pow(g, i, p): i for i in range(n)}

    # Compute g^(-n) mod p correctly
    g_inv = pow(g, -1, p)  # Modular inverse of g mod p
    g_inv_n = pow(g_inv, n, p)  # Compute g^(-n) mod p

    # Giant steps
    for j in range(n):
        y = (h * pow(g_inv_n, j, p)) % p
        if y in baby_steps:
            base_result = j * n + baby_steps[y]

            # Find the correct exponent by checking all multiples of (p-1)
            for k in range(0, 10):  # Adjust range if needed
                candidate = base_result + k * p_minus_1
                if candidate < p_minus_1 and pow(g, candidate, p) == h:
                    return candidate  # Return correct exponent

            return base_result  # If no better match is found, return the closest match

    return None  # If no valid solution found



# Main execution
if __name__ == "__main__":
    # a) Check if p is prime
    print("=== (a) Checking primality of p ===")
    p: int = 4194329
    print(f"Is {p} probably prime? {is_probably_prime(p)}")

    # b) Generate global parameters
    print("\n=== (b) Generating global parameters ===")
    g = generate_parameters(p)
    print(f"Generated generator g: {g}")

    # c) Generate private and public keys
    print("\n=== (c) Generating public-private key pairs ===")
    a, b, A, B = generate_keys(p, g)
    print(f"Private keys: a = {a}, b = {b}")
    print(f"Public keys: A = {A}, B = {B}")

    # d) Compute shared key
    print("\n=== (d) Computing shared secret key ===")
    shared_key = compute_shared_key(a, b, A, B, p)
    print(f"Shared key: {shared_key}")

    # e) Attack the protocol using Baby-Step Giant-Step
    print("\n=== (e) Attacking the protocol (solving discrete logarithm) ===")
    recovered_a = baby_step_giant_step(g, A, p)
    recovered_b = baby_step_giant_step(g, B, p)
    print(f"Recovered private keys: a = {recovered_a}, b = {recovered_b}")
    
    if recovered_a is not None and recovered_b is not None:
        recomputed_shared_key = pow(B, recovered_a, p)
        print(f"Recomputed shared key: {recomputed_shared_key}")
    else:
        print("Failed to recover private keys.")
