# Estimasi Parameter & Pengujian Hipotesis (1 & 2 Populasi)

---

## 1. Perbedaan Utama Estimasi Parameter dan Pengujian Hipotesis

Dalam statistika inferensial, terdapat dua cabang besar yang digunakan untuk menarik kesimpulan tentang populasi berdasarkan data sampel, yaitu **Estimasi Parameter** dan **Pengujian Hipotesis**.

| Karakteristik | Estimasi Parameter (Uji Parameter) | Pengujian Hipotesis |
| --- | --- | --- |
| **Tujuan Utama** | Mengestimasi atau menduga nilai riil dari parameter populasi yang tidak diketahui. | Menguji keabsahan suatu klaim, pernyataan, atau asumsi spesifik mengenai parameter populasi. |
| **Output Analisis** | Berupa **Estimasi Titik** (satu nilai tunggal, misal $\bar{x}$) atau **Estimasi Interval** (Interval Kepercayaan / *Confidence Interval*). | Berupa keputusan statistik untuk **Menolak $H_0$** atau **Gagal Menolak $H_0$** berdasarkan tingkat signifikansi ($\alpha$). |
| **Pertanyaan Inti** | *"Berapakah nilai rata-rata ($\mu$) atau proporsi ($p$) sesungguhnya dari populasi ini?"* | *"Apakah benar rata-rata populasi ($\mu$) ini sudah berubah dan lebih besar dari nilai standar lama?"* |
| **Dasar Tindakan** | Membangun batas atas dan bawah di mana parameter populasi diyakini berada di dalam rentang tersebut. | Membandingkan bukti empiris dari sampel dengan kondisi teoretis di bawah asumsi hipotesis nol. |

---

## 2. Konsep Fundamental Pengujian Hipotesis

### A. Definisi Hipotesis Statistik

Hipotesis adalah suatu pranyataan atau asumsi sementara mengenai nilai parameter populasi.

* **Hipotesis Nol ($H_0$)**: Hipotesis yang mencerminkan status quo, tidak ada perbedaan, atau tidak ada efek perlakuan. Pernyataan di dalam $H_0$ **selalu** mengandung tanda kesamaan ($=$, $\le$, atau $\ge$).
* **Hipotesis Alternatif ($H_1$ atau $H_a$)**: Hipotesis yang berlawanan dengan $H_0$ dan merupakan klaim ilmiah yang ingin dibuktikan oleh peneliti. Pernyataan di dalam $H_1$ **selalu** mengandung tanda ketidaksamaan ($\ne$, $<$, atau $>$).

### B. Matriks Kesalahan Pengujian (Type I & Type II Errors)

Pengambilan keputusan berdasarkan sampel memiliki risiko kesalahan karena keterbatasan informasi:

| Kondisi Aktual Populasi | Keputusan: Gagal Menolak $H_0$ | Keputusan: Menolak $H_0$ |
| --- | --- | --- |
| **$H_0$ Benar** | Keputusan Tepat ($1 - \alpha$) | **Kesalahan Tipe I ($\alpha$)** |
| **$H_0$ Salah** | **Kesalahan Tipe II ($\beta$)** | Keputusan Tepat ($1 - \beta$) / *Power of Test* |

* **Kesalahan Tipe I ($\alpha$)**: Menolak $H_0$ padahal kenyataannya $H_0$ benar. Nilai $\alpha$ disebut sebagai **Tingkat Signifikansi** (*Significance Level*).
* **Kesalahan Tipe II ($\beta$)**: Gagal menolak $H_0$ padahal kenyataannya $H_0$ salah.

### C. Pendekatan Pengambilan Keputusan

Terdapat dua metode matematis untuk menentukan keputusan menolak atau gagal menolak $H_0$:

#### 1. Pendekatan Nilai Kritis (*Critical Value Approach*)

