# Kumpulan Rumus EAS Kalkulus 2 (Cheat Sheet)

Kumpulan rumus ini disusun secara **linear** berdasarkan kisi-kisi EAS Selasa/Kamis. Setiap rumus dilengkapi dengan **alasan (reasoning)** agar Anda tidak sekadar menghafal buta, tetapi memahami *mengapa* rumus tersebut berbentuk seperti itu.

---

## 1. Menghitung Volume Benda Putar

**Konsep Utama:** Volume adalah hasil penjumlahan (integral) luas irisan tipis yang memiliki ketebalan tertentu.

### A. Metode Cakram (Disk) & Cincin (Washer)
Digunakan saat partisi (strip irisan) **tegak lurus** dengan sumbu putar.
*   **Rumus Cakram:** $V = \pi \int_{a}^{b} [f(x)]^2 \, dx$
    *   *Reasoning:* Irisan berupa tabung gepeng tanpa lubang. Luas alas tabung adalah luas lingkaran ($\pi r^2$) dengan $r = f(x)$, dan ketebalannya $dx$.
*   **Rumus Cincin:** $V = \pi \int_{a}^{b} \left( [R(x)]^2 - [r(x)]^2 \right) dx$
    *   *Reasoning:* Irisan berupa cakram yang tengahnya berlubang (seperti donat pipih). Jadi, Luas Lingkaran Besar dikurangi Luas Lingkaran Kecil: $\pi R^2 - \pi r^2$, lalu dikali ketebalan $dx$.
    *   *Awas Jebakan:* Jangan pernah menghitung $(R - r)^2$. Kuadratkan dulu baru dikurang!

### B. Metode Kulit Tabung (Shell)
Digunakan saat partisi (strip irisan) **sejajar** dengan sumbu putar.
*   **Rumus:** $V = 2\pi \int_{a}^{b} r(x) \cdot h(x) \, dx$
    *   *Reasoning:* Bayangkan kaleng silinder tak berselimut yang dibelah lalu dibentangkan menjadi persegi panjang. Panjangnya adalah keliling lingkaran ($2\pi r$), tingginya $h$, dan ketebalannya $dx$.
    *   *Kapan Dipakai:* Saat memutar terhadap sumbu $y$ tapi fungsi hanya berbentuk $y=f(x)$ (susah diubah jadi $x=f(y)$). Jari-jarinya $r(x) = x$, tingginya $h(x) = f(x)$.

---

## 2. Panjang Suatu Kurva (Arc Length)

**Konsep Utama:** Memecah kurva menjadi garis-garis lurus super pendek, lalu menjumlahkannya dengan Teorema Pythagoras.

### A. Kurva Kartesian
*   **Fungsi $y = f(x)$:** $L = \int_{a}^{b} \sqrt{1 + \left(\frac{dy}{dx}\right)^2} \, dx$
    *   *Reasoning:* Dari Pythagoras $ds^2 = dx^2 + dy^2$. Jika $dx^2$ dikeluarkan dari akar, maka bentuknya menjadi $\sqrt{1 + (dy/dx)^2} dx$.
*   **Fungsi $x = g(y)$:** $L = \int_{c}^{d} \sqrt{1 + \left(\frac{dx}{dy}\right)^2} \, dy$

### B. Kurva Parametrik ($x=f(t), y=g(t)$)
*   **Rumus:** $L = \int_{t_1}^{t_2} \sqrt{\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2} \, dt$
    *   *Reasoning:* Sama dengan Pythagoras $ds = \sqrt{dx^2 + dy^2}$, tapi kali ini kita keluarkan $dt^2$, maka jadinya dibagi $dt^2$ di dalam akar.

---

## 3. Koordinat Kutub & Grafiknya

**Konsep Utama:** Mengganti grid kotak-kotak $(x,y)$ dengan jarak dari pusat ($r$) dan sudut perputaran ($\theta$).

### A. Konversi
*   $x = r \cos \theta$
*   $y = r \sin \theta$
*   $r^2 = x^2 + y^2$
    *   *Reasoning:* Gunakan segitiga siku-siku. Samping/miring = $\cos$, depan/miring = $\sin$. Pythagoras: $x^2+y^2 = r^2$.

### B. Hafalan Cepat Grafik Kutub
*   $r = a \cos(n\theta)$ atau $r = a \sin(n\theta)$ $\rightarrow$ **Kurva Bunga (Rose)**
    *   *Tips:* Jika $n$ genap, jumlah daun = $2n$. Jika $n$ ganjil, jumlah daun = $n$.
*   $r = a \pm b \cos\theta$ $\rightarrow$ **Kardioid / Limaçon**
    *   *Tips:* Jika $a = b$ (misal $1+\cos\theta$), namanya Kardioid (berbentuk hati, menyentuh $(0,0)$). Jika $a < b$ (misal $1+2\cos\theta$), ada *inner loop* (putaran ke dalam).

---

## 4. Luas & Volume dalam Koordinat Kutub

### A. Luas Daerah Kutub
*   **Satu Kurva:** $A = \frac{1}{2} \int_{\alpha}^{\beta} r^2 \, d\theta$
    *   *Reasoning:* Mengapa ada $1/2$? Karena ini berasal dari rumus luas juring lingkaran di geometri dasar: $Luas = \frac{1}{2} r^2 \theta$. Jika $\theta$ sangat kecil ($d\theta$), menjadi elemen luas $dA$.
