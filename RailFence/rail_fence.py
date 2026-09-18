"""
Task 3: Rail Fence Cipher (Encryption & Decryption)
"""

def encrypt_rail_fence(text: str, rails: int) -> str:
    """
    Encrypts a string using the Rail Fence cipher with n rails.
    Handles all characters including spaces and punctuation.
    """
    if rails == 1 or len(text) <= rails:
        return text

    # Create empty strings for each rail
    fence = ["" for _ in range(rails)]
    
    current_rail = 0
    direction = 1 # 1 for moving down, -1 for moving up

    # Traverse the text and place each character on the correct rail
    for char in text:
        fence[current_rail] += char
        
        # Change direction if we hit the top or bottom rail
        if current_rail == 0:
            direction = 1
        elif current_rail == rails - 1:
            direction = -1
            
        current_rail += direction

    # Join all rails to form the final ciphertext
    return "".join(fence)


def decrypt_rail_fence(ciphertext: str, rails: int) -> str:
    """
    Decrypts a Rail Fence encrypted string.
    """
    if rails == 1 or len(ciphertext) <= rails:
        return ciphertext

    # Create a matrix to mark where characters belong
    matrix = [['\n' for _ in range(len(ciphertext))] for _ in range(rails)]
    
    # First, mark the zig-zag path with a placeholder '*'
    current_rail = 0
    direction = 1
    
    for i in range(len(ciphertext)):
        matrix[current_rail][i] = '*'
        
        if current_rail == 0:
            direction = 1
        elif current_rail == rails - 1:
            direction = -1
            
        current_rail += direction
        
    # Now, fill the marked places with actual ciphertext characters row by row
    index = 0
    for r in range(rails):
        for c in range(len(ciphertext)):
            if matrix[r][c] == '*' and index < len(ciphertext):
                matrix[r][c] = ciphertext[index]
                index += 1
                
    # Finally, read the matrix in the zig-zag pattern to reconstruct the plaintext
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
    print("=" * 50)
    print(" RAIL FENCE CIPHER UTILITY ")
    print("=" * 50)
    
    # Test Case 1: Encryption & Decryption validation
    test_plain = "WEAREDISCOVEREDFLEEATONCE"
    test_rails = 3
    expected_cipher = "WECRLTEERDSOEEFEAOCAIVDEN"
    
    print(f"\n[Test Case 1: Basic String]")
    print(f"Plaintext:  {test_plain}")
    print(f"Rails:      {test_rails}")
    
    encrypted = encrypt_rail_fence(test_plain, test_rails)
    print(f"Encrypted:  {encrypted}")
    print(f"Expected:   {expected_cipher}")
    print(f"Status:     {'[PASS]' if encrypted == expected_cipher else '[FAIL]'}")
    
    decrypted = decrypt_rail_fence(encrypted, test_rails)
    print(f"Decrypted:  {decrypted}")
    print(f"Status:     {'[PASS]' if decrypted == test_plain else '[FAIL]'}")
    
    # Test Case 2: Decrypting 'HLOOLELWRD'
    print(f"\n[Test Case 2: Decrypting specific string]")
    test_cipher_2 = "HLOOLELWRD"
    
    # As requested by the prompt
    test_rails_2_requested = 3
    print(f"Ciphertext: {test_cipher_2}")
    print(f"Rails:      {test_rails_2_requested} (As requested in prompt)")
    decrypted_2_req = decrypt_rail_fence(test_cipher_2, test_rails_2_requested)
    print(f"Decrypted:  {decrypted_2_req}")
    
    # The mathematically correct number of rails to get "HELLOWORLD"
    test_rails_2_actual = 2
    print(f"\nRails:      {test_rails_2_actual} (Actual required rails for HELLOWORLD)")
    decrypted_2_act = decrypt_rail_fence(test_cipher_2, test_rails_2_actual)
    print(f"Decrypted:  {decrypted_2_act}")
    
    # Test Case 3: Edge cases (Spaces, Punctuation, Case Sensitivity)
    print(f"\n[Test Case 3: Edge Cases (Spaces, Punctuation)]")
    edge_case_plain = "Hello, World! (Rail Fence)"
    edge_rails = 4
    
    print(f"Plaintext:  {edge_case_plain}")
    edge_encrypted = encrypt_rail_fence(edge_case_plain, edge_rails)
    print(f"Encrypted:  {edge_encrypted}")
    edge_decrypted = decrypt_rail_fence(edge_encrypted, edge_rails)
    print(f"Decrypted:  {edge_decrypted}")
    print(f"Status:     {'[PASS]' if edge_decrypted == edge_case_plain else '[FAIL]'}")
    print("=" * 50)

if __name__ == "__main__":
    main()
