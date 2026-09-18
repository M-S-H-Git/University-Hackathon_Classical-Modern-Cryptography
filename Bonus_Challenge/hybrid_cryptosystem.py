"""
Challenge 1: Hybrid Cryptosystem
Combines RSA (key exchange) + Playfair Cipher (message encryption).

Flow:
  1. Alice generates RSA keypair
  2. Alice sends PUBLIC key to Bob
  3. Bob generates a random Playfair keyword
  4. Bob ENCRYPTS the keyword with Alice's RSA public key  -> sends ciphertext
  5. Alice DECRYPTS the keyword with her RSA private key
  6. Both now share the same Playfair keyword
  7. Alice sends a secret message (Playfair encrypted)
  8. Bob decrypts it
  9. Bob replies (Playfair encrypted)
  10. Alice decrypts it
"""

import secrets
import string
import time
from Crypto.Util.number import getPrime, inverse

# ──────────────────────────────────────────────────────────────
#  RSA Engine
# ──────────────────────────────────────────────────────────────

def rsa_generate_keys(bits=512):
    """Generate RSA public/private keypair."""
    p = getPrime(bits)
    q = getPrime(bits)
    while q == p:
        q = getPrime(bits)

    n   = p * q
    phi = (p - 1) * (q - 1)
    e   = 65537
    d   = inverse(e, phi)
    return (e, n), (d, n)


def rsa_encrypt_bytes(data: bytes, public_key: tuple) -> int:
    """Encrypt raw bytes using RSA public key, returns ciphertext integer."""
    e, n = public_key
    m_int = int.from_bytes(data, byteorder='big')
    if m_int >= n:
        raise ValueError("Message too large for this RSA key size.")
    return pow(m_int, e, n)


def rsa_decrypt_bytes(cipher_int: int, private_key: tuple) -> bytes:
    """Decrypt RSA ciphertext integer back to bytes."""
    d, n = private_key
    m_int = pow(cipher_int, d, n)
    byte_len = (m_int.bit_length() + 7) // 8
    return m_int.to_bytes(byte_len, byteorder='big')


# ──────────────────────────────────────────────────────────────
#  Playfair Engine
# ──────────────────────────────────────────────────────────────

def build_matrix(keyword: str) -> list:
    """Build a 5x5 Playfair matrix from a keyword (I/J combined)."""
    keyword = keyword.upper().replace("J", "I")
    seen, order = set(), []
    for ch in keyword:
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            order.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.add(ch)
            order.append(ch)
    return [order[i*5: i*5+5] for i in range(5)]


def build_pos(matrix: list) -> dict:
    """Build character -> (row, col) lookup map."""
    return {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}


def prepare_text(text: str) -> str:
    """Convert plaintext to valid Playfair digraph pairs."""
    text = text.upper().replace("J", "I")
    text = "".join(ch for ch in text if ch.isalpha())
    result = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 == len(text):
            result.append(a + "X")
            i += 1
        elif text[i] == text[i + 1]:
            result.append(a + "X")
            i += 1
        else:
            result.append(a + text[i + 1])
            i += 2
    return "".join(result)


def playfair_apply(text: str, matrix: list, encrypt: bool) -> str:
    """Apply Playfair cipher rules (encrypt=True for encryption, False for decryption)."""
    pos   = build_pos(matrix)
    shift = 1 if encrypt else -1
    text  = prepare_text(text) if encrypt else text.upper().replace("J", "I")
    pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    result = []
    for pair in pairs:
        a, b = pair[0], pair[1]
        r1, c1 = pos[a]
        r2, c2 = pos[b]
        if r1 == r2:
            result.append(matrix[r1][(c1 + shift) % 5])
            result.append(matrix[r2][(c2 + shift) % 5])
        elif c1 == c2:
            result.append(matrix[(r1 + shift) % 5][c1])
            result.append(matrix[(r2 + shift) % 5][c2])
        else:
            result.append(matrix[r1][c2])
            result.append(matrix[r2][c1])
    return "".join(result)


def playfair_encrypt(plaintext: str, keyword: str) -> str:
    return playfair_apply(plaintext, build_matrix(keyword), encrypt=True)


def playfair_decrypt(ciphertext: str, keyword: str) -> str:
    return playfair_apply(ciphertext, build_matrix(keyword), encrypt=False)


