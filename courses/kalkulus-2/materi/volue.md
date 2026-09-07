# MODUL BELAJAR (LANJUTAN) — VOLUME DENGAN KOORDINAT POLAR & TATA CARA MENGGAMBAR GRAFIK POLAR

> Modul ini melengkapi *Modul_Koordinat_Polar.md* sebelumnya. Bagian A membahas penerapan koordinat polar pada integral lipat dua untuk menghitung **volume**. Bagian B membahas **prosedur sistematis** untuk menggambar kurva polar dari nol, termasuk jenis kurva yang belum dibahas di modul pertama (rose curve, lemniscate, spiral).

---

## DAFTAR ISI

**PART A — Volume dengan Koordinat Polar**
1. Kapan Koordinat Polar Dipakai untuk Volume?
2. Elemen Luas $dA = r\,dr\,d\theta$ — Dari Mana Asalnya?
3. Rumus Volume & Prosedur Konversi
4. Contoh Soal Volume
5. Bonus: Volume Antara Dua Permukaan

**PART B — Tata Cara Menggambar Grafik Kurva Polar**
6. Mengenali Bentuk Kurva (Tabel Lengkap)
7. Tiga Uji Simetri
8. Prosedur Langkah-demi-Langkah Menggambar
9. Contoh Penerapan Lengkap: Menggambar $r=2\sin(3\theta)$
10. Rangkuman & Tips Cepat

---

# PART A — VOLUME DENGAN KOORDINAT POLAR

## 1. Kapan Koordinat Polar Dipakai untuk Volume?

Topik ini muncul dari **integral lipat dua** (*double integral*), yang dipakai untuk menghitung volume di bawah suatu permukaan $z=f(x,y)$, di atas suatu daerah $D$ pada bidang-$xy$:

$$
V = \iint_D f(x,y)\, dA
$$

Kalau daerah $D$ berbentuk lingkaran, sektor, atau cincin (*annulus*) — bentuk yang "natural" dalam radius dan sudut — menghitungnya langsung di Cartesian sering menghasilkan integral yang berat (banyak butuh substitusi trigonometri). Mengonversi ke polar membuat batas integrasi jadi jauh lebih sederhana: cukup rentang $r$ dan rentang $\theta$.

**Ciri-ciri soal yang "minta dikonversi ke polar":**
- Daerah berbentuk piringan penuh atau sebagian, misalnya $x^2+y^2 \le a^2$
- Daerah berbentuk cincin, misalnya $a^2 \le x^2+y^2 \le b^2$
- Fungsi yang diintegralkan mengandung bentuk $x^2+y^2$ atau $\sqrt{x^2+y^2}$

## 2. Elemen Luas $dA = r\,dr\,d\theta$ — Dari Mana Asalnya?

Bagian ini sering dihafal mentah-mentah tanpa dipahami, padahal asalnya cukup intuitif.

Saat kita membagi daerah polar menjadi potongan-potongan kecil menggunakan garis radius (konstan $r$) dan garis sudut (konstan $\theta$), setiap potongan kecil itu **bukan** persegi panjang sempurna — melainkan potongan kecil yang menyerupai trapesium melengkung.

Potongan kecil ini punya:
- Panjang sisi "radial" $\approx dr$
- Panjang sisi "melengkung" $\approx r\,d\theta$ *(karena panjang busur = radius × sudut)*

Jadi luas potongan kecil ini $\approx (dr)(r\,d\theta) = r\,dr\,d\theta$ — **bukan** $dr\,d\theta$ saja. Faktor tambahan $r$ inilah yang **paling sering terlupakan** saat mengonversi integral lipat dua ke polar.

$$
\boxed{dA = r\, dr\, d\theta}
$$

> ⚠️ **Kesalahan paling umum:** menulis $\displaystyle\iint f(x,y)\,dx\,dy = \iint f(r\cos\theta,r\sin\theta)\,dr\,d\theta$ — ini **salah**, karena lupa mengalikan dengan $r$. Yang benar selalu ada faktor $r$ ekstra di depan $dr\,d\theta$.

## 3. Rumus Volume & Prosedur Konversi

$$
\boxed{V = \int_{\alpha}^{\beta}\int_{h_1(\theta)}^{h_2(\theta)} f(r\cos\theta,\, r\sin\theta)\cdot r \;dr\,d\theta}
$$

**Prosedur konversi langkah-demi-langkah:**

