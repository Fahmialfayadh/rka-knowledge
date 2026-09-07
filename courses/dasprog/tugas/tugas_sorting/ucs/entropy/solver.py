import os
import subprocess
import struct

# Konfigurasi
BINARY = "./entropy-discord"
LIB_NAME = "hack.so"
ENTROPY_FILE = "my_entropy"
STATUS_FILE = "fake_status"

def setup():
    print("[+] Compiling hook library...")
    # Kompilasi shared library
    os.system(f"gcc -shared -fPIC -ldl hack.c -o {LIB_NAME}")
    
    # Buat fake status agar TracerPid terlihat 0 (bersih dari debugger)
    with open(STATUS_FILE, "w") as f:
        f.write("Name:\tentropy\nState:\tR (running)\nTracerPid:\t0\n")

def get_expected_value():
    print("[+] Running binary to trigger leak...")
    # Buat dummy entropy dulu (misal 8 bytes kosong)
    with open(ENTROPY_FILE, "wb") as f:
        f.write(b'\x00' * 16)

    # Jalankan dengan LD_PRELOAD
    env = os.environ.copy()
    env["LD_PRELOAD"] = f"./{LIB_NAME}"
    
    try:
        # Kita tangkap output stderr/stdout karena program akan panic
        result = subprocess.run([BINARY], env=env, capture_output=True, text=True)
        output = result.stderr + result.stdout
        
        # Cari pesan "Expected: 0x..." 
        if "Expected:" in output:
            import re
            # Regex untuk menangkap angka hex setelah "Expected:"
            match = re.search(r"Expected:\s+(0x[0-9a-fA-F]+)", output)
            if match:
                val_hex = match.group(1)
                print(f"[!] Found expected value: {val_hex}")
                return int(val_hex, 16)
    except Exception as e:
        print(f"[-] Error running binary: {e}")
    return None

def solve(target_int):
    # CATATAN: Anda harus menyesuaikan logika ini.
    # Jika program melakukan XOR sederhana, target_int mungkin adalah input yang benar.
    # Jika ada transformasi matematika, Anda harus membalik (inverse) rumusnya di sini.
    
    print(f"[+] Generating payload for target: {hex(target_int)}")
    
    # Contoh: Asumsi input harus berupa raw bytes dari target integer (Little Endian)
    # Sesuaikan 'Q' (unsigned long long 64-bit) atau 'I' (unsigned int 32-bit)
    payload = struct.pack("<Q", target_int) 
    
    with open(ENTROPY_FILE, "wb") as f:
        f.write(payload)
        
    print("[+] Payload written. Re-running to capture flag...")
    env = os.environ.copy()
    env["LD_PRELOAD"] = f"./{LIB_NAME}"
    subprocess.run([BINARY], env=env)

if __name__ == "__main__":
    setup()
    target = get_expected_value()
    if target:
        solve(target)
    else:
        print("[-] Failed to find expected value. Check manual output.")