# ANOVA (Analysis of Variance) — Catatan Belajar

---

## BAGIAN 1 — Distribusi F

Distribusi F adalah dasar dari semua uji di catatan ini. Sifatnya:

- Ditentukan oleh **2 parameter**: derajat bebas numerator ($df_1$) dan derajat bebas denominator ($df_2$).
- Nilainya **tidak pernah negatif**, dari 0 sampai ∞.
- Distribusi **kontinu**, bentuknya **menjulur positif** (semakin besar F, kurva makin mendekati sumbu X).

---

## BAGIAN 2 — Uji Kesamaan Dua Variansi (F-Test)

**Buat apa?** Untuk menjawab: *"apakah dua populasi punya variansi yang sama?"* — ini dasar sebelum ANOVA, karena salah satu syarat ANOVA adalah variansi semua kelompok harus sama.

**Variabel:**

| Simbol | Arti |
|---|---|
| $S_1^2,\ S_2^2$ | variansi sampel populasi 1 dan 2 |
| $n_1,\ n_2$ | ukuran sampel populasi 1 dan 2 |

**Hipotesis (dua arah):**
$$H_0: \sigma_1^2 = \sigma_2^2 \qquad H_1: \sigma_1^2 \neq \sigma_2^2$$

**Rumus:**
$$F = \frac{S_1^2}{S_2^2} \qquad df_{numerator}=n_1-1,\quad df_{denominator}=n_2-1$$

$H_0$ ditolak jika $F_{hitung} > F_{kritis}$ (dari tabel F).

> Untuk uji **satu arah** (mis. "populasi 1 variansinya lebih besar"), taruh variansi yang diduga lebih besar di pembilang.

### Contoh Soal 1

> Rata-rata *rate of return* sampel **10 saham internet** = 12,6%, std dev = 3,9%. Rata-rata sampel **8 saham utilitas** = 10,9%, std dev = 3,5%. Pada $\alpha=0{,}05$, apakah saham internet variasinya **lebih besar**?

**Step 1 — Hipotesis** (satu arah, karena tanya "lebih besar"):
$$H_0: \sigma^2_{internet} \leq \sigma^2_{utilitas} \qquad H_1: \sigma^2_{internet} > \sigma^2_{utilitas}$$

**Step 2 — $\alpha = 0{,}05$**

**Step 3 — Statistik uji:** distribusi F

**Step 4 — Aturan keputusan:**
$df = (n_{internet}-1,\ n_{utilitas}-1) = (9,\ 7)$. $F_{0{,}05;\,9,7}=3{,}68$.
Tolak $H_0$ jika $F_{hitung}>3{,}68$.

**Step 5 — Hitung & simpulkan:**
$$F = \frac{S_{internet}^2}{S_{utilitas}^2} = \frac{3{,}9^2}{3{,}5^2} = \frac{15{,}21}{12{,}25} = 1{,}2416$$

$F_{hitung}=1{,}2416 < F_{kritis}=3{,}68$ (p = 0,3965 > 0,05)

> **Kesimpulan:** $H_0$ tidak ditolak. Tidak cukup bukti variasi saham internet lebih besar dari utilitas.

---

## BAGIAN 3 — ANOVA Satu Arah

**Buat apa?** Menjawab: *"apakah 3 atau lebih kelompok populasi punya rata-rata (mean) yang sama?"*

### 3.1 Syarat ANOVA

1. Sampel dari populasi **berdistribusi normal**.
2. Sampel **saling independen**.
3. Semua populasi punya **standar deviasi yang sama** (homogen).

### 3.2 Hipotesis Umum

Untuk $k$ kelompok:
$$H_0: \mu_1=\mu_2=\dots=\mu_k \qquad H_1: \text{tidak semua mean sama}$$

### 3.3 Ide Dasar

$$\text{Total Variation (}TSS\text{)} = \text{Treatment Variation (}SST\text{)} + \text{Error Variation (}SSE\text{)}$$

### 3.4 Variabel