Membandingkan nilai **Statistik Uji** hasil hitung data sampel dengan **Nilai Kritis** yang didapatkan dari tabel distribusi statistika berdasarkan nilai $\alpha$. Jika nilai Statistik Uji jatuh di dalam **Daerah Penolakan** (*Rejection Region*), maka $H_0$ ditolak.

#### 2. Pendekatan nilai-*p* (*p-Value Approach*)

Nilai-*p* (*p-value*) adalah tingkat probabilitas untuk mendapatkan nilai statistik uji yang sekstrim atau lebih ekstrem daripada nilai yang teramati, dengan asumsi bahwa $H_0$ adalah benar.

* Jika $\text{nilai-}p \le \alpha \rightarrow$ **Tolak $H_0$**
* Jika $\text{nilai-}p > \alpha \rightarrow$ **Gagal Menolak $H_0$**

### D. Prosedur Umum Uji Hipotesis (6 Langkah Linear)

1. Formulasikan $H_0$ dan $H_1$ secara matematis.
2. Tentukan tingkat signifikansi ($\alpha$).
3. Pilih jenis statistik uji yang sesuai dan definisikan batas **Daerah Penolakan** (Nilai Kritis).
4. Hitung nilai Statistik Uji dari data sampel.
5. Ambil keputusan statistik (Bandingkan nilai hitung dengan nilai kritis atau bandingkan nilai-*p* dengan $\alpha$).
6. Tuliskan kesimpulan ilmiah secara kontekstual sesuai masalah.

---

## 3. Pengujian Parameter 1 Populasi

### A. Uji Rata-rata ($\mu$) — Varians Populasi ($\sigma^2$) Diketahui

Digunakan jika ukuran sampel bebas ($n$ besar atau kecil) asalkan asumsi populasi berdistribusi normal dan nilai standar deviasi populasi ($\sigma$) diketahui secara pasti.

#### Rumus Statistik Uji ($Z_{\text{hitung}}$):

$$Z = \frac{\bar{x} - \mu_0}{\frac{\sigma}{\sqrt{n}}}$$

#### Variabel:

* $Z$: Nilai standar Z (Statistik Uji).
* $\bar{x}$: Rata-rata matematis sampel data.
* $\mu_0$: Nilai rata-rata populasi yang dihipotesiskan pada $H_0$.
* $\sigma$: Standar deviasi (simpangan baku) populasi asli.
* $n$: Ukuran atau jumlah sampel data.

#### Kriteria Daerah Penolakan $H_0$:

* **Uji Satu Arah Kiri** ($H_1: \mu < \mu_0$) $\rightarrow$ Tolak $H_0$ jika $Z < -Z_{\alpha}$
* **Uji Satu Arah Kanan** ($H_1: \mu > \mu_0$) $\rightarrow$ Tolak $H_0$ jika $Z > Z_{\alpha}$
* **Uji Dua Arah** ($H_1: \mu \ne \mu_0$) $\rightarrow$ Tolak $H_0$ jika $Z < -Z_{\alpha/2}$ atau $Z > Z_{\alpha/2}$

---

#### Contoh Soal 1 (Uji Z - Dua Arah):

Sebuah perusahaan lampu mengklaim bahwa daya tahan produk lampu LED mereka memiliki rata-rata $\mu = 800$ jam dengan standar deviasi populasi $\sigma = 40$ jam. Seorang peneliti mengambil sampel acak sebanyak $n = 30$ lampu dan menemukan bahwa rata-rata daya tahannya adalah $\bar{x} = 788$ jam. Ujilah apakah daya tahan lampu LED tersebut sudah berubah dari klaim perusahaan menggunakan $\alpha = 5\%$.

#### Solusi Soal 1:

**Langkah 1 (Formulasi Hipotesis):**

* $H_0: \mu = 800$ jam (Daya tahan rata-rata lampu sama dengan klaim awal)
* $H_1: \mu \ne 800$ jam (Daya tahan rata-rata lampu sudah berubah/tidak sama)

