# Implementation Plan: Full God Mode Suite in Godot ⚡🌍

Tentu saja! Jika kita ingin melakukan *porting*, kita harus memindahkan **seluruh** persenjataan Dewa Anda dari Python ke Godot. Karena Godot menggunakan sistem *Boids* murni tanpa A* (berdasarkan pengamatan `Unit.gd`), cara kita menerapkan rintangan (Gunung/Air) akan sedikit berbeda tapi jauh lebih mulus secara pergerakan.

## 🏗️ Arsitektur Perubahan (The God Mode)

### 1. Sistem "God Power" UI (`Scripts/UI.gd`)
- Kita akan menyuntikkan deretan tombol kekuatan Dewa di atas (atau di panel khusus) yang menggunakan gaya *Retro 9-Slice*.
- Daftar kekuatan:
  1. `💧 Water`
  2. `⛰ Mountain`
  3. `🌲 Forest`
  4. `🟩 Eraser`
  5. `💣 Bomb`
  6. `⚡ Lightning`
  7. `🔴 Spawn Red`
  8. `🔵 Spawn Blue`
  9. `👻 Possess Hero`

### 2. Terrain & Boids Repulsors (`Scripts/World.gd` & `Scripts/Unit.gd`)
Di Python, kita mengubah `GridMap`. Di Godot, fisika dimatikan (pergerakan manual Boids). Jadi, kita akan meniru efek benturan dengan gaya kemudi (Steering Behaviors):
- **Water & Mountain:** Saat dipanggil, Godot akan memunculkan sebuah *Node2D* (Obstacle) di lokasi kursor. `Unit.gd` di dalam fungsi Boids-nya akan membaca *Obstacle* ini dan mendapatkan **Daya Tolak (Repulsion) Super Kuat** agar unit otomatis membelok dan berjalan memutarinya tanpa tersangkut.
- **Forest:** Memanggil `ResourceScene` baru (`rtype = "wood"`) di posisi kursor.
- **Eraser:** Menghapus *Obstacle* atau *Resource* yang berada di bawah kursor.

### 3. Destruction Powers (`Scripts/World.gd`)
- **Bomb:** Ledakan radius besar! Memanggil fungsi `get_units_near()` dan mengurangi HP mereka secara masif. Ditambah pemanggilan `EventBus.shake_camera(10.0, 0.5)` untuk efek guncangan layar.
- **Lightning:** Serangan area kecil mematikan dengan efek kilat vertikal (menggunakan `Line2D` yang muncul sesaat).

### 4. Hero Possession Mechanics (`Scripts/Unit.gd` & `World.gd`)
Sama seperti konsep sebelumnya:
- **AI Bypass:** Jika `is_possessed = true`, fungsi AI pekerja/pasukan berhenti, digantikan fungsi `_tick_hero()`.
- **Keyboard (WASD):** Menggerakkan Hero.
- **Kursor Mouse:** Membidik arah hadap.
- **Left Click (Slash):** *Damage* area di depan karakter menggunakan *dot product*.
- **Right Click / Space (Dash):** Melesat cepat (kecepatan x8) sambil memberikan *damage* ke musuh di sepanjang lintasannya.

### 5. Visual Effects & Polish
- **Brush Indikator:** Kursor akan memiliki bayangan lingkaran transparan (Brush) saat salah satu kekuatan Dewa aktif agar pemain tahu area jangkauannya.
- **Aura Pahlawan:** Lingkaran emas dan *cooldown bar* kecil di atas kepala Hero.
- **VFX Godot:** Kita akan memanfaatkan kemampuan Godot seperti `Tween` untuk ledakan dan `CanvasItem` kustom untuk garis tebasan pedang.

## ❓ Open Questions / User Review Required
1. **Navigasi Rintangan (Boids):** Apakah Anda setuju gunung/sungai murni mengandalkan daya tolak (*repulsion*)? Ini membuat unit terlihat lebih organik mengalir seperti air saat menghindari gunung.
2. **Akses Tombol UI:** Tombol kekuatan dewanya cukup banyak. Apakah Anda ingin tombolnya di jejer memanjang di bagian atas layar (sebelah *Time Controls*), atau disembunyikan dalam menu pop-up/panel kecil di pojok bawah?

Silakan tinjau proposal lengkap God Mode ini. Jawab pertanyaannya, dan kita akan segera memulai integrasi masif ini!
