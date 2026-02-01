import pygame
import time
import random

# Pygame'i başlat
pygame.init()

# Renkler
BEYAZ = (255, 255, 255)
SARI = (255, 255, 102)
SIYAH = (0, 0, 0)
KIRMIZI = (213, 50, 80)
YESIL = (0, 255, 0)
MAVI = (50, 153, 213)

# Ekran Boyutları
GENISLIK = 600
YUKSEKLIK = 400

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption('Yapay Zeka Yılan Oyunu')

saat = pygame.time.Clock()

yilan_blok = 10
yilan_hizi = 15

font_stil = pygame.font.SysFont("bahnschrift", 25)
skor_font = pygame.font.SysFont("comicsansms", 35)

def skoru_goster(skor):
    deger = skor_font.render("Skor: " + str(skor), True, SARI)
    ekran.blit(deger, [0, 0])

def yilan(yilan_blok, yilan_listesi):
    for x in yilan_listesi:
        pygame.draw.rect(ekran, YESIL, [x[0], x[1], yilan_blok, yilan_blok])

def mesaj(msg, color):
    mesaj_yazisi = font_stil.render(msg, True, color)
    ekran.blit(mesaj_yazisi, [GENISLIK / 6, YUKSEKLIK / 3])

def oyunu_baslat():
    oyun_bitti = False
    oyun_kapandi = False

    x1 = GENISLIK / 2
    y1 = YUKSEKLIK / 2

    x1_degisim = 0
    y1_degisim = 0

    yilan_listesi = []
    yilan_uzunlugu = 1

    yem_x = round(random.randrange(0, GENISLIK - yilan_blok) / 10.0) * 10.0
    yem_y = round(random.randrange(0, YUKSEKLIK - yilan_blok) / 10.0) * 10.0

    while not oyun_bitti:

        while oyun_kapandi == True:
            ekran.fill(SIYAH)
            mesaj("Kaybettin! Tekrar oyna: C, Cikis: Q", KIRMIZI)
            skoru_goster(yilan_uzunlugu - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        oyun_bitti = True
                        oyun_kapandi = False
                    if event.key == pygame.K_c:
                        oyunu_baslat()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyun_bitti = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_degisim = -yilan_blok
                    y1_degisim = 0
                elif event.key == pygame.K_RIGHT:
                    x1_degisim = yilan_blok
                    y1_degisim = 0
                elif event.key == pygame.K_UP:
                    y1_degisim = -yilan_blok
                    x1_degisim = 0
                elif event.key == pygame.K_DOWN:
                    y1_degisim = yilan_blok
                    x1_degisim = 0

        if x1 >= GENISLIK or x1 < 0 or y1 >= YUKSEKLIK or y1 < 0:
            oyun_kapandi = True
        
        x1 += x1_degisim
        y1 += y1_degisim
        ekran.fill(SIYAH)
        pygame.draw.rect(ekran, KIRMIZI, [yem_x, yem_y, yilan_blok, yilan_blok])
        
        yilan_basi = []
        yilan_basi.append(x1)
        yilan_basi.append(y1)
        yilan_listesi.append(yilan_basi)
        
        if len(yilan_listesi) > yilan_uzunlugu:
            del yilan_listesi[0]

        for x in yilan_listesi[:-1]:
            if x == yilan_basi:
                oyun_kapandi = True

        yilan(yilan_blok, yilan_listesi)
        skoru_goster(yilan_uzunlugu - 1)

        pygame.display.update()

        if x1 == yem_x and y1 == yem_y:
            yem_x = round(random.randrange(0, GENISLIK - yilan_blok) / 10.0) * 10.0
            yem_y = round(random.randrange(0, YUKSEKLIK - yilan_blok) / 10.0) * 10.0
            yilan_uzunlugu += 1

        saat.tick(yilan_hizi)

    pygame.quit()
    quit()

oyunu_baslat()