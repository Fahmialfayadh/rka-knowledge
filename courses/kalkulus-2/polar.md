# MODUL BELAJAR — KOORDINAT POLAR
### (Calculus II — Bab 9.6, 9.7, 9.8: *Polar Coordinates*, *Tangents with Polar Coordinates*, *Area with Polar Coordinates*)

> Disusun ulang dan diadaptasi dari struktur materi *Paul's Online Math Notes* (Lamar University), ditulis ulang dengan bahasa sendiri, ditata linear, plus contoh soal tambahan agar lebih mudah dipahami dan langsung bisa dipakai untuk belajar atau latihan ujian.

---

## DAFTAR ISI

1. Konsep Dasar Koordinat Polar
2. Konversi Polar ↔ Cartesian
3. Mengonversi Persamaan Antar Sistem Koordinat
4. Grafik-Grafik Umum dalam Koordinat Polar
5. Titik Potong di Pusat (Pole)
6. **Turunan** dalam Koordinat Polar (Garis Singgung)
7. **Integral** dalam Koordinat Polar (Luas Daerah)
8. Bonus: Panjang Kurva (Arc Length) Polar
9. Rangkuman Rumus (Cheat Sheet)
10. Latihan Mandiri + Kunci Jawaban

---

## 1. KONSEP DASAR KOORDINAT POLAR

Selama ini kita biasa menentukan posisi titik dengan sistem **Cartesian** $(x, y)$: bergerak $x$ satuan horizontal, lalu $y$ satuan vertikal dari titik asal (origin).

Sistem **polar** menentukan posisi titik dengan cara berbeda: alih-alih bergerak horizontal-vertikal, kita:

1. Tentukan **jarak** $r$ dari titik asal (disebut **kutub**, *pole*) ke titik tersebut.
2. Tentukan **sudut** $\theta$ yang dibentuk garis penghubung itu terhadap sumbu-$x$ positif (diukur berlawanan arah jarum jam).

Jadi sebuah titik ditulis sebagai pasangan $(r, \theta)$.

### Catatan penting: $r$ boleh negatif

Berbeda dari intuisi awal, $r$ tidak harus positif.

- Jika $r > 0$ → titik berada **pada kuadran yang sama** dengan arah $\theta$.
- Jika $r < 0$ → titik berada **pada kuadran yang berlawanan** (180° dari arah $\theta$).

Contohnya, $(2, \tfrac{\pi}{6})$ dan $(-2, \tfrac{\pi}{6})$ adalah dua titik yang berbeda, terletak di kuadran yang berlawanan.

### Koordinat Polar Tidak Tunggal!

Ini adalah perbedaan besar dengan Cartesian. Di Cartesian, satu titik = satu pasangan koordinat. Di polar, **satu titik punya banyak (tak terhingga) representasi koordinat**, karena kita bisa menambahkan putaran penuh ($2\pi$) atau memakai $r$ negatif dengan sudut yang disesuaikan.

Secara umum, titik $(r, \theta)$ sama dengan:

$$
(r,\ \theta + 2\pi n) \qquad \text{atau} \qquad (-r,\ \theta + (2n+1)\pi), \quad n \in \mathbb{Z}
$$

**Contoh:** keempat pasangan berikut menunjuk ke titik yang **sama**:

$$
\left(5, \frac{\pi}{3}\right) = \left(5, -\frac{5\pi}{3}\right) = \left(-5, \frac{4\pi}{3}\right) = \left(-5, -\frac{2\pi}{3}\right)
$$

Dan untuk titik asal/pole itu sendiri: $r = 0$ untuk **berapapun** nilai $\theta$. Jadi pole punya koordinat $(0, \theta)$, untuk sembarang $\theta$.

---

## 2. KONVERSI POLAR ↔ CARTESIAN

Bayangkan segitiga siku-siku yang dibentuk oleh $x$, $y$, dan $r$ sebagai sisi miring, dengan $\theta$ sebagai sudutnya. Dari situ kita dapatkan dua arah konversi.

### A. Polar → Cartesian

$$
\boxed{x = r\cos\theta \qquad y = r\sin\theta}
$$

### B. Cartesian → Polar

Dari $x^2 + y^2 = r^2\cos^2\theta + r^2\sin^2\theta = r^2(\cos^2\theta + \sin^2\theta) = r^2$, kita dapat:

$$
\boxed{r^2 = x^2 + y^2 \qquad \Rightarrow \qquad r = \sqrt{x^2+y^2}}
$$

Untuk sudutnya, dari $\dfrac{y}{x} = \dfrac{r\sin\theta}{r\cos\theta} = \tan\theta$:

$$
\boxed{\theta_1 = \tan^{-1}\left(\frac{y}{x}\right) \qquad \text{ATAU} \qquad \theta_2 = \theta_1 + \pi}
$$

> ⚠️ **Hati-hati!** Fungsi $\tan^{-1}$ (arctan) hanya mengembalikan nilai pada rentang $-\frac{\pi}{2} < \theta < \frac{\pi}{2}$ — artinya hasilnya **selalu** "seolah-olah" di kuadran I atau IV. Kalau titik aslinya berada di kuadran II atau III, kamu **harus** menambahkan $\pi$ ke hasil arctan tadi. Ini adalah sumber kesalahan paling umum di topik ini.

### Contoh Soal 1

**Soal:** Konversikan titik berikut.
(a) $\left(-4, \dfrac{2\pi}{3}\right)$ (polar) → Cartesian
(b) $(-3, -3)$ (Cartesian) → polar

**Penyelesaian (a):**

$$
x = -4\cos\left(\frac{2\pi}{3}\right) = -4\left(-\frac{1}{2}\right) = 2
$$

$$
y = -4\sin\left(\frac{2\pi}{3}\right) = -4\left(\frac{\sqrt3}{2}\right) = -2\sqrt3
$$

Jadi titik Cartesian-nya adalah $(2, -2\sqrt3)$.

**Penyelesaian (b):**

$$
r = \sqrt{(-3)^2+(-3)^2} = \sqrt{18} = 3\sqrt2
$$

$$
\theta = \tan^{-1}\left(\frac{-3}{-3}\right) = \tan^{-1}(1) = \frac{\pi}{4}
$$

Tapi titik $(-3,-3)$ berada di **kuadran III**, sedangkan $\frac{\pi}{4}$ adalah sudut kuadran I — berarti kita harus menambahkan $\pi$:

$$
\theta = \frac{\pi}{4} + \pi = \frac{5\pi}{4}
$$

Jadi koordinat polarnya adalah $\left(3\sqrt2, \dfrac{5\pi}{4}\right)$.

> 💡 Bisa juga ditulis dengan $r$ negatif: $\left(-3\sqrt2, \dfrac{\pi}{4}\right)$ — keduanya menunjuk titik yang sama, sesuai sifat ketidaktunggalan koordinat polar di Bagian 1.

---

## 3. MENGONVERSI PERSAMAAN ANTAR SISTEM KOORDINAT

Rumus konversi di atas juga bisa dipakai untuk mengubah **persamaan** (bukan cuma titik) dari satu sistem ke sistem lainnya.

### Contoh Soal 2 — Cartesian ke Polar

**Soal:** Ubah $3x + 2x^3 = 1 - xy$ ke koordinat polar.

**Penyelesaian:** Substitusi langsung $x = r\cos\theta$, $y = r\sin\theta$:

$$
3(r\cos\theta) + 2(r\cos\theta)^3 = 1 - (r\cos\theta)(r\sin\theta)
$$

$$
3r\cos\theta + 2r^3\cos^3\theta = 1 - r^2\cos\theta\sin\theta
$$

Selesai — tidak perlu disederhanakan lebih lanjut, karena tujuannya hanya mengganti sistem koordinat.

### Contoh Soal 3 — Polar ke Cartesian (Trik "kali r di kedua sisi")

**Soal:** Ubah $r = 6\sin\theta$ ke koordinat Cartesian, dan identifikasi bentuk grafiknya.

**Penyelesaian:** Tidak ada substitusi langsung untuk $\sin\theta$ saja yang menghasilkan Cartesian murni. Trik standarnya: **kalikan kedua sisi dengan $r$** supaya muncul pola $r\sin\theta = y$:

$$
r^2 = 6r\sin\theta
$$

Sekarang substitusi $r^2 = x^2+y^2$ dan $r\sin\theta = y$:

$$
x^2 + y^2 = 6y
$$

**Mengidentifikasi bentuknya** — lengkapkan kuadrat pada $y$:

$$
x^2 + y^2 - 6y = 0
$$

