import random
from sympy import isprime, primerange, gcd
from math import isqrt, ceil


# Subtask a) Check primality with 95% confidence
def is_probably_prime(n, k=10):
    """Perform the Miller-Rabin primality test."""
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

# Subtask b) Generate global parameters
def generate_parameters(p):
    if not is_probably_prime(p):
        raise ValueError("p must be prime.")
    phi = p - 1
    factors = list(primerange(1, isqrt(phi) + 1))
    g = 2
    while True:
        if all(pow(g, phi // q, p) != 1 for q in factors):
            break
        g += 1
    return g

# Subtask c) Compute public messages
def generate_keys(p, g):
    a = random.randint(1, p - 1)
    b = random.randint(1, p - 1)
    A = pow(g, a, p)
    B = pow(g, b, p)
    return a, b, A, B

# Subtask d) Compute shared key
def compute_shared_key(a, b, A, B, p):
    key1 = pow(B, a, p)
    key2 = pow(A, b, p)
    return key1 if key1 == key2 else None

# Subtask e) Attack using Baby-Step Giant-Step
def baby_step_giant_step(g, h, p):
    n = isqrt(p - 1) + 1
    baby_steps = {pow(g, i, p): i for i in range(n)}
    g_inv_n = pow(g, -n, p)
    
    for j in range(n):
        y = (h * pow(g_inv_n, j, p)) % p
        if y in baby_steps:
            return j * n + baby_steps[y]
    return None


# Main program
if __name__ == "__main__":
    # a)
    p = 4194329
    print(f"Is {p} probably prime? {is_probably_prime(p)}")
    
    # b)
    # Generate parameters
    g = generate_parameters(p)
    print(f"Generated generator g: {g}")
    
    # Key exchange
    a, b, A, B = generate_keys(p, g)
    print(f"Private keys: a = {a}, b = {b}")
    print(f"Public keys: A = {A}, B = {B}")
    
    # Compute shared key
    shared_key = compute_shared_key(a, b, A, B, p)
    print(f"Shared key: {shared_key}")
    
    # e)
    # Attack the protocol
    recovered_a = baby_step_giant_step(g, A, p)
    recovered_b = baby_step_giant_step(g, B, p)
    print(f"Recovered private keys: a = {recovered_a}, b = {recovered_b}")
    print(f"Recomputed shared key: {pow(B, recovered_a, p)}")
