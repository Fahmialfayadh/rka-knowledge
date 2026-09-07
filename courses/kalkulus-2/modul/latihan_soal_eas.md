# Latihan Soal EAS Kalkulus 2 — Prediksi Selasa/Kamis

> **Disusun mengikuti format & pola soal EAS Kalkulus 2 ITS (SKPB – ITS)**
> Kisi-kisi: Volume Benda Putar · Panjang Kurva · Koordinat Kutub · Grafik Kutub · Luas & Volume Kutub · Garis Singgung & Panjang Busur Kutub · Deret Tak Hingga

---

## PAKET A

---

1. Gambarkan daerah yang dibatasi oleh $y = x^2$ dan $y = 2x$, dan kemudian dapatkan volume benda putar yang terbentuk jika daerah tersebut diputar mengelilingi sumbu $x$.

2. Dapatkan $\frac{dy}{dx}$ dari kurva $y = \frac{x^3}{6} + \frac{1}{2x}$, dan kemudian dapatkan panjang kurva tersebut pada interval $1 \le x \le 3$.

3. Gambarkan daerah di dalam kardioid $r = 2 + 2\cos\theta$ dan di dalam lingkaran $r = 2$, dan kemudian dapatkan luas daerah tersebut.

4. Dapatkan $\frac{dy}{dx}$ dari kurva polar $r = 1 + \sin\theta$ di titik $\theta = \frac{\pi}{6}$, dan kemudian tentukan persamaan garis singgungnya.

5. Diketahui deret $\displaystyle\sum_{n=1}^{\infty} \frac{n^2}{3^n}$. Gunakan uji rasio untuk menentukan apakah deret tersebut konvergen atau divergen. Jika konvergen, tentukan apakah konvergensinya mutlak atau bersyarat.

---

### Pembahasan Paket A

---

### Pembahasan Soal 1

**Langkah 1: Sketsa dan Titik Potong**

Samakan kedua persamaan:
$$x^2 = 2x \implies x^2 - 2x = 0 \implies x(x-2) = 0$$

Titik potong: $x = 0$ dan $x = 2$.

Pada interval $[0, 2]$, ambil nilai uji $x = 1$:
- $y = 2(1) = 2$ (kurva atas)
- $y = 1^2 = 1$ (kurva bawah)

Jadi $y = 2x$ di atas $y = x^2$.

**Langkah 2: Pilih Metode**

Sumbu putar: sumbu-$x$ (horizontal). Strip vertikal tegak lurus sumbu putar → **Metode Cincin (Washer)**.

Karena daerah tidak menempel sumbu putar (ada celah antara $y = x^2$ dan sumbu-$x$), tetapi daerah ini membentuk rongga saat diputar:
- Jari-jari luar: $R(x) = 2x$ (kurva terjauh dari sumbu-$x$)
- Jari-jari dalam: $r(x) = x^2$ (kurva terdekat dari sumbu-$x$)

**Langkah 3: Susun Integral**
$$V = \pi \int_{0}^{2} \left[ (2x)^2 - (x^2)^2 \right] dx = \pi \int_{0}^{2} (4x^2 - x^4) \, dx$$

**Langkah 4: Hitung Integral**
$$V = \pi \left[ \frac{4x^3}{3} - \frac{x^5}{5} \right]_{0}^{2}$$

Evaluasi pada $x = 2$:
$$V = \pi \left( \frac{4(8)}{3} - \frac{32}{5} \right) = \pi \left( \frac{32}{3} - \frac{32}{5} \right)$$

Samakan penyebut (KPK = 15):
$$V = \pi \left( \frac{160}{15} - \frac{96}{15} \right) = \frac{64\pi}{15}$$

$$\boxed{V = \frac{64\pi}{15} \approx 13{,}40 \text{ satuan volume}}$$

---

### Pembahasan Soal 2

**Langkah 1: Hitung Turunan**
$$y = \frac{x^3}{6} + \frac{1}{2x} = \frac{x^3}{6} + \frac{x^{-1}}{2}$$
$$\frac{dy}{dx} = \frac{3x^2}{6} - \frac{1}{2x^2} = \frac{x^2}{2} - \frac{1}{2x^2}$$

**Langkah 2: Hitung $\left(\frac{dy}{dx}\right)^2$ dan Bentuk $1 + \left(\frac{dy}{dx}\right)^2$**
$$\left(\frac{dy}{dx}\right)^2 = \left(\frac{x^2}{2} - \frac{1}{2x^2}\right)^2 = \frac{x^4}{4} - \frac{1}{2} + \frac{1}{4x^4}$$