**Langkah 2 (Tingkat Signifikansi):**

* $\alpha = 0,05$
* Karena uji dua arah, tentukan $\alpha/2 = 0,025$.

**Langkah 3 (Nilai Kritis & Daerah Penolakan):**

* Dari tabel Z normal standar, nilai $Z_{0,025} = 1,96$.
* Daerah Penolakan: Tolak $H_0$ jika $Z < -1,96$ atau $Z > 1,96$.

**Langkah 4 (Perhitungan Statistik Uji):**

* $\bar{x} = 788$, $\mu_0 = 800$, $\sigma = 40$, $n = 30$.

$$Z = \frac{788 - 800}{\frac{40}{\sqrt{30}}} = \frac{-12}{\frac{40}{5,477}} = \frac{-12}{7,303} = -1,643$$



**Langkah 5 (Keputusan Statistik):**

* Nilai $Z_{\text{hitung}} = -1,643$ berada di luar daerah penolakan (karena $-1,643 > -1,96$).
* Maka, keputusan statistik adalah **Gagal Menolak $H_0$**.

**Langkah 6 (Kesimpulan):**

* Dengan tingkat signifikansi $5\%$, data sampel tidak memberikan bukti yang cukup untuk menyatakan bahwa rata-rata daya tahan lampu LED telah berubah dari klaim perusahaan sebesar $800$ jam.

---

### B. Uji Rata-rata ($\mu$) — Varians Populasi ($\sigma^2$) Tidak Diketahui

Digunakan jika nilai simpangan baku populasi ($\sigma$) tidak diketahui, sehingga posisinya digantikan oleh simpangan baku sampel ($s$). Pengujian ini menggunakan distribusi Student's *t*.

#### Rumus Statistik Uji ($t_{\text{hitung}}$):

$$t = \frac{\bar{x} - \mu_0}{\frac{s}{\sqrt{n}}}$$

#### Variabel:

* $t$: Nilai statistik uji $t$ yang mengikuti derajat bebas (*degree of freedom*).
* $s$: Standar deviasi sampel data $\rightarrow s = \sqrt{\frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n - 1}}$.
* $df$: Derajat bebas pengujian $\rightarrow df = n - 1$.

#### Kriteria Daerah Penolakan $H_0$:

* **Uji Satu Arah Kiri** ($H_1: \mu < \mu_0$) $\rightarrow$ Tolak $H_0$ jika $t < -t_{(\alpha, \, df)}$
* **Uji Satu Arah Kanan** ($H_1: \mu > \mu_0$) $\rightarrow$ Tolak $H_0$ jika $t > t_{(\alpha, \, df)}$
* **Uji Dua Arah** ($H_1: \mu \ne \mu_0$) $\rightarrow$ Tolak $H_0$ jika $t < -t_{(\alpha/2, \, df)}$ atau $t > t_{(\alpha/2, \, df)}$

---

#### Contoh Soal 2 (Uji t - Satu Arah Kanan):

Manajer kendali mutu menyatakan bahwa mesin pengisi minuman otomatis rata-rata mengeluarkan volume lebih dari $250$ ml per botol. Diambil sampel acak sebanyak $n = 16$ botol, diperoleh rata-rata sampel $\bar{x} = 254$ ml dan standar deviasi sampel $s = 8$ ml. Ujilah klaim manajer tersebut dengan tingkat signifikansi $\alpha = 1\%$.

#### Solusi Soal 2:

**Langkah 1 (Formulasi Hipotesis):**

* $H_0: \mu \le 250$ ml
* $H_1: \mu > 250$ ml (Klaim manajer bahwa volume rata-rata di atas $250$ ml)

**Langkah 2 (Tingkat Signifikansi):**

* $\alpha = 0,01$

**Langkah 3 (Nilai Kritis & Daerah Penolakan):**

