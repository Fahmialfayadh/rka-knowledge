# write utf 8
file1 = open("quotes_5054251015.txt", "w", encoding="utf-8")  
L = ["人生は一度きり \n", "Carpe diem \n", "To be or not to be \n"]
file1.writelines(L)
file1.close()