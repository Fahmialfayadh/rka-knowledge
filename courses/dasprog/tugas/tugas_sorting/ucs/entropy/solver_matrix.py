import os
import subprocess
import struct
import re
import sys

# --- KONFIGURASI ---
BINARY = "./entropy-discord"
LIB_OUTPUT = "hack.so"
FAKE_ENTROPY = "my_entropy"
TARGET_VAL = 0xCAFEBABE13371337

# --- FUNGSI BANTUAN ---
def run_binary(payload_bytes):
    # Padding 64 bytes agar aman
    with open(FAKE_ENTROPY, "wb") as f:
        f.write(payload_bytes + b'\x00' * 64)

    env = os.environ.copy()
    env["LD_PRELOAD"] = f"./{LIB_OUTPUT}"
    
    # Matikan ASLR
    cmd = ["setarch", "x86_64", "-R", BINARY]
    try:
        res = subprocess.run(cmd, env=env, capture_output=True, text=True)
    except FileNotFoundError:
        res = subprocess.run([BINARY], env=env, capture_output=True, text=True)
    
    # Ambil nilai "Got: 0x..." atau "Transformed value: 0x..."
    output = res.stdout + res.stderr
    match = re.search(r"(?:Got:|Transformed value:)\s+(0x[0-9a-fA-F]+)", output)
    if match:
        return int(match.group(1), 16)
    return None

def solve_linear_system(basis, target):
    # Gaussian Elimination over GF(2)
    # basis: list of integers (vektor basis)
    # target: integer
    
    n = len(basis) # Jumlah variabel (bit input yang kita probe)
    # Kita butuh mapping: basis_index -> pivot_bit
    pivots = {} 
    
    # Matrix state (untuk tracking solusi)
    # Kita simpan pasangan (value, mask_solusi)
    # mask_solusi mencatat bit input mana yang membentuk value ini
    matrix = []
    for i, val in enumerate(basis):
        matrix.append((val, 1 << i))
        
    # Eliminasi
    final_mask = 0
    current_target = target
    
    # Proses setiap bit output (64 bit)
    for bit in range(64):
        pivot_idx = -1
        
        # Cari baris yang memiliki bit ini set
        for i in range(len(matrix)):
            val, mask = matrix[i]
            if (val >> bit) & 1:
                pivot_idx = i
                break
        
        if pivot_idx != -1:
            # Kita temukan pivot untuk bit ini
            pivot_val, pivot_mask = matrix.pop(pivot_idx)
            
            # Eliminasi baris lain
            new_matrix = []
            for val, mask in matrix:
                if (val >> bit) & 1:
                    val ^= pivot_val
                    mask ^= pivot_mask
                new_matrix.append((val, mask))
            matrix = new_matrix
            
            # Cek apakah bit ini nyala di target kita?
            if (current_target >> bit) & 1:
                current_target ^= pivot_val
                final_mask ^= pivot_mask
                
    if current_target != 0:
        print("[-] Sistem tidak linear sempurna atau kurang basis vektor.")
        return None
        
    return final_mask

# --- MAIN SOLVER ---
def main():
    if not os.path.exists(LIB_OUTPUT):
        print("[!] hack.so belum ada. Menjalankan kompilasi...")
        os.system(f"gcc -shared -fPIC -ldl hack.c -o {LIB_OUTPUT}")

    print("[1] Probing BASE offset (Input Kosong)...")
    base_output = run_binary(b'\x00' * 16)
    if base_output is None:
        print("[X] Gagal menjalankan binary.")
        return
    print(f"    Base Output: {hex(base_output)}")
    
    # Target yang ingin dicapai setelah dikurangi offset dasar
    # Karena Asumsi: Output = (Linear_Comb(Input)) ^ Base
    # Maka: Linear_Comb(Input) = Target ^ Base
    needed_diff = TARGET_VAL ^ base_output
    print(f"    Needed Diff: {hex(needed_diff)}")
    
    print("[2] Probing 128 Bits (Ini memakan waktu ~10 detik)...")
    basis_vectors = []
    
    # Kita probe 128 bit (16 bytes)
    for i in range(128):
        # Buat payload dengan hanya 1 bit yang nyala
        # i // 8 = byte ke berapa
        # i % 8  = bit ke berapa di byte itu
        
        byte_idx = i // 8
        bit_idx = i % 8
        
        # Buat byte array kosong
        arr = bytearray(16)
        arr[byte_idx] = 1 << bit_idx
        
        res = run_binary(arr)
        
        # Vektor basis adalah: (Output Probe) XOR (Base Output)
        # Ini mengisolasi efek dari satu bit tersebut
        basis_vectors.append(res ^ base_output)
        
        # Progress bar sederhana
        if i % 16 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
            
    print("\n[3] Solving Linear System...")
    # Cari kombinasi bit input yang menghasilkan needed_diff
    solution_mask = solve_linear_system(basis_vectors, needed_diff)
    
    if solution_mask is None:
        print("[X] Gagal menemukan solusi linear. Transformasi mungkin hash satu arah.")
        return

    print(f"[+] Solusi ditemukan! Input Mask: {hex(solution_mask)}")
    
    # Konversi solusi (integer 128 bit) menjadi bytes
    final_payload = solution_mask.to_bytes(16, byteorder='little')
    
    print("[4] Mengirim Final Payload...")
    # Jalankan sekali lagi dengan payload yang sudah dihitung
    
    # Padding manual untuk run terakhir
    with open(FAKE_ENTROPY, "wb") as f:
        f.write(final_payload + b'\x00' * 64)

    env = os.environ.copy()
    env["LD_PRELOAD"] = f"./{LIB_OUTPUT}"
    cmd = ["setarch", "x86_64", "-R", BINARY]
    
    res = subprocess.run(cmd, env=env, capture_output=True, text=True)
    print("\n" + "="*30)
    print(res.stdout)
    print("="*30)
    
    if "PCTF{" in res.stdout:
        print("\n[!!!] CONGRATULATIONS! FLAG CAPTURED! [!!!]")

if __name__ == "__main__":
    main()