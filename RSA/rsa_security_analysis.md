# Task 7: RSA Security Analysis Report

---

## 1. Why is RSA Considered Secure?

RSA's security rests on the **Integer Factorization Problem (IFP)**: given a large composite number $n = p \times q$, it is computationally infeasible to recover the two prime factors $p$ and $q$ in polynomial time, even for the most powerful computers available today.

### The Mathematics of Security

When RSA keys are generated, two large primes $p$ and $q$ are multiplied together. The result, $n$, is made **public**. While multiplication of two numbers is trivially easy (polynomial time), the **reverse operation — factorization — scales exponentially** with the size of $n$.

```
                     EASY (milliseconds)
   p × q  ─────────────────────────────────►  n
   (secret)                                (public)

                     HARD (billions of years)
   n      ─────────────────────────────────►  p, q
   (public)                                (secret)
```

The best known classical algorithm for general-purpose integer factorization, the **General Number Field Sieve (GNFS)**, runs in sub-exponential time:

$$O\!\left(\exp\!\left(\!\left(\tfrac{64}{9}\right)^{1/3}\!(\ln n)^{1/3}(\ln\ln n)^{2/3}\right)\right)$$

For a 2048-bit RSA key, this translates to approximately $2^{112}$ operations — computationally infeasible for any classical adversary. This is why NIST recommends a **minimum key size of 2048 bits** for RSA through 2030 [1].

The **Discrete Logarithm Problem (DLP)** provides a second layer of theoretical hardness: even if $n$ were factored, computing the private exponent $d$ from the public exponent $e$ requires solving a computationally intractable modular inverse [2].

---

## 2. Common RSA Attacks

### Attack 1: Small Exponent Attack (e = 3)

**Overview:** Using a small public exponent like $e = 3$ drastically speeds up encryption but creates a devastating vulnerability when the same message $M$ is encrypted to multiple parties without proper padding.