Tambahkan 1:
$$1 + \left(\frac{dy}{dx}\right)^2 = \frac{x^4}{4} + \frac{1}{2} + \frac{1}{4x^4}$$

Perhatikan bahwa ini adalah **kuadrat sempurna**:
$$\frac{x^4}{4} + \frac{1}{2} + \frac{1}{4x^4} = \left(\frac{x^2}{2} + \frac{1}{2x^2}\right)^2$$

Sehingga:
$$\sqrt{1 + \left(\frac{dy}{dx}\right)^2} = \frac{x^2}{2} + \frac{1}{2x^2}$$

**Langkah 3: Susun dan Hitung Integral**
$$L = \int_{1}^{3} \left( \frac{x^2}{2} + \frac{1}{2x^2} \right) dx = \left[ \frac{x^3}{6} - \frac{1}{2x} \right]_{1}^{3}$$

Evaluasi batas atas ($x = 3$):
$$\frac{27}{6} - \frac{1}{6} = \frac{26}{6} = \frac{13}{3}$$

Evaluasi batas bawah ($x = 1$):
$$\frac{1}{6} - \frac{1}{2} = \frac{1}{6} - \frac{3}{6} = -\frac{2}{6} = -\frac{1}{3}$$

$$L = \frac{13}{3} - \left(-\frac{1}{3}\right) = \frac{13}{3} + \frac{1}{3} = \frac{14}{3}$$

$$\boxed{L = \frac{14}{3} \approx 4{,}67 \text{ satuan panjang}}$$

---

### Pembahasan Soal 3

**Langkah 1: Sketsa dan Cari Titik Potong**

Samakan kedua kurva:
$$2 + 2\cos\theta = 2 \implies 2\cos\theta = 0 \implies \cos\theta = 0$$
$$\theta = \frac{\pi}{2} \quad \text{dan} \quad \theta = \frac{3\pi}{2}$$

**Langkah 2: Identifikasi Daerah**

Pada $\theta = 0$: $r_1 = 2 + 2(1) = 4$ dan $r_2 = 2$. Kardioid di **luar**.
Pada $\theta = \pi$: $r_1 = 2 + 2(-1) = 0$ dan $r_2 = 2$. Lingkaran di **luar**.

Daerah irisan (di dalam keduanya) ada di interval $-\frac{\pi}{2} \le \theta \le \frac{\pi}{2}$, di mana kedua kurva membentuk daerah tertutup. Di interval ini, kurva yang **lebih dalam** (lebih dekat ke titik asal) adalah lingkaran $r = 2$ (karena kardioid lebih besar). Jadi daerah di dalam keduanya pada interval ini dibatasi oleh $r = 2$.

Pada interval $\frac{\pi}{2} \le \theta \le \frac{3\pi}{2}$, kardioid lebih kecil dari lingkaran, sehingga daerah irisan dibatasi oleh kardioid $r = 2 + 2\cos\theta$.

Gunakan simetri terhadap sumbu-$x$:

$$A = 2\left[\frac{1}{2}\int_{0}^{\pi/2} (2)^2 \, d\theta + \frac{1}{2}\int_{\pi/2}^{\pi} (2+2\cos\theta)^2 \, d\theta\right]$$

$$A = \int_{0}^{\pi/2} 4 \, d\theta + \int_{\pi/2}^{\pi} (2+2\cos\theta)^2 \, d\theta$$

**Langkah 3: Hitung Integral Pertama**
$$\int_{0}^{\pi/2} 4 \, d\theta = 4 \cdot \frac{\pi}{2} = 2\pi$$

**Langkah 4: Hitung Integral Kedua**
Jabarkan:
$$(2 + 2\cos\theta)^2 = 4 + 8\cos\theta + 4\cos^2\theta$$

Gunakan identitas $\cos^2\theta = \frac{1+\cos 2\theta}{2}$:
$$= 4 + 8\cos\theta + 2(1 + \cos 2\theta) = 6 + 8\cos\theta + 2\cos 2\theta$$

$$\int_{\pi/2}^{\pi} (6 + 8\cos\theta + 2\cos 2\theta) \, d\theta = \left[6\theta + 8\sin\theta + \sin 2\theta\right]_{\pi/2}^{\pi}$$

Evaluasi pada $\theta = \pi$:
$$6\pi + 8\sin\pi + \sin 2\pi = 6\pi + 0 + 0 = 6\pi$$

