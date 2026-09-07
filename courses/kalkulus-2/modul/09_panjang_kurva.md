# Modul 9: Panjang Suatu Kurva

## 1. Pendahuluan
Dalam geometri dasar, kita dapat dengan mudah menghitung panjang garis lurus menggunakan rumus jarak Euclidean, atau menghitung panjang keliling lingkaran menggunakan rumus $2\pi r$. Namun, bagaimana jika kita ingin menghitung panjang lintasan melengkung yang tidak beraturan? Misalnya, bentuk lintasan roket, kabel listrik yang menggantung kendor di antara dua tiang (kurva *katenari*), atau jalan raya yang berkelok-kelok di pegunungan?

Di sinilah integral tentu berperan penting. **Panjang kurva** (*arc length*) adalah ukuran panjang fisik suatu segmen kurva sepanjang lintasan melengkungnya. 

**Prasyarat:** Sebelum memulai modul ini, pastikan Anda sudah menguasai:
1. Aturan rantai turunan dan turunan fungsi logaritma/trigonometri.
2. Aljabar kuadrat sempurna (pemfaktoran).
3. Aturan dasar integral tentu.

---

## 2. Konsep Dasar
Ide dasar untuk mencari panjang kurva halus $y = f(x)$ dari batas $x = a$ ke $x = b$ adalah dengan memotong kurva tersebut menjadi $n$ segmen garis lurus yang sangat kecil.

Misalkan kita memperbesar salah satu segmen kecil tersebut:
- Segmen tersebut memiliki perubahan mendatar sebesar $\Delta x_i$ dan perubahan tegak sebesar $\Delta y_i$.
- Berdasarkan teorema Pythagoras, panjang segmen garis kecil $\Delta s_i$ adalah:
  $$\Delta s_i = \sqrt{(\Delta x_i)^2 + (\Delta y_i)^2}$$
- Kita dapat memanipulasi aljabar persamaan di atas dengan mengeluarkan $\Delta x_i$:
  $$\Delta s_i = \sqrt{1 + \left(\frac{\Delta y_i}{\Delta x_i}\right)^2} \Delta x_i$$
