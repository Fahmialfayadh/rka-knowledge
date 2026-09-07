import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Arc, FancyArrowPatch


# Setup directory
output_dir = 'modul/images'
os.makedirs(output_dir, exist_ok=True)

# Common styling
plt.style.use('default')
def setup_ax(ax, title=""):
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.axhline(0, color='black', lw=1.2)
    ax.axvline(0, color='black', lw=1.2)

print("Generating images...")

# 1. 01_luas_kurva_ex1.png
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(-1, 6, 400)
y1 = 5 * x
y2 = x**2
ax.plot(x, y1, label='$y=5x$', color='C0')
ax.plot(x, y2, label='$y=x^2$', color='C1')
xf = np.linspace(0, 5, 100)
ax.fill_between(xf, 5*xf, xf**2, color='C0', alpha=0.3)
setup_ax(ax)
ax.legend()
plt.savefig(os.path.join(output_dir, '01_luas_kurva_ex1.png'), bbox_inches='tight', dpi=150)
plt.close()

# 2. 01_luas_kurva_ex2.png
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(-3, 5, 400)
y1 = 2 * x + 3
y2 = x**2
ax.plot(x, y1, label='$y=2x+3$', color='C0')
ax.plot(x, y2, label='$y=x^2$', color='C1')
xf = np.linspace(-1, 3, 100)
ax.fill_between(xf, 2*xf+3, xf**2, color='C0', alpha=0.3)
setup_ax(ax)
ax.legend()
plt.savefig(os.path.join(output_dir, '01_luas_kurva_ex2.png'), bbox_inches='tight', dpi=150)
plt.close()

# 3. 02_luas_putar_ex1.png
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(0, 1.2, 100)
ax.plot(x, x, label='$y=x$', color='C0', lw=2)
ax.plot(x, -x, color='C0', ls='--', alpha=0.5)
# Draw ellipses to show 3D revolution
for xi in [0.25, 0.5, 0.75, 1.0]:
    ell = Ellipse(xy=(xi, 0), width=0.1*xi, height=2*xi, fill=False, color='C0', alpha=0.5)
    ax.add_patch(ell)
xf = np.linspace(0, 1, 100)
ax.fill_between(xf, xf, -xf, color='C0', alpha=0.1)
setup_ax(ax, "Surface of Revolution: $y=x$ around x-axis")
ax.legend()
plt.savefig(os.path.join(output_dir, '02_luas_putar_ex1.png'), bbox_inches='tight', dpi=150)
plt.close()

# 4. 02_luas_putar_ex2.png
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(0, 4.5, 400)
ax.plot(x, np.sqrt(x), label='$y=\sqrt{x}$', color='C0', lw=2)
ax.plot(x, -np.sqrt(x), color='C0', ls='--', alpha=0.5)
xf = np.linspace(1, 4, 100)
for xi in [1, 2, 3, 4]:
    ell = Ellipse(xy=(xi, 0), width=0.15*np.sqrt(xi), height=2*np.sqrt(xi), fill=False, color='C0', alpha=0.5)
    ax.add_patch(ell)
ax.fill_between(xf, np.sqrt(xf), -np.sqrt(xf), color='C0', alpha=0.1)
setup_ax(ax, "Surface of Revolution: $y=\sqrt{x}$ around x-axis")
ax.legend()
plt.savefig(os.path.join(output_dir, '02_luas_putar_ex2.png'), bbox_inches='tight', dpi=150)
plt.close()

# 5. 03_centroid_ex1.png
fig, ax = plt.subplots(figsize=(5, 5))
x = np.linspace(-0.2, 1.2, 200)
ax.plot(x, x, label='$y=x$')
ax.plot(x, x**2, label='$y=x^2$')
xf = np.linspace(0, 1, 100)
ax.fill_between(xf, xf, xf**2, color='gray', alpha=0.3)
cx, cy = 0.5, 0.4
ax.plot(cx, cy, 'ro', label=f'Centroid ({cx}, {cy})')
setup_ax(ax)
ax.legend()
plt.savefig(os.path.join(output_dir, '03_centroid_ex1.png'), bbox_inches='tight', dpi=150)
plt.close()

# 6. 03_centroid_ex2.png
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(0, 4.5, 200)
ax.plot(x, np.sqrt(x), label='$y=\sqrt{x}$')
ax.axvline(4, color='green', label='$x=4$')
xf = np.linspace(0, 4, 100)
ax.fill_between(xf, np.sqrt(xf), 0, color='gray', alpha=0.3)
cx, cy = 2.4, 1.5
ax.plot(cx, cy, 'ro', label=f'Centroid ({cx:.1f}, {cy:.1f})')
setup_ax(ax)
ax.legend()
plt.savefig(os.path.join(output_dir, '03_centroid_ex2.png'), bbox_inches='tight', dpi=150)
plt.close()