Evaluasi pada $\theta = \pi/2$:
$$6 \cdot \frac{\pi}{2} + 8\sin\frac{\pi}{2} + \sin\pi = 3\pi + 8 + 0 = 3\pi + 8$$

$$\int_{\pi/2}^{\pi} = 6\pi - (3\pi + 8) = 3\pi - 8$$

**Langkah 5: Jumlahkan**
$$A = 2\pi + 3\pi - 8 = 5\pi - 8$$

$$\boxed{A = 5\pi - 8 \approx 7{,}71 \text{ satuan luas}}$$

---

### Pembahasan Soal 4

**Langkah 1: Hitung Turunan**
$$r = 1 + \sin\theta \implies \frac{dr}{d\theta} = \cos\theta$$

**Langkah 2: Evaluasi pada $\theta = \pi/6$**
- $r = 1 + \sin(\pi/6) = 1 + \frac{1}{2} = \frac{3}{2}$
- $\frac{dr}{d\theta} = \cos(\pi/6) = \frac{\sqrt{3}}{2}$

Koordinat Kartesian titik singgung:
$$x_0 = r\cos\theta = \frac{3}{2} \cdot \frac{\sqrt{3}}{2} = \frac{3\sqrt{3}}{4}$$
$$y_0 = r\sin\theta = \frac{3}{2} \cdot \frac{1}{2} = \frac{3}{4}$$

**Langkah 3: Hitung Pembilang dan Penyebut $\frac{dy}{dx}$**

Pembilang ($\frac{dy}{d\theta}$):
$$\frac{dy}{d\theta} = \frac{dr}{d\theta}\sin\theta + r\cos\theta = \frac{\sqrt{3}}{2} \cdot \frac{1}{2} + \frac{3}{2} \cdot \frac{\sqrt{3}}{2} = \frac{\sqrt{3}}{4} + \frac{3\sqrt{3}}{4} = \frac{4\sqrt{3}}{4} = \sqrt{3}$$

Penyebut ($\frac{dx}{d\theta}$):
$$\frac{dx}{d\theta} = \frac{dr}{d\theta}\cos\theta - r\sin\theta = \frac{\sqrt{3}}{2} \cdot \frac{\sqrt{3}}{2} - \frac{3}{2} \cdot \frac{1}{2} = \frac{3}{4} - \frac{3}{4} = 0$$

**Langkah 4: Analisis Kemiringan**

Karena $\frac{dx}{d\theta} = 0$ dan $\frac{dy}{d\theta} = \sqrt{3} \neq 0$, maka kemiringan garis singgung **tidak terdefinisi** (bagi dengan nol). Artinya garis singgung di titik tersebut adalah **garis vertikal**.

**Langkah 5: Persamaan Garis Singgung**

$$\boxed{x = \frac{3\sqrt{3}}{4}}$$

(Garis singgung vertikal yang melewati titik $\left(\frac{3\sqrt{3}}{4}, \frac{3}{4}\right)$.)

---

### Pembahasan Soal 5

**Langkah 1: Identifikasi Suku Umum dan Suku Berikutnya**
$$a_n = \frac{n^2}{3^n}, \quad a_{n+1} = \frac{(n+1)^2}{3^{n+1}}$$

**Langkah 2: Hitung Limit Rasio**
$$\rho = \lim_{n \to \infty} \left|\frac{a_{n+1}}{a_n}\right| = \lim_{n \to \infty} \frac{(n+1)^2}{3^{n+1}} \cdot \frac{3^n}{n^2}$$

$$= \lim_{n \to \infty} \frac{(n+1)^2}{3 \cdot n^2} = \frac{1}{3} \lim_{n \to \infty} \left(\frac{n+1}{n}\right)^2 = \frac{1}{3} \cdot 1^2 = \frac{1}{3}$$

**Langkah 3: Kesimpulan**

Karena $\rho = \frac{1}{3} < 1$, berdasarkan Uji Rasio deret $\sum \frac{n^2}{3^n}$ **konvergen**.

Karena semua suku bernilai positif ($a_n > 0$ untuk semua $n$), maka $\sum |a_n| = \sum a_n$ konvergen. Jadi:

$$\boxed{\text{Deret konvergen mutlak}}$$

---
---

## PAKET B

---

1. Gambarkan daerah yang dibatasi oleh $y = \sqrt{x}$, $y = 0$, dan $x = 4$, dan kemudian dapatkan volume benda putar yang terbentuk jika daerah tersebut diputar mengelilingi sumbu $y$.

