"""
Playfair Cipher — Encryption & Decryption
==========================================
Keyword : MONARCHY
Ciphertext: BXDREOGHBXLQZUMRVBXDREOGHBX
"""

# ─────────────────────────────────────────────────────────────
# 1.  BUILD THE 5×5 KEY MATRIX
# ─────────────────────────────────────────────────────────────

def build_matrix(keyword: str) -> list:
    """
    Constructs the 5×5 Playfair key matrix.
    - Removes duplicate letters from the keyword (preserving order).
    - Combines I and J into one cell (I used).
    - Fills the grid row-by-row with remaining alphabet letters.
    """
    keyword = keyword.upper().replace("J", "I")
    seen  = set()
    order = []

    # Add keyword letters first (unique only)
    for ch in keyword:
        if ch not in seen and ch.isalpha():
            seen.add(ch)
            order.append(ch)

    # Append remaining alphabet letters (no J)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.add(ch)
            order.append(ch)

    # Reshape into 5×5 grid
    matrix = [order[i*5 : i*5+5] for i in range(5)]
    return matrix


def print_matrix(matrix: list) -> None:
    """Pretty-prints the 5×5 key matrix."""
    print("\n  +-----------+-----------+")
    print("  | Col:  0  1  2  3  4   |")
    print("  +-----------+-----------+")
    for i, row in enumerate(matrix):
        cells = "  ".join(row)
        print(f"  | Row {i}:  {cells}   |")
    print("  +-----------+-----------+\n")


def build_position_map(matrix: list) -> dict:
    """Returns {letter: (row, col)} lookup dictionary."""
    pos = {}
    for r, row in enumerate(matrix):
        for c, ch in enumerate(row):
            pos[ch] = (r, c)
    return pos


# ─────────────────────────────────────────────────────────────
# 2.  SPLIT TEXT INTO DIGRAPHS
# ─────────────────────────────────────────────────────────────

def make_digraphs(text: str, filler: str = "X") -> list:
    """
    Prepares plaintext into Playfair digraph pairs:
    - Inserts filler between repeated letters in a pair.
    - Appends filler if the text length is odd.
    (Used during encryption.)
    """
    text = text.upper().replace("J", "I").replace(" ", "")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 == len(text):          # single letter at end
            pairs.append(a + filler)
            i += 1
        elif text[i] == text[i+1]:      # repeated-letter pair → insert filler
            pairs.append(a + filler)
            i += 1
        else:
            pairs.append(a + text[i+1])
            i += 2
    return pairs


def split_ciphertext(ciphertext: str) -> list:
    """Splits ciphertext into consecutive digraph pairs."""
    ct = ciphertext.upper().replace(" ", "")
    if len(ct) % 2 != 0:
        print(f"\n  [NOTE] Odd-length ciphertext ({len(ct)} chars). "
              f"Trailing '{ct[-1]}' is null padding — discarded.\n")
        ct = ct[:-1]
    return [ct[i:i+2] for i in range(0, len(ct), 2)]


# ─────────────────────────────────────────────────────────────
# 3.  APPLY PLAYFAIR RULES (per digraph)
# ─────────────────────────────────────────────────────────────

def apply_rule(a: str, b: str,
               matrix: list,
               pos: dict,
               mode: str = "decrypt") -> tuple:
    """
    Applies the correct Playfair rule to digraph (a, b).

    Returns: (result_a, result_b, rule_name)

    mode = 'decrypt' → same-row shifts LEFT, same-col shifts UP
    mode = 'encrypt' → same-row shifts RIGHT, same-col shifts DOWN
    """
    r1, c1 = pos[a]
    r2, c2 = pos[b]
    shift = -1 if mode == "decrypt" else 1

    if r1 == r2:                        # SAME ROW
        nc1 = (c1 + shift) % 5
        nc2 = (c2 + shift) % 5
        return matrix[r1][nc1], matrix[r2][nc2], "Same Row"

    elif c1 == c2:                      # SAME COLUMN
        nr1 = (r1 + shift) % 5
        nr2 = (r2 + shift) % 5
        return matrix[nr1][c1], matrix[nr2][c2], "Same Column"

    else:                               # RECTANGLE
        return matrix[r1][c2], matrix[r2][c1], "Rectangle"


# ─────────────────────────────────────────────────────────────
# 4.  HIGH-LEVEL DECRYPT / ENCRYPT
# ─────────────────────────────────────────────────────────────