| Simbol | Arti |
|---|---|
| $i$ | indeks observasi |
| $k$ | jumlah kelompok *treatment* |
| $n_k$ | jumlah observasi kelompok ke-$k$ |
| $n$ | jumlah total observasi (semua kelompok) |
| $X_{i.k}$ | nilai observasi ke-$i$ pada kelompok ke-$k$ |
| $\bar{X}_k$ | mean kelompok ke-$k$ |
| $\bar{X}_G$ | *grand mean* (mean dari seluruh data) |
| $SST,\ SSE,\ TSS$ | lihat 3.3 |
| $MST,\ MSE$ | *mean square* treatment & error |

### 3.5 Rumus & Tabel ANOVA

$$F = \frac{MST}{MSE}, \qquad df=(k-1,\ n-k)$$

| Sumber | SS | df | MS | F |
|---|---|---|---|---|
| Treatment | $SST=\sum_k n_k(\bar{X}_k-\bar{X}_G)^2$ | $k-1$ | $MST=SST/(k-1)$ | $MST/MSE$ |
| Error | $SSE=\sum_i\sum_k(X_{i.k}-\bar{X}_k)^2$ | $n-k$ | $MSE=SSE/(n-k)$ | |
| Total | $TSS=\sum_i(X_i-\bar{X}_G)^2$ | $n-1$ | | |

> Shortcut: $SST = TSS - SSE$ (tidak perlu hitung $SST$ langsung dari rumusnya).

### 3.6 Lima Langkah Pengerjaan (dipakai di semua soal ANOVA)

1. Nyatakan $H_0$ dan $H_1$
2. Tetapkan $\alpha$
3. Statistik uji = distribusi F
4. Aturan keputusan: cari $F_{kritis}$ dari tabel F dengan $df=(k-1,\ n-k)$; tolak $H_0$ jika $F_{hitung}>F_{kritis}$
5. Hitung & simpulkan

### Contoh Soal 2 — Rosenbaum Restaurants

> Katy ingin tahu apakah ada perbedaan rata-rata jumlah makan malam *meat loaf* yang terjual per hari di 3 restoran: **Aynor, Loris, Lander**. $\alpha=0{,}05$.

**Data:**

| Hari | Aynor | Loris | Lander |
|---|---|---|---|
| Day 1 | 13 | 10 | 18 |
| Day 2 | 12 | 12 | 16 |
| Day 3 | 14 | 13 | 17 |
| Day 4 | 12 | 11 | 17 |
| Day 5 | — | — | 17 |
| $n_k$ | 4 | 4 | 5 |
| $\bar{X}_k$ | 12,75 | 11,50 | 17,00 |

$n=13$, $k=3$, $\bar{X}_G = 14{,}00$

**Step 1:** $H_0: \mu_{Aynor}=\mu_{Loris}=\mu_{Lander}$, $H_1:$ tidak semua sama

**Step 2:** $\alpha=0{,}05$

**Step 3:** distribusi F

**Step 4:** $df=(k-1,\ n-k)=(2,\ 10)$. $F_{0{,}05;\,2,10}=4{,}10$. Tolak $H_0$ jika $F_{hitung}>4{,}10$.

**Step 5 — Hitung:**

*(a) TSS* — deviasi setiap data terhadap grand mean:

| Restoran | Subtotal |
|---|---|
| Aynor: $(13-14)^2+(12-14)^2+(14-14)^2+(12-14)^2$ | 9,00 |
| Loris: $(10-14)^2+(12-14)^2+(13-14)^2+(11-14)^2$ | 30,00 |
| Lander: $(18-14)^2+(16-14)^2+3\times(17-14)^2$ | 47,00 |

$TSS = 9{,}00+30{,}00+47{,}00 = 86{,}00$

*(b) SSE* — deviasi setiap data terhadap mean kelompoknya sendiri:

| Restoran | Subtotal |
|---|---|
| Aynor (12,75): $(13-12{,}75)^2+(12-12{,}75)^2+(14-12{,}75)^2+(12-12{,}75)^2$ | 2,75 |
| Loris (11,50): $(10-11{,}5)^2+(12-11{,}5)^2+(13-11{,}5)^2+(11-11{,}5)^2$ | 5,00 |
| Lander (17,00): $(18-17)^2+(16-17)^2+3\times(17-17)^2$ | 2,00 |

$SSE = 2{,}75+5{,}00+2{,}00 = 9{,}75$

*(c) SST* (shortcut): $SST = TSS-SSE = 86{,}00-9{,}75 = 76{,}25$

*(d) Tabel ANOVA:*