2. Dapatkan $\frac{dx}{dt}$ dan $\frac{dy}{dt}$ dari persamaan parametrik $x = 3\cos t$ dan $y = 3\sin t$, $0 \le t \le \frac{\pi}{2}$. Selanjutnya dapatkan panjang busurnya.

3. Gambarkan kurva dari rose $r = 3\cos 2\theta$, dan kemudian dapatkan luas daerah di dalam kurva tersebut.

4. Dapatkan $\frac{dy}{dx}$ dari kurva kardioid $r = 1 + \cos\theta$, dan kemudian tentukan titik-titik $\theta$ di mana garis singgungnya horizontal. Selanjutnya dapatkan panjang busur total kardioid tersebut.

5. Diketahui deret $\displaystyle\sum_{n=1}^{\infty} (-1)^{n+1} \frac{1}{\sqrt{n}}$. Tentukan apakah deret tersebut konvergen mutlak, konvergen bersyarat, atau divergen. Jelaskan langkah-langkahnya.

---

### Pembahasan Paket B

---

### Pembahasan Soal 1

**Langkah 1: Sketsa Daerah**

Daerah dibatasi oleh $y = \sqrt{x}$ (atas), $y = 0$ (bawah), dan $x = 4$ (kanan), dengan batas kiri di $x = 0$ (titik potong $\sqrt{x}$ dan sumbu-$x$).

Sumbu putar: sumbu-$y$ (vertikal). Strip vertikal sejajar dengan sumbu-$y$ → **Metode Kulit Tabung (Shell)**.

**Langkah 2: Tentukan Jari-jari dan Tinggi**
- Jari-jari tabung: $r = x$ (jarak dari strip ke sumbu-$y$)
- Tinggi tabung: $h = \sqrt{x}$ (tinggi strip vertikal)

**Langkah 3: Susun Integral**
$$V = 2\pi \int_{0}^{4} x \cdot \sqrt{x} \, dx = 2\pi \int_{0}^{4} x^{3/2} \, dx$$

**Langkah 4: Hitung Integral**
$$V = 2\pi \left[ \frac{2}{5} x^{5/2} \right]_{0}^{4} = 2\pi \cdot \frac{2}{5} \cdot 4^{5/2}$$

Hitung $4^{5/2} = (\sqrt{4})^5 = 2^5 = 32$:
$$V = 2\pi \cdot \frac{2}{5} \cdot 32 = 2\pi \cdot \frac{64}{5} = \frac{128\pi}{5}$$

$$\boxed{V = \frac{128\pi}{5} \approx 80{,}42 \text{ satuan volume}}$$

---

### Pembahasan Soal 2

**Langkah 1: Hitung Turunan Terhadap $t$**
$$\frac{dx}{dt} = -3\sin t, \quad \frac{dy}{dt} = 3\cos t$$

**Langkah 2: Susun Integran Panjang Busur**
$$\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2 = 9\sin^2 t + 9\cos^2 t = 9(\sin^2 t + \cos^2 t) = 9$$

$$\sqrt{9} = 3$$

**Langkah 3: Hitung Integral**
$$L = \int_{0}^{\pi/2} 3 \, dt = 3 \left[t\right]_{0}^{\pi/2} = 3 \cdot \frac{\pi}{2}$$

$$\boxed{L = \frac{3\pi}{2} \approx 4{,}71 \text{ satuan panjang}}$$

> [!NOTE]
> Ini sesuai harapan: kurva $x = 3\cos t$, $y = 3\sin t$ adalah seperempat lingkaran berjari-jari 3. Kelilingnya $\frac{1}{4}(2\pi \cdot 3) = \frac{3\pi}{2}$.

---

### Pembahasan Soal 3

**Langkah 1: Sketsa Kurva Rose**

$r = 3\cos 2\theta$ adalah kurva rose dengan $n = 2$ (genap), sehingga memiliki $2n = 4$ daun.

Setiap daun terbentuk saat $\cos 2\theta \ge 0$:
- Daun 1: $-\frac{\pi}{4} \le \theta \le \frac{\pi}{4}$
- Daun 2: $\frac{3\pi}{4} \le \theta \le \frac{5\pi}{4}$
- (dan dua daun lagi dari nilai negatif $r$: $\frac{\pi}{4} \le \theta \le \frac{3\pi}{4}$ dan $\frac{5\pi}{4} \le \theta \le \frac{7\pi}{4}$)

**Langkah 2: Hitung Luas Satu Daun**

