# Modul 10: Garis Singgung dan Panjang Busur di Koordinat Kutub

## 1. Pendahuluan
Pada Modul 5 dan 6, kita telah mempelajari dasar-dasar koordinat kutub (polar) beserta cara menghitung luas daerah di dalamnya. Namun, untuk menganalisis gerak objek yang melintasi kurva polar secara dinamis, kita memerlukan alat kalkulus diferensial dan integral tambahan, yaitu menentukan **kemiringan garis singgung** dan **panjang busur** kurva polar.

Sebagai contoh:
- Menentukan arah gerak satelit yang mengorbit bumi dalam lintasan elips polar.
- Menghitung panjang kabel antena spiral atau lintasan partikel bermuatan dalam medan magnet.

**Prasyarat:** Sebelum memulai modul ini, pastikan Anda sudah menguasai:
1. Hubungan konversi koordinat kutub ke Kartesian ($x = r\cos\theta$ dan $y = r\sin\theta$).
2. Aturan perkalian pada turunan ($(uv)' = u'v + uv'$).
3. Identitas trigonometri dasar dan rumus sudut ganda.

---

## 2. Konsep Dasar

### A. Garis Singgung Kurva Kutub
Ketika kita memiliki kurva polar $r = f(\theta)$, kita sering kali ingin mencari kemiringan garis singgungnya dalam ruang dua dimensi. Kemiringan garis singgung didefinisikan sebagai perubahan tegak terhadap mendatar, yaitu $m = \frac{dy}{dx}$ (bukan $\frac{dr}{d\theta}$). 

Untuk mencari $\frac{dy}{dx}$, kita memandang $\theta$ sebagai parameter dan menulis koordinat $x$ dan $y$ dalam bentuk parametrik terhadap $\theta$:
$$x = r\cos\theta = f(\theta)\cos\theta$$
$$y = r\sin\theta = f(\theta)\sin\theta$$

Menggunakan aturan turunan berantai untuk fungsi parametrik, kemiringan garis singgung diperoleh dari:
$$\frac{dy}{dx} = \frac{\frac{dy}{d\theta}}{\frac{dx}{d\theta}}$$

Dengan menerapkan aturan perkalian turunan pada $x$ dan $y$:
- $\frac{dy}{d\theta} = \frac{dr}{d\theta}\sin\theta + r\cos\theta$
- $\frac{dx}{d\theta} = \frac{dr}{d\theta}\cos\theta - r\sin\theta$

Sehingga diperoleh rumus kemiringan garis singgung pada koordinat kutub.

---

### B. Panjang Busur Kurva Kutub
Untuk mencari panjang kurva polar $r = f(\theta)$ dari sudut $\theta = \alpha$ ke $\theta = \beta$, kita dapat bertolak dari rumus panjang busur parametrik:
$$L = \int_{\alpha}^{\beta} \sqrt{\left(\frac{dx}{d\theta}\right) ^2 + \left(\frac{dy}{d\theta}\right)^2} \, d\theta$$

Jika kita kuadratkan komponen turunan di atas dan menjumlahkannya:
$$\left(\frac{dx}{d\theta}\right)^2 + \left(\frac{dy}{d\theta}\right)^2 = \left(\frac{dr}{d\theta}\cos\theta - r\sin\theta\right)^2 + \left(\frac{dr}{d\theta}\sin\theta + r\cos\theta\right)^2$$

Setelah menjabarkan perkalian aljabar di atas, suku-suku tengah $-2r\frac{dr}{d\theta}\sin\theta\cos\theta$ dan $+2r\frac{dr}{d\theta}\sin\theta\cos\theta$ akan saling menghilangkan. Dengan menggunakan identitas trigonometri $\sin^2\theta + \cos^2\theta = 1$, persamaan tersebut menyusut menjadi:
$$\left(\frac{dx}{d\theta}\right)^2 + \left(\frac{dy}{d\theta}\right)^2 = r^2 + \left(\frac{dr}{d\theta}\right)^2$$

Sehingga rumus panjang busur kutub menjadi sangat sederhana.

---

## 3. Rumus Utama

### A. Kemiringan Garis Singgung (Slope)
Kemiringan garis singgung $m$ dari kurva polar $r = f(\theta)$ pada titik $\theta$ adalah:

$$\frac{dy}{dx} = \frac{\frac{dr}{d\theta}\sin\theta + r\cos\theta}{\frac{dr}{d\theta}\cos\theta - r\sin\theta}$$

---

### B. Garis Singgung Horizontal dan Vertikal
- **Garis Singgung Horizontal:** Terjadi saat kemiringan $m = 0$, yang dipenuhi jika:
  $$\frac{dy}{d\theta} = 0 \quad \text{dan} \quad \frac{dx}{d\theta} \neq 0$$
- **Garis Singgung Vertikal:** Terjadi saat kemiringan $m$ tak terdefinisi (garis tegak), yang dipenuhi jika:
  $$\frac{dx}{d\theta} = 0 \quad \text{dan} \quad \frac{dy}{d\theta} \neq 0$$

---

### C. Panjang Busur Kutub
Panjang busur kurva polar $r = f(\theta)$ dari $\theta = \alpha$ hingga $\theta = \beta$:

$$L = \int_{\alpha}^{\beta} \sqrt{r^2 + \left(\frac{dr}{d\theta}\right)^2} \, d\theta$$

---

## 4. Langkah Pengerjaan Sistematis

### A. Menghitung Garis Singgung
1. **Hitung Turunan Pertama:** Carilah turunan $r$ terhadap $\theta$, yaitu $\frac{dr}{d\theta} = f'(\theta)$.
2. **Evaluasi pada Sudut yang Ditanyakan:** Masukkan nilai sudut $\theta_0$ ke dalam persamaan $r$ dan $\frac{dr}{d\theta}$ untuk mendapatkan nilai konstan.
3. **Hitung Pembilang dan Penyebut:**
   - Pembilang: $\frac{dy}{d\theta} = \frac{dr}{d\theta}\sin\theta + r\cos\theta$
   - Penyebut: $\frac{dx}{d\theta} = \frac{dr}{d\theta}\cos\theta - r\sin\theta$
4. **Hitung Kemiringan $m$:** Bagilah pembilang dengan penyebut.
5. **Persamaan Garis Singgung Kartesian (jika diminta):**
   - Cari koordinat Kartesian titik tersebut: $x_0 = r_0\cos\theta_0$ dan $y_0 = r_0\sin\theta_0$.
   - Masukkan ke rumus garis lurus: $y - y_0 = m(x - x_0)$.

### B. Menghitung Panjang Busur
1. **Tentukan Batas Integrasi:** Identifikasi interval sudut $[\alpha, \beta]$.
2. **Hitung Turunan $\frac{dr}{d\theta}$:** Cari turunan dari fungsi polar yang diberikan.
3. **Sederhanakan Bentuk $r^2 + \left(\frac{dr}{d\theta}\right)^2$:**
   - Gunakan identitas trigonometri untuk menyederhanakan persamaan di dalam tanda akar.
   - Waspadai kemunculan bentuk kuadrat sempurna seperti $A(1 \pm \cos\theta)$ atau $A(1 \pm \sin\theta)$ yang dapat disederhanakan menggunakan rumus sudut setengah.
4. **Hitung Integral:** Evaluasi integral tentu. Jika fungsi akar mengandung nilai mutlak, gunakan sifat simetri kurva untuk mempermudah perhitungan.

---

## 5. Contoh Soal & Pembahasan Langkah demi Langkah

### Contoh Soal 1: Garis Singgung Kardioid
Tentukan kemiringan garis singgung kurva kardioid $r = 1 + \sin\theta$ di titik $\theta = \frac{\pi}{3}$.

#### Penyelesaian:

**Langkah 1: Hitung Turunan Pertama**
$$r = 1 + \sin\theta \rightarrow \frac{dr}{d\theta} = \cos\theta$$

**Langkah 2: Evaluasi Nilai pada $\theta = \frac{\pi}{3}$**
- $r = 1 + \sin\left(\frac{\pi}{3}\right) = 1 + \frac{\sqrt{3}}{2}$
- $\frac{dr}{d\theta} = \cos\left(\frac{\pi}{3}\right) = \frac{1}{2}$

**Langkah 3: Hitung Nilai Turunan Parametrik**
- Pembilang ($\frac{dy}{d\theta}$):
  $$\frac{dy}{d\theta} = \frac{dr}{d\theta}\sin\theta + r\cos\theta$$
  $$\frac{dy}{d\theta} = \left(\frac{1}{2}\right)\sin\left(\frac{\pi}{3}\right) + \left(1 + \frac{\sqrt{3}}{2}\right)\cos\left(\frac{\pi}{3}\right)$$
  $$\frac{dy}{d\theta} = \left(\frac{1}{2}\right)\left(\frac{\sqrt{3}}{2}\right) + \left(1 + \frac{\sqrt{3}}{2}\right)\left(\frac{1}{2}\right) = \frac{\sqrt{3}}{4} + \frac{1}{2} + \frac{\sqrt{3}}{4} = \frac{1 + \sqrt{3}}{2}$$

- Penyebut ($\frac{dx}{d\theta}$):
  $$\frac{dx}{d\theta} = \frac{dr}{d\theta}\cos\theta - r\sin\theta$$
  $$\frac{dx}{d\theta} = \left(\frac{1}{2}\right)\cos\left(\frac{\pi}{3}\right) - \left(1 + \frac{\sqrt{3}}{2}\right)\sin\left(\frac{\pi}{3}\right)$$
  $$\frac{dx}{d\theta} = \left(\frac{1}{2}\right)\left(\frac{1}{2}\right) - \left(1 + \frac{\sqrt{3}}{2}\right)\left(\frac{\sqrt{3}}{2}\right) = \frac{1}{4} - \frac{\sqrt{3}}{2} - \frac{3}{4} = -\frac{2}{4} - \frac{\sqrt{3}}{2} = -\frac{1 + \sqrt{3}}{2}$$

**Langkah 4: Hitung Kemiringan $m = \frac{dy}{dx}$**
$$m = \frac{\frac{dy}{d\theta}}{\frac{dx}{d\theta}} = \frac{\frac{1 + \sqrt{3}}{2}}{-\frac{1 + \sqrt{3}}{2}} = -1$$

**Jawaban:** Kemiringan garis singgung kardioid tersebut pada $\theta = \frac{\pi}{3}$ adalah $-1$.

---

### Contoh Soal 2: Panjang Busur Kardioid (Dengan Simetri)
Tentukan panjang busur total dari kardioid $r = 1 + \cos\theta$ untuk satu putaran penuh ($0 \le \theta \le 2\pi$).

#### Penyelesaian:

**Langkah 1: Identifikasi Batas Integrasi dan Hitung Turunan**
- Batas: $\theta \in [0, 2\pi]$
- $r = 1 + \cos\theta \rightarrow \frac{dr}{d\theta} = -\sin\theta$

**Langkah 2: Sederhanakan Bentuk $r^2 + \left(\frac{dr}{d\theta}\right)^2$**
$$r^2 + \left(\frac{dr}{d\theta}\right)^2 = (1 + \cos\theta)^2 + (-\sin\theta)^2$$
$$= 1 + 2\cos\theta + \cos^2\theta + \sin^2\theta$$
Ingat identitas $\cos^2\theta + \sin^2\theta = 1$:
$$= 2 + 2\cos\theta = 2(1 + \cos\theta)$$

Gunakan rumus setengah sudut: $1 + \cos\theta = 2\cos^2\left(\frac{\theta}{2}\right)$
$$r^2 + \left(\frac{dr}{d\theta}\right)^2 = 2 \cdot 2\cos^2\left(\frac{\theta}{2}\right) = 4\cos^2\left(\frac{\theta}{2}\right)$$

Jika ditarik akar:
$$\sqrt{r^2 + \left(\frac{dr}{d\theta}\right)^2} = \sqrt{4\cos^2\left(\frac{\theta}{2}\right)} = 2\left|\cos\left(\frac{\theta}{2}\right)\right|$$

**Langkah 3: Sifat Simetri untuk Menghilangkan Nilai Mutlak**
Kurva kardioid simetris terhadap sumbu-x (garis kutub $\theta = 0$). Nilai $\cos\left(\frac{\theta}{2}\right)$ akan positif pada interval $[0, \pi]$ dan negatif pada $[\pi, 2\pi]$.
Untuk menghindari kesalahan integrasi nilai mutlak, kita cukup mengintegralkan dari $0$ hingga $\pi$, lalu hasilnya dikalikan $2$:
$$L = 2 \int_{0}^{\pi} 2\cos\left(\frac{\theta}{2}\right) \, d\theta$$
$$L = 4 \int_{0}^{\pi} \cos\left(\frac{\theta}{2}\right) \, d\theta$$

**Langkah 4: Hitung Nilai Integral**
$$L = 4 \left[ 2\sin\left(\frac{\theta}{2}\right) \right]_{0}^{\pi}$$
$$L = 8 \left( \sin\left(\frac{\pi}{2}\right) - \sin(0) \right)$$
$$L = 8 (1 - 0) = 8 \text{ satuan panjang}$$

**Jawaban:** Panjang busur total kardioid tersebut adalah $8$ satuan panjang.

---

## 6. Ringkasan & Tips Ujian

* **Kemiringan vs Laju Perubahan:**
  - $\frac{dr}{d\theta}$ adalah laju perubahan jarak titik terhadap titik asal jika sudut berubah.
  - $\frac{dy}{dx}$ adalah kemiringan geometris garis singgung sesungguhnya. **Jangan tertukar dalam ujian!**

* **Identitas Sudut Setengah yang Wajib Diingat:**
  Identitas ini sangat sering muncul pada soal panjang busur polar untuk membuang simbol akar kuadrat:
  - $1 + \cos\theta = 2\cos^2\left(\frac{\theta}{2}\right)$
  - $1 - \cos\theta = 2\sin^2\left(\frac{\theta}{2}\right)$

* **Kesalahan Fatal Ujian (Mengabaikan Nilai Mutlak):**
  Jika Anda mengintegralkan $2\cos\left(\frac{\theta}{2}\right)$ langsung dari $0$ ke $2\pi$ tanpa memisahkannya atau menggunakan simetri:
  $$\text{SALAH: } \int_{0}^{2\pi} 2\cos\left(\frac{\theta}{2}\right) \, d\theta = \left[ 4\sin\left(\frac{\theta}{2}\right) \right]_{0}^{2\pi} = 4\sin(\pi) - 4\sin(0) = 0$$
  Panjang busur fisik kurva nyata **tidak mungkin bernilai 0**. Gunakan selalu sifat simetri atau pisahkan batas integrasi di titik di mana fungsi di bawah akar bernilai nol.
