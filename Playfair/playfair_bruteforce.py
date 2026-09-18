"""
Task 2: Playfair Brute-Force Cryptanalysis
"""
import itertools

def build_matrix(keyword):
    """Builds a standard 5x5 Playfair matrix with I/J combined."""
    keyword = keyword.upper().replace("J", "I")
    seen = set()
    order = []
    
    # Add unique letters from keyword
    for ch in keyword:
        if ch not in seen and ch.isalpha():
            seen.add(ch)
            order.append(ch)
            
    # Add remaining alphabet
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.add(ch)
            order.append(ch)
            
    # Reshape to 5x5
    return [order[i*5 : i*5+5] for i in range(5)]

def build_position_map(matrix):
    """Maps letter -> (row, col)."""
    pos = {}
    for r in range(5):
        for c in range(5):
            pos[matrix[r][c]] = (r, c)
    return pos

def apply_rule(a, b, matrix, pos):
    """Applies Playfair decryption rules (Same Row -> Left, Same Col -> Up, Rectangle)."""
    r1, c1 = pos[a]
    r2, c2 = pos[b]

    if r1 == r2:                        
        return matrix[r1][(c1 - 1) % 5], matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:                      
        return matrix[(r1 - 1) % 5][c1], matrix[(r2 - 1) % 5][c2]
    else:                               
        return matrix[r1][c2], matrix[r2][c1]

def playfair_decrypt(ciphertext, keyword):
    """Decrypts ciphertext using a given keyword."""
    matrix = build_matrix(keyword)
    pos = build_position_map(matrix)
    
    ct = ciphertext.upper().replace(" ", "").replace("J", "I")
    if len(ct) % 2 != 0:
        ct = ct[:-1] # discard padding if odd
        
    pairs = [ct[i:i+2] for i in range(0, len(ct), 2)]
    
    plaintext = []
    for pair in pairs:
        a, b = pair[0], pair[1]
        
        # If double letters bypass standard Playfair insertion
        if a == b:
            plaintext.append(a + b)
        else:
            pa, pb = apply_rule(a, b, matrix, pos)
            plaintext.append(pa + pb)
            
    return "".join(plaintext)


def main():
    ciphertext = "QEBZFSFDBUJPODMBTTJGZDBOTPMWFCZDPNQVUJOH"
    
    # Common 6-letter security words
    security_keywords = [
        "SECURE", "SAFETY", "SHIELD", "SECRET", "CIPHER", 
        "HACKER", "ENIGMA", "DEFEND", "PATROL", "GUARDS", 
        "CASTLE", "ACCESS", "SYSTEM", "ATTACK", "THREAT", 
        "BREACH", "CYBERA", "CRYPTO", "ALARMS", "ROUTER", 
        "SERVER", "POLICY", "BACKUP", "CENSOR", "DEFENC"
    ]
    
    print(f"[*] Starting Brute-Force Cryptanalysis")
    print(f"[*] Ciphertext: {ciphertext}")
    print(f"[*] Testing {len(security_keywords)} security-related keywords...\n")
    
    found = False
    for word in security_keywords:
        decrypted = playfair_decrypt(ciphertext, word)
        
        if "CRYPTOGRAPHY" in decrypted:
            print(f"[+] SUCCESS! Keyword found: {word}")
            print(f"[+] Decrypted Text: {decrypted}")
            found = True
            break
            
    if not found:
        print("[-] Keyword not found in basic list. Script logic complete.")
        print("\nNote: Please refer to the cryptanalysis writeup for a deeper")
        print("analysis of the provided ciphertext's mathematical properties.")

if __name__ == "__main__":
    main()