Luas satu daun (misalnya daun di kuadran I):
$$A_1 = \frac{1}{2}\int_{-\pi/4}^{\pi/4} (3\cos 2\theta)^2 \, d\theta = \frac{1}{2}\int_{-\pi/4}^{\pi/4} 9\cos^2 2\theta \, d\theta$$

Gunakan identitas $\cos^2 u = \frac{1 + \cos 2u}{2}$:
$$A_1 = \frac{9}{2}\int_{-\pi/4}^{\pi/4} \frac{1 + \cos 4\theta}{2} \, d\theta = \frac{9}{4}\int_{-\pi/4}^{\pi/4} (1 + \cos 4\theta) \, d\theta$$

$$A_1 = \frac{9}{4}\left[\theta + \frac{\sin 4\theta}{4}\right]_{-\pi/4}^{\pi/4}$$

Evaluasi:
$$= \frac{9}{4}\left[\left(\frac{\pi}{4} + \frac{\sin\pi}{4}\right) - \left(-\frac{\pi}{4} + \frac{\sin(-\pi)}{4}\right)\right]$$
$$= \frac{9}{4}\left[\frac{\pi}{4} + 0 + \frac{\pi}{4} - 0\right] = \frac{9}{4} \cdot \frac{\pi}{2} = \frac{9\pi}{8}$$

**Langkah 3: Luas Total (4 Daun)**
$$A = 4 \cdot A_1 = 4 \cdot \frac{9\pi}{8} = \frac{9\pi}{2}$$

$$\boxed{A = \frac{9\pi}{2} \approx 14{,}14 \text{ satuan luas}}$$

---

### Pembahasan Soal 4

#### Bagian (a): Garis Singgung Horizontal

**Langkah 1: Hitung Turunan**
$$r = 1 + \cos\theta \implies \frac{dr}{d\theta} = -\sin\theta$$

**Langkah 2: Hitung $\frac{dy}{d\theta}$ dan $\frac{dx}{d\theta}$**
$$\frac{dy}{d\theta} = \frac{dr}{d\theta}\sin\theta + r\cos\theta = -\sin\theta\sin\theta + (1+\cos\theta)\cos\theta$$
$$= -\sin^2\theta + \cos\theta + \cos^2\theta$$

Gunakan identitas $\cos^2\theta - \sin^2\theta = \cos 2\theta$:
$$= \cos 2\theta + \cos\theta = 2\cos^2\theta - 1 + \cos\theta$$

Faktorkan:
$$= (2\cos\theta - 1)(\cos\theta + 1)$$

$$\frac{dx}{d\theta} = \frac{dr}{d\theta}\cos\theta - r\sin\theta = -\sin\theta\cos\theta - (1+\cos\theta)\sin\theta$$
$$= -\sin\theta(\cos\theta + 1 + \cos\theta) = -\sin\theta(1 + 2\cos\theta)$$

**Langkah 3: Garis Singgung Horizontal ($\frac{dy}{d\theta} = 0$, $\frac{dx}{d\theta} \ne 0$)**

$(2\cos\theta - 1)(\cos\theta + 1) = 0$
- $\cos\theta = \frac{1}{2} \implies \theta = \frac{\pi}{3}$ dan $\theta = \frac{5\pi}{3}$
- $\cos\theta = -1 \implies \theta = \pi$

Periksa $\frac{dx}{d\theta}$ di $\theta = \pi$: $-\sin\pi(1 + 2\cos\pi) = 0 \cdot (-1) = 0$ → **keduanya nol** → perlu L'Hôpital atau pendekatan lain. Titik ini adalah *cusp* (puncak runcing) kardioid, bukan garis singgung biasa.

Titik-titik dengan garis singgung horizontal:

$$\boxed{\theta = \frac{\pi}{3} \quad \text{dan} \quad \theta = \frac{5\pi}{3}}$$

---

#### Bagian (b): Panjang Busur Total

**Langkah 1: Sederhanakan $r^2 + (dr/d\theta)^2$**
$$r^2 + \left(\frac{dr}{d\theta}\right)^2 = (1+\cos\theta)^2 + \sin^2\theta = 1 + 2\cos\theta + \cos^2\theta + \sin^2\theta = 2 + 2\cos\theta$$

Identitas setengah sudut: $1 + \cos\theta = 2\cos^2(\theta/2)$
$$= 2 \cdot 2\cos^2\left(\frac{\theta}{2}\right) = 4\cos^2\left(\frac{\theta}{2}\right)$$

$$\sqrt{r^2 + \left(\frac{dr}{d\theta}\right)^2} = 2\left|\cos\left(\frac{\theta}{2}\right)\right|$$