* Hitung derajat bebas: $df = n - 1 = 16 - 1 = 15$.
* Berdasarkan tabel distribusi $t$ pada $\alpha = 0,01$ dan $df = 15$, diperoleh nilai kritis $t_{(0,01, \, 15)} = 2,602$.
* Daerah Penolakan: Tolak $H_0$ jika $t > 2,602$.

**Langkah 4 (Perhitungan Statistik Uji):**


$$t = \frac{254 - 250}{\frac{8}{\sqrt{16}}} = \frac{4}{\frac{8}{4}} = \frac{4}{2} = 2,000$$

**Langkah 5 (Keputusan Statistik):**

* Nilai $t_{\text{hitung}} = 2,000$ lebih kecil daripada nilai kritis $2,602$ ($2,000 < 2,602$).
* Maka, keputusan statistik adalah **Gagal Menolak $H_0$**.

**Langkah 6 (Kesimpulan):**

* Pada tingkat signifikansi $1\%$, data sampel belum memberikan bukti empiris yang cukup kuat untuk mendukung klaim manajer bahwa rata-rata volume minuman yang dikeluarkan mesin di atas $250$ ml.

---

### C. Uji Proporsi Populasi ($p$)

Digunakan untuk menguji nilai persentase atau rasio biner binominal pada satu populasi dengan asumsi ukuran sampel cukup besar ($np_0 \ge 5$ dan $n(1-p_0) \ge 5$), sehingga dapat didekati dengan distribusi normal Z.

#### Rumus Statistik Uji ($Z_{\text{hitung}}$):

$$Z = \frac{\hat{p} - p_0}{\sqrt{\frac{p_0(1 - p_0)}{n}}}$$

#### Variabel:

* $\hat{p}$: Proporsi sukses pada sampel data $\rightarrow \hat{p} = \frac{x}{n}$ ($x$ adalah jumlah kejadian sukses).
* $p_0$: Nilai proporsi populasi teoretis yang dihipotesiskan pada $H_0$.

---

### D. Uji Varians Populasi ($\sigma^2$)

Digunakan jika fokus pengujian tertuju pada tingkat penyebaran, konsistensi, atau variabilitas dari suatu data tunggal. Pengujian ini menggunakan distribusi Chi-Square ($\chi^2$).

#### Rumus Statistik Uji ($\chi^2_{\text{hitung}}$):

$$\chi^2 = \frac{(n - 1)s^2}{\sigma_0^2}$$

#### Variabel:

* $\chi^2$: Statistik uji Chi-Square dengan derajat bebas $df = n - 1$.
* $\sigma_0^2$: Nilai varians populasi teoretis yang dihipotesiskan pada $H_0$.

#### Kriteria Daerah Penolakan $H_0$:

* **Uji Satu Arah Kiri** ($H_1: \sigma^2 < \sigma_0^2$) $\rightarrow$ Tolak $H_0$ jika $\chi^2 < \chi^2_{(1-\alpha, \, df)}$
* **Uji Satu Arah Kanan** ($H_1: \sigma^2 > \sigma_0^2$) $\rightarrow$ Tolak $H_0$ jika $\chi^2 > \chi^2_{(\alpha, \, df)}$
* **Uji Dua Arah** ($H_1: \sigma^2 \ne \sigma_0^2$) $\rightarrow$ Tolak $H_0$ jika $\chi^2 < \chi^2_{(1-\alpha/2, \, df)}$ atau $\chi^2 > \chi^2_{(\alpha/2, \, df)}$

---

## 4. Pengujian Hipotesis Parameter 2 Populasi

### A. Uji Perbandingan Dua Rata-rata ($\mu_1 - \mu_2$) — Sampel Independen

Sampel independen berarti data pada sampel grup pertama tidak memiliki ketergantungan atau keterkaitan dengan data pada sampel grup kedua.

#### Kasus 1: Varians Populasi ($\sigma_1^2$ dan $\sigma_2^2$) Diketahui