**How it works (Håstad's Broadcast Attack):**

Suppose Alice sends the same message $M$ to three recipients, each with the same exponent $e = 3$ but different moduli $n_1, n_2, n_3$.

Each recipient receives:
$$C_1 = M^3 \bmod n_1, \quad C_2 = M^3 \bmod n_2, \quad C_3 = M^3 \bmod n_3$$

An adversary who intercepts all three ciphertexts can apply the **Chinese Remainder Theorem (CRT)** to reconstruct:

$$C^* \equiv M^3 \pmod{n_1 \cdot n_2 \cdot n_3}$$

If $M^3 < n_1 \cdot n_2 \cdot n_3$ (likely for small messages), the adversary simply computes the integer **cube root** of $C^*$ over the integers — no modular reduction needed — and recovers $M$ entirely.

```
  Intercepted:  C1, C2, C3
       │
       ▼
   CRT reconstruction → M^3 (no mod reduction)
       │
       ▼
   Cube root → M (PLAINTEXT RECOVERED)
```

**Real-world example:** In 1998, Coppersmith extended this to show that even with a single recipient, if part of the message is known, small $e$ allows full plaintext recovery via lattice-based methods [3].

**Mitigation:** Always use $e = 65537$ (a Fermat prime) combined with OAEP padding.

---

### Attack 2: Wiener's Attack (Small Private Key d)

**Overview:** Generating a small private key $d$ speeds up decryption but completely breaks security if $d < \frac{1}{3} n^{1/4}$.

**How it works:**

RSA requires $e \cdot d \equiv 1 \pmod{\phi(n)}$, which can be written as:

$$e \cdot d = k \cdot \phi(n) + 1 \quad \text{for some integer } k$$

Dividing both sides by $d \cdot \phi(n)$:

$$\frac{e}{\phi(n)} = \frac{k}{d} + \frac{1}{d \cdot \phi(n)}$$

Since $\phi(n) \approx n$, this is approximately:

$$\frac{e}{n} \approx \frac{k}{d}$$

Michael Wiener (1990) proved that the fraction $\frac{k}{d}$ appears as a **convergent in the continued fraction expansion** of $\frac{e}{n}$, which can be computed in polynomial time [2].

```
  Public: e, n
       │
       ▼
  Compute continued fraction expansion of e/n
       │
       ▼
  Test each convergent k/d
       │
       ▼
  Check if φ(n) = (e*d - 1)/k is an integer
  and n factors as roots of x² - (n - φ(n) + 1)x + n = 0
       │
       ▼
  Private key d RECOVERED
```

**Real-world impact:** For a 1024-bit RSA key, Wiener's attack succeeds if $d < n^{0.25} \approx 2^{256}$. This is a massive portion of the keyspace.

**Mitigation:** Always generate $d$ using a cryptographically secure random prime pair; never deliberately choose a small $d$.

---

## 3. Padding Schemes: Why Textbook RSA is Insecure

### The Problem with Raw (Textbook) RSA

Raw RSA — computing $C = M^e \bmod n$ directly — is **deterministic** and **malleable**, creating multiple attack vectors:

| Vulnerability | Description |
|---|---|
| **Determinism** | Encrypting the same $M$ always yields the same $C$. An attacker can build a dictionary of common encrypted values. |
| **Malleability** | Given $C = M^e \bmod n$, an attacker can compute $C' = r^e \cdot C \bmod n$, which decrypts to $r \cdot M$ — a useful transformation without knowing $M$. |
| **Short Message Weakness** | If $M$ is small and $e = 3$, then $M^3 < n$ and the cube root of $C$ over integers directly reveals $M$. |
| **Chosen Plaintext Attack** | An attacker can submit crafted ciphertexts for decryption and deduce information about the key. |

### PKCS#1 v1.5 Padding

Defined in RFC 8017 [1], PKCS#1 v1.5 padding adds a structured random prefix to the message before encryption:

```
  Block:  0x00 | 0x02 | [random non-zero bytes] | 0x00 | Message
                        ↑ at least 8 bytes ↑
```

This introduces **non-determinism** (the random bytes differ each time) and ensures the ciphertext leaks no information about the plaintext. However, it is vulnerable to the **Bleichenbacher padding oracle attack** (1998), where an adversary can decrypt any ciphertext by submitting ~1 million chosen ciphertexts to a server that reveals whether padding is valid.

### OAEP (Optimal Asymmetric Encryption Padding)

Defined in RFC 8017 and standardized by PKCS#1 v2.x, OAEP is the **modern and recommended** standard. It uses a pair of hash functions (typically SHA-256) and a Mask Generation Function (MGF) to provide **semantic security (IND-CCA2)**.

```
           Message (M)
               │
               ▼
   M || 0...0 (padding)     ← (k - hLen - 1) bytes total
               │    ┌────────────────────────────┐
               │    │ Random seed (r)             │
               ▼    ▼                             │
         XOR with MGF(r)  → masked_message       │
               │                                  │
               │    ┌──────────────────────────── ┘
               ▼    ▼
         XOR with MGF(masked_message) → masked_seed
               │
               ▼
       0x00 || masked_seed || masked_message
               │
               ▼
       RSA Encryption (EM^e mod n)
```

OAEP was **proven IND-CCA2 secure** under the RSA assumption and the Random Oracle Model by Fujisaki et al. (2001) [3], meaning even an attacker with access to a decryption oracle cannot distinguish encryptions of two chosen plaintexts.

---

## Summary Table

| Aspect | Textbook RSA | PKCS#1 v1.5 | OAEP |
|---|---|---|---|
| Randomized | No | Yes | Yes |
| Secure against CCA | No | Partially | Yes (IND-CCA2) |
| Padding Oracle Vulnerable | N/A | Yes (Bleichenbacher) | No |
| Recommended for new systems | No | No | **Yes** |

---

## References

[1] National Institute of Standards and Technology (NIST), *NIST SP 800-131A Rev. 2: Transitioning the Use of Cryptographic Algorithms and Key Lengths*, U.S. Dept. of Commerce, 2019. Available: https://doi.org/10.6028/NIST.SP.800-131Ar2

[2] M. J. Wiener, "Cryptanalysis of short RSA secret exponents," *IEEE Transactions on Information Theory*, vol. 36, no. 3, pp. 553–558, May 1990. Available: https://doi.org/10.1109/18.54902

[3] E. Fujisaki, T. Okamoto, D. Pointcheval, and J. Stern, "RSA-OAEP Is Secure under the RSA Assumption," *Journal of Cryptology*, vol. 17, pp. 81–104, 2004. Available: https://doi.org/10.1007/s00145-002-0204-y
