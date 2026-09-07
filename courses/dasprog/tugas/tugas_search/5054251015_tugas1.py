import sys

# bisect left
def cari_posisi_terkiri(daftar_data, nilai_yang_dicari):
    """
    Mencari indeks elemen terkecil di dalam daftar_data 
    yang nilainya >= nilai_yang_dicari.
    """
    batas_kiri = 0
    batas_kanan = len(daftar_data) - 1
    # inisialisasi posisi terbaik dengan batas kiri
    posisi_terbaik = batas_kiri 

    while batas_kiri <= batas_kanan:
        indeks_tengah = (batas_kiri + batas_kanan) // 2
        nilai_tengah = daftar_data[indeks_tengah]
        
        if nilai_tengah >= nilai_yang_dicari:
            posisi_terbaik = indeks_tengah
            batas_kanan = indeks_tengah - 1
        else:
            # nilai tengah terlalu kecil, cari di sebelah kanan
            batas_kiri = indeks_tengah + 1
            
    return posisi_terbaik

def solve():
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    daftar_berat_paket = [int(x) for x in input_data[1:]]

    # tails menyimpan elemen "ujung" dari kemungkinan barisan naik
    tails = []

    for berat_sekarang in daftar_berat_paket:
        # tails kosong atau berat paket sekarang LEBIH BESAR dari ujung barisan saat ini
        if not tails or berat_sekarang > tails[-1]:
            tails.append(berat_sekarang)
        
        # jika berat lebih kecil/sama, kita cari posisi untuk menimpanya
        else:
            index_diganti = cari_posisi_terkiri(tails, berat_sekarang)
            
            # ganti dengan berat yang baru
            tails[index_diganti] = berat_sekarang

    print(len(tails))
solve()