Sangat jarang terjadi di realitas, menggunakan uji Z dua populasi.

##### Rumus Statistik Uji ($Z_{\text{hitung}}$):

$$Z = \frac{(\bar{x}_1 - \bar{x}_2) - D_0}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}$$

##### Variabel:

* $D_0$: Selisih rata-rata teoretis populasi yang dihipotesiskan (umumnya bernilai $0$).

---

#### Kasus 2: Varians Populasi Tidak Diketahui, namun Diasumsikan Sama ($\sigma_1^2 = \sigma_2^2$)

Menggunakan metode varians gabungan (*pooled variance*) dengan distribusi $t$.

##### Rumus Statistik Uji ($t_{\text{hitung}}$):

$$t = \frac{(\bar{x}_1 - \bar{x}_2) - D_0}{s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$$

##### Rumus Varians Gabungan ($s_p^2$):

$$s_p^2 = \frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}$$

$$s_p = \sqrt{s_p^2}$$

##### Derajat Bebas (*df*):

$$df = n_1 + n_2 - 2$$

---

#### Kasus 3: Varians Populasi Tidak Diketahui dan Diasumsikan Berbeda ($\sigma_1^2 \ne \sigma_2^2$)

Menggunakan pendekatan metode *Smith-Satterthwaite* untuk menghitung nilai modifikasi derajat bebas.

##### Rumus Statistik Uji ($t_{\text{hitung}}$):

$$t = \frac{(\bar{x}_1 - \bar{x}_2) - D_0}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$

##### Rumus Modifikasi Derajat Bebas (*df*):

$$df = \frac{\left( \frac{s_1^2}{n_1} + \frac{s_2^2}{n_2} \right)^2}{\frac{\left(\frac{s_1^2}{n_1}\right)^2}{n_1 - 1} + \frac{\left(\frac{s_2^2}{n_2}\right)^2}{n_2 - 1}}$$


*(Nilai hasil perhitungan df selalu dibulatkan ke bawah ke bilangan bulat terdekat)*

---

#### Contoh Soal 3 (Uji t Independen - Kasus $\sigma_1^2 = \sigma_2^2$):

Sebuah metode pengajaran baru diterapkan pada kelas A, sementara kelas B menggunakan metode konvensional. Di akhir semester, dilakukan ujian dengan hasil sebagai berikut:

* Kelas A ($n_1 = 12$ siswa): $\bar{x}_1 = 85$, $s_1 = 6$
* Kelas B ($n_2 = 10$ siswa): $\bar{x}_2 = 79$, $s_2 = 5$

Dengan asumsi varians kedua populasi berdistribusi normal dan bernilai sama, ujilah apakah rata-rata nilai ujian metode baru (Kelas A) lebih tinggi secara signifikan daripada metode konvensional (Kelas B) pada tingkat $\alpha = 5\%$.

#### Solusi Soal 3:

**Langkah 1 (Hipotesis):**

* $H_0: \mu_1 - \mu_2 \le 0$ (Rata-rata nilai kelas A tidak lebih besar dari kelas B)
* $H_1: \mu_1 - \mu_2 > 0$ (Rata-rata nilai kelas A lebih tinggi dari kelas B)

**Langkah 2 (Signifikansi):**

* $\alpha = 0,05$

**Langkah 3 (Nilai Kritis & Batas Keputusan):**

* $df = n_1 + n_2 - 2 = 12 + 10 - 2 = 20$.
* Berdasarkan tabel distribusi $t$ untuk uji satu arah kanan pada $\alpha = 0,05$ dan $df = 20$, diperoleh $t_{(0,05, \, 20)} = 1,725$.
* Daerah Penolakan: Tolak $H_0$ jika $t > 1,725$.

**Langkah 4 (Perhitungan Statistik Uji):**

1. *Hitung Varians Gabungan ($s_p^2$):*

