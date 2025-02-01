import random
from math import gcd

# Miller-Rabin Primality Test
def is_probable_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

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

# a) Check if p and q are prime
p = 2903
q = 4091

print(f"Is p={p} probably prime? {is_probable_prime(p)}")
print(f"Is q={q} probably prime? {is_probable_prime(q)}")

# b) Compute n, Euler's totient function phi(n), and private exponent d
n = p * q
phi = (p - 1) * (q - 1)
e = 4097

if gcd(e, phi) != 1:
    raise ValueError("e and phi(n) are not coprime.")

# Extended Euclidean Algorithm to find modular inverse of e modulo phi(n)
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

_, d, _ = extended_gcd(e, phi)
d = d % phi if d > 0 else d + phi  # Ensure d is positive

print(f"Computed private exponent d={d}")

# c) Encrypt the message "Att"
message = "Att"
m = ord('A') * 256**2 + ord('t') * 256 + ord('t')  # Convert to integer
c = pow(m, e, n)  # Encrypt

print(f"Message '{message}' encrypted as: c={c}")

# d) Decrypt the message
decrypted_m = pow(c, d, n)  # Decrypt
z1 = decrypted_m // 256**2
z2 = (decrypted_m % 256**2) // 256
z3 = decrypted_m % 256
decrypted_message = chr(z1) + chr(z2) + chr(z3)  # Convert back to string

print(f"Decrypted message: {decrypted_message}")

# e) Factorize n using Pollard's Rho algorithm
def pollards_rho(n):
    def f(x):
        return (x**2 + 1) % n

    x, y, d = 2, 2, 1
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    if d == n:
        return None  # Factorization failed
    return d

# Given n in the task
n_to_factor = 11876173
factor = pollards_rho(n_to_factor)

if factor:
    print(f"Found factor: {factor}, other factor: {n_to_factor // factor}")
else:
    print("Failed to find a factor using Pollard's Rho.")

