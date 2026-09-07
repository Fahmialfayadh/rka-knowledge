# Data extracted from challenge.c
TARGET = [
    0x5A, 0x3D, 0x5B, 0x9C, 0x98, 0x73, 0xAE, 0x32, 0x25, 0x47,
    0x48, 0x51, 0x6C, 0x71, 0x3A, 0x62, 0xB8, 0x7B, 0x63, 0x57,
    0x25, 0x89, 0x58, 0xBF, 0x78, 0x34, 0x98, 0x71, 0x68, 0x59
]

XOR_KEY = [0x42, 0x73, 0x21, 0x69, 0x37]
MAGIC_ADD = 0x2A
FLAG_LEN = 30

# Copy target to a buffer we can modify
buffer = list(TARGET)

# --- REVERSE OPERATION 4: XOR with Index ---
# Forward was: buffer[i] ^= i
for i in range(FLAG_LEN):
    buffer[i] ^= i

# --- REVERSE OPERATION 3: Subtract Magic Constant ---
# Forward was: buffer[i] = (buffer[i] + MAGIC_ADD) % 256
for i in range(FLAG_LEN):
    buffer[i] = (buffer[i] - MAGIC_ADD) % 256

# --- REVERSE OPERATION 2: Swap Adjacent Pairs ---
# Forward was: Swap (0,1), (2,3), etc.
for i in range(0, FLAG_LEN, 2):
    # Swap adjacent bytes
    buffer[i], buffer[i+1] = buffer[i+1], buffer[i]

# --- REVERSE OPERATION 1: XOR with Rotating Key ---
# Forward was: buffer[i] ^= XOR_KEY[i % 5]
for i in range(FLAG_LEN):
    buffer[i] ^= XOR_KEY[i % 5]

# Convert bytes to characters and print
flag = "".join(chr(b) for b in buffer)
print(f"The Flag is: {flag}")