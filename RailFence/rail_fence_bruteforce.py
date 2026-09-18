"""
Task 4: Rail Fence Cryptanalysis (Brute-Force)
"""

def decrypt_rail_fence(ciphertext: str, rails: int) -> str:
    """Decrypts a Rail Fence encrypted string."""
    if rails == 1 or len(ciphertext) <= rails:
        return ciphertext

    matrix = [['\n' for _ in range(len(ciphertext))] for _ in range(rails)]
    
    current_rail = 0
    direction = 1
    
    for i in range(len(ciphertext)):
        matrix[current_rail][i] = '*'
        if current_rail == 0:
            direction = 1
        elif current_rail == rails - 1:
            direction = -1
        current_rail += direction
        
    index = 0
    for r in range(rails):
        for c in range(len(ciphertext)):
            if matrix[r][c] == '*' and index < len(ciphertext):
                matrix[r][c] = ciphertext[index]
                index += 1
                
    result = []
    current_rail = 0
    direction = 1
    
    for c in range(len(ciphertext)):
        result.append(matrix[current_rail][c])
        if current_rail == 0:
            direction = 1
        elif current_rail == rails - 1:
            direction = -1
        current_rail += direction
        
    return "".join(result)

def main():
    ciphertext = "TEITELHDVLSNHDTISEIIEA"
    
    print("=" * 60)
    print(" TASK 4: RAIL FENCE CRYPTANALYSIS (RAILS 2-6) ")
    print("=" * 60)
    print(f"Ciphertext : {ciphertext}")
    print("-" * 60)
    
    for rails in range(2, 7):
        candidate = decrypt_rail_fence(ciphertext, rails)
        print(f"Rails = {rails}: {candidate}")
        
    print("=" * 60)

if __name__ == "__main__":
    main()
