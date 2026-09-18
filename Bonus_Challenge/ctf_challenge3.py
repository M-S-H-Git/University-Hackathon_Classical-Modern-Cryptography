"""
Challenge 3: Capture The Flag - Crypto Puzzle Solver
======================================================
Given ciphertext: "TIEHSRSCAEHTSIHTSI"

The puzzle layers describe decryption steps in order:
  Layer 1: Rail Fence (4 rails)   - decrypt first
  Layer 2: Playfair (SECURITY)    - decrypt second
  Layer 3: Caesar Shift +5        - undo third (shift -5)
"""

# ──────────────────────────────────────────────────────────────
#  Layer 1: Rail Fence Cipher
# ──────────────────────────────────────────────────────────────

def rail_fence_decrypt(ciphertext: str, rails: int) -> str:
    """Decrypt a Rail Fence ciphertext using the matrix fill-and-read method."""
    n = len(ciphertext)
    if rails == 1 or n <= rails:
        return ciphertext

    # Mark which rail each position belongs to
    matrix = [[None] * n for _ in range(rails)]
    rail, direction = 0, 1
    for i in range(n):
        matrix[rail][i] = True
        if rail == 0:          direction = 1
        elif rail == rails-1:  direction = -1
        rail += direction

    # Fill rails with ciphertext characters row by row
    idx = 0
    for r in range(rails):
        for c in range(n):
            if matrix[r][c] is True:
                matrix[r][c] = ciphertext[idx]
                idx += 1

    # Read off in zig-zag order
    result = []
    rail, direction = 0, 1
    for c in range(n):
        result.append(matrix[rail][c])
        if rail == 0:          direction = 1
        elif rail == rails-1:  direction = -1
        rail += direction

    return "".join(result)


# ──────────────────────────────────────────────────────────────
#  Layer 2: Playfair Cipher
# ──────────────────────────────────────────────────────────────

def build_playfair_matrix(keyword: str) -> list:
    """Build a 5x5 Playfair matrix (I/J combined)."""
    keyword = keyword.upper().replace("J", "I")
    seen, order = set(), []
    for ch in keyword:
        if ch.isalpha() and ch not in seen:
            seen.add(ch); order.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.add(ch); order.append(ch)
    return [order[i*5: i*5+5] for i in range(5)]


def build_pos(matrix: list) -> dict:
    return {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}


def playfair_decrypt(ciphertext: str, keyword: str) -> tuple:
    """
    Decrypt a Playfair ciphertext.
    Returns (plaintext, list of (pair, rule, result)) for display.
    """
    matrix = build_playfair_matrix(keyword)
    pos    = build_pos(matrix)

    ct = ciphertext.upper().replace("J", "I").replace(" ", "")
    if len(ct) % 2 != 0:
        ct = ct[:-1]

    pairs = [ct[i:i+2] for i in range(0, len(ct), 2)]
    result = []
    trace  = []

    for pair in pairs:
        a, b = pair[0], pair[1]
        r1, c1 = pos[a]
        r2, c2 = pos[b]

        if r1 == r2:
            rule = "Same Row  -> shift LEFT"
            pa = matrix[r1][(c1-1) % 5]
            pb = matrix[r2][(c2-1) % 5]
        elif c1 == c2:
            rule = "Same Col  -> shift UP"
            pa = matrix[(r1-1) % 5][c1]
            pb = matrix[(r2-1) % 5][c2]
        else:
            rule = "Rectangle -> swap cols"
            pa = matrix[r1][c2]
            pb = matrix[r2][c1]

        result += [pa, pb]
        trace.append((pair, rule, pa+pb))

    return "".join(result), trace


# ──────────────────────────────────────────────────────────────
#  Layer 3: Caesar Cipher
# ──────────────────────────────────────────────────────────────