**Langkah 2: Gunakan Simetri**
$\cos(\theta/2) \ge 0$ untuk $\theta \in [0, \pi]$. Karena kardioid simetris terhadap sumbu-$x$:
$$L = 2\int_{0}^{\pi} 2\cos\left(\frac{\theta}{2}\right) d\theta = 4\int_{0}^{\pi} \cos\left(\frac{\theta}{2}\right) d\theta$$

**Langkah 3: Hitung Integral**
$$L = 4\left[2\sin\left(\frac{\theta}{2}\right)\right]_{0}^{\pi} = 8(\sin(\pi/2) - \sin 0) = 8(1 - 0)$$

$$\boxed{L = 8 \text{ satuan panjang}}$$

---

### Pembahasan Soal 5

**Langkah 1: Uji Konvergensi Mutlak**

Tinjau deret nilai mutlak:
$$\sum_{n=1}^{\infty} \left|(-1)^{n+1} \frac{1}{\sqrt{n}}\right| = \sum_{n=1}^{\infty} \frac{1}{n^{1/2}}$$

Ini adalah **deret-$p$** dengan $p = \frac{1}{2} \le 1$, sehingga **divergen**.

Kesimpulan: Deret **tidak** konvergen mutlak.

**Langkah 2: Uji Deret Berganti Tanda (Uji Leibniz)**

Misalkan $b_n = \frac{1}{\sqrt{n}}$. Periksa dua syarat Leibniz:

1. **Monoton turun:**
$$b_{n+1} = \frac{1}{\sqrt{n+1}} < \frac{1}{\sqrt{n}} = b_n \quad \text{untuk semua } n \ge 1 \quad \checkmark$$

2. **Limit nol:**
$$\lim_{n \to \infty} \frac{1}{\sqrt{n}} = 0 \quad \checkmark$$

Kedua syarat terpenuhi, sehingga deret $\sum (-1)^{n+1} \frac{1}{\sqrt{n}}$ **konvergen**.

**Langkah 3: Kesimpulan**

Deret asli konvergen (Uji Leibniz) tetapi deret nilai mutlaknya divergen (deret-$p$, $p = 1/2$).

$$\boxed{\text{Konvergen Bersyarat}}$$

---
---

## PAKET C

---

1. Gambarkan daerah yang dibatasi oleh $y = 4 - x^2$ dan sumbu $x$, dan kemudian dapatkan volume benda putar yang terbentuk jika daerah tersebut diputar mengelilingi garis $x = -1$.

2. Dapatkan $\frac{dx}{dt}$ dan $\frac{dy}{dt}$ dari persamaan parametrik $x = t - \sin t$ dan $y = 1 - \cos t$, $0 \le t \le 2\pi$. Selanjutnya dapatkan panjang busur sikloid tersebut.

3. Gambarkan daerah di dalam kardioid $r = 1 + \cos\theta$, dan kemudian dapatkan luas daerah tersebut.

4. Dapatkan $\frac{dy}{dx}$ dari kurva polar $r = 2\cos\theta$ di titik $\theta = \frac{\pi}{4}$, dan kemudian tentukan persamaan garis singgungnya. Selanjutnya dapatkan panjang busur $r = 2\cos\theta$ untuk $0 \le \theta \le \frac{\pi}{2}$.

5. Diketahui deret $\displaystyle\sum_{n=1}^{\infty} \frac{1}{n(n+1)}$. Tuliskan bentuk pecahan parsialnya, dan kemudian tentukan jumlah deret tersebut.

---

### Pembahasan Paket C

---

### Pembahasan Soal 1

**Langkah 1: Sketsa dan Titik Potong**

$y = 4 - x^2$ memotong sumbu-$x$ ($y = 0$):
$$4 - x^2 = 0 \implies x^2 = 4 \implies x = -2, \, x = 2$$

Daerah: parabola terbuka ke bawah dari $x = -2$ sampai $x = 2$, di atas sumbu-$x$.

Sumbu putar: garis vertikal $x = -1$. Strip vertikal sejajar $x = -1$ → **Metode Kulit Tabung**.

**Langkah 2: Tentukan Jari-jari dan Tinggi**
- Jari-jari: jarak dari strip di $x$ ke garis $x = -1$: $r = x - (-1) = x + 1$
- Tinggi: $h = 4 - x^2$

**Langkah 3: Susun Integral**
$$V = 2\pi \int_{-2}^{2} (x+1)(4-x^2) \, dx$$

