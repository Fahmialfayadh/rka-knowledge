#!/usr/bin/env python3
import os

print("[DEBUG] solver.py is executing")

# ================== GF(2) Linear Solver ==================

def solve_gf2_linear(matrix, target):
    """
    Solve matrix * x = target over GF(2).
    matrix: list of m rows, each row is list of n bits (0/1)
    target: list of m bits
    Returns: list of n bits (solution) or None if no solution.
    """
    m = len(matrix)
    if m == 0:
        return []

    n = len(matrix[0])
    # Build augmented matrix [A | b]
    aug = [matrix[i][:] + [target[i]] for i in range(m)]

    row = 0
    for col in range(n):
        # Find pivot
        pivot = None
        for r in range(row, m):
            if aug[r][col] == 1:
                pivot = r
                break
        if pivot is None:
            continue

        # Swap pivot row to current row
        aug[row], aug[pivot] = aug[pivot], aug[row]

        # Eliminate this column in all other rows
        for r in range(m):
            if r != row and aug[r][col] == 1:
                for c in range(col, n + 1):
                    aug[r][c] ^= aug[row][c]

        row += 1
        if row == m:
            break

    # Check inconsistency: 0 ... 0 | 1
    for r in range(row, m):
        if all(aug[r][c] == 0 for c in range(n)) and aug[r][n] == 1:
            return None

    # Back substitution: build one particular solution (free vars = 0)
    sol = [0] * n
    for r in range(row):
        pivot_col = None
        for c in range(n):
            if aug[r][c] == 1:
                pivot_col = c
                break
        if pivot_col is not None:
            sol[pivot_col] = aug[r][n]

    return sol


# ================== PRG Transition ==================

def next_state(state, A, B):
    """
    Compute next_state = A * state XOR B over GF(2).
    state: 32-bit int
    A: 32x32 matrix of bits (list of 32 lists of 32 bits)
    B: 32-bit int
    """
    new_state = 0
    for i in range(32):
        bit = 0
        # dot product of row i with input bits
        for j in range(32):
            bit ^= A[i][j] & ((state >> j) & 1)
        new_state |= (bit << i)

    new_state ^= B
    return new_state & 0xFFFFFFFF


# ================== Reconstruction & Decryption ==================

def load_states(path):
    if not os.path.exists(path):
        print(f"[ERROR] {path} not found")
        return None
    states = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # int(x, 0) supports decimal or 0x-prefixed
            states.append(int(line, 0))
    return states


def reconstruct_A_B(states):
    """
    Reconstruct A (32x32) and B (32-bit) from leaked states.
    We solve 32 independent systems (one per output bit).
    """
    n_trans = len(states) - 1
    if n_trans < 33:
        print("[ERROR] Not enough transitions to solve for each bit (need >= 33)")
        return None, None

    print(f"[DEBUG] Using {n_trans} transitions for reconstruction")

    A = []
    B_bits = []

    # For each output bit i, solve:
    #  sum_j A[i][j] * in_bit_j  XOR B[i] = out_bit_i
    for bit_idx in range(32):
        eqs = []
        tgs = []
        for k in range(n_trans):
            s_in = states[k]
            s_out = states[k + 1]

            # Build one equation row: 32 bits for A[i][:], + 1 bit for B[i]
            row = []
            for j in range(32):
                row.append((s_in >> j) & 1)
            row.append(1)  # coefficient for B[i]

            out_bit = (s_out >> bit_idx) & 1
            eqs.append(row)
            tgs.append(out_bit)

        sol = solve_gf2_linear(eqs, tgs)
        if sol is None:
            print(f"[ERROR] No solution for output bit {bit_idx}")
            return None, None

        row_A = sol[:32]
        B_i = sol[32]
        A.append(row_A)
        B_bits.append(B_i)

    # Pack B bits into int
    B = 0
    for i in range(32):
        if B_bits[i] & 1:
            B |= (1 << i)

    return A, B


def verify_transitions(states, A, B, limit=None):
    """
    Verify that next_state(states[i]) == states[i+1] for all i.
    """
    if limit is None or limit > len(states) - 1:
        limit = len(states) - 1

    ok = True
    for i in range(limit):
        calc = next_state(states[i], A, B)
        if calc != states[i + 1]:
            print(f"[ERROR] Mismatch at index {i}: expected {hex(states[i+1])}, got {hex(calc)}")
            ok = False
    if ok:
        print("[DEBUG] All transitions verified OK (first", limit, ")")
    return ok


