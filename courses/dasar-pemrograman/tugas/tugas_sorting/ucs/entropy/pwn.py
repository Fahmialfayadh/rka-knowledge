import os
import subprocess
import struct
import re
import sys

BINARY = "./entropy-discord"
LIB_OUTPUT = "hack.so"
FAKE_ENTROPY = "my_entropy"
FAKE_STATUS = "fake_status"
TARGET_VAL = 0xCAFEBABE13371337

def run_binary(payload_bytes):
    # Tulis payload ke file entropy
    # Padding 128 bytes agar tidak EOF
    with open(FAKE_ENTROPY, "wb") as f:
        f.write(payload_bytes + b'\x00' * 128)

    env = os.environ.copy()
    env["LD_PRELOAD"] = f"./{LIB_OUTPUT}"
    
    # Matikan ASLR dengan setarch
    cmd = ["setarch", "x86_64", "-R", BINARY]
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    except FileNotFoundError:
        result = subprocess.run([BINARY], env=env, capture_output=True, text=True)
        
    return result.stdout + result.stderr

def solve():
    print("[1] Compiling hook (if needed)...")
    os.system(f"gcc -shared -fPIC -ldl hack.c -o {LIB_OUTPUT}")
    
    # Tahap 1: Kirim 16 Bytes NOL
    # Byte 0-7 (Input) = 0, Byte 8-15 (Salt) = 0
    print("[2] Phase 1: Sending ZERO payload to probe transformation...")
    zero_payload = b'\x00' * 16
    output1 = run_binary(zero_payload)
    
    match = re.search(r"Got:\s+(0x[0-9a-fA-F]+)", output1)
    if not match:
        print("[X] Failed to get probe output. Log:\n", output1)
        sys.exit(1)
        
    base_output = int(match.group(1), 16)
    print(f"[!] Probe Result (Base Output): {hex(base_output)}")
    
    # Tahap 2: Hitung Salt yang dibutuhkan
    # Salt = Target ^ Base_Output
    needed_salt = TARGET_VAL ^ base_output
    print(f"[3] Calculated Magic Salt: {hex(needed_salt)}")
    
    # Tahap 3: Serangan Final
    # Input tetap 0 (agar FungsiRumit(0) konsisten)
    # Salt diisi dengan needed_salt
    final_input = b'\x00' * 8  # Input tetap 0
    final_salt = struct.pack("<Q", needed_salt) # Salt manipulasi
    
    final_payload = final_input + final_salt
    
    print("[4] Phase 2: Sending Payload + Magic Salt...")
    output2 = run_binary(final_payload)
    
    print("\n" + "="*30)
    print(output2)
    print("="*30)
    
    if "PCTF{" in output2:
        print("[+] FLAG CAPTURED!")
    else:
        print("[-] Failed. Try checking if endianness is reversed?")

if __name__ == "__main__":
    solve()