*   **Di antara 2 Kurva:** $A = \frac{1}{2} \int_{\alpha}^{\beta} \left( r_{\text{luar}}^2 - r_{\text{dalam}}^2 \right) d\theta$

### B. Volume Kutub (Jarang muncul, tapi jika ditanya)
Gunakan rumus integrasi Kartesius tapi variabelnya disubstitusi.
Contoh untuk metode Cakram putar sumbu-$x$:
*   $V = \pi \int y^2 dx \rightarrow$ ganti $y = r\sin\theta$ dan $dx = (\frac{dx}{d\theta}) d\theta$.

---

## 5. Garis Singgung & Panjang Busur Kutub

### A. Kemiringan Garis Singgung ($m = dy/dx$)
*   **Rumus:** $\frac{dy}{dx} = \frac{\frac{dr}{d\theta}\sin\theta + r\cos\theta}{\frac{dr}{d\theta}\cos\theta - r\sin\theta}$
    *   *Reasoning:* Ingat bahwa gradien itu selau $\frac{dy}{dx}$. Tapi karena kurva kita $r(\theta)$, maka $x = r\cos\theta$ dan $y = r\sin\theta$. Kita turunkan $y$ dan $x$ terhadap $\theta$ menggunakan **aturan perkalian ($uv' + u'v$)**.
    *   *Awas Jebakan:* Kemiringan BUKAN $\frac{dr}{d\theta}$. $\frac{dr}{d\theta}$ hanya menunjukkan seberapa cepat radius memanjang, bukan kemiringan kurva.
    *   *Singgung Horizontal:* Jika Pembilang $= 0$.
    *   *Singgung Vertikal:* Jika Penyebut $= 0$.

### B. Panjang Busur Kutub
*   **Rumus:** $L = \int_{\alpha}^{\beta} \sqrt{r^2 + \left(\frac{dr}{d\theta}\right)^2} \, d\theta$
    *   *Reasoning:* Berasal dari panjang kurva parametrik $\sqrt{(\frac{dx}{d\theta})^2 + (\frac{dy}{d\theta})^2}$. Saat turunan perkaliannya dikuadratkan, suku tengah saling coret (plus dan minus), dan bersisa $(r')^2(\cos^2+\sin^2) + r^2(\sin^2+\cos^2) = (r')^2 + r^2$. Sangat elegan!

---

## 6. Deret Tak Hingga

**Konsep Utama:** Kapan hasil dari penjumlahan barisan bilangan hingga tak hingga tidak akan meledak ($\infty$)? Jika suku-sukunya mengecil cukup cepat.

### A. Deret Geometri ($\sum a \cdot r^{n-1}$)
*   **Konvergen jika:** $|r| < 1$. Jumlahnya: $S = \frac{a}{1 - r}$.
    *   *Reasoning:* Jika rasio $r$ adalah desimal (misal $1/2$), tiap suku makin kecil. Kalau dijumlah tak berhingga kali akan punya batas henti.

### B. Uji Divergensi (Cek limit $a_n$)
*   Jika $\lim_{n \to \infty} a_n \neq 0$, pasti **Divergen**.
    *   *Reasoning:* Jika suku terakhir di ketakhinggaan tidak bernilai nol (misal nilainya selalu 1), maka Anda menambahkan angka 1 terus-menerus. Hasilnya pasti meledak.

### C. Uji Rasio (Kasta Tertinggi untuk Faktorial/Eksponen)
*   **Rumus:** $\rho = \lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right|$
*   Konvergen jika $\rho < 1$, Divergen jika $\rho > 1$. Gagal jika $\rho = 1$.
    *   *Reasoning:* Pada dasarnya uji ini bertanya: "Untuk jangka panjang, apakah deret ini bertingkah seperti deret geometri dengan rasio kurang dari 1?". Sangat ampuh jika ada $n!$ atau $3^n$ karena gampang dicoret.

### D. Uji Banding Limit (Untuk pecahan Aljabar)
*   Bandingkan dengan deret-p: $\sum \frac{1}{n^p}$. Konvergen jika $p > 1$.
    *   *Reasoning:* Jika bentuknya $\frac{3n^2}{n^4+5}$, abaikan konstanta kecil saat $n$ sangat besar. Fungsinya "bertingkah" seperti $\frac{n^2}{n^4} = \frac{1}{n^2}$. Karena $\frac{1}{n^2}$ (p=2) konvergen, maka deret asli ikut konvergen.

### E. Uji Leibniz (Deret Berganti Tanda)
*   Bentuk $\sum (-1)^n b_n$ **Konvergen** jika dua syarat dipenuhi:
    1.  Limit $b_n$ = 0 (Ujungnya nol).
    2.  $b_{n+1} \le b_n$ (Monoton mengecil).
    *   *Reasoning:* Karena tanda plus-minus, deret ini melangkah maju lalu mundur. Jika langkahnya makin lama makin pendek hingga diam (nol), deret akan berhenti ("converge") di satu titik.