def load_cipher(path):
    if not os.path.exists(path):
        print(f"[ERROR] {path} not found")
        return None
    with open(path, "rb") as f:
        return f.read()


def gen_keystream(A, B, start_state, n_bytes, mode="post", offset=0):
    """
    Generate keystream bytes from PRG.
    mode = "pre"  -> keystream_byte = state & 0xFF, lalu state = next_state(...)
    mode = "post" -> state = next_state(...), lalu keystream_byte = state & 0xFF
    offset: buang beberapa langkah awal dulu.
    """
    s = start_state & 0xFFFFFFFF

    # burn some steps if offset > 0
    for _ in range(offset):
        if mode == "pre":
            # burn but don't use output
            s = next_state(s, A, B)
        else:
            s = next_state(s, A, B)

    ks = []
    for _ in range(n_bytes):
        if mode == "pre":
            ks.append(s & 0xFF)
            s = next_state(s, A, B)
        else:  # post
            s = next_state(s, A, B)
            ks.append(s & 0xFF)
    return bytes(ks)


def score_plaintext(pt: bytes):
    """
    Simple heuristic scoring: fraction of bytes that are printable ASCII.
    """
    if not pt:
        return 0.0
    printable = 0
    for b in pt:
        if 32 <= b <= 126 or b in (9, 10, 13):  # basic text
            printable += 1
    return printable / len(pt)


def main():
    print("[DEBUG] Enter main()")

    # ---------- Load leak ----------
    leak_path = "keystream_leak.txt"
    states = load_states(leak_path)
    if states is None or len(states) < 2:
        print("[ERROR] Failed to load enough states")
        return

    print(f"[DEBUG] Loaded {len(states)} states from {leak_path}")

    # ---------- Reconstruct A and B ----------
    A, B = reconstruct_A_B(states)
    if A is None:
        print("[ERROR] Reconstruction failed")
        return

    print("[DEBUG] Reconstruction done")
    print("[DEBUG] B =", hex(B))

    # Verify transitions (just to be sure)
    verify_transitions(states, A, B)

    # ---------- Load cipher ----------
    cipher_path = "cipher.txt"
    ct = load_cipher(cipher_path)
    if ct is None:
        print("[ERROR] Failed to load cipher")
        return

    print(f"[DEBUG] Cipher length: {len(ct)} bytes")

    # ---------- Try different hypotheses for keystream ----------
    best_candidates = []

    modes = ["pre", "post"]
    max_offset = 4  # burn up to 4 steps
    max_start_idx = len(states)  # try starting from any leaked state

    for mode in modes:
        for offset in range(max_offset + 1):
            for si, start_state in enumerate(states):
                ks = gen_keystream(A, B, start_state, len(ct), mode=mode, offset=offset)
                pt = bytes(c ^ k for c, k in zip(ct, ks))
                sc = score_plaintext(pt)

                best_candidates.append((sc, mode, offset, si, pt))

    # Sort by score descending
    best_candidates.sort(key=lambda x: x[0], reverse=True)

    print("\n[RESULT] Top candidates (by printable score):")
    for idx, (sc, mode, offset, si, pt) in enumerate(best_candidates[:5]):
        print("=" * 60)
        print(f"[Candidate {idx}] score={sc:.3f}, mode={mode}, offset={offset}, start_state_index={si}")
        # Print first 200 bytes as text preview
        try:
            preview = pt[:200].decode("utf-8", errors="replace")
        except Exception:
            preview = str(pt[:200])
        print(preview)

    # Also, if any contains 'flag' or 'CTF{' etc, highlight
    print("\n[RESULT] Candidates containing 'flag' or 'CTF{' (if any):")
    for sc, mode, offset, si, pt in best_candidates:
        low = pt.lower()
        if b"flag" in low or b"ctf{" in low or b"flag{" in low:
            print("=" * 60)
            print(f"[FLAG-LIKE] score={sc:.3f}, mode={mode}, offset={offset}, start_state_index={si}")
            try:
                txt = pt.decode("utf-8", errors="replace")
            except Exception:
                txt = str(pt)
            print(txt)
            break  # print first match only

if __name__ == "__main__":
    main()
