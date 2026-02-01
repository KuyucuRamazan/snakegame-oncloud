```python
import pygame
import random

# Pygame Kütüphanesi Kullanımı
pygame.init()

# Renk ve grafik ayarları
renk_siyah = (0, 0, 0)
renk_beyaz = (255, 255, 255)
renk_yeşil = (0, 128, 0)

# Pencere boyutu ve pozisyonaffectleri
pencere_boyutu = (800, 600)
pencere_pozisyonu = (100, 100)
pencere = pygame.display.set_mode(pencere_boyutu)

# Tıklayıcı objeler
yılan_kordinatlari = [(200, 200), (220, 200), (240, 200)]
yumurta_kordinatleri = (random.randint(0, 800), random.randint(0, 600))

# Skor Tablosu
skor = 0

# Oyunun temel işlemleri
def yılan_hareketi():
    global yılan_kordinatlari
    yilan_sabit_kordinatlar = [y for x, y in yılan_kordinatlari]
    yılan_kordinatlari.pop()
    yılan_kordinatlari.insert(0, (yilan_sabit_kordinatlar[0] + 20, yilan_sabit_kordinatlar[1]))

def yumurta_yenilmesi(yumurta):
    global skor
    if yılan_kordinatlari[-1][0] == yumurta[0] and yılan_kordinatlari[-1][1] == yumurta[1]:
        skor += 1
        return True

def oyun_bitimi():
    global yalan_kordinatlari
    if yalan_kordinatlari[-1][0] < 0 or yalan_kordinatlari[-1][0] > 780:
        print("Oyun Bitti!")
        pygame.quit()
        quit()

# Oyun loopu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and yalan_kordinatlari[-1][0] - 20 > 0:
                yılan_hareketi()
            elif event.key == pygame.K_RIGHT and yalan_kordinatlari[-1][0] + 20 < 780:
                yılan_hareketi()
            elif event.key == pygame.K_UP and yalan_kordinatlari[-1][1] - 20 > 0:
                yılan_hareketi()
            elif event.key == pygame.K_DOWN and yalan_kordinatlari[-1][1] + 20 < 580:
                yılan_hareketi()

    pencere.fill(renk_siyah)
    for x, y in yalan_kordinatlari:
        pygame.draw.rect(pencere, renk_yeşil, (x, y, 20, 20))
    pygame.draw.rect(pencere, renk_beyaz, (yumurta_kordinatleri[0], yumurta_kordinatleri[1], 20, 20))

    if yumurta_yenilmesi(yumurta_kordinatleri):
        yumurta_kordinatleri = (random.randint(0, 780), random.randint(0, 580))
    oyun_bitimi()

    pygame.display.update()
    pygame.time.Clock().tick(60)
```