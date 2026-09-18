# Playfair Cipher — Manual Decryption

**Keyword:** `MONARCHY`  
**Ciphertext:** `BXDREOGHBXLQZUMRVBXDREOGHBX`

---

## Step 1 — 5×5 Key Matrix Construction

### 1a. Extract unique letters from keyword (in order)

```
MONARCHY → M O N A R C H Y   (all 8 letters are unique, no duplicates)
```

### 1b. List remaining alphabet (skip keyword letters; combine I/J into one cell)

Remaining letters after removing `{M, O, N, A, R, C, H, Y}` from the 26-letter alphabet (I/J share one cell):

```
B  D  E  F  G  I/J  K  L  P  Q  S  T  U  V  W  X  Z   (17 remaining)
```

### 1c. Fill the 5×5 grid — row by row

| Col→ | **0** | **1** | **2** | **3** | **4** |
|:----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| **Row 0** | **M** | **O** | **N** | **A** | **R** |
| **Row 1** | **C** | **H** | **Y** | **B** | **D** |
| **Row 2** | **E** | **F** | **G** | **I** | **K** |
| **Row 3** | **L** | **P** | **Q** | **S** | **T** |
| **Row 4** | **U** | **V** | **W** | **X** | **Z** |

> **Key positions quick-reference:**  
> M(0,0) O(0,1) N(0,2) A(0,3) R(0,4)  
> C(1,0) H(1,1) Y(1,2) B(1,3) D(1,4)  
> E(2,0) F(2,1) G(2,2) I(2,3) K(2,4)  
> L(3,0) P(3,1) Q(3,2) S(3,3) T(3,4)  
> U(4,0) V(4,1) W(4,2) X(4,3) Z(4,4)

---

## Step 2 — Playfair Decryption Rules

| Case | Rule |
|------|------|
| **Same row** | Replace each letter with the one immediately to its **LEFT** (wrap around) |
| **Same column** | Replace each letter with the one immediately **ABOVE** (wrap around) |
| **Rectangle** | Replace each letter with the letter in the **same row** but at the **other letter's column** |

---

## Step 3 — Split Ciphertext into Digraphs

```
Ciphertext:  B X D R E O G H B X L Q Z U M R V B X D R E O G H B X
                                                                    ↑
                                                  (27th char = trailing padding 'X')
```

| # | Digraph |
|:-:|:-------:|
| 1 | BX |
| 2 | DR |
| 3 | EO |
| 4 | GH |
| 5 | BX |
| 6 | LQ |
| 7 | ZU |
| 8 | MR |
| 9 | VB |
| 10 | XD |
| 11 | RE |
| 12 | OG |
| 13 | HB |
| — | X *(trailing padding — discarded)* |

---

## Step 4 — Decrypt Each Digraph

### Pair 1: **BX**

```
B → position (1, 3)
X → position (4, 3)
```
Same **column** (col 3) → shift each letter **UP** by one row:

```
B (row 1, col 3)  →  row 0, col 3  =  A
X (row 4, col 3)  →  row 3, col 3  =  S
```
✅ **BX → AS**

---

### Pair 2: **DR**

```
D → position (1, 4)
R → position (0, 4)
```
Same **column** (col 4) → shift each letter **UP** by one row:

```
D (row 1, col 4)  →  row 0, col 4  =  R
R (row 0, col 4)  →  row 4, col 4  =  Z  ← wraps from top to bottom
```
✅ **DR → RZ**

---

### Pair 3: **EO**

```
E → position (2, 0)
O → position (0, 1)
```
Different row AND different column → **Rectangle rule**:

```
E (row 2, col 0)  →  row 2, col of O (=1)  =  F
O (row 0, col 1)  →  row 0, col of E (=0)  =  M
```
✅ **EO → FM**

---

### Pair 4: **GH**

```
G → position (2, 2)
H → position (1, 1)
```
Different row AND different column → **Rectangle rule**:

```
G (row 2, col 2)  →  row 2, col of H (=1)  =  F
H (row 1, col 1)  →  row 1, col of G (=2)  =  Y
```
✅ **GH → FY**

---

### Pair 5: **BX**  *(identical to Pair 1)*

✅ **BX → AS**

---

### Pair 6: **LQ**

```
L → position (3, 0)
Q → position (3, 2)
```
Same **row** (row 3) → shift each letter **LEFT** by one column:

```
L (row 3, col 0)  →  row 3, col 4  =  T  ← wraps from left to right
Q (row 3, col 2)  →  row 3, col 1  =  P
```
✅ **LQ → TP**

---

### Pair 7: **ZU**

```
Z → position (4, 4)
U → position (4, 0)
```
Same **row** (row 4) → shift each letter **LEFT** by one column:

```
Z (row 4, col 4)  →  row 4, col 3  =  X
U (row 4, col 0)  →  row 4, col 4  =  Z  ← wraps from left to right
```
✅ **ZU → XZ**

---

### Pair 8: **MR**

```
M → position (0, 0)
R → position (0, 4)
```
Same **row** (row 0) → shift each letter **LEFT** by one column:

```
M (row 0, col 0)  →  row 0, col 4  =  R  ← wraps from left to right
R (row 0, col 4)  →  row 0, col 3  =  A
```
✅ **MR → RA**

---

### Pair 9: **VB**

```
V → position (4, 1)
B → position (1, 3)
```
Different row AND different column → **Rectangle rule**:

```
V (row 4, col 1)  →  row 4, col of B (=3)  =  X
B (row 1, col 3)  →  row 1, col of V (=1)  =  H
```
✅ **VB → XH**

---

### Pair 10: **XD**

```
X → position (4, 3)
D → position (1, 4)
```
Different row AND different column → **Rectangle rule**:

```
X (row 4, col 3)  →  row 4, col of D (=4)  =  Z
D (row 1, col 4)  →  row 1, col of X (=3)  =  B
```
✅ **XD → ZB**

---

### Pair 11: **RE**

```
R → position (0, 4)
E → position (2, 0)
```
Different row AND different column → **Rectangle rule**:

```
R (row 0, col 4)  →  row 0, col of E (=0)  =  M
E (row 2, col 0)  →  row 2, col of R (=4)  =  K
```
✅ **RE → MK**

---

### Pair 12: **OG**

```
O → position (0, 1)
G → position (2, 2)
```
Different row AND different column → **Rectangle rule**:

```
O (row 0, col 1)  →  row 0, col of G (=2)  =  N
G (row 2, col 2)  →  row 2, col of O (=1)  =  F
```
✅ **OG → NF**

---

### Pair 13: **HB**

```
H → position (1, 1)
B → position (1, 3)
```
Same **row** (row 1) → shift each letter **LEFT** by one column:

```
H (row 1, col 1)  →  row 1, col 0  =  C
B (row 1, col 3)  →  row 1, col 2  =  Y
```
✅ **HB → CY**

---

## Step 5 — Full Decryption Summary

| # | Cipher | Rule | Plaintext |
|:-:|:------:|:----:|:---------:|
| 1 | BX | Same Column ↑ | **AS** |
| 2 | DR | Same Column ↑ (wrap) | **RZ** |
| 3 | EO | Rectangle | **FM** |
| 4 | GH | Rectangle | **FY** |
| 5 | BX | Same Column ↑ | **AS** |
| 6 | LQ | Same Row ← (wrap) | **TP** |
| 7 | ZU | Same Row ← (wrap) | **XZ** |
| 8 | MR | Same Row ← (wrap) | **RA** |
| 9 | VB | Rectangle | **XH** |
| 10 | XD | Rectangle | **ZB** |
| 11 | RE | Rectangle | **MK** |
| 12 | OG | Rectangle | **NF** |
| 13 | HB | Same Row ← | **CY** |

### Final Plaintext

```
AS  RZ  FM  FY  AS  TP  XZ  RA  XH  ZB  MK  NF  CY
```

> **Concatenated:** `ASRZFMFYASTPXZRAXHZBMKNFCY`

> [!NOTE]
> The ciphertext has 27 characters (odd), which is atypical for Playfair since encryption always produces an even-length output. The trailing `X` is a null-padding character appended during encryption to bring the plaintext to an even length — it is discarded during decryption. The repeated substring `BXDREOGHBX` appears at positions 1–10 and 18–27 in the raw ciphertext, demonstrating the cipher's ability to diffuse repetitive plaintext patterns across pair boundaries.

---

## Rule Application Diagram (Visual Summary)

```
5×5 Key Matrix:
┌───┬───┬───┬───┬───┐
│ M │ O │ N │ A │ R │  ← Row 0
├───┼───┼───┼───┼───┤
│ C │ H │ Y │ B │ D │  ← Row 1
├───┼───┼───┼───┼───┤
│ E │ F │ G │ I │ K │  ← Row 2
├───┼───┼───┼───┼───┤
│ L │ P │ Q │ S │ T │  ← Row 3
├───┼───┼───┼───┼───┤
│ U │ V │ W │ X │ Z │  ← Row 4
└───┴───┴───┴───┴───┘
  0   1   2   3   4   ← Col

SAME ROW  → shift LEFT  (decrypt)
SAME COL  → shift UP    (decrypt)
RECTANGLE → swap columns (same for encrypt & decrypt)
```