$$s_p^2 = \frac{(12 - 1)(6^2) + (10 - 1)(5^2)}{12 + 10 - 2} = \frac{(11)(36) + (9)(25)}{20} = \frac{396 + 225}{20} = \frac{621}{20} = 31,05$$


$$s_p = \sqrt{31,05} = 5,572$$


2. *Hitung Nilai $t_{\text{hitung}}$ ($D_0 = 0$):*

$$t = \frac{(85 - 79) - 0}{5,572 \sqrt{\frac{1}{12} + \frac{1}{10}}} = \frac{6}{5,572 \sqrt{0,0833 + 0,1}} = \frac{6}{5,572 \sqrt{0,1833}} = \frac{6}{5,572 \times 0,428} = \frac{6}{2,385} = 2,516$$



**Langkah 5 (Keputusan Statistik):**

* Nilai $t_{\text{hitung}} = 2,516$ jatuh di dalam daerah penolakan ($2,516 > 1,725$).
* Keputusan: **Tolak $H_0$**.

**Langkah 6 (Kesimpulan):**

* Pada tingkat signifikansi $5\%$, data memberikan bukti kuat untuk menyimpulkan bahwa metode pengajaran baru menghasilkan rata-rata nilai ujian siswa yang lebih tinggi secara signifikan dibandingkan metode pengajaran konvensional.

---

### B. Uji Perbandingan Rata-rata Berpasangan (*Paired Samples t-test*)

Digunakan jika elemen data pada sampel pertama dan sampel kedua saling berhubungan atau berpasangan secara langsung (misal desain penelitian *Sebelum vs Sesudah* perlakuan pada subjek yang sama).

#### Rumus Statistik Uji ($t_{\text{hitung}}$):

$$t = \frac{\bar{d} - D_0}{\frac{s_d}{\sqrt{n}}}$$

#### Rumus Selisih Data ($d_i$):

$$d_i = x_{1i} - x_{2i}$$

#### Rumus Rata-rata Selisih ($\bar{d}$) dan Standar Deviasi Selisih ($s_d$):

$$\bar{d} = \frac{\sum_{i=1}^{n} d_i}{n}$$

$$s_d = \sqrt{\frac{\sum_{i=1}^{n}(d_i - \bar{d})^2}{n - 1}}$$

#### Derajat Bebas (*df*):

$$df = n - 1 \quad \text{(di mana } n \text{ adalah total jumlah pasangan data)}$$

---

#### Contoh Soal 4 (Uji t Berpasangan):

Sebuah program pelatihan kebugaran diuji untuk melihat efeknya terhadap penurunan berat badan. Diambil sampel acak sebanyak $5$ peserta, berat badan mereka sebelum dan sesudah program diukur (dalam kg):

| Peserta | Sebelum ($X_1$) | Sesudah ($X_2$) |
| --- | --- | --- |
| 1 | 80 | 76 |
| 2 | 75 | 74 |
| 3 | 92 | 87 |
| 4 | 68 | 66 |
| 5 | 85 | 81 |

Ujilah dengan $\alpha = 5\%$ apakah program pelatihan tersebut efektif menurunkan berat badan peserta ($D_0 = 0$).

#### Solusi Soal 4:

**Langkah 1 (Hipotesis):**

* $H_0: \mu_d \le 0$ (Program pelatihan tidak menurunkan berat badan)
* $H_1: \mu_d > 0$ (Program pelatihan efektif menurunkan berat badan, karena selisih $X_1 - X_2 > 0$)

**Langkah 2 (Signifikansi):**

* $\alpha = 0,05$

**Langkah 3 (Nilai Kritis & Batas Keputusan):**

* $df = n - 1 = 5 - 1 = 4$.
* Nilai tabel $t_{(0,05, \, 4)} = 2,132$.
* Daerah Penolakan: Tolak $H_0$ jika $t > 2,132$.

**Langkah 4 (Perhitungan Statistik Uji):**