def playfair_decrypt(ciphertext: str, keyword: str, verbose: bool = True) -> str:
    """
    Decrypts ciphertext using the Playfair cipher.
    Prints a full step-by-step breakdown when verbose=True.
    """
    matrix = build_matrix(keyword)
    pos    = build_position_map(matrix)

    if verbose:
        print("=" * 62)
        print("   PLAYFAIR CIPHER  —  STEP-BY-STEP DECRYPTION")
        print("=" * 62)

        # Step 1: Matrix
        print("\n  [STEP 1]  5x5 KEY MATRIX  (keyword:", keyword + ")")
        print_matrix(matrix)

        # Step 2: Split
        print("  [STEP 2]  SPLIT CIPHERTEXT INTO DIGRAPHS")

    pairs = split_ciphertext(ciphertext)

    if verbose:
        print("  Pairs:", "  |  ".join(pairs), "\n")

        # Step 3: Decrypt each pair
        print("  [STEP 3]  DECRYPT EACH DIGRAPH")
        print("  " + "-" * 60)
        print(f"  {'#':>2}  {'Cipher':6}  {'Positions':24}  {'Rule':14}  Plain")
        print("  " + "-" * 60)

    plaintext = []

    for idx, pair in enumerate(pairs, start=1):
        a, b = pair[0], pair[1]
        r1, c1 = pos[a]
        r2, c2 = pos[b]
        pa, pb, rule = apply_rule(a, b, matrix, pos, mode="decrypt")
        nr1, nc1 = pos[pa]
        nr2, nc2 = pos[pb]
        plaintext.append(pa + pb)

        if verbose:
            pos_str   = f"{a}({r1},{c1})  {b}({r2},{c2})"
            plain_str = f"{pa}({nr1},{nc1}) {pb}({nr2},{nc2})"
            print(f"  {idx:>2}  {pair:6}  {pos_str:24}  {rule:14}  {plain_str}")

    result = "".join(plaintext)

    if verbose:
        print("  " + "-" * 60)
        print("\n  [STEP 4]  FINAL PLAINTEXT")
        print("  Grouped :", "  ".join(plaintext))
        print("  Joined  :", result)
        print("\n" + "=" * 62)

    return result


def playfair_encrypt(plaintext: str, keyword: str, verbose: bool = True) -> str:
    """
    Encrypts plaintext using the Playfair cipher.
    Prints a full step-by-step breakdown when verbose=True.
    """
    matrix = build_matrix(keyword)
    pos    = build_position_map(matrix)
    pairs  = make_digraphs(plaintext)

    if verbose:
        print("=" * 62)
        print("   PLAYFAIR CIPHER  —  STEP-BY-STEP ENCRYPTION")
        print("=" * 62)
        print(f"\n  Keyword   : {keyword}")
        print(f"  Plaintext : {plaintext}")
        print(f"  Digraphs  : {'  '.join(pairs)}")
        print_matrix(matrix)
        print("  " + "-" * 40)
        print(f"  {'#':>2}  {'Plain':6}  {'Rule':14}  Cipher")
        print("  " + "-" * 40)

    ciphertext = []

    for idx, pair in enumerate(pairs, start=1):
        a, b = pair[0], pair[1]
        ca, cb, rule = apply_rule(a, b, matrix, pos, mode="encrypt")
        ciphertext.append(ca + cb)
        if verbose:
            print(f"  {idx:>2}  {pair:6}  {rule:14}  {ca}{cb}")

    result = "".join(ciphertext)

    if verbose:
        print("  " + "-" * 40)
        print(f"\n  Ciphertext: {result}\n")
        print("=" * 62)

    return result


# ─────────────────────────────────────────────────────────────
# 5.  MAIN — Run the assignment problem
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    KEYWORD    = "MONARCHY"
    CIPHERTEXT = "BXDREOGHBXLQZUMRVBXDREOGHBX"

    print("\n  Keyword    :", KEYWORD)
    print("  Ciphertext :", CIPHERTEXT, "\n")

    # ── Decrypt ──
    plaintext = playfair_decrypt(CIPHERTEXT, KEYWORD, verbose=True)

    # -- Round-trip verification --
    print("\n  -- ROUND-TRIP VERIFICATION --")
    re_enc = playfair_encrypt(plaintext, KEYWORD, verbose=False)
    # Original had an odd char; compare first 26 chars
    expected = CIPHERTEXT if len(CIPHERTEXT) % 2 == 0 else CIPHERTEXT[:-1]
    status = "PASS" if re_enc == expected else "MISMATCH"
    print(f"  Re-encrypted  : {re_enc}")
    print(f"  Expected      : {expected}")
    print(f"  Verification  : [{status}]\n")