# ──────────────────────────────────────────────────────────────
#  Display helpers
# ──────────────────────────────────────────────────────────────

def banner(title: str):
    width = 62
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def step(actor: str, action: str):
    tag = f"[{actor}]"
    print(f"\n{tag:<8} {action}")


def show(label: str, value, truncate=120):
    val_str = str(value)
    if len(val_str) > truncate:
        val_str = val_str[:truncate] + "..."
    print(f"           {label:<20} {val_str}")


def separator():
    print("           " + "-" * 50)


# ──────────────────────────────────────────────────────────────
#  Main simulation
# ──────────────────────────────────────────────────────────────

def simulate():
    banner("HYBRID CRYPTOSYSTEM: RSA + PLAYFAIR CIPHER")
    print("  Alice and Bob establish a secure channel using RSA")
    print("  key exchange, then communicate via Playfair cipher.")

    # ── STEP 1: Alice generates RSA keypair ──────────────────
    banner("STEP 1: Alice Generates RSA Key Pair")
    step("ALICE", "Generating 512-bit RSA keypair ...")
    t0 = time.time()
    alice_pub, alice_priv = rsa_generate_keys(bits=512)
    elapsed = time.time() - t0
    e, n = alice_pub
    d, _ = alice_priv
    show("Public  e :", e)
    show("Modulus n :", n)
    show("Private d :", d)
    show("Key gen time:", f"{elapsed:.4f} seconds")

    # ── STEP 2: Alice shares public key ──────────────────────
    banner("STEP 2: Alice Sends Public Key to Bob")
    step("ALICE", "Sharing public key (e, n) over an insecure channel.")
    show("Sent (e, n):", f"e={e}, n={str(n)[:40]}...")
    step("BOB",   "Received Alice's public key.")

    # ── STEP 3: Bob generates Playfair keyword ────────────────
    banner("STEP 3: Bob Generates a Random Playfair Keyword")
    keyword = "".join(secrets.choice(string.ascii_uppercase) for _ in range(8))
    step("BOB", f"Generated random 8-letter Playfair keyword.")
    show("Keyword (secret):", keyword)
    show("Matrix will use :", "Standard 5x5 with I/J combined")

    # ── STEP 4: Bob encrypts keyword with Alice's public key ──
    banner("STEP 4: Bob Encrypts the Keyword with Alice's RSA Public Key")
    step("BOB", "Encrypting keyword using Alice's public key ...")
    keyword_bytes   = keyword.encode("ascii")
    keyword_cipher  = rsa_encrypt_bytes(keyword_bytes, alice_pub)
    step("BOB", "Encrypted keyword (RSA ciphertext):")
    show("RSA Ciphertext:", keyword_cipher)
    step("BOB", "Sending RSA ciphertext to Alice over the network.")

    # ── STEP 5: Alice decrypts the keyword ────────────────────
    banner("STEP 5: Alice Decrypts the Keyword Using Her RSA Private Key")
    step("ALICE", "Received RSA ciphertext from Bob.")
    step("ALICE", "Decrypting with her private key ...")
    recovered_bytes   = rsa_decrypt_bytes(keyword_cipher, alice_priv)
    recovered_keyword = recovered_bytes.decode("ascii")
    show("Recovered keyword:", recovered_keyword)

    match = recovered_keyword == keyword
    step("VERIFY", f"Keyword match: {'[OK] SUCCESS' if match else '[FAIL] MISMATCH'}")
    if not match:
        print("  ERROR: Keyword exchange failed. Aborting.")
        return

    separator()
    print("           Both Alice and Bob now share the Playfair keyword:")
    print(f"           >> Shared keyword: {keyword} <<")
    separator()

    # ── STEP 6: Show the shared Playfair matrix ───────────────
    banner("STEP 6: Shared Playfair Key Matrix")
    matrix = build_matrix(keyword)
    print()
    print("           " + "+-----------Playfair Matrix-----------+")
    for row in matrix:
        print("           |  " + "   ".join(row) + "  |")
    print("           +-------------------------------------+")

    # ── STEP 7: Alice sends an encrypted message to Bob ───────
    banner("STEP 7: Alice Sends an Encrypted Message to Bob")
    alice_msg = "MEET ME AT THE CLOCK TOWER TONIGHT AT MIDNIGHT"
    step("ALICE", f"Plaintext : \"{alice_msg}\"")
    alice_cipher = playfair_encrypt(alice_msg, keyword)
    step("ALICE", "Encrypting with shared Playfair keyword ...")
    show("Ciphertext:", alice_cipher)
    step("ALICE", "Sending ciphertext to Bob.")

    # ── STEP 8: Bob decrypts Alice's message ──────────────────
    banner("STEP 8: Bob Decrypts Alice's Message")
    step("BOB", f"Received ciphertext: {alice_cipher}")
    step("BOB", "Decrypting with shared Playfair keyword ...")
    bob_decrypted = playfair_decrypt(alice_cipher, keyword)
    show("Decrypted :", bob_decrypted)

    # ── STEP 9: Bob sends an encrypted reply ──────────────────
    banner("STEP 9: Bob Sends an Encrypted Reply to Alice")
    bob_msg = "UNDERSTOOD I WILL BE THERE WITH THE DOCUMENTS"
    step("BOB", f"Plaintext : \"{bob_msg}\"")
    bob_cipher = playfair_encrypt(bob_msg, keyword)
    step("BOB", "Encrypting with shared Playfair keyword ...")
    show("Ciphertext:", bob_cipher)
    step("BOB", "Sending ciphertext to Alice.")

    # ── STEP 10: Alice decrypts Bob's reply ───────────────────
    banner("STEP 10: Alice Decrypts Bob's Reply")
    step("ALICE", f"Received ciphertext: {bob_cipher}")
    step("ALICE", "Decrypting with shared Playfair keyword ...")
    alice_decrypted = playfair_decrypt(bob_cipher, keyword)
    show("Decrypted :", alice_decrypted)

    # ── Final summary ─────────────────────────────────────────
    banner("COMMUNICATION COMPLETE - SESSION SUMMARY")
    print()
    print("  Participant   Action                   Status")
    print("  " + "-" * 56)
    print(f"  Alice         RSA Key Generation       OK")
    print(f"  Alice->Bob    Public Key Exchange       OK")
    print(f"  Bob           Keyword Generation        OK  ({keyword})")
    print(f"  Bob->Alice    RSA Keyword Encryption    OK")
    print(f"  Alice         RSA Keyword Decryption    OK")
    print(f"  Alice->Bob    Playfair Message          OK")
    print(f"  Bob           Playfair Decryption       OK")
    print(f"  Bob->Alice    Playfair Reply            OK")
    print(f"  Alice         Playfair Decryption       OK")
    print()

    # ── Security Analysis ─────────────────────────────────────
    banner("SECURITY ANALYSIS: VULNERABILITIES OF THIS HYBRID SYSTEM")
    print("""
  1. PLAYFAIR CIPHER IS WEAK
     Playfair is a classical cipher, NOT computationally secure.
     It leaks digraph frequencies and can be broken with ~1000
     characters of ciphertext using hill-climbing algorithms.
     It should be replaced with AES-GCM for real-world use.

  2. NO FORWARD SECRECY
     The same Playfair keyword is used for ALL messages in the
     session. If the keyword is ever exposed (e.g., via Playfair
     cryptanalysis), ALL past messages are compromised. A modern
     system (e.g., TLS 1.3) would use ephemeral Diffie-Hellman
     to derive fresh session keys, providing forward secrecy.

  3. RSA WITHOUT PADDING (TEXTBOOK RSA)
     This implementation uses raw RSA for keyword encryption.
     An attacker who captures the ciphertext can perform a chosen
     ciphertext attack. Production systems must use RSA-OAEP
     (PKCS#1 v2.1) padding.

  4. NO AUTHENTICATION / MAN-IN-THE-MIDDLE RISK
     Alice has no way to verify that the public key she holds
     actually belongs to Bob, and vice versa. A MITM attacker
     could substitute their own RSA public key and intercept all
     Playfair keywords. Fix: use digital certificates (PKI) or
     a pre-shared authentication mechanism.

  5. NO MESSAGE INTEGRITY CHECK
     There is no MAC (Message Authentication Code) or digital
     signature on the Playfair ciphertext. An active attacker
     can modify ciphertext bytes in transit and neither party
     will detect the corruption. Fix: use an AEAD cipher like
     AES-GCM which provides built-in authentication.
""")
    print("=" * 62)


if __name__ == "__main__":
    simulate()