Jabarkan integran:
$$(x+1)(4-x^2) = 4x - x^3 + 4 - x^2$$

$$V = 2\pi \int_{-2}^{2} (4x - x^3 + 4 - x^2) \, dx$$

**Langkah 4: Pisahkan Fungsi Ganjil dan Genap**

Pada interval simetris $[-2, 2]$:
- Fungsi ganjil: $4x$ dan $-x^3$ → integralnya $= 0$
- Fungsi genap: $4$ dan $-x^2$ → gandakan integralnya pada $[0,2]$

$$V = 2\pi \cdot 2\int_{0}^{2} (4 - x^2) \, dx = 4\pi \left[4x - \frac{x^3}{3}\right]_{0}^{2}$$

$$= 4\pi \left(8 - \frac{8}{3}\right) = 4\pi \cdot \frac{16}{3} = \frac{64\pi}{3}$$

$$\boxed{V = \frac{64\pi}{3} \approx 67{,}02 \text{ satuan volume}}$$

---

### Pembahasan Soal 2

**Langkah 1: Hitung Turunan Terhadap $t$**
$$\frac{dx}{dt} = 1 - \cos t, \quad \frac{dy}{dt} = \sin t$$

**Langkah 2: Hitung Integran Panjang Busur**
$$\left(\frac{dx}{dt}\right)^2 + \left(\frac{dy}{dt}\right)^2 = (1-\cos t)^2 + \sin^2 t$$
$$= 1 - 2\cos t + \cos^2 t + \sin^2 t = 2 - 2\cos t$$

Identitas setengah sudut: $1 - \cos t = 2\sin^2(t/2)$
$$= 2 \cdot 2\sin^2(t/2) = 4\sin^2(t/2)$$

$$\sqrt{4\sin^2(t/2)} = 2|\sin(t/2)| = 2\sin(t/2) \quad (\text{karena } \sin(t/2) \ge 0 \text{ untuk } 0 \le t \le 2\pi)$$

**Langkah 3: Hitung Integral**
$$L = \int_{0}^{2\pi} 2\sin\left(\frac{t}{2}\right) dt = \left[-4\cos\left(\frac{t}{2}\right)\right]_{0}^{2\pi}$$

$$= -4\cos(\pi) - (-4\cos(0)) = -4(-1) + 4(1) = 4 + 4 = 8$$

$$\boxed{L = 8 \text{ satuan panjang}}$$

---

### Pembahasan Soal 3

**Langkah 1: Gunakan Simetri Kardioid**

Kardioid $r = 1 + \cos\theta$ simetris terhadap sumbu-$x$.
$$A = 2 \cdot \frac{1}{2}\int_{0}^{\pi} (1+\cos\theta)^2 \, d\theta = \int_{0}^{\pi} (1 + 2\cos\theta + \cos^2\theta) \, d\theta$$

**Langkah 2: Gunakan Identitas**
$$\cos^2\theta = \frac{1+\cos 2\theta}{2}$$

$$A = \int_{0}^{\pi} \left(1 + 2\cos\theta + \frac{1+\cos 2\theta}{2}\right) d\theta = \int_{0}^{\pi} \left(\frac{3}{2} + 2\cos\theta + \frac{\cos 2\theta}{2}\right) d\theta$$

**Langkah 3: Hitung**
$$A = \left[\frac{3}{2}\theta + 2\sin\theta + \frac{\sin 2\theta}{4}\right]_{0}^{\pi}$$

Evaluasi pada $\theta = \pi$:
$$\frac{3\pi}{2} + 2\sin\pi + \frac{\sin 2\pi}{4} = \frac{3\pi}{2} + 0 + 0 = \frac{3\pi}{2}$$

Evaluasi pada $\theta = 0$: semuanya $= 0$.

$$\boxed{A = \frac{3\pi}{2} \approx 4{,}71 \text{ satuan luas}}$$

---

### Pembahasan Soal 4

#### Bagian (a): Garis Singgung di $\theta = \pi/4$

**Langkah 1: Hitung Turunan**
$$r = 2\cos\theta \implies \frac{dr}{d\theta} = -2\sin\theta$$

**Langkah 2: Evaluasi pada $\theta = \pi/4$**
- $r = 2\cos(\pi/4) = 2 \cdot \frac{\sqrt{2}}{2} = \sqrt{2}$
- $\frac{dr}{d\theta} = -2\sin(\pi/4) = -\sqrt{2}$
- $\cos(\pi/4) = \sin(\pi/4) = \frac{\sqrt{2}}{2}$