1. **Bayangkan/gambar daerah $D$** di bidang-$xy$ — ini langkah paling penting, jangan dilewat.
2. **Tentukan rentang $\theta$** (dari $\alpha$ sampai $\beta$) — sudut mana saja yang "menyapu" daerah tersebut.
3. **Tentukan rentang $r$** sebagai fungsi $\theta$ — dari batas dalam $h_1(\theta)$ ke batas luar $h_2(\theta)$.
4. **Substitusikan** $x=r\cos\theta,\ y=r\sin\theta$ ke dalam $f(x,y)$.
5. **Jangan lupa kalikan dengan $r$** (elemen luas), baru integralkan. Urutan integrasi biasanya dari dalam ke luar: $dr$ dulu, lalu $d\theta$.

## 4. Contoh Soal Volume

### Contoh Soal 1 — Volume di bawah paraboloid, di atas piringan penuh

**Soal:** Hitung volume benda pejal yang dibatasi di atas oleh $z=9-x^2-y^2$ dan di bawah oleh bidang $z=0$.

**Penyelesaian:**

Daerah $D$ adalah lingkaran tempat $z=0$, yaitu saat $9-x^2-y^2=0 \Rightarrow x^2+y^2=9$ — piringan radius $3$ berpusat di origin.

Dalam polar: $\theta\in[0,2\pi]$, $r\in[0,3]$. Substitusi $x^2+y^2=r^2$:

$$
V=\int_0^{2\pi}\int_0^3(9-r^2)\cdot r\;dr\,d\theta = \int_0^{2\pi}\int_0^3(9r-r^3)\,dr\,d\theta
$$

Integralkan dulu terhadap $r$:

$$
\int_0^3(9r-r^3)\,dr=\left[\frac{9r^2}{2}-\frac{r^4}{4}\right]_0^3=\frac{81}{2}-\frac{81}{4}=\frac{81}{4}
$$

Lalu terhadap $\theta$:

$$
V=\int_0^{2\pi}\frac{81}{4}\,d\theta=\frac{81}{4}\times2\pi=\frac{81\pi}{2}
$$

**Volume benda pejal tersebut adalah $\dfrac{81\pi}{2}$ satuan volume.**

### Contoh Soal 2 — Volume di atas daerah sektor (bukan piringan penuh)

**Soal:** Hitung volume benda pejal di bawah $z=x^2+y^2$, di atas piringan $x^2+y^2\le4$, tetapi **hanya** pada kuadran pertama ($x\ge0,\ y\ge0$).

**Penyelesaian:**

Karena hanya kuadran I: $\theta\in\left[0,\dfrac{\pi}{2}\right]$, dan $r\in[0,2]$.

$$
V=\int_0^{\pi/2}\int_0^2 r^2\cdot r\;dr\,d\theta=\int_0^{\pi/2}\int_0^2 r^3\,dr\,d\theta
$$

$$
\int_0^2 r^3\,dr=\left[\frac{r^4}{4}\right]_0^2=\frac{16}{4}=4
$$

$$
V=\int_0^{\pi/2}4\,d\theta=4\times\frac{\pi}{2}=2\pi
$$

**Volume bagian sektor ini adalah $2\pi$ satuan volume.**

> 💡 **Cek kewajaran:** kalau soal yang sama dikerjakan untuk piringan penuh ($\theta:0\to2\pi$, bukan hanya kuadran I), hasilnya akan menjadi $4\times$ lipat dari hasil di atas — masuk akal, karena kuadran I memang hanya $\frac14$ dari piringan penuh.

## 5. Bonus: Volume Antara Dua Permukaan

Kalau benda pejal dibatasi oleh dua permukaan, $z=f(x,y)$ di atas dan $z=g(x,y)$ di bawah, dengan $f\ge g$ pada daerah $D$:

$$
V=\iint_D\big[f(x,y)-g(x,y)\big]\,dA = \int_\alpha^\beta\int_{h_1(\theta)}^{h_2(\theta)}\big[f(r\cos\theta,r\sin\theta)-g(r\cos\theta,r\sin\theta)\big]\cdot r\;dr\,d\theta
$$

Prosedurnya identik dengan sebelumnya — hanya fungsi yang diintegralkan berubah menjadi selisih dua permukaan.

---

# PART B — TATA CARA MENGGAMBAR GRAFIK KURVA POLAR

## 6. Mengenali Bentuk Kurva (Tabel Lengkap)