$$
x^2 + (y^2 - 6y + 9) = 9
$$

$$
x^2 + (y-3)^2 = 9
$$

Ini adalah **lingkaran** berpusat di $(0, 3)$ dengan radius $3$.

> Ini sekaligus menunjukkan kenapa koordinat polar berguna: persamaan $r = 6\sin\theta$ jauh lebih ringkas dibanding bentuk Cartesian-nya.

---

## 4. GRAFIK-GRAFIK UMUM DALAM KOORDINAT POLAR

### A. Garis

| Persamaan Polar | Bentuk Cartesian | Keterangan |
|---|---|---|
| $\theta = \beta$ | $y = (\tan\beta)\, x$ | Garis lurus melalui origin, kemiringan $\tan\beta$ |
| $r\cos\theta = a$ | $x = a$ | Garis vertikal |
| $r\sin\theta = b$ | $y = b$ | Garis horizontal |

### B. Lingkaran

| Persamaan Polar | Pusat | Radius |
|---|---|---|
| $r = a$ | $(0,0)$ | $\lvert a\rvert$ |
| $r = 2a\cos\theta$ | $(a, 0)$ | $\lvert a\rvert$ |
| $r = 2b\sin\theta$ | $(0, b)$ | $\lvert b\rvert$ |
| $r = 2a\cos\theta + 2b\sin\theta$ | $(a, b)$ | $\sqrt{a^2+b^2}$ |

> Catatan: lingkaran $r=a$ butuh rentang $0 \le \theta \le 2\pi$ untuk digambar lengkap, sedangkan tiga lainnya sudah lengkap hanya dengan $0 \le \theta \le \pi$.

### C. Kardioid dan Limaçon

Bentuk umum: $r = a \pm b\cos\theta$ atau $r = a \pm b\sin\theta$.

| Jenis | Kondisi | Ciri |
|---|---|---|
| **Kardioid** | $a = b$ (jadi $r = a \pm a\cos\theta$) | Bentuk hati, **selalu** melewati pole |
| **Limaçon dengan loop dalam** | $a < b$ | Ada loop kecil di dalam, melewati pole dua kali |
| **Limaçon tanpa loop** | $a > b$ | Tidak melewati pole sama sekali |

**Tips cepat membaca soal:** lihat rasio $a/b$.
- $a = b$ → kardioid.
- $a/b < 1$ → ada loop dalam.
- $a/b > 1$ → tidak ada loop.

---

## 5. TITIK POTONG DI PUSAT (POLE)

Untuk kurva yang punya loop dalam (seperti limaçon dengan loop), kita sering perlu tahu **pada sudut $\theta$ berapa** kurva tersebut melewati pole (origin). Caranya: set $r = 0$, lalu selesaikan untuk $\theta$.

### Contoh Soal 4

**Soal:** Pada sudut berapa kurva $r = 1 + 2\cos\theta$ melewati pole?

**Penyelesaian:**

$$
0 = 1 + 2\cos\theta \quad\Rightarrow\quad \cos\theta = -\frac{1}{2} \quad\Rightarrow\quad \theta = \frac{2\pi}{3},\ \frac{4\pi}{3}
$$

Kedua sudut ini nanti akan kita pakai lagi di Bagian 7 untuk menghitung luas loop dalamnya.

---

## 6. TURUNAN DALAM KOORDINAT POLAR (GARIS SINGGUNG)

### Konsep

Karena $x = r(\theta)\cos\theta$ dan $y = r(\theta)\sin\theta$ keduanya merupakan fungsi dari parameter $\theta$, kemiringan garis singgung $\dfrac{dy}{dx}$ dicari memakai **aturan parametrik**, bukan turunan polar langsung:

$$
\frac{dy}{dx} = \frac{dy/d\theta}{dx/d\theta}
$$

Karena $r$ sendiri adalah fungsi dari $\theta$ — yaitu $r = r(\theta)$ — kita perlu **aturan hasil kali (product rule)** saat menurunkan $x$ dan $y$ terhadap $\theta$:

$$
\boxed{\frac{dy}{d\theta} = \frac{dr}{d\theta}\sin\theta + r\cos\theta}
$$

$$
\boxed{\frac{dx}{d\theta} = \frac{dr}{d\theta}\cos\theta - r\sin\theta}
$$

Sehingga rumus utamanya:

$$
\boxed{\frac{dy}{dx} = \dfrac{\dfrac{dr}{d\theta}\sin\theta + r\cos\theta}{\dfrac{dr}{d\theta}\cos\theta - r\sin\theta}}
$$

### Garis Singgung Horizontal & Vertikal

- **Horizontal** ($dy/dx = 0$): saat $\dfrac{dy}{d\theta} = 0$, **dan** $\dfrac{dx}{d\theta} \neq 0$ di titik yang sama.
- **Vertikal** (kemiringan tak terdefinisi): saat $\dfrac{dx}{d\theta} = 0$, **dan** $\dfrac{dy}{d\theta} \neq 0$.
- Kalau **keduanya** nol bersamaan → biasanya itu adalah titik *cusp* (titik lancip) atau pole, perlu analisis tambahan (limit), bukan garis singgung horizontal/vertikal biasa.

### Contoh Soal 5 — Mencari kemiringan di satu titik

**Soal:** Diberikan kardioid $r = 2 + 2\sin\theta$. Tentukan kemiringan garis singgung pada $\theta = \dfrac{\pi}{3}$.

**Penyelesaian:**

Pertama, $\dfrac{dr}{d\theta} = 2\cos\theta$.

Pada $\theta = \frac{\pi}{3}$: $\sin\theta = \frac{\sqrt3}{2}$, $\cos\theta = \frac{1}{2}$, sehingga $r = 2 + 2\left(\frac{\sqrt3}{2}\right) = 2+\sqrt3$ dan $\dfrac{dr}{d\theta} = 2\left(\frac12\right) = 1$.

$$
\frac{dy}{d\theta} = (1)\left(\frac{\sqrt3}{2}\right) + (2+\sqrt3)\left(\frac{1}{2}\right) = \frac{\sqrt3}{2} + 1 + \frac{\sqrt3}{2} = 1+\sqrt3
$$

$$
\frac{dx}{d\theta} = (1)\left(\frac{1}{2}\right) - (2+\sqrt3)\left(\frac{\sqrt3}{2}\right) = \frac12 - \frac{2\sqrt3+3}{2} = \frac{1-2\sqrt3-3}{2} = -1-\sqrt3
$$

$$
\frac{dy}{dx} = \frac{1+\sqrt3}{-1-\sqrt3} = -1
$$

**Kemiringan garis singgungnya adalah $-1$.** Titik singgungnya sendiri ada di $\left(\dfrac{2+\sqrt3}{2},\ \dfrac{2\sqrt3+3}{2}\right)$ (dihitung dari $x=r\cos\theta$, $y=r\sin\theta$).

### Contoh Soal 6 — Mencari semua garis singgung horizontal

**Soal:** Tentukan semua titik di kardioid $r = 1+\cos\theta$ dengan garis singgung horizontal, untuk $0 \le \theta < 2\pi$.

**Penyelesaian:**

$\dfrac{dr}{d\theta} = -\sin\theta$, sehingga:

$$
\frac{dy}{d\theta} = -\sin\theta\sin\theta + (1+\cos\theta)\cos\theta = -\sin^2\theta + \cos\theta + \cos^2\theta
$$

Gunakan $\cos^2\theta - \sin^2\theta = \cos2\theta$:

$$
\frac{dy}{d\theta} = \cos2\theta + \cos\theta
$$

Set $=0$, lalu ubah $\cos2\theta = 2\cos^2\theta - 1$:

$$
2\cos^2\theta - 1 + \cos\theta = 0 \quad\Rightarrow\quad 2\cos^2\theta + \cos\theta - 1 = 0
$$

Misalkan $c = \cos\theta$, faktorkan:

$$
2c^2 + c - 1 = 0 \quad\Rightarrow\quad (2c-1)(c+1) = 0 \quad\Rightarrow\quad c = \frac12 \ \text{atau}\ c=-1
$$

Jadi $\theta = \dfrac{\pi}{3},\ \dfrac{5\pi}{3}$ (dari $\cos\theta=\frac12$), atau $\theta = \pi$ (dari $\cos\theta=-1$).

**Cek apakah $dx/d\theta \neq 0$ di titik-titik ini** (supaya bukan cusp):

$$
\frac{dx}{d\theta} = -\sin\theta(1+2\cos\theta)
$$

- Di $\theta=\frac{\pi}{3}$: $\sin\theta=\frac{\sqrt3}{2}\neq0$, dan $1+2\cos\theta = 1+1=2\neq0$ → **valid**, garis singgung horizontal.
- Di $\theta=\frac{5\pi}{3}$: secara simetri, juga **valid**.
- Di $\theta=\pi$: $\sin\pi = 0$, jadi $dx/d\theta = 0$ **juga** di sini → ini bukan garis singgung horizontal biasa, melainkan **titik cusp** kardioid (dan kebetulan $r(\pi) = 1+\cos\pi = 0$, jadi titik ini juga adalah pole-nya).

> Inilah kenapa langkah "cek $dx/d\theta \neq 0$" itu wajib — kalau dilewat, kamu bisa salah menganggap titik cusp sebagai garis singgung horizontal biasa.

---

## 7. INTEGRAL DALAM KOORDINAT POLAR (LUAS DAERAH)

### Konsep & Rumus Dasar

Berbeda dari Cartesian (yang menghitung luas dengan menjumlahkan "potongan persegi panjang" tipis), di polar kita menjumlahkan **potongan sektor lingkaran** tipis. Luas satu sektor lingkaran kecil dengan radius $r$ dan sudut $d\theta$ adalah $\frac12 r^2\, d\theta$ (analog dari rumus luas sektor $\frac12 r^2 \theta$).

Menjumlahkan (mengintegralkan) semua sektor tipis dari $\theta=\alpha$ sampai $\theta=\beta$:

$$
\boxed{A = \int_{\alpha}^{\beta} \frac12\, r^2\, d\theta}
$$

> ⚠️ Pastikan kamu pakai $r$ (fungsi $\theta$ dari soal), **bukan** $f(\theta)$ secara simbolik — substitusikan persamaan $r$-nya langsung sebelum mengintegralkan.

### Luas Antara Dua Kurva Polar

Kalau ada kurva luar $r_{\text{luar}}$ dan kurva dalam $r_{\text{dalam}}$ yang membentuk daerah cincin (annulus-like):

$$
\boxed{A = \int_{\alpha}^{\beta} \frac12\left(r_{\text{luar}}^2 - r_{\text{dalam}}^2\right) d\theta}
$$

### Contoh Soal 7 — Luas total kardioid

**Soal:** Hitung luas total yang dilingkupi oleh kardioid $r = 3(1+\cos\theta)$.

**Penyelesaian:** Kardioid digambar lengkap untuk $0 \le \theta \le 2\pi$, jadi:

$$
A = \int_0^{2\pi} \frac12\big[3(1+\cos\theta)\big]^2 d\theta = \frac{9}{2}\int_0^{2\pi} (1+\cos\theta)^2\, d\theta
$$

Bukakan kuadratnya:

$$
(1+\cos\theta)^2 = 1 + 2\cos\theta + \cos^2\theta
$$

Pakai identitas $\cos^2\theta = \frac{1+\cos2\theta}{2}$:

$$
= 1 + 2\cos\theta + \frac12 + \frac12\cos2\theta = \frac32 + 2\cos\theta + \frac12\cos2\theta
$$

Integralkan suku per suku:

$$
\int \left(\frac32 + 2\cos\theta + \frac12\cos2\theta\right) d\theta = \frac{3\theta}{2} + 2\sin\theta + \frac14\sin2\theta
$$

Evaluasi dari $0$ ke $2\pi$ — semua suku $\sin$ akan nol di kedua batas, hanya suku $\theta$ yang menyumbang:

$$
\left[\frac{3\theta}{2}\right]_0^{2\pi} = \frac{3(2\pi)}{2} - 0 = 3\pi
$$

Jadi:

$$
A = \frac92 \times 3\pi = \frac{27\pi}{2}
$$

**Luas total kardioid tersebut adalah $\dfrac{27\pi}{2}$ satuan luas.**

> 💡 Pola umum: kardioid $r=a(1+\cos\theta)$ punya luas total $\frac32\pi a^2$. Cek: dengan $a=3$ → $\frac32\pi(9) = \frac{27\pi}{2}$. Cocok!

### Contoh Soal 8 — Luas loop dalam (limaçon)

**Soal:** Hitung luas loop dalam dari $r = 1+2\cos\theta$ (limaçon dengan loop dalam, karena $a=1<b=2$).