Koordinat Kartesian:
$$x_0 = \sqrt{2} \cdot \frac{\sqrt{2}}{2} = 1, \quad y_0 = \sqrt{2} \cdot \frac{\sqrt{2}}{2} = 1$$

**Langkah 3: Hitung $\frac{dy}{dx}$**

Pembilang:
$$\frac{dy}{d\theta} = (-\sqrt{2})\frac{\sqrt{2}}{2} + \sqrt{2} \cdot \frac{\sqrt{2}}{2} = -1 + 1 = 0$$

Karena $\frac{dy}{d\theta} = 0$, periksa penyebut:
$$\frac{dx}{d\theta} = (-\sqrt{2})\frac{\sqrt{2}}{2} - \sqrt{2} \cdot \frac{\sqrt{2}}{2} = -1 - 1 = -2 \neq 0$$

Maka $\frac{dy}{dx} = \frac{0}{-2} = 0$ → **Garis singgung horizontal**.

$$\boxed{y = 1}$$

---

#### Bagian (b): Panjang Busur $r = 2\cos\theta$ untuk $0 \le \theta \le \pi/2$

$$r^2 + \left(\frac{dr}{d\theta}\right)^2 = 4\cos^2\theta + 4\sin^2\theta = 4$$

$$L = \int_{0}^{\pi/2} \sqrt{4} \, d\theta = \int_{0}^{\pi/2} 2 \, d\theta = 2 \cdot \frac{\pi}{2} = \pi$$

$$\boxed{L = \pi \approx 3{,}14 \text{ satuan panjang}}$$

> [!NOTE]
> Ini masuk akal: $r = 2\cos\theta$ adalah lingkaran berpusat $(1,0)$ berjari-jari 1. Setengah keliling lingkaran tersebut: $\frac{1}{2}(2\pi \cdot 1) = \pi$.

---

### Pembahasan Soal 5

**Langkah 1: Pecahan Parsial**
$$\frac{1}{n(n+1)} = \frac{A}{n} + \frac{B}{n+1}$$

Kalikan kedua ruas dengan $n(n+1)$:
$$1 = A(n+1) + Bn$$

- Substitusi $n = 0$: $1 = A$
- Substitusi $n = -1$: $1 = -B \implies B = -1$

$$\frac{1}{n(n+1)} = \frac{1}{n} - \frac{1}{n+1}$$

**Langkah 2: Tulis Jumlah Parsial (Deret Teleskopik)**
$$S_k = \sum_{n=1}^{k} \left(\frac{1}{n} - \frac{1}{n+1}\right)$$

$$= \left(1 - \frac{1}{2}\right) + \left(\frac{1}{2} - \frac{1}{3}\right) + \left(\frac{1}{3} - \frac{1}{4}\right) + \dots + \left(\frac{1}{k} - \frac{1}{k+1}\right)$$

Suku-suku tengah saling menghilangkan:
$$S_k = 1 - \frac{1}{k+1}$$

**Langkah 3: Hitung Limit**
$$S = \lim_{k \to \infty} S_k = \lim_{k \to \infty} \left(1 - \frac{1}{k+1}\right) = 1 - 0 = 1$$

$$\boxed{S = 1}$$

---

## Ringkasan Pola Soal EAS ITS Kalkulus 2

> [!IMPORTANT]
> **Pola tetap 5 soal essai, masing-masing 1 topik:**
>
> | No | Pola Instruksi Khas ITS | Topik Kisi-kisi Anda |
> |:--:|:--|:--|
> | 1 | "Gambarkan daerah... kemudian dapatkan volume..." | Volume Benda Putar |
> | 2 | "Dapatkan dy/dx... kemudian dapatkan panjang..." | Panjang Kurva |
> | 3 | "Gambarkan daerah di dalam... dapatkan luas..." | Luas/Volume Koordinat Kutub |
> | 4 | "Dapatkan dy/dx dari kurva polar... garis singgung... panjang busur..." | Garis Singgung & Busur Kutub |
> | 5 | "Diketahui deret... tentukan konvergen/divergen..." | Deret Tak Hingga |

> [!WARNING]
> **Berdasarkan bocoran EAS ITS Senin:**
> - Soal nomor 1 selalu meminta Anda **menggambar sketsa** dulu — jangan langsung hitung!
> - Soal parametrik / polar sering menggunakan **identitas trigonometri** untuk menyederhanakan.
> - Soal barisan/deret selalu minta **jelaskan langkah** — bukan hanya jawaban akhir.
