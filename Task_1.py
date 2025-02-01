import random
from math import gcd

# Function for Miller-Rabin primality test
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

# b) Compute n and d
n = p * q
phi = (p - 1) * (q - 1)
e = 4097

if gcd(e, phi) != 1:
    raise ValueError("e and phi are not coprime.")

# Extended Euclidean Algorithm
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

_, d, _ = extended_gcd(e, phi)
d = d % phi
if d < 0:
    d += phi

print(f"Computed d={d}")

# c) Encrypt the message "Att"
message = "Att"
m = ord('A') * 256**2 + ord('t') * 256 + ord('t')
c = pow(m, e, n)
print(f"Message {message} encrypted as: c={c}")

# d) Decrypt the message
decrypted_m = pow(c, d, n)
z1 = decrypted_m // 256**2
z2 = (decrypted_m % 256**2) // 256
z3 = decrypted_m % 256
decrypted_message = chr(z1) + chr(z2) + chr(z3)
print(f"Decrypted message: {decrypted_message}")

# e) Factorize n using Pollard's rho algorithm
def pollards_rho(n):
    def f(x):
        return (x**2 + 1) % n

    x, y, d = 2, 2, 1
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    if d == n:
        return None
    return d

factor = pollards_rho(11876173)
if factor:
    print(f"Found factor: {factor}, other factor: {11876173 // factor}")
else:
    print("Failed to find a factor using Pollard's rho.")
