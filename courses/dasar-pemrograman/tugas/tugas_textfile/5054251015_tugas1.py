file1 = open("5054251015.txt", "w")  
L = ["Nama saya Fahmi Alfayadh \n", "Asal saya dari Medan \n", "Saya suka dasprog \n"]

file1.write("Hello \n")          # write single line
file1.writelines(L)              # write multiple lines
file1.close()                    # close file

file1 = open("5054251015.txt", "r+") # reopen file in read+append mode

print("Output of read():")
print(file1.read())              # read whole file
print()

file1.seek(0)                    # move cursor to start
print("Output of readline():")
print(file1.readline())          # read first line
print()

file1.seek(0)
print("Output of read(9):")
print(file1.read(9))             # read first 9 chars
print()

file1.seek(0)
print("Output of readline(9):")
print(file1.readline(9))         # read 9 chars from line
print()

file1.seek(0)
print("Output of readlines():")
print(file1.readlines())         # read all lines as list
print()

file1.close()
