file1 = open("5054251015.txt", "w")  
L = ["Nama saya Fahmi Alfayadh \n", "Asal saya dari Medan \n", "Saya suka dasprog \n"]

file1.write("Hello \n")          # write single line
file1.writelines(L)              # write multiple lines
file1.close()                    # close file
file1 = open("5054251015.txt", "r+") # reopen file in read+append mode
file1.seek(0)                    # move cursor to start         
print("Output of readline():")
print(file1.readline())          # read first line
print()

file1.seek(0)
print("Output of read(9):")
print(file1.read(100))             # read first 9 chars
print()