| Sumber | SS | df | MS | F |
|---|---|---|---|---|
| Treatment | 76,25 | 2 | 38,125 | **39,103** |
| Error | 9,75 | 10 | 0,975 | |
| Total | 86,00 | 12 | | |

$F_{hitung}=39{,}103 > F_{kritis}=4{,}10$ (p = 0,000018 < 0,05)

> **Kesimpulan:** $H_0$ ditolak. Rata-rata penjualan di 3 restoran tidak sama (minimal 2 di antaranya berbeda).

---

## BAGIAN 4 — CI Selisih Dua Mean *Treatment* (lanjutan ANOVA)

**Buat apa?** Setelah $H_0$ ANOVA ditolak, kita baru tahu "ada beda" — tapi belum tahu treatment mana yang beda. CI ini dipakai untuk cek **pasangan** treatment tertentu.

**Rumus:**
$$(\bar{X}_1-\bar{X}_2)\ \pm\ t_{\alpha/2,\,n-k}\sqrt{MSE\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}$$

$t$ dari tabel-t dengan $df=n-k$; $MSE=SSE/(n-k)$ (ambil dari tabel ANOVA).

> Jika interval **memuat 0** → tidak ada beda signifikan. Jika **tidak memuat 0** → beda signifikan.

### Contoh Soal 3 — Lanjutan Contoh 2

> 95% CI untuk selisih mean **Lander** vs **Aynor**.

$\bar{X}_{Lander}=17{,}00\ (n=5)$, $\bar{X}_{Aynor}=12{,}75\ (n=4)$, $MSE=0{,}975$, $df=10$, $t_{0{,}025,10}=2{,}228$

$$17{,}00-12{,}75=4{,}25$$
$$\sqrt{0{,}975\left(\tfrac{1}{5}+\tfrac{1}{4}\right)}=\sqrt{0{,}43875}=0{,}6624$$
$$\text{margin}=2{,}228\times0{,}6624=1{,}476$$
$$CI_{95\%}=4{,}25\pm1{,}476=(2{,}77\ ;\ 5{,}73)$$

> **Kesimpulan:** 0 tidak ada dalam interval → mean Aynor berbeda signifikan dari Lander.

---

## BAGIAN 5 — ANOVA Dua Arah (dengan *Block*)

**Buat apa?** Kalau ada **dua** sumber pengaruh yang ingin diuji sekaligus: *treatment* (fokus utama) dan *block* (faktor tambahan yang dikontrol).

$$TSS = SST + SSB + SSE$$

**Variabel tambahan:**

| Simbol | Arti |
|---|---|
| $b$ | jumlah *block* |
| $\bar{X}_b$ | mean sampel *block* ke-$b$ |
| $SSB$ | variasi antar *block*; $SSB = k\sum_b(\bar{X}_b-\bar{X}_G)^2$ (catatan: koefisien $k$ ini sebenarnya jumlah *treatment*, bukan jumlah block — lihat Contoh Soal 4) |
| $MSB$ | $SSB/(b-1)$ |

**Tabel ANOVA dua arah:**

| Sumber | SS | df | MS | F |
|---|---|---|---|---|
| Treatment ($k$) | $SST$ | $k-1$ | $MST=SST/(k-1)$ | $MST/MSE$ |
| Block ($b$) | $SSB$ | $b-1$ | $MSB=SSB/(b-1)$ | $MSB/MSE$ |
| Error | $SSE=TSS-SST-SSB$ | $(k-1)(b-1)$ | $MSE=SSE/[(k-1)(b-1)]$ | |
| Total | $TSS$ | $n-1$ | | |

Karena ada 2 sumber pengaruh → dilakukan **2 uji terpisah** (Treatment Effect & Block Effect), masing-masing 5 langkah, tapi pakai **MSE yang sama**.

### Contoh Soal 4 — Bieber Manufacturing Co.

> Apakah ada perbedaan rata-rata produksi antar **shift**, dan antar **karyawan**? $\alpha=0{,}05$.

**Data (unit produksi):**

| Karyawan (*block*) | Day | Evening | Night | $\bar{X}_b$ |
|---|---|---|---|---|
| McCartney | 31 | 25 | 35 | 30,33 |
| Neary | 33 | 26 | 33 | 30,67 |
| Schoen | 28 | 24 | 30 | 27,33 |
| Thompson | 30 | 29 | 28 | 29,00 |
| Wagner | 28 | 26 | 27 | 27,00 |
| **$\bar{X}_k$** | **30,00** | **26,00** | **30,60** | |

