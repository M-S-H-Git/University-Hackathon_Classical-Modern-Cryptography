# University Hackathon: Classical and Modern Cryptography

Solutions for a university cryptography hackathon covering classical ciphers, RSA implementation, cryptanalysis, and a multi-layer capture-the-flag puzzle.

## Topics

- Playfair cipher: manual decryption and cryptanalysis analysis
- Rail Fence cipher: encryption, decryption, and bounded brute-force analysis
- RSA: key generation, text encryption, decryption, digital signatures, and weak-key attacks
- Hybrid cryptosystem: RSA key exchange combined with Playfair messaging
- CTF puzzle: Rail Fence, Playfair, and Caesar decryption pipeline

## Requirements

- Python 3.8 or newer
- `pycryptodome`

Install the dependency:

```bash
python -m pip install pycryptodome
```

## Project Structure

```text
.
|-- Playfair/
|   |-- playfair.py
|   |-- playfair_bruteforce.py
|   `-- playfair_decryption.md
|-- RailFence/
|   |-- rail_fence.py
|   `-- rail_fence_bruteforce.py
|-- RSA/
|   |-- rsa_tool.py
|   |-- break_weak_rsa.py
|   |-- rsa_manual_steps.md
|   |-- rsa_security_analysis.md
|   `-- RSA_Security_Analysis.docx
|-- Bonus_Challenge/
|   |-- hybrid_cryptosystem.py
|   `-- ctf_challenge3.py
|-- University Hackathon_Classical & Modern Cryptography_Report.pdf
`-- README.md
```

## Run The Solutions

Run commands from the project root:

```bash
python Playfair/playfair.py
python Playfair/playfair_bruteforce.py
python RailFence/rail_fence.py
python RailFence/rail_fence_bruteforce.py
python RSA/rsa_tool.py
python RSA/break_weak_rsa.py
python Bonus_Challenge/hybrid_cryptosystem.py
python Bonus_Challenge/ctf_challenge3.py
```

## Solution Summary

### Playfair

`playfair.py` constructs the 5x5 key matrix for `MONARCHY`, decrypts the supplied ciphertext, and demonstrates the Playfair rules. `playfair_bruteforce.py` analyzes the second challenge and identifies that its ciphertext has Caesar-shift characteristics rather than being valid standard Playfair ciphertext.

### Rail Fence

`rail_fence.py` supports encryption and decryption with a user-selected rail count while preserving spaces, punctuation, and case. `rail_fence_bruteforce.py` tests rails 2 through 6 against the supplied ciphertext and identifies:

```text
Plaintext: THEDEVILISINTHEDETAILS
Rails: 3
```

### RSA

`rsa_tool.py` generates two random 512-bit primes, computes the public and private keys, encrypts and decrypts UTF-8 text, reports key-generation time, and demonstrates a digital signature. The implementation is educational and uses textbook RSA arithmetic; it is not suitable for protecting real messages because it does not implement OAEP or a standardized signature scheme.

`break_weak_rsa.py` demonstrates factoring small RSA moduli using trial division, Fermat factorization, and Pollard's Rho, then recovers the corresponding private keys and plaintexts.

### Bonus Challenges

`hybrid_cryptosystem.py` demonstrates RSA key exchange followed by Playfair message exchange between Alice and Bob. `ctf_challenge3.py` automates the three-layer CTF decryption pipeline:

1. Rail Fence decryption with 4 rails
2. Playfair decryption using the key `SECURITY`
3. Caesar shift reversal

## Security Notes

These scripts are designed for learning and experimentation. They intentionally demonstrate insecure or obsolete constructions, including Playfair, textbook RSA, and RSA with small educational keys. For production systems, use authenticated modern cryptography such as AES-GCM or ChaCha20-Poly1305 for message encryption and RSA-OAEP or an established modern key-exchange protocol where RSA is required. Do not use the sample implementations to protect sensitive data.

## Report

The complete assignment solutions, manual calculations, security analysis, diagrams, and references are available in [University Hackathon_Classical & Modern Cryptography_Report.pdf](University%20Hackathon_Classical%20%26%20Modern%20Cryptography_Report.pdf).

## Author

Muhammed Salah Hussain  
GitHub: [M-S-H-Git](https://github.com/M-S-H-Git)