Sebelum menggambar, langkah pertama selalu: **kenali dulu jenis kurvanya** dari bentuk persamaan. Ini langsung memberi gambaran kasar bentuk grafiknya tanpa perlu plot titik satu per satu.

| Bentuk Persamaan | Nama Kurva | Ciri Bentuk |
|---|---|---|
| θ = β | Garis | Lurus melalui origin |
| r cos θ = a atau r sin θ = b | Garis | Vertikal / horizontal |
| r = a | Lingkaran | Pusat origin, radius \|a\| |
| r = 2a cos θ atau r = 2b sin θ | Lingkaran | Pusat di sumbu x/y, menyentuh origin |
| r = a ± a cos θ atau r = a ± a sin θ | Kardioid | Bentuk hati, 1 lekukan di pole |
| r = a ± b cos θ, a < b | Limaçon loop dalam | Ada loop kecil di tengah |
| r = a ± b cos θ, a > b | Limaçon tanpa loop | Oval tidak simetris |
| r = a cos(nθ) atau r = a sin(nθ) | Rose curve | n kelopak jika n ganjil, 2n jika n genap |
| r² = a² cos(2θ) atau r² = a² sin(2θ) | Lemniscate | Bentuk angka 8 |
| r = aθ | Spiral Archimedes | Spiral keluar terus |

> 💡 **Catatan rose curve:** jumlah kelopak $=n$ jika $n$ ganjil, atau $2n$ jika $n$ genap. Contoh: $r=3\sin(2\theta)$ punya $4$ kelopak (karena $n=2$, genap). $r=3\sin(3\theta)$ punya $3$ kelopak (karena $n=3$, ganjil).

## 7. Tiga Uji Simetri

Sebelum membuat tabel titik, cek dulu simetrinya — ini menghemat banyak pekerjaan karena kamu hanya perlu menghitung separuh (atau bahkan seperempat) titik, sisanya tinggal dicerminkan.

| Uji | Cara | Simetri Terhadap |
|---|---|---|
| θ → -θ | Persamaan tetap sama? | Sumbu kutub (sumbu x) |
| θ → π - θ | Persamaan tetap sama? | Sumbu y |
| r → -r atau θ → θ + π | Persamaan tetap sama? | Pole (origin) |

**Contoh cepat:** untuk $r=3+3\cos\theta$ — ganti $\theta\to-\theta$: $\cos(-\theta)=\cos\theta$, persamaan tetap sama → **simetris terhadap sumbu kutub**. Ini cocok dengan kardioid yang memang simetris terhadap sumbu-$x$.

## 8. Prosedur Langkah-demi-Langkah Menggambar

1. **Identifikasi jenis kurva** dari tabel di Bagian 6.
2. **Lakukan uji simetri** (Bagian 7) — tentukan sumbu simetrinya kalau ada.
3. **Cari titik potong dengan pole:** set $r=0$, selesaikan untuk $\theta$.
4. **Cari $\lvert r\rvert$ maksimum:** ini "jarak terjauh" kurva dari pole, biasanya saat fungsi trigonometrinya bernilai $\pm1$.
5. **Buat tabel nilai $r$** pada sudut-sudut kunci (umumnya kelipatan $30°$ atau $45°$) dalam satu periode penuh. Cek dulu periode kurvanya — kurva rose dengan $n$ ganjil misalnya sudah lengkap hanya dengan $\theta\in[0,\pi]$, tidak perlu sampai $2\pi$.
6. **Plot titik-titiknya.** Ingat: kalau $r$ negatif pada suatu titik tabel, titik itu sebenarnya berada di **arah berlawanan** ($\theta+\pi$), bukan di arah $\theta$ aslinya.
7. **Hubungkan titik secara berurutan** sesuai urutan kenaikan $\theta$ — jangan asal sambung sembarang urutan, karena beberapa kurva (limaçon dengan loop, rose curve) "melipat" balik melalui pole beberapa kali.
8. **(Opsional) Verifikasi** dengan kalkulator grafik atau software (Desmos, GeoGebra) untuk soal yang kompleks.

## 9. Contoh Penerapan Lengkap: Menggambar $r=2\sin(3\theta)$

**Langkah 1 — Identifikasi jenis:** bentuk $r=a\sin(n\theta)$ dengan $a=2,\ n=3$ → **rose curve**. Karena $n=3$ ganjil → **3 kelopak**.

**Langkah 2 — Uji simetri:** ganti $\theta\to\pi-\theta$:

$$
\sin\big(3(\pi-\theta)\big)=\sin(3\pi-3\theta)=\sin3\pi\cos3\theta-\cos3\pi\sin3\theta=0-(-1)\sin3\theta=\sin3\theta
$$

Hasilnya sama → **simetris terhadap $\theta=\pi/2$** (sumbu-$y$).

**Langkah 3 — Titik potong pole:**

$$
0=2\sin3\theta \;\Rightarrow\; \sin3\theta=0 \;\Rightarrow\; 3\theta=0,\pi,2\pi,3\pi,\dots \;\Rightarrow\; \theta=0,\ \frac{\pi}{3},\ \frac{2\pi}{3},\ \pi,\dots
$$

**Langkah 4 — $\lvert r\rvert$ maksimum:** $\sin3\theta=\pm1$ saat $3\theta=\dfrac{\pi}{2}+k\pi$, sehingga $\theta=\dfrac{\pi}{6},\ \dfrac{\pi}{2},\ \dfrac{5\pi}{6},\dots$ — di titik-titik ini $\lvert r\rvert=2$ (jarak terjauh kelopak dari pole).

**Langkah 5 — Tabel nilai** (karena $n$ ganjil, kurva lengkap hanya butuh $\theta\in[0,\pi]$):

| $\theta$ | $0°$ | $30°$ | $60°$ | $90°$ | $120°$ | $150°$ | $180°$ |
|---|---|---|---|---|---|---|---|
| $3\theta$ | $0°$ | $90°$ | $180°$ | $270°$ | $360°$ | $450°$ | $540°$ |
| $r=2\sin3\theta$ | $0$ | $2$ | $0$ | $-2$ | $0$ | $2$ | $0$ |

**Langkah 6 & 7 — Plot dan hubungkan.** Perhatikan pola yang terbentuk:

- $\theta:0°\to60°$ → kelopak pertama: keluar dari pole, mencapai $r=2$ di $\theta=30°$, lalu balik ke pole di $\theta=60°$.
- $\theta:60°\to120°$ → karena $r$ **negatif** sepanjang interval ini, kelopak kedua justru muncul di arah **berlawanan** — efektif sekitar $\theta+180°$, yaitu mengarah ke bawah (sekitar $270°$).
- $\theta:120°\to180°$ → kelopak ketiga, mengarah ke $\theta\approx150°$.

Hasil akhirnya: tiga kelopak simetris mengarah ke $30°$, $150°$, dan $270°$ — saling berjarak $120°$ satu sama lain, konsisten dengan rumus jarak antar-kelopak $=360°/n$.

> *(Lihat visualisasi grafiknya pada chat — divisualisasikan terpisah dari modul ini supaya filenya tetap ringan dan mudah dicetak.)*

## 10. Rangkuman & Tips Cepat

**Checklist sebelum menggambar kurva polar apapun:**

- [ ] Sudah identifikasi jenis kurva dari bentuk persamaannya?
- [ ] Sudah cek tiga uji simetri?
- [ ] Sudah cari titik potong pole ($r=0$)?
- [ ] Sudah cari $\lvert r\rvert$ maksimum?
- [ ] Sudah tentukan rentang $\theta$ minimum untuk kurva lengkap (tidak selalu $2\pi$)?
- [ ] Sudah waspada terhadap nilai $r$ negatif saat plotting?

**Tabel periode minimum untuk kurva lengkap (hemat waktu menggambar):**

| Kurva | Rentang $\theta$ minimum |
|---|---|
| $r=a$ (lingkaran pusat origin) | $[0, 2\pi]$ |
| $r=2a\cos\theta$ atau $2b\sin\theta$ (lingkaran offset) | $[0, \pi]$ |
| Kardioid / Limaçon | $[0, 2\pi]$ |
| Rose curve, $n$ ganjil | $[0, \pi]$ |
| Rose curve, $n$ genap | $[0, 2\pi]$ |
| Lemniscate | $[0, 2\pi]$ *(dengan bagian yang tidak terdefinisi saat $\cos2\theta<0$ atau $\sin2\theta<0$, tergantung bentuknya)* |

---

*Modul ini melengkapi modul sebelumnya. Kalau Profesor butuh latihan tambahan khusus volume (misalnya soal dengan daerah cincin/annulus, bukan piringan penuh), atau mau dibuatkan versi cheat-sheet dua halaman gabungan dari kedua modul ini, tinggal bilang saja.*