$k=3$ (shift), $b=5$ (karyawan), $n=15$, $\bar{X}_G=28{,}87$

#### A) Treatment Effect (Shift)

1. $H_0:\mu_{Day}=\mu_{Evening}=\mu_{Night}$, $H_1:$ tidak semua sama
2. $\alpha=0{,}05$
3. distribusi F
4. $df=(2,8)$, $F_{0{,}05;2,8}=4{,}46$ → tolak $H_0$ jika $F_{hitung}>4{,}46$
5. Hitung:
$$SST=5(30{,}00-28{,}87)^2+5(26{,}00-28{,}87)^2+5(30{,}60-28{,}87)^2=62{,}53$$
$$MST=62{,}53/2=31{,}27 \qquad F_{hitung}=31{,}27/5{,}43=5{,}75$$

> **Kesimpulan:** $5{,}75>4{,}46$ (p=0,028) → $H_0$ ditolak. Ada beda produksi antar shift.

#### B) Block Effect (Karyawan)

1. $H_0:\mu_{McCartney}=\mu_{Neary}=\mu_{Schoen}=\mu_{Thompson}=\mu_{Wagner}$, $H_1:$ tidak semua sama
2. $\alpha=0{,}05$
3. distribusi F
4. $df=(4,8)$, $F_{0{,}05;4,8}=3{,}84$ → tolak $H_0$ jika $F_{hitung}>3{,}84$
5. Hitung SSB:

| Karyawan | $3(\bar{X}_b-28{,}87)^2$ | Subtotal |
|---|---|---|
| McCartney | $3(30{,}33-28{,}87)^2$ | 6,42 |
| Neary | $3(30{,}67-28{,}87)^2$ | 9,68 |
| Schoen | $3(27{,}33-28{,}87)^2$ | 7,08 |
| Thompson | $3(29{,}00-28{,}87)^2$ | 0,09 |
| Wagner | $3(27{,}00-28{,}87)^2$ | 10,49 |

$$SSB=6{,}42+9{,}68+7{,}08+0{,}09+10{,}49=33{,}73$$
$$MSB=33{,}73/4=8{,}43 \qquad F_{hitung}=8{,}43/5{,}43=1{,}55$$

> **Kesimpulan:** $1{,}55<3{,}84$ (p=0,276) → $H_0$ tidak ditolak. Tidak ada beda produksi antar karyawan.

#### Tabel ANOVA Lengkap

$TSS=139{,}73$ (diketahui), $SSE=139{,}73-62{,}53-33{,}73=43{,}47$

| Sumber | SS | df | MS | F |
|---|---|---|---|---|
| Treatment (Shift) | 62,53 | 2 | 31,27 | 5,75 |
| Block (Karyawan) | 33,73 | 4 | 8,43 | 1,55 |
| Error | 43,47 | 8 | 5,43 | |
| Total | 139,73 | 14 | | |

---

## BAGIAN 6 — Rumus Cepat (Cheat Sheet)

**Uji Dua Variansi:** $F=S_1^2/S_2^2$, $df=(n_1-1,\ n_2-1)$

**ANOVA Satu Arah:**
$$SST=\sum_k n_k(\bar{X}_k-\bar{X}_G)^2 \quad SSE=\sum_i\sum_k(X_{i.k}-\bar{X}_k)^2 \quad TSS=SST+SSE$$
$$F=\frac{SST/(k-1)}{SSE/(n-k)}, \qquad df=(k-1,\ n-k)$$

**CI Selisih Mean:** $(\bar{X}_1-\bar{X}_2)\pm t_{\alpha/2,n-k}\sqrt{MSE(\tfrac{1}{n_1}+\tfrac{1}{n_2})}$

**ANOVA Dua Arah:**
$$SSB=k\sum_b(\bar{X}_b-\bar{X}_G)^2 \quad SSE=TSS-SST-SSB$$
$$F_{treatment}=\frac{SST/(k-1)}{SSE/[(k-1)(b-1)]}, \quad F_{block}=\frac{SSB/(b-1)}{SSE/[(k-1)(b-1)]}$$