1. *Hitung nilai $d_i$ untuk masing-masing baris:*
* $d_1 = 80 - 76 = 4$
* $d_2 = 75 - 74 = 1$
* $d_3 = 92 - 87 = 5$
* $d_4 = 68 - 66 = 2$
* $d_5 = 85 - 81 = 4$


2. *Hitung rata-rata selisih ($\bar{d}$):*

$$\bar{d} = \frac{4 + 1 + 5 + 2 + 4}{5} = \frac{16}{5} = 3,2\text{ kg}$$


3. *Hitung Standar Deviasi Selisih ($s_d$):*

$$\sum(d_i - \bar{d})^2 = (4-3,2)^2 + (1-3,2)^2 + (5-3,2)^2 + (2-3,2)^2 + (4-3,2)^2$$


$$= (0,8)^2 + (-2,2)^2 + (1,8)^2 + (-1,2)^2 + (0,8)^2 = 0,64 + 4,84 + 3,24 + 1,44 + 0,64 = 10,8$$


$$s_d = \sqrt{\frac{10,8}{5 - 1}} = \sqrt{\frac{10,8}{4}} = \sqrt{2,7} = 1,643\text{ kg}$$


4. *Hitung Nilai Statistik Uji $t$:*

$$t = \frac{3,2 - 0}{\frac{1,643}{\sqrt{5}}} = \frac{3,2}{\frac{1,643}{2,236}} = \frac{3,2}{0,735} = 4,354$$



**Langkah 5 (Keputusan Statistik):**

* Nilai $t_{\text{hitung}} = 4,354$ jauh lebih besar daripada nilai kritis $2,132$ ($4,354 > 2,132$).
* Keputusan: **Tolak $H_0$**.

**Langkah 6 (Kesimpulan):**

* Pada tingkat signifikansi $5\%$, dapat disimpulkan bahwa program pelatihan kebugaran tersebut terbukti efektif dalam menurunkan berat badan peserta secara signifikan.

---

### C. Uji Perbandingan Dua Proporsi Populasi ($p_1 - p_2$)

Digunakan untuk menguji apakah ada perbedaan persentase kesuksesan yang signifikan antara dua kelompok populasi yang terpisah.

#### Rumus Statistik Uji ($Z_{\text{hitung}}$):

$$Z = \frac{(\hat{p}_1 - \hat{p}_2) - 0}{\sqrt{\bar{p}(1 - \bar{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}$$

#### Rumus Estimasi Proporsi Gabungan ($\bar{p}$):

$$\bar{p} = \frac{x_1 + x_2}{n_1 + n_2}$$

#### Variabel:

* $x_1, x_2$: Jumlah kejadian sukses pada sampel kelompok 1 dan kelompok 2.
* $\hat{p}_1, \hat{p}_2$: Nilai proporsi individu sampel $\rightarrow \hat{p}_1 = \frac{x_1}{n_1}$ dan $\hat{p}_2 = \frac{x_2}{n_2}$.

---

### D. Uji Rasio Varians 2 Populasi ($\sigma_1^2 / \sigma_2^2$)

Digunakan untuk menguji homogenitas kesamaan varians antara dua kelompok populasi independen. Pengujian ini menggunakan distribusi F (*Fisher-Snedecor*).

#### Rumus Statistik Uji ($F_{\text{hitung}}$):

$$F = \frac{s_1^2}{s_2^2}$$

#### Variabel & Aturan Penentuan Pembilang:

* $F$: Nilai rasio F dengan derajat bebas pembilang $df_1 = n_1 - 1$ dan derajat bebas penyebut $df_2 = n_2 - 1$.
* **Aturan Penting**: Demi menyederhanakan perhitungan tabel satu arah kanan, selalu posisikan kelompok data yang memiliki nilai varians sampel terbesar sebagai pembilang di sisi atas ($s_1^2 > s_2^2$), sehingga jaminan nilai $F_{\text{hitung}} > 1$.