**Penyelesaian:** Dari Contoh Soal 4, kurva ini melewati pole pada $\theta=\frac{2\pi}{3}$ dan $\theta=\frac{4\pi}{3}$ — inilah batas integrasi untuk loop dalamnya (loop dalam terjadi **di antara** dua sudut ini).

$$
A = \int_{2\pi/3}^{4\pi/3} \frac12 (1+2\cos\theta)^2\, d\theta
$$

Bukakan kuadratnya:

$$
(1+2\cos\theta)^2 = 1 + 4\cos\theta + 4\cos^2\theta = 1+4\cos\theta+2(1+\cos2\theta) = 3+4\cos\theta+2\cos2\theta
$$

Integralkan:

$$
\int (3+4\cos\theta+2\cos2\theta)\, d\theta = 3\theta + 4\sin\theta + \sin2\theta
$$

Evaluasi pada batas atas $\theta=\frac{4\pi}{3}$:

$$
3\left(\frac{4\pi}{3}\right) + 4\sin\left(\frac{4\pi}{3}\right) + \sin\left(\frac{8\pi}{3}\right) = 4\pi + 4\left(-\frac{\sqrt3}{2}\right) + \frac{\sqrt3}{2} = 4\pi - 2\sqrt3 + \frac{\sqrt3}{2} = 4\pi - \frac{3\sqrt3}{2}
$$

Pada batas bawah $\theta=\frac{2\pi}{3}$:

$$
3\left(\frac{2\pi}{3}\right) + 4\sin\left(\frac{2\pi}{3}\right) + \sin\left(\frac{4\pi}{3}\right) = 2\pi + 4\left(\frac{\sqrt3}{2}\right) - \frac{\sqrt3}{2} = 2\pi + 2\sqrt3 - \frac{\sqrt3}{2} = 2\pi + \frac{3\sqrt3}{2}
$$

Selisihnya (atas $-$ bawah):

$$
\left(4\pi - \frac{3\sqrt3}{2}\right) - \left(2\pi + \frac{3\sqrt3}{2}\right) = 2\pi - 3\sqrt3
$$

Jangan lupa faktor $\frac12$ di depan integral:

$$
A = \frac12\left(2\pi - 3\sqrt3\right) = \pi - \frac{3\sqrt3}{2} \approx 0{,}5435
$$

**Luas loop dalamnya adalah $\pi - \dfrac{3\sqrt3}{2}$ satuan luas (kira-kira $0{,}54$).**

---

## 8. BONUS: PANJANG KURVA (ARC LENGTH) POLAR

Kalau dosen/soal juga menyentuh panjang kurva, ini rumusnya — diturunkan dari rumus panjang kurva parametrik $L=\int\sqrt{(dx/d\theta)^2+(dy/d\theta)^2}\,d\theta$, lalu disederhanakan memakai identitas $\sin^2+\cos^2=1$:

$$
\boxed{L = \int_{\alpha}^{\beta} \sqrt{r^2 + \left(\dfrac{dr}{d\theta}\right)^2}\; d\theta}
$$

**Cek cepat:** untuk lingkaran $r=a$ (konstan, jadi $dr/d\theta=0$), rumus ini memberi $L=\int_0^{2\pi} \sqrt{a^2}\,d\theta = 2\pi a$ — sesuai keliling lingkaran. ✅ Ini cara bagus mengecek apakah rumus ditulis/diingat dengan benar.

---

## 9. RANGKUMAN RUMUS (CHEAT SHEET)

| Kategori | Rumus |
|---|---|
| Polar → Cartesian | $x=r\cos\theta,\quad y=r\sin\theta$ |
| Cartesian → Polar | $r=\sqrt{x^2+y^2},\quad \theta=\tan^{-1}(y/x)$ *(±π sesuai kuadran)* |
| Garis | $\theta=\beta$ (lewat origin); $r\cos\theta=a$ (vertikal); $r\sin\theta=b$ (horizontal) |
| Lingkaran pusat origin | $r=a$ |
| Lingkaran pusat $(a,0)$ | $r=2a\cos\theta$ |
| Lingkaran pusat $(0,b)$ | $r=2b\sin\theta$ |
| Kardioid | $r=a\pm a\cos\theta$ atau $a\pm a\sin\theta$ |
| Limaçon (loop dalam) | $r=a\pm b\cos\theta,\ a<b$ |
| Limaçon (tanpa loop) | $r=a\pm b\cos\theta,\ a>b$ |
| Titik potong pole | Set $r=0$, selesaikan $\theta$ |
| **Turunan** $dy/dx$ | $\dfrac{(dr/d\theta)\sin\theta + r\cos\theta}{(dr/d\theta)\cos\theta - r\sin\theta}$ |
| **Luas** satu kurva | $A=\displaystyle\int_\alpha^\beta \tfrac12 r^2\, d\theta$ |
| **Luas** antar kurva | $A=\displaystyle\int_\alpha^\beta \tfrac12 (r_{\text{luar}}^2-r_{\text{dalam}}^2)\, d\theta$ |
| Panjang kurva | $L=\displaystyle\int_\alpha^\beta \sqrt{r^2+(dr/d\theta)^2}\, d\theta$ |

---

## 10. LATIHAN MANDIRI

Coba kerjakan dulu sebelum melihat kunci jawaban di bagian paling bawah.

1. Konversikan $\left(6, \dfrac{5\pi}{6}\right)$ (polar) ke Cartesian.
2. Konversikan $(4, -4)$ (Cartesian) ke polar.
3. Identifikasi jenis kurva $r = 3 - 5\sin\theta$ (kardioid / limaçon loop dalam / limaçon tanpa loop?), dan jika ada, tentukan sudut saat kurva melewati pole.
4. Tentukan kemiringan garis singgung kurva $r = 2\theta$ (spiral) di $\theta = \dfrac{\pi}{2}$. *(Petunjuk: $dr/d\theta = 2$, konstan.)*
5. Hitung luas satu putaran penuh kurva $r = 4\sin\theta$ (lingkaran).
6. Hitung luas daerah yang berada di dalam $r=3$ dan di luar $r = 3 - 3\cos\theta$ (kamu perlu cari batas $\theta$ perpotongan dua kurva ini dulu).

### Kunci Jawaban Singkat

1. $x = 6\cos(5\pi/6) = -3\sqrt3$, $y=6\sin(5\pi/6)=3$ → $(-3\sqrt3,\ 3)$
2. $r=\sqrt{32}=4\sqrt2$; $\theta=\tan^{-1}(-1)=-\pi/4$ (sudah benar kuadran IV, tidak perlu +π) → $\left(4\sqrt2, -\dfrac{\pi}{4}\right)$
3. $a=3,\ b=5 \Rightarrow a<b$ → **limaçon dengan loop dalam**. Pole: $3-5\sin\theta=0 \Rightarrow \sin\theta=3/5 \Rightarrow \theta=\sin^{-1}(0{,}6)\approx 0{,}6435$ rad dan $\theta\approx \pi-0{,}6435$ rad.
4. $dy/d\theta = 2\sin\theta+2\theta\cos\theta$, $dx/d\theta=2\cos\theta-2\theta\sin\theta$. Di $\theta=\pi/2$: $dy/d\theta=2(1)+2(\pi/2)(0)=2$; $dx/d\theta=2(0)-2(\pi/2)(1)=-\pi$. Slope $=2/(-\pi)=-2/\pi$.
5. Lingkaran radius $2$ (karena $2b=4\Rightarrow b=2$) → Luas $=\pi(2)^2=4\pi$. *(Cek dengan integral: $A=\int_0^\pi \frac12(4\sin\theta)^2 d\theta = 4\pi$ ✓)*
6. Cari perpotongan: $3 = 3-3\cos\theta \Rightarrow \cos\theta=0 \Rightarrow \theta=\pi/2, 3\pi/2$. Luas $=\int_{\pi/2}^{3\pi/2}\frac12\left[3^2-(3-3\cos\theta)^2\right]d\theta$. Setelah dibuka dan diintegralkan, hasilnya $= \dfrac{9\pi}{2} - 18$ *(silakan verifikasi langkah integralnya sendiri sebagai latihan tambahan — proses sama seperti Contoh Soal 8)*.

---

*Modul ini disusun untuk membantu pemahaman bertahap: konsep dasar → konversi → grafik → turunan → integral. Kalau ada bagian yang masih kurang jelas atau ingin ditambah contoh soal jenis tertentu (misalnya soal yang menggabungkan turunan dan luas sekaligus, yang biasanya muncul di UAS), tinggal bilang saja, Profesor.*