def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt Caesar cipher by reversing the shift."""
    result = []
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            result.append(chr((ord(ch) - base - shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


# ──────────────────────────────────────────────────────────────
#  Display helpers
# ──────────────────────────────────────────────────────────────

def banner(title: str):
    print("\n" + "=" * 62)
    print("  " + title)
    print("=" * 62)

def step_header(n: int, title: str):
    print(f"\n  [LAYER {n}] {title}")
    print("  " + "-" * 55)

def show(label: str, value: str):
    print(f"  {label:<28} {value}")


# ──────────────────────────────────────────────────────────────
#  Main Solver
# ──────────────────────────────────────────────────────────────

def solve():
    CT          = "TIEHSRSCAEHTSIHTSI"
    RAILS       = 4
    PF_KEYWORD  = "SECURITY"
    CAESAR_SHIFT = 5

    banner("CTF CHALLENGE 3 - AUTOMATED DECRYPTION SOLVER")
    show("Given Ciphertext :", CT)
    show("Length           :", str(len(CT)))
    print()
    print("  Decryption pipeline:")
    print("  [1] Rail Fence decrypt (4 rails)")
    print("  [2] Playfair decrypt   (key: SECURITY)")
    print("  [3] Caesar undo        (shift -5)")

    # ──────────────────────────────────────────────
    #  LAYER 1: Rail Fence Decrypt
    # ──────────────────────────────────────────────
    step_header(1, "Rail Fence Decrypt (4 rails)")

    # Show zig-zag positions
    n = len(CT)
    rail_positions = [[] for _ in range(RAILS)]
    rail, direction = 0, 1
    for i in range(n):
        rail_positions[rail].append(i)
        if rail == 0:          direction = 1
        elif rail == RAILS-1:  direction = -1
        rail += direction

    print("  Zig-zag rail assignments:")
    idx = 0
    for r in range(RAILS):
        chars = CT[idx: idx + len(rail_positions[r])]
        print(f"    Rail {r} | positions {str(rail_positions[r]):<30} | chars: {chars}")
        idx += len(rail_positions[r])

    layer1 = rail_fence_decrypt(CT, RAILS)

    # Visualize zig-zag with the decrypted result
    print()
    print("  Reading back in zig-zag order:")
    fence = [['.' for _ in range(n)] for _ in range(RAILS)]
    rail, direction = 0, 1
    for i, ch in enumerate(layer1):
        fence[rail][i] = ch
        if rail == 0:          direction = 1
        elif rail == RAILS-1:  direction = -1
        rail += direction
    for r in range(RAILS):
        print(f"    Rail {r}: " + " ".join(fence[r]))

    show("\n  Layer 1 Result :", layer1)

    # ──────────────────────────────────────────────
    #  LAYER 2: Playfair Decrypt
    # ──────────────────────────────────────────────
    step_header(2, "Playfair Decrypt (key: SECURITY)")

    matrix = build_playfair_matrix(PF_KEYWORD)
    print("  5x5 Key Matrix:")
    print()
    print("       " + "   ".join([f"C{i}" for i in range(5)]))
    for r, row in enumerate(matrix):
        print(f"  R{r} | " + "  ".join(row) + " |")
    print()

    layer2, trace = playfair_decrypt(layer1, PF_KEYWORD)

    print(f"  {'Pair':<6} {'Rule':<28} {'Decrypted'}")
    print("  " + "-" * 45)
    for pair, rule, dec in trace:
        print(f"  {pair:<6} {rule:<28} {dec}")

    show("\n  Layer 2 Result :", layer2)

    # ──────────────────────────────────────────────
    #  LAYER 3: Caesar Decrypt
    # ──────────────────────────────────────────────
    step_header(3, "Caesar Undo (shift -5)")
    print("  The cipher applied +5 shift; we reverse with -5.")
    print()

    cipher_row = "  Cipher: " + " ".join(layer2)
    print(cipher_row)
    layer3 = caesar_decrypt(layer2, CAESAR_SHIFT)
    plain_row  = "  Plain:  " + " ".join(layer3)
    print(plain_row)

    show("\n  Layer 3 Result :", layer3)

    # ──────────────────────────────────────────────
    #  FINAL FLAG
    # ──────────────────────────────────────────────
    banner("FINAL SOLUTION")

    flag = f"FLAG{{{layer3}}}"

    print()
    print(f"  {'Layer':<8} {'Operation':<32} {'Output'}")
    print("  " + "-" * 62)
    print(f"  {'Start':<8} {'Given ciphertext':<32} {CT}")
    print(f"  {'L1':<8} {'Rail Fence decrypt (4 rails)':<32} {layer1}")
    print(f"  {'L2':<8} {'Playfair decrypt (SECURITY)':<32} {layer2}")
    print(f"  {'L3':<8} {'Caesar undo (-5)':<32} {layer3}")
    print()
    print("  " + "*" * 52)
    print(f"  **  {flag}")
    print("  " + "*" * 52)
    print()


if __name__ == "__main__":
    solve()
