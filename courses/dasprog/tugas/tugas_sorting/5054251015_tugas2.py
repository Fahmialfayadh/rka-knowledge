n, minimal = map(int, input().split())
list_penyihir = list(map(int, input().split()))
list_penyihir.sort()

temp = []
if len(list_penyihir) > 0:
    temp.append(list_penyihir[0])
    terakhir_diambil = list_penyihir[0]

    for i in range(1, len(list_penyihir)):
        
        # selisih dengan anggota tim terakhir yang valid
        selisih = list_penyihir[i] - terakhir_diambil
        
        if selisih >= minimal:
            temp.append(list_penyihir[i])
            terakhir_diambil = list_penyihir[i] # updte nilai terakhir

print(len(temp))
print(*temp)