- Berdasarkan Teorema Nilai Rata-rata untuk turunan, rasio selisih $\frac{\Delta y_i}{\Delta x_i}$ mendekati nilai turunan $f'(x_i^*)$ untuk suatu titik di interval tersebut.
  $$\Delta s_i \approx \sqrt{1 + [f'(x_i^*)]^2} \Delta x_i$$

Jika kita mengambil limit $n \to \infty$ (lebar segmen $\Delta x_i \to 0$), jumlah Riemann dari segmen-segmen garis tersebut akan berkonvergensi menjadi integral tentu yang menghasilkan panjang kurva sebenarnya ($L$):

$$L = \int_{a}^{b} \sqrt{1 + \left(\frac{dy}{dx}\right)^2} \, dx$$

---

## 3. Rumus Utama

### A. Kurva Kartesian dalam Bentuk $y = f(x)$
Jika kurva didefinisikan oleh fungsi $y = f(x)$ pada interval $[a, b]$, di mana turunan $f'(x)$ kontinu:

$$L = \int_{a}^{b} \sqrt{1 + \left(\frac{dy}{dx}\right)^2} \, dx$$

---

### B. Kurva Kartesian dalam Bentuk $x = g(y)$
Jika kurva didefinisikan oleh fungsi $x = g(y)$ pada interval $[c, d]$, di mana turunan $g'(y)$ kontinu:

$$L = \int_{c}^{d} \sqrt{1 + \left(\frac{dx}{dy}\right)^2} \, dy$$

---

### C. Kurva Parametrik dalam Bentuk $x = f(t), y = g(t)$
Jika kurva didefinisikan secara parametrik oleh $x = f(t)$ dan $y = g(t)$ untuk interval parameter $t \in [\alpha, \beta]$:
- Dari hubungan Pythagoras awal $ds = \sqrt{dx^2 + dy^2}$, kita bagi dengan $dt$:
  $$ds = \sqrt{\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2} \, dt$$

$$L = \int_{\alpha}^{\beta} \sqrt{\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2} \, dt$$

---

## 4. Langkah Pengerjaan Sistematis

Menghitung panjang kurva sering kali melibatkan integral dengan bentuk akar $\sqrt{\dots}$. Oleh karena itu, pengerjaan yang sistematis sangat penting agar tidak terjebak dalam integral yang rumit:

1. **Tentukan Persamaan dan Batas:** Identifikasi variabel integrasi ($x$, $y$, atau parameter $t$) dan tentukan batas bawah serta batas atasnya.
2. **Hitung Turunan:** Cari $dy/dx$, $dx/dy$, atau turunan parametrik $dx/dt$ dan $dy/dt$.
3. **Sederhanakan Bentuk di Dalam Akar:**
   - Susun bentuk $1 + (dy/dx)^2$ (atau padanannya).
   - Lakukan penyederhanaan aljabar. Waspadai pola **Kuadrat Sempurna** (*perfect square trick*) yang sering dirancang dalam soal ujian agar akar $\sqrt{\dots}$ dapat hilang.
4. **Susun Integral:** Masukkan hasil penyederhanaan ke dalam rumus panjang kurva.
5. **Hitung Nilai Integral:** Selesaikan integral tersebut dan evaluasi batasnya.

---

## 5. Contoh Soal & Pembahasan Langkah demi Langkah

### Contoh Soal 1: Substitusi Sederhana
Tentukan panjang kurva $y = \frac{2}{3}x^{3/2}$ dari titik $x = 0$ hingga $x = 3$.

#### Penyelesaian:

**Langkah 1: Tentukan Persamaan dan Batas**
- Persamaan: $y = \frac{2}{3}x^{3/2}$
- Batas integrasi: $x \in [0, 3]$ (maka $a = 0$ dan $b = 3$)

**Langkah 2: Hitung Turunan**
$$\frac{dy}{dx} = \frac{2}{3} \cdot \left(\frac{3}{2}x^{1/2}\right) = x^{1/2} = \sqrt{x}$$

**Langkah 3: Sederhanakan Bentuk di Dalam Akar**
$$1 + \left(\frac{dy}{dx}\right)^2 = 1 + (\sqrt{x})^2 = 1 + x$$

**Langkah 4: Menyusun Integral**
$$L = \int_{0}^{3} \sqrt{1 + x} \, dx$$

**Langkah 5: Hitung Nilai Integral**
Gunakan teknik substitusi:
Misalkan $u = 1 + x \rightarrow du = dx$.
- Batas baru:
  - Jika $x = 0 \rightarrow u = 1 + 0 = 1$
  - Jika $x = 3 \rightarrow u = 1 + 3 = 4$

Maka:
$$L = \int_{1}^{4} \sqrt{u} \, du = \int_{1}^{4} u^{1/2} \, du$$
$$L = \left[ \frac{2}{3}u^{3/2} \right]_{1}^{4}$$
$$L = \frac{2}{3} \left( 4^{3/2} - 1^{3/2} \right)$$
Ingat bahwa $4^{3/2} = (\sqrt{4})^3 = 2^3 = 8$, dan $1^{3/2} = 1$:
$$L = \frac{2}{3} (8 - 1) = \frac{2}{3} (7) = \frac{14}{3} \approx 4.67 \text{ satuan panjang}$$

**Jawaban:** Panjang kurva tersebut adalah $\frac{14}{3}$ atau sekitar $4.67$ satuan panjang.

---

### Contoh Soal 2: Trik Kuadrat Sempurna (Perfect Square Trick)
Hitunglah panjang kurva $y = \frac{x^2}{4} - \frac{\ln x}{2}$ pada interval $[1, e]$.

#### Penyelesaian:

**Langkah 1: Tentukan Persamaan dan Batas**
- Persamaan: $y = \frac{x^2}{4} - \frac{\ln x}{2}$
- Batas integrasi: $x \in [1, e]$ (maka $a = 1$ dan $b = e$)

**Langkah 2: Hitung Turunan**
$$\frac{dy}{dx} = \frac{2x}{4} - \frac{1}{2x} = \frac{x}{2} - \frac{1}{2x}$$

**Langkah 3: Sederhanakan Bentuk di Dalam Akar**
Ini adalah bagian krusial. Mari kuadratkan turunan tersebut:
$$\left(\frac{dy}{dx}\right)^2 = \left(\frac{x}{2} - \frac{1}{2x}\right)^2 = \frac{x^2}{4} - 2\left(\frac{x}{2}\right)\left(\frac{1}{2x}\right) + \frac{1}{4x^2}$$
$$\left(\frac{dy}{dx}\right)^2 = \frac{x^2}{4} - \frac{1}{2} + \frac{1}{4x^2}$$

Sekarang tambahkan 1:
$$1 + \left(\frac{dy}{dx}\right)^2 = 1 + \frac{x^2}{4} - \frac{1}{2} + \frac{1}{4x^2}$$
$$1 + \left(\frac{dy}{dx}\right)^2 = \frac{x^2}{4} + \frac{1}{2} + \frac{1}{4x^2}$$

Perhatikan bahwa tanda suku tengah berubah dari $-\frac{1}{2}$ menjadi $+\frac{1}{2}$. Ini memungkinkan kita memfaktorkannya kembali menjadi kuadrat sempurna:
$$\frac{x^2}{4} + \frac{1}{2} + \frac{1}{4x^2} = \left(\frac{x}{2} + \frac{1}{2x}\right)^2$$

Sehingga ketika ditarik akar:
$$\sqrt{1 + \left(\frac{dy}{dx}\right)^2} = \sqrt{\left(\frac{x}{2} + \frac{1}{2x}\right)^2} = \frac{x}{2} + \frac{1}{2x}$$

**Langkah 4: Menyusun Integral**
$$L = \int_{1}^{e} \left( \frac{x}{2} + \frac{1}{2x} \right) \, dx$$

**Langkah 5: Hitung Nilai Integral**
$$L = \left[ \frac{x^2}{4} + \frac{1}{2}\ln|x| \right]_{1}^{e}$$
Evaluasi batas atas ($x = e$):
$$\text{Atas} = \frac{e^2}{4} + \frac{1}{2}\ln(e) = \frac{e^2}{4} + \frac{1}{2}$$
Evaluasi batas bawah ($x = 1$):
$$\text{Bawah} = \frac{1^2}{4} + \frac{1}{2}\ln(1) = \frac{1}{4} + 0 = \frac{1}{4}$$
Kurangkan batas atas dengan batas bawah:
$$L = \left(\frac{e^2}{4} + \frac{1}{2}\right) - \frac{1}{4} = \frac{e^2}{4} + \frac{1}{4} = \frac{e^2 + 1}{4} \approx 2.10 \text{ satuan panjang}$$

**Jawaban:** Panjang kurva tersebut adalah $\frac{e^2 + 1}{4}$ atau sekitar $2.10$ satuan panjang.

---

## 6. Ringkasan & Tips Ujian

* **Trik Kuadrat Sempurna:** Soal ujian panjang kurva sering kali melibatkan bentuk logaritma atau fungsi hiperbolik karena mereka memiliki pola turunan yang jika ditambahkan 1 akan membentuk kuadrat sempurna, menghilangkan simbol akar:
  $$1 + \left(\frac{1}{2}(e^x - e^{-x})\right)^2 = \left(\frac{1}{2}(e^x + e^{-x})\right)^2$$
  Mengenali pola ini akan menghemat banyak waktu saat ujian.

* **Kesalahan Umum di Lembar Jawaban:**
  1. **Lupa menguadratkan turunan:** Banyak mahasiswa langsung memasukkan turunan $\frac{dy}{dx}$ di bawah tanda akar: $\int \sqrt{1 + \frac{dy}{dx}} \, dx$. Ini **salah besar**.
  2. **Salah aljabar kuadrat:** Ingat bahwa $(A - B)^2 = A^2 - 2AB + B^2$, jangan lupa menulis suku tengah $-2AB$. Kehilangan suku tengah ini akan menggagalkan trik kuadrat sempurna.
  3. **Mengintegralkan fungsi aslinya:** Karena terburu-buru, terkadang mahasiswa langsung mengintegralkan fungsi $f(x)$ tanpa menggunakan rumus panjang kurva. Selalu baca instruksi soal dengan teliti.
