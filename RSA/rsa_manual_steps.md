# Task 5: Manual RSA Key Generation & Encryption

**Given:**
- $p = 61$
- $q = 53$
- $e = 17$
- $M = 65$

---

### 1. Calculate $n$
The modulus $n$ is the product of the two primes.
$n = p \times q$
$n = 61 \times 53$
**$n = 3233$**

### 2. Calculate $\phi(n)$
Euler's totient function for the product of two primes:
$\phi(n) = (p - 1)(q - 1)$
$\phi(n) = (61 - 1) \times (53 - 1)$
$\phi(n) = 60 \times 52$
**$\phi(n) = 3120$**

### 3. Verify $\gcd(e, \phi(n)) = 1$
Using the Euclidean Algorithm:
- $3120 = 17 \times 183 + 9$
- $17 = 9 \times 1 + 8$
- $9 = 8 \times 1 + 1$
- $8 = 1 \times 8 + 0$

Since the last non-zero remainder is 1, **$\gcd(17, 3120) = 1$**.

### 4. Compute Private Key $d$
We need to find $d$ such that $e \times d \equiv 1 \pmod{\phi(n)}$. 
This is found using the **Extended Euclidean Algorithm** by working backward from our GCD steps:
- $1 = 9 - (8 \times 1)$
- Substitute $8 = 17 - (9 \times 1)$:
  $1 = 9 - (17 - 9)$
  $1 = 2 \times 9 - 17$
- Substitute $9 = 3120 - (17 \times 183)$:
  $1 = 2 \times (3120 - 17 \times 183) - 17$
  $1 = 2 \times 3120 - 366 \times 17 - 17$
  $1 = 2 \times 3120 - 367 \times 17$

Therefore, the coefficient for 17 is $-367$.
To find the positive modular inverse: 
$d = -367 \pmod{3120}$
$d = 3120 - 367$
**$d = 2753$**

### 5. Encrypt Message $M = 65$
$C \equiv M^e \pmod n$
$C \equiv 65^{17} \pmod{3233}$
**(Calculation Breakdown):**
- $65^2 \equiv 4225 \equiv 992 \pmod{3233}$
- $65^4 \equiv 992^2 \equiv 984064 \equiv 1332 \pmod{3233}$
- $65^8 \equiv 1332^2 \equiv 1774224 \equiv 2636 \pmod{3233}$
- $65^{16} \equiv 2636^2 \equiv 6948496 \equiv 1809 \pmod{3233}$
- $65^{17} \equiv 65^{16} \times 65 \equiv 1809 \times 65 \equiv 117585 \equiv 2790 \pmod{3233}$

**Ciphertext $C = 2790$**

### 6. Decrypt $C$ back to verify $M$
$M \equiv C^d \pmod n$
$M \equiv 2790^{2753} \pmod{3233}$
Using modular exponentiation (fast exponentiation algorithm):
**$M = 65$**
*(Verification successful)*
