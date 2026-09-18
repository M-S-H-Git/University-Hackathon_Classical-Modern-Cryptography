"""
Task 6: Complete RSA Implementation
"""
import time
import math
from Crypto.Util.number import getPrime, inverse

def text_to_int(text: str) -> int:
    """Converts a string to an integer using UTF-8 encoding."""
    return int.from_bytes(text.encode('utf-8'), byteorder='big')

def int_to_text(integer: int) -> str:
    """Converts an integer back to a UTF-8 string."""
    byte_length = (integer.bit_length() + 7) // 8
    return integer.to_bytes(byte_length, byteorder='big').decode('utf-8')

def rsa_key_generation(bits=512):
    """Generates RSA public and private keys."""
    start_time = time.time()
    
    # 1. Generate random prime numbers p and q
    p = getPrime(bits)
    q = getPrime(bits)
    
    # Ensure p != q
    while p == q:
        q = getPrime(bits)
        
    # 2. Compute n and φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # 3. Choose public exponent e
    # 65537 is commonly used because it's a prime and makes encryption fast
    e = 65537 
    if math.gcd(e, phi) != 1:
        # Fallback to finding a valid e if 65537 divides phi
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
            
    # 4. Compute private key d
    d = inverse(e, phi)
    
    time_taken = time.time() - start_time
    
    return {
        'public_key': (e, n),
        'private_key': (d, n),
        'p': p,
        'q': q,
        'phi': phi,
        'time_taken': time_taken
    }

def rsa_encrypt(message: str, public_key: tuple) -> int:
    """Encrypts a string message."""
    e, n = public_key
    m_int = text_to_int(message)
    if m_int >= n:
        raise ValueError("Message is too long for this key size.")
    
    c = pow(m_int, e, n)
    return c

def rsa_decrypt(ciphertext: int, private_key: tuple) -> str:
    """Decrypts a ciphertext integer back to string."""
    d, n = private_key
    m_int = pow(ciphertext, d, n)
    return int_to_text(m_int)

def rsa_sign(message: str, private_key: tuple) -> int:
    """Signs a message using the private key (M^d mod n)."""
    d, n = private_key
    m_int = text_to_int(message)
    signature = pow(m_int, d, n)
    return signature

def rsa_verify(message: str, signature: int, public_key: tuple) -> bool:
    """Verifies a signature using the public key (S^e mod n == M)."""
    e, n = public_key
    m_int = text_to_int(message)
    verified_m_int = pow(signature, e, n)
    return m_int == verified_m_int

def main():
    print("=" * 60)
    print(" TASK 6: COMPLETE RSA IMPLEMENTATION ")
    print("=" * 60)
    
    # Key Generation
    print("[*] Generating 512-bit RSA Keys...")
    keys = rsa_key_generation(bits=512)
    e, n = keys['public_key']
    d, _ = keys['private_key']
    
    print(f"\n--- KEY GENERATION DETAILS ---")
    print(f"Time Taken : {keys['time_taken']:.4f} seconds")
    print(f"Prime p    : {keys['p']}")
    print(f"Prime q    : {keys['q']}")
    print(f"Modulus n  : {n}")
    print(f"Totient phi: {keys['phi']}")
    print(f"Public e   : {e}")
    print(f"Private d  : {d}")
    
    # Message to process (must be >= 50 characters as per prompt)
    message = "Cryptography is the ultimate shield for securing digital communication in the modern world."
    print(f"\n--- ENCRYPTION / DECRYPTION ---")
    print(f"Original Text (Length {len(message)}):")
    print(f"\"{message}\"")
    
    # Encrypt
    ciphertext = rsa_encrypt(message, keys['public_key'])
    print(f"\nCiphertext (Integer Representation):")
    print(f"{ciphertext}")
    
    # Decrypt
    decrypted = rsa_decrypt(ciphertext, keys['private_key'])
    print(f"\nDecrypted Text:")
    print(f"\"{decrypted}\"")
    print(f"Status: {'[PASS] SUCCESS' if message == decrypted else '[FAIL] FAILED'}")
    
    # Digital Signature
    print(f"\n--- DIGITAL SIGNATURE ---")
    print("[*] Signing the original message with the Private Key...")
    signature = rsa_sign(message, keys['private_key'])
    print(f"Signature (Integer Representation):")
    print(f"{signature}")
    
    print("[*] Verifying the signature with the Public Key...")
    is_valid = rsa_verify(message, signature, keys['public_key'])
    print(f"Signature Verification Status: {'[PASS] VALID' if is_valid else '[FAIL] INVALID'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