# 7. 04_parametric_ex1.png
fig, ax = plt.subplots(figsize=(6, 5))
t = np.linspace(-2.5, 2.5, 400)
x = t**2 - 1
y = t**3 - 3*t
ax.plot(x, y, label='$(t^2-1, t^3-3t)$')
ax.plot(0, 2, 'ro', label='Horizontal Tangent')
ax.plot(0, -2, 'ro')
ax.axhline(2, color='r', ls='--', alpha=0.5)
ax.axhline(-2, color='r', ls='--', alpha=0.5)
setup_ax(ax)
ax.legend()
plt.savefig(os.path.join(output_dir, '04_parametric_ex1.png'), bbox_inches='tight', dpi=150)
plt.close()

# 8. 04_parametric_ex3.png (Cycloid)
fig, ax = plt.subplots(figsize=(7, 3))
t = np.linspace(0, 2*np.pi, 200)
x = t - np.sin(t)
y = 1 - np.cos(t)
ax.plot(x, y, label='Cycloid')
ax.fill_between(x, y, 0, color='C0', alpha=0.3)
setup_ax(ax)
ax.set_aspect('equal')
ax.legend()
plt.savefig(os.path.join(output_dir, '04_parametric_ex3.png'), bbox_inches='tight', dpi=150)
plt.close()

# 9. 05_polar_concept.png
fig, ax = plt.subplots(figsize=(5, 5))
r = 3
theta = np.pi / 4
x, y = r * np.cos(theta), r * np.sin(theta)
ax.plot([0, x], [0, y], 'b-', lw=2)
ax.plot(x, y, 'ro')
ax.annotate('P(r, $\\theta$)', xy=(x, y), xytext=(x+0.2, y+0.2), fontsize=12)
ax.annotate('r', xy=(x/2, y/2), xytext=(x/2-0.3, y/2+0.1), fontsize=12, color='blue')
arc = Arc((0,0), 1.5, 1.5, angle=0, theta1=0, theta2=45, color='red', lw=1.5)
ax.add_patch(arc)
ax.annotate('$\\theta$', xy=(0.8, 0.3), fontsize=12, color='red')
setup_ax(ax)
ax.set_xlim(-1, 4)
ax.set_ylim(-1, 4)
plt.savefig(os.path.join(output_dir, '05_polar_concept.png'), bbox_inches='tight', dpi=150)
plt.close()

# 10. 05_polar_cardioid.png
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
theta = np.linspace(0, 2*np.pi, 400)
r = 1 + np.cos(theta)
ax.plot(theta, r, color='C0', lw=2)
ax.set_title('Cardioid: $r = 1 + \cos\\theta$')
plt.savefig(os.path.join(output_dir, '05_polar_cardioid.png'), bbox_inches='tight', dpi=150)
plt.close()

# 11. 05_polar_limacon.png
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
r = 1 + 2*np.cos(theta)
ax.plot(theta, r, color='C1', lw=2)
ax.set_title('Limaçon: $r = 1 + 2\cos\\theta$')
plt.savefig(os.path.join(output_dir, '05_polar_limacon.png'), bbox_inches='tight', dpi=150)
plt.close()

# 12. 05_polar_rose.png
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
r = np.cos(3*theta)
ax.plot(theta, r, color='C2', lw=2)
ax.set_title('Rose Curve: $r = \cos(3\\theta)$')
plt.savefig(os.path.join(output_dir, '05_polar_rose.png'), bbox_inches='tight', dpi=150)
plt.close()

# 13. 06_polar_sector.png
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
theta_sector = np.linspace(np.pi/6, np.pi/3, 100)
r_sector = 1 + 0.5*np.sin(3*theta_sector)
ax.plot(theta_sector, r_sector, color='black', lw=2)
ax.fill_between(theta_sector, 0, r_sector, color='orange', alpha=0.5)
ax.plot([np.pi/6, np.pi/6], [0, 1 + 0.5*np.sin(3*np.pi/6)], 'k--')
ax.plot([np.pi/3, np.pi/3], [0, 1 + 0.5*np.sin(3*np.pi/3)], 'k--')
ax.set_title('Polar Sector Area')
plt.savefig(os.path.join(output_dir, '06_polar_sector.png'), bbox_inches='tight', dpi=150)
plt.close()

# 14. 06_polar_area_ex1.png
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
theta = np.linspace(0, 2*np.pi, 400)
r = 1 + np.cos(theta)
ax.plot(theta, r, color='C0', lw=2)
ax.fill_between(theta, 0, r, color='C0', alpha=0.3)
ax.set_title('Area of Cardioid')
plt.savefig(os.path.join(output_dir, '06_polar_area_ex1.png'), bbox_inches='tight', dpi=150)
plt.close()

# 15. 06_polar_area_ex2.png
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})
theta = np.linspace(0, 2*np.pi, 400)
r1 = 3 * np.sin(theta)
r2 = 1 + np.sin(theta)
ax.plot(theta, r1, label='$r=3\sin\\theta$', color='C0')
ax.plot(theta, r2, label='$r=1+\sin\\theta$', color='C1')
theta_fill = np.linspace(np.pi/6, 5*np.pi/6, 200)
r1_fill = 3 * np.sin(theta_fill)
r2_fill = 1 + np.sin(theta_fill)
ax.fill_between(theta_fill, r2_fill, r1_fill, color='purple', alpha=0.3)
ax.legend(loc='lower right')
plt.savefig(os.path.join(output_dir, '06_polar_area_ex2.png'), bbox_inches='tight', dpi=150)
plt.close()

# 16. 07_sequence_conv_div.png
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
n = np.arange(1, 21)
ax1.plot(n, 1/n, 'bo')
ax1.set_title('Konvergen: $a_n = 1/n$')
setup_ax(ax1)
ax2.plot(n, n**2 / 10, 'ro')
ax2.set_title('Divergen: $a_n = n^2$')
setup_ax(ax2)
plt.savefig(os.path.join(output_dir, '07_sequence_conv_div.png'), bbox_inches='tight', dpi=150)
plt.close()

# 17. 07_sequence_squeeze.png
fig, ax = plt.subplots(figsize=(7, 4))
n = np.arange(1, 31)
an = ((-1)**n) / n
ax.plot(n, an, 'bo', label='$(-1)^n / n$')
x_cont = np.linspace(1, 30, 200)
ax.plot(x_cont, 1/x_cont, 'r--', label='$1/n$')
ax.plot(x_cont, -1/x_cont, 'g--', label='$-1/n$')
setup_ax(ax, 'Teorema Apit (Squeeze Theorem)')
ax.legend()
plt.savefig(os.path.join(output_dir, '07_sequence_squeeze.png'), bbox_inches='tight', dpi=150)
plt.close()

# 18. 07_sequence_mct.png
fig, ax = plt.subplots(figsize=(7, 4))
n = np.arange(1, 15)
an = np.zeros(14)
an[0] = 1
for i in range(1, 14):
    an[i] = np.sqrt(2 + an[i-1])
ax.plot(n, an, 'bo-', label='$a_{n+1} = \sqrt{2+a_n}$')
ax.axhline(2, color='r', ls='--', label='Limit L = 2')
setup_ax(ax, 'Monotonic Sequence Theorem')
ax.legend()
plt.savefig(os.path.join(output_dir, '07_sequence_mct.png'), bbox_inches='tight', dpi=150)
plt.close()

# 19. 08_volume_putar_ex1.png
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(-0.5, 2.5, 200)
ax.plot(x, 2*x, label='$y=2x$')
ax.plot(x, x**2, label='$y=x^2$')
xf = np.linspace(0, 2, 100)
ax.fill_between(xf, xf**2, 2*xf, color='C2', alpha=0.4)
ax.annotate('', xy=(1.5, -0.5), xytext=(1.5, 0.5),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.5", color='black', lw=1.5))
ax.text(1.6, -0.2, "Putar Sumbu-X")
setup_ax(ax, 'Volume Benda Putar (Metode Cincin)')
ax.legend()
plt.savefig(os.path.join(output_dir, '08_volume_putar_ex1.png'), bbox_inches='tight', dpi=150)
plt.close()

# 20. 08_volume_putar_ex2.png
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(0, 2.5, 200)
ax.plot(x, x**2, label='$y=x^2$')
ax.axvline(2, color='r', label='$x=2$')
xf = np.linspace(0, 2, 100)
ax.fill_between(xf, 0, xf**2, color='orange', alpha=0.4)
ax.annotate('', xy=(-0.5, 2), xytext=(0.5, 2),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.5", color='black', lw=1.5))
ax.text(0.6, 2, "Putar Sumbu-Y")
setup_ax(ax, 'Volume Benda Putar (Metode Kulit Tabung)')
ax.legend()
plt.savefig(os.path.join(output_dir, '08_volume_putar_ex2.png'), bbox_inches='tight', dpi=150)
plt.close()

print("All 20 images generated successfully!")
