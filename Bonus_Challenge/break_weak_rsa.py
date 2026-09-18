"""
Challenge 2: Breaking Weak RSA
Tasks:
  1. Factor n=3233 using trial division (small primes < 100)
  2. Compute private key d and decrypt C=2790
  3. Factor n=10403 using Fermat's Factorization + Pollard's Rho
  4. Explain why each method works
"""
import math
import random
import time

# ──────────────────────────────────────────────────────────────
#  Helper utilities
# ──────────────────────────────────────────────────────────────

def extended_gcd(a: int, b: int):
    """Extended Euclidean Algorithm. Returns (gcd, x, y) s.t. a*x + b*y = gcd."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(e: int, phi: int) -> int:
    """Compute modular inverse of e mod phi using Extended Euclidean Algorithm."""
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError(f"Inverse doesn't exist: gcd({e}, {phi}) = {g}")
    return x % phi


def banner(title: str):
    w = 64
    print("\n" + "=" * w)
    print(f"  {title}")
    print("=" * w)


def section(title: str):
    print(f"\n  --- {title} ---")


def show(label: str, value):
    print(f"  {label:<32} {value}")


# ──────────────────────────────────────────────────────────────
#  1. Trial Division Factoring (for small n)
# ──────────────────────────────────────────────────────────────

def trial_division_factor(n: int, verbose=True) -> tuple:
    """
    Factor n by trying every odd divisor from 2 up to sqrt(n).
    Efficient for small n where factors are < 100.
    Returns (p, q) if found, else raises ValueError.
    """
    if verbose:
        section("Trial Division Factoring")
        print(f"  Testing divisors from 2 to sqrt({n}) = {math.isqrt(n)}")
        print()

    attempts = 0
    for p in range(2, math.isqrt(n) + 1):
        attempts += 1
        if n % p == 0:
            q = n // p
            if verbose:
                print(f"  Tried {attempts} divisors.")
                print(f"  FOUND: {n} = {p} x {q}")
                if all(
                    p % i != 0 for i in range(2, math.isqrt(p) + 1)
                ) and p > 1:
                    print(f"  Confirmed: {p} is prime")
                if all(
                    q % i != 0 for i in range(2, math.isqrt(q) + 1)
                ) and q > 1:
                    print(f"  Confirmed: {q} is prime")
            return p, q

    raise ValueError(f"Could not factor {n} by trial division.")


# ──────────────────────────────────────────────────────────────
#  2. RSA Key Recovery & Decryption
# ──────────────────────────────────────────────────────────────

def rsa_recover_and_decrypt(n: int, e: int, C: int, p: int, q: int):
    """Given factors p and q, recover private key d and decrypt ciphertext C."""
    section("RSA Private Key Recovery")

    phi = (p - 1) * (q - 1)
    show("phi(n) = (p-1)(q-1) =", phi)
    show("gcd(e, phi(n)) =", math.gcd(e, phi))

    # Extended Euclidean step-by-step display
    print(f"\n  Computing d = e^-1 mod phi(n) using Extended Euclidean:")
    print(f"  Solving: {e} * d == 1 (mod {phi})")
    d = mod_inverse(e, phi)
    print(f"  Solution: d = {d}")
    print(f"  Verify:   ({e} x {d}) mod {phi} = {(e * d) % phi}  <-- must be 1")

    section("Decryption")
    print(f"  Formula:   M = C^d mod n")
    print(f"  M = {C}^{d} mod {n}")
    M = pow(C, d, n)
    show("Decrypted integer M =", M)
    show("As ASCII character =", chr(M) if 32 <= M <= 126 else "(non-printable)")

    return d, M


# ──────────────────────────────────────────────────────────────
#  3a. Fermat's Factorization Method
# ──────────────────────────────────────────────────────────────

def fermat_factor(n: int, verbose=True) -> tuple:
    """
    Fermat's Factorization: Express n = a^2 - b^2 = (a+b)(a-b).
    Works well when p and q are CLOSE TOGETHER (a and b will be small).
    """
    if verbose:
        section("Fermat's Factorization Method")
        print(f"  Key idea: n = a^2 - b^2 = (a+b)(a-b)")
        print(f"  Start with a = ceil(sqrt(n)), check if a^2 - n is a perfect square.")
        print()

    a = math.isqrt(n)
    if a * a < n:
        a += 1

    iterations = 0
    while True:
        b2 = a * a - n
        b  = math.isqrt(b2)
        iterations += 1
        if verbose and iterations <= 10:
            print(f"  Iter {iterations:>3}: a={a}, a^2-n={b2}, sqrt={b:.4f}, "
                  f"perfect_square={b * b == b2}")
        if b * b == b2:
            p = a + b
            q = a - b
            if verbose:
                print(f"\n  Found after {iterations} iterations!")
                print(f"  a = {a}, b = {b}")
                print(f"  p = a + b = {p}")
                print(f"  q = a - b = {q}")
                print(f"  Verify: p x q = {p} x {q} = {p * q}  (= n? {p * q == n})")
            return p, q
        a += 1


# ──────────────────────────────────────────────────────────────
#  3b. Pollard's Rho Algorithm
# ──────────────────────────────────────────────────────────────

def pollard_rho(n: int, verbose=True) -> tuple:
    """
    Pollard's Rho: A probabilistic factoring algorithm.
    Uses Floyd's cycle detection on the sequence x_{i+1} = x_i^2 + c (mod n).
    Finds a non-trivial factor by detecting GCD collisions.
    """
    if verbose:
        section("Pollard's Rho Algorithm")
        print(f"  Key idea: Use pseudo-random sequence x = x^2 + c (mod n).")
        print(f"  Track two pointers (tortoise/hare) — find cycle via Floyd's algorithm.")
        print(f"  A non-trivial gcd(|x-y|, n) reveals a factor.")
        print()

    def f(x, c):
        return (x * x + c) % n

    for c in range(1, 20):
        x = 2
        y = 2
        d = 1
        steps = 0
        while d == 1:
            x = f(x, c)         # tortoise: 1 step
            y = f(f(y, c), c)   # hare:     2 steps
            d = math.gcd(abs(x - y), n)
            steps += 1
            if verbose and steps <= 8:
                print(f"  c={c}, step={steps:>3}: x={x:>6}, y={y:>6}, "
                      f"gcd(|x-y|={abs(x-y):>6}, n) = {d}")

        if d != n:
            p = d
            q = n // d
            if verbose:
                print(f"\n  Factor found with c={c} after {steps} steps!")
                print(f"  p = {p}")
                print(f"  q = {q}")
                print(f"  Verify: p x q = {p} x {q} = {p * q}  (= n? {p * q == n})")
            return p, q

    raise ValueError("Pollard's Rho failed to find a factor.")


# ──────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────

def main():

    # ══════════════════════════════════════════════════════════
    #  PART A: n = 3233, e = 17, C = 2790
    # ══════════════════════════════════════════════════════════

    banner("PART A — Factoring n = 3233 (Trial Division)")
    n1, e1, C1 = 3233, 17, 2790
    show("n =", n1)
    show("e =", e1)
    show("C =", C1)

    t0 = time.perf_counter()
    p1, q1 = trial_division_factor(n1, verbose=True)
    t1 = time.perf_counter()
    show("\nTime to factor:", f"{(t1-t0)*1000:.4f} ms")

    d1, M1 = rsa_recover_and_decrypt(n1, e1, C1, p1, q1)

    print(f"\n  RESULT")
    print(f"  n = {n1} = {p1} x {q1}")
    print(f"  e = {e1}")
    print(f"  d = {d1}")
    print(f"  C = {C1}")
    print(f"  M = {M1}  ('{chr(M1)}')")

    # ══════════════════════════════════════════════════════════
    #  PART B: n = 10403, e = 7, C = 1985
    # ══════════════════════════════════════════════════════════

    banner("PART B — Factoring n = 10403 (Fermat + Pollard's Rho)")
    n2, e2, C2 = 10403, 7, 1985
    show("n =", n2)
    show("e =", e2)
    show("C =", C2)

    # ── Fermat's Method ───────────────────────────────────────
    banner("PART B-1: Fermat's Factorization on n = 10403")
    t0 = time.perf_counter()
    p2f, q2f = fermat_factor(n2, verbose=True)
    t1 = time.perf_counter()
    show("\nTime to factor:", f"{(t1-t0)*1000:.4f} ms")

    d2f, M2f = rsa_recover_and_decrypt(n2, e2, C2, p2f, q2f)

    print(f"  n = {n2} = {p2f} x {q2f}")
    print(f"  d = {d2f}  |  M = {M2f}  ('{chr(M2f) if 32<=M2f<=126 else M2f}')") 

    # ── Pollard's Rho ─────────────────────────────────────────
    banner("PART B-2: Pollard's Rho on n = 10403")
    t0 = time.perf_counter()
    p2r, q2r = pollard_rho(n2, verbose=True)
    t1 = time.perf_counter()
    show("\nTime to factor:", f"{(t1-t0)*1000:.4f} ms")

    d2r, M2r = rsa_recover_and_decrypt(n2, e2, C2, p2r, q2r)

    print(f"\n  RESULT (via Pollard's Rho)")
    print(f"  n = {n2} = {p2r} x {q2r}")
    print(f"  d = {d2r}  |  M = {M2r}  ('{chr(M2r) if 32<=M2r<=126 else M2r}')")

    # ══════════════════════════════════════════════════════════
    #  EXPLANATION: Why these methods work
    # ══════════════════════════════════════════════════════════

    banner("EXPLANATION: Why These Attacks Work")
    lines = [
        "  FERMAT'S FACTORIZATION - works when p and q are close together",
        "  " + "-" * 61,
        "  If n = p * q and p ~= q, then both primes are near sqrt(n).",
        "  We can write n = a^2 - b^2 where a ~= sqrt(n) and b is small.",
        "",
        "  For n = 10403:  sqrt(10403) ~= 102.0",
        "    p = 101, q = 103  --> a = (103+101)/2 = 102, b = (103-101)/2 = 1",
        "",
        "  Fermat finds this in just 1 iteration because b=1 is tiny!",
        "  The RSA standard mandates that |p - q| must be large (> 2^100)",
        "  for exactly this reason. If p and q are close, n can be",
        "  factored in seconds even for 2048-bit keys.",
        "",
        "  POLLARD'S RHO - exploits the birthday paradox",
        "  " + "-" * 61,
        "  The birthday paradox says that in a group of size m, you need",
        "  only ~sqrt(m) random elements before two share a property.",
        "",
        "  Pollard's Rho generates a pseudo-random sequence mod n.",
        "  Because the sequence mod p repeats with period ~sqrt(p), the",
        "  algorithm finds x == y (mod p) after ~sqrt(p) steps - even",
        "  without knowing p! The GCD then reveals p from n.",
        "",
        "  For n = 10403 with p = 101:  sqrt(p) ~= 10 steps to factor.",
        "  Compare this to trial division which needs up to ~102 steps.",
        "",
        "  Both methods are catastrophic for RSA when:",
        "    - Primes are close (|p-q| is small)  --> Fermat wins",
        "    - One prime is small                 --> Pollard's Rho wins",
        "    - Primes are chosen non-randomly     --> Both win quickly",
    ]
    for line in lines:
        print(line)
    print("=" * 64)


if __name__ == "__main__":
    main()
