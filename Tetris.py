import pygame
import sys
import random
import copy
from pygame.draw import rect
from pygame.locals import *

# from random import randint
# from math import pi
pygame.init()

# ---CZAS--------------------------------------------------------------------------------------------------------------
class Timer():

    def __init__(self):
        self._start = 0

    def start(self):
        self._start = pygame.time.get_ticks()

    def current(self):
        return (pygame.time.get_ticks() - self._start) / 1000

t = Timer()
t.start()

# ---KOLORY------------------------------------------------------------------------------------------------------------

BLACK = (0, 0, 0)
GREY = (120, 120, 120)
GREYDARK = (66, 66, 66)
GREYLIGHT = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 144)
ORANGE = (255, 166, 0)
BLUELIGHT = (0, 255, 255)

def vertical(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1,height)).convert_alpha()
    dd = 1.0/height
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er-sr)*dd
    gm = (eg-sg)*dd
    bm = (eb-sb)*dd
    am = (ea-sa)*dd
    for y in range(height):
        bigSurf.set_at((0,y),
                        (int(sr + rm*y),
                         int(sg + gm*y),
                         int(sb + bm*y),
                         int(sa + am*y))
                      )
    return pygame.transform.scale(bigSurf, size)
# ---OKIENKO-----------------------------------------------------------------------------------------------------------
szerokosc = 700
wysokosc = 720
okienko = pygame.display.set_mode((szerokosc, wysokosc))
okienko.fill(GREY)
pygame.display.set_caption("Tetris version 1.1")

# ---ZMIENNE-----------------------------------------------------------------------------------------------------------
grubosc = 1
kwadracik = 40

poz_tetrisa_x = int(szerokosc * 0.1)                    # wyrazone w pikselach początek tablicy
poz_tetrisa_y = int(wysokosc * 0.1)                     # wyrazone w pikselach początek tablicy

wym_x = 10                                              # wyrazone w liczbie kratek
wym_y = 15                                              # wyrazone w liczbie kratek

wym_tablicy_x = wym_x*kwadracik
wym_tablicy_y = wym_y*kwadracik


poz_f_x = 4  # indeks
poz_f_y = 0  # indeks

poz_next_fig_x = poz_tetrisa_x + wym_tablicy_x + kwadracik * 2
poz_next_fig_y = poz_tetrisa_y + kwadracik * 7 + 11


poz_tetrisa_start = 4  # indeks
tablica = [[0 for n in range(wym_x)] for n in range(wym_y)]   # tablica
zmienna = 1

punkty = 0
level = 1
pom_level = 0
suma_rzedow = 0
end = 0
tetrisy = 0

# ---WYGLĄD------------------------------------------------------------------------------------------------------------

pygame.draw.rect(okienko, BLACK,        [poz_tetrisa_x + 3, poz_tetrisa_y + 3, 400, 600])
pygame.draw.rect(okienko, GREYDARK,     [poz_tetrisa_x, poz_tetrisa_y, 400, 600], grubosc)
pygame.draw.rect(okienko, GREYLIGHT,    [poz_tetrisa_x + grubosc, poz_tetrisa_y + grubosc, 400 - grubosc * 2, 600 - grubosc * 2])


for i in range(wym_x-1):
    pygame.draw.line(okienko, GREY, [i * kwadracik + poz_tetrisa_x + kwadracik, poz_tetrisa_y + 2],
                    [i * kwadracik + poz_tetrisa_x + kwadracik, poz_tetrisa_y + 600 - 3], 1)
for i in range(wym_y-1):
    pygame.draw.line(okienko, GREY, [poz_tetrisa_x + 2, i * kwadracik + poz_tetrisa_y + kwadracik],
                    [poz_tetrisa_x + 400 - 3, i * kwadracik + poz_tetrisa_y + kwadracik], 1)


pygame.draw.circle(okienko, BLACK, [152, 723], 40)
pygame.draw.circle(okienko, GREYDARK, [150, 720], 40)
pygame.draw.circle(okienko, GREYLIGHT, [150, 720], 37)

pygame.draw.circle(okienko, BLACK, [352, 723], 40)
pygame.draw.circle(okienko, GREYDARK, [350, 720], 40)
pygame.draw.circle(okienko, GREYLIGHT, [350, 720], 37)


# ---FIGURY------------------------------------------------------------------------------------------------------------

def blok(poz_x, poz_y, kolor):  # rysuje blok w tablicy w danym kolorze
    pygame.draw.rect(okienko, kolor, [poz_x + 1, poz_y + 1, kwadracik - 1, kwadracik - 1])

#    pygame.draw.rect(okienko, kolor, [poz_x + kwadracik + 1, poz_y + 1, kwadracik - 1, kwadracik - 1])
#    pygame.draw.rect(okienko, kolor, [poz_x + 1, poz_y + kwadracik + 1, kwadracik - 1, kwadracik - 1])
#    pygame.draw.rect(okienko, kolor, [poz_x + kwadracik + 1, poz_y + kwadracik + 1, kwadracik - 1, kwadracik - 1])

f_fig1 = [
    [1, 1],
    [1, 1]]

f_fig2 = [
    [0, 2, 0],
    [0, 2, 0],
    [2, 2, 0]]

f_fig3 = [
    [0, 3, 0],
    [0, 3, 0],
    [0, 3, 3]]

f_fig4 = [
    [4, 0, 0],
    [4, 4, 0],
    [0, 4, 0]]

f_fig5 = [
    [0, 0, 5],
    [0, 5, 5],
    [0, 5, 0]]

f_fig6 = [
    [0, 6, 0],
    [6, 6, 6],
    [0, 0, 0]]

f_fig7 = [
    [0, 7, 0, 0],
    [0, 7, 0, 0],
    [0, 7, 0, 0],
    [0, 7, 0, 0]]


def fig(liczba):  # po podaniu liczby z tablicy zwraca figurę
    if liczba == 1:
        return f_fig1
    if liczba == 2:
        return f_fig2
    if liczba == 3:
        return f_fig3
    if liczba == 4:
        return f_fig4
    if liczba == 5:
        return f_fig5
    if liczba == 6:
        return f_fig6
    if liczba == 7:
        return f_fig7


def wyswietl_tablice():  # dosłownie, wyświetla tablicę
    p_x = poz_tetrisa_x
    p_y = poz_tetrisa_y
    for i in range(wym_y):
        for j in range(wym_x):
            if tablica[i][j] == 1:
                blok(j * 40 + poz_tetrisa_x, i * 40 + poz_tetrisa_y, YELLOW)
            if tablica[i][j] == 2:
                blok(j * 40 + poz_tetrisa_x, i * 40 + poz_tetrisa_y, BLUE)
            if tablica[i][j] == 3:
                blok(j * 40 + poz_tetrisa_x, i * 40 + poz_tetrisa_y, ORANGE)
            if tablica[i][j] == 4:
                blok(j * 40 + poz_tetrisa_x, i * 40 + poz_tetrisa_y, GREEN)
            if tablica[i][j] == 5:
                blok(j * 40 + poz_tetrisa_x, i * 40 + poz_tetrisa_y, RED)
            if tablica[i][j] == 6:
                blok(j * 40 + poz_tetrisa_x, i * 40 + poz_tetrisa_y, MAGENTA)
            if tablica[i][j] == 7:
                blok(j * 40 + poz_tetrisa_x, i * 40 + poz_tetrisa_y, BLUELIGHT)
            p_x = p_x + 40
            p_y = p_y + 40

def czy_w_granicy(x, y):
    if 0 <= x <= wym_x-1 and 0 <= y <= wym_y-1:
        return 1
    return 0

def dodaj_do_tablicy(figura, x, y):                             # dodaje do tablicy figurę na stałe, kiedy blok się ZATRZYMA
    for j in range(len(figura)):
        for i in range(len(figura)):
            if czy_w_granicy(i+x, j+y) and tablica[j + y][i + x] == 0:
                tablica[j + y][i + x] = figura[j][i]
    return tablica

def czy_moze_tu_byc(x, y, figura):
    for i in range(len(figura)):
        for j in range(len(figura)):
            if figura[j][i] > 0 and czy_w_granicy(x + i, y + j) and tablica[j + y][i + x] > 0:
                return 0
            if x + i >= wym_x and figura[j][i] > 0:
                return 0
            if x + i < 0 and figura[j][i] > 0:
                return 0
            if y + j >= wym_y and figura[j][i] > 0:
                return 0
    return 1

def pokaz_figure(figura, x, y):  # osobno pokazuje figurę bez tablicy
    for i in range(len(figura)):
        for j in range(len(figura)):
            if figura[i][j] == 1:
                blok(j * 40 + poz_tetrisa_x + 40 * x, i * 40 + poz_tetrisa_y + 40 * y, YELLOW)
            if figura[i][j] == 2:
                blok(j * 40 + poz_tetrisa_x + 40 * x, i * 40 + poz_tetrisa_y + 40 * y, BLUE)
            if figura[i][j] == 3:
                blok(j * 40 + poz_tetrisa_x + 40 * x, i * 40 + poz_tetrisa_y + 40 * y, ORANGE)
            if figura[i][j] == 4:
                blok(j * 40 + poz_tetrisa_x + 40 * x, i * 40 + poz_tetrisa_y + 40 * y, GREEN)
            if figura[i][j] == 5:
                blok(j * 40 + poz_tetrisa_x + 40 * x, i * 40 + poz_tetrisa_y + 40 * y, RED)
            if figura[i][j] == 6:
                blok(j * 40 + poz_tetrisa_x + 40 * x, i * 40 + poz_tetrisa_y + 40 * y, MAGENTA)
            if figura[i][j] == 7:
                blok(j * 40 + poz_tetrisa_x + 40 * x, i * 40 + poz_tetrisa_y + 40 * y, BLUELIGHT)

def obroc_figure(figura):
    kopia = copy.deepcopy(figura)
    for i in range(len(figura)):
        for j in range(len(figura)):
            kopia[i][j] = figura[j][len(figura)-1-i]
    return kopia

def usun_rzedy(tablica, suma_rzedow):
    rzadek = False
    ile_rzedow = 0
    for k in range(4):
        for i in range(wym_y):
            for j in range(wym_x):
                if tablica[wym_y-i-1][j] > 0:
                    rzadek = True
                else:
                    rzadek = False
                    break
            if rzadek:
                tablica.pop(wym_y - i - 1)
                tablica.insert(0, [0 for n in range(wym_x)])
                ile_rzedow = ile_rzedow + 1
                suma_rzedow = suma_rzedow + 1
                break
    return ile_rzedow

def wyswietl_punkty(ile_rzedow, punkty, level):
    if ile_rzedow == 1:
        punkty = punkty + 40 * (level + 1)
    if ile_rzedow == 2:
        punkty = punkty + 100 * (level + 1)
    if ile_rzedow == 3:
        punkty = punkty + 300 * (level + 1)
    if ile_rzedow == 4:
        punkty = punkty + 1200 * (level + 1)

    return punkty

def losuj_kolor_punkty(punkty):
    kolorek = 1
    if punkty > 30:
        kolorek = random.randint(1, 7)

    if kolorek == 1:
        return WHITE
    if kolorek == 2:
        return RED
    if kolorek == 3:
        return GREEN
    if kolorek == 4:
        return BLUE
    if kolorek == 5:
        return YELLOW
    if kolorek == 6:
        return MAGENTA
    if kolorek == 7:
        return ORANGE
    if kolorek == 8:
        return BLUELIGHT

#def przyspiesz(czas):

# ---ZMIENNE CZ. 2-----------------------------------------------------------------------------------------------------
wyb_fig = random.randint(1, 7)
next_fig = random.randint(1, 7)
licznik = 0
aktualna_figura = fig(wyb_fig)
aktualna_poz_x = 4
aktualna_poz_y = 0
stop = False
czas = 300

# ---GŁÓWNA------------------------------------------------------------------------------------------------------------

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_LEFT and czy_moze_tu_byc(aktualna_poz_x-1, aktualna_poz_y, aktualna_figura):
            aktualna_poz_x = aktualna_poz_x - 1
        if event.type == KEYDOWN and event.key == K_RIGHT and czy_moze_tu_byc(aktualna_poz_x+1, aktualna_poz_y, aktualna_figura):
            aktualna_poz_x = aktualna_poz_x + 1
        if event.type == KEYDOWN and event.key == K_DOWN:
            czas = 200
            licznik = czas
        if event.type == KEYDOWN and event.key == K_UP:
            czas = 400
        if event.type == KEYDOWN and event.key == K_SPACE and czy_moze_tu_byc(aktualna_poz_x, aktualna_poz_y, obroc_figure(aktualna_figura)):
            aktualna_figura = obroc_figure(aktualna_figura)

    # ---RYSOWANIE TŁA-------------------------------------------------------------------------------------------------
    okienko.fill(GREY)
    pygame.draw.rect(okienko, BLACK, [poz_tetrisa_x + 3, poz_tetrisa_y + 3, wym_tablicy_x, wym_tablicy_y])
    pygame.draw.rect(okienko, GREYDARK, [poz_tetrisa_x, poz_tetrisa_y, wym_tablicy_x, wym_tablicy_y], grubosc)
    pygame.draw.rect(okienko, GREYLIGHT,
                     [poz_tetrisa_x + grubosc, poz_tetrisa_y + grubosc, wym_tablicy_x - grubosc * 2, wym_tablicy_y - grubosc * 2])

    pygame.draw.rect(okienko, BLACK, [poz_tetrisa_x + 3, poz_tetrisa_y + 3, wym_tablicy_x, wym_tablicy_y])
    pygame.draw.rect(okienko, GREYDARK, [poz_tetrisa_x, poz_tetrisa_y, wym_tablicy_x, wym_tablicy_y], grubosc)
    pygame.draw.rect(okienko, GREYLIGHT,
                     [poz_tetrisa_x + grubosc, poz_tetrisa_y + grubosc, wym_tablicy_x - grubosc * 2, wym_tablicy_y - grubosc * 2])

    for i in range(wym_x-1):
        pygame.draw.line(okienko, GREY,     [i * 40 + poz_tetrisa_x + 40, poz_tetrisa_y + 2],
                                                [i * 40 + poz_tetrisa_x + 40, poz_tetrisa_y + wym_tablicy_y - 3], 1)
    for i in range(wym_y-1):
        pygame.draw.line(okienko, GREY,     [poz_tetrisa_x + 2, i * 40 + poz_tetrisa_y + 40],
                                                [poz_tetrisa_x + wym_tablicy_x - 3, i * 40 + poz_tetrisa_y + 40], 1)

    pygame.draw.line(okienko,   BLACK,      [poz_tetrisa_x + wym_tablicy_x + kwadracik + 1, poz_tetrisa_y + 11],
                     [poz_tetrisa_x + wym_tablicy_x + kwadracik +1, poz_tetrisa_y + 601 - 10], 2)

    pygame.draw.line(okienko,   GREYLIGHT,  [poz_tetrisa_x + wym_tablicy_x + kwadracik, poz_tetrisa_y + 10],
                     [poz_tetrisa_x + wym_tablicy_x + kwadracik, poz_tetrisa_y + wym_tablicy_y - 10], 2)

 #   pygame.draw.circle(okienko, BLACK,      [poz_tetrisa_x + 60 + 2, poz_tetrisa_y + wym_tablicy_y + 63], 40)
 #   pygame.draw.circle(okienko, GREYDARK,   [poz_tetrisa_x + 60, poz_tetrisa_y + wym_tablicy_y + 60], 40)
 #   pygame.draw.circle(okienko, GREYLIGHT,  [poz_tetrisa_x + 60, poz_tetrisa_y + wym_tablicy_y + 60], 37)

 #   pygame.draw.circle(okienko, BLACK,      [poz_tetrisa_x + wym_tablicy_x - 60 + 2, poz_tetrisa_y + wym_tablicy_y + 63], 40)
 #   pygame.draw.circle(okienko, GREYDARK,   [poz_tetrisa_x + wym_tablicy_x - 60, poz_tetrisa_y + wym_tablicy_y + 60], 40)
 #   pygame.draw.circle(okienko, GREYLIGHT,  [poz_tetrisa_x + wym_tablicy_x - 60, poz_tetrisa_y + wym_tablicy_y + 60], 37)

    myfont = pygame.font.SysFont('Arial', 30)                   # ustawianie czcionki i wielkosci czcionki
    endfont = pygame.font.SysFont('Arial Black', 60)

    tetdark = myfont.render('TETRIS', False, BLACK)             # Napis "Tetris"
    tetlight = myfont.render('TETRIS', False, YELLOW)

    dark = myfont.render('Points', False, BLACK)                # Napis "Punkty"
    light = myfont.render('Points', False, WHITE)

    dark1 = myfont.render('Level', False, BLACK)                # Napis "Level"
    light1 = myfont.render('Level', False, WHITE)

    rzedydark = myfont.render('Tetris', False, BLACK)                # Napis "tetris"
    rzedylight = myfont.render('Tetris', False, WHITE)

    riblight = endfont.render('YOU LOSE', False, YELLOW)         # Napis "you loose"
    ribdark = endfont.render('YOU LOSE', False, BLACK)

    # ---PUNKTACJA I RZĘDY---------------------------------------------------------------------------------------------
    liczba_rzedow = usun_rzedy(tablica, suma_rzedow)
    pom_level = liczba_rzedow + pom_level

    if pom_level % 10 == 0:
        level = int(pom_level / 10)

    prev_punkty = punkty
    punkty = wyswietl_punkty(liczba_rzedow, punkty, level)      # liczy punkty na podstawie levela
    if(punkty - prev_punkty == 1200 * (level + 1)):
        tetrisy = tetrisy + 1

    wybrany_kolor = losuj_kolor_punkty(prev_punkty - punkty)

    darkpunkty = myfont.render(str(punkty), False, BLACK)
    lightpunkty = myfont.render(str(punkty), False, wybrany_kolor)

    darklevel = myfont.render(str(level), False, BLACK)
    lightlevel = myfont.render(str(level), False, WHITE)

    darkrzedy = myfont.render(str(tetrisy), False, BLACK)
    lightrzedy = myfont.render(str(tetrisy), False, WHITE)

# ---WYSWIETLANIE TEKSTU-------------------------------------------------------------------------------------------

    odstep = 40

    okienko.blit(tetdark, (poz_tetrisa_x + int(wym_tablicy_x/2) - kwadracik + 2, int(poz_tetrisa_y/2) - 15 + 2))        # TYTUŁ
    okienko.blit(tetlight, (poz_tetrisa_x + int(wym_tablicy_x/2) - kwadracik, int(poz_tetrisa_y/2) - 15))

    akapit = poz_tetrisa_x + wym_tablicy_x
    okienko.blit(dark, (akapit + kwadracik * 2 + 1, poz_tetrisa_y + odstep * 0 + 12))                      # wyswietla napis "punkty"
    okienko.blit(light, (akapit + kwadracik * 2, poz_tetrisa_y + odstep * 0 + 11))

    okienko.blit(darkpunkty, (akapit + kwadracik * 2 + 1, poz_tetrisa_y + odstep * 1 + 12))                # liczba punktow
    okienko.blit(lightpunkty, (akapit + kwadracik * 2, poz_tetrisa_y + odstep * 1 + 11))

    okienko.blit(dark1, (akapit + kwadracik * 2 + 1, poz_tetrisa_y + odstep * 3 + 12))                     # wyswietla napis "level"
    okienko.blit(light1, (akapit + kwadracik * 2, poz_tetrisa_y + odstep * 3 + 11))

    okienko.blit(darklevel, (akapit + kwadracik * 2 + 1, poz_tetrisa_y + odstep * 4 + 12))                 # numer levela
    okienko.blit(lightlevel, (akapit + kwadracik * 2, poz_tetrisa_y + odstep * 4 + 11))

    okienko.blit(rzedydark, (akapit + kwadracik * 2 + 1, poz_tetrisa_y + odstep * 6 + 12))                 # wyswietla napis "Tetris"
    okienko.blit(rzedylight, (akapit + kwadracik * 2, poz_tetrisa_y + odstep * 6 + 11))

    okienko.blit(darkrzedy, (akapit + kwadracik * 2 + 1, poz_tetrisa_y + odstep * 7 + 12))                 # ile tetrisów wpadło
    okienko.blit(lightrzedy, (akapit + kwadracik * 2, poz_tetrisa_y + odstep * 7 + 11))

# ----- NASTEPNA FIGURA - obiekt --------------------------------------------------------------------------------------

    nextdark = myfont.render('Next', False, BLACK)             # Napis "next"
    nextlight = myfont.render('Next', False, WHITE)

    okienko.blit(nextdark, (akapit + kwadracik * 2 + 1, poz_tetrisa_y + odstep * 9 + 12))  # ile tetrisów wpadło
    okienko.blit(nextlight, (akapit + kwadracik * 2, poz_tetrisa_y + odstep * 9 + 11))

    nastepna_figura = fig(next_fig)
    pygame.draw.rect(okienko, BLACK, [akapit + kwadracik * 2 - 20, poz_tetrisa_y + odstep * 10 + 20, kwadracik * 4, kwadracik * 5], grubosc)

    pokaz_figure(nastepna_figura, wym_x + 2, wym_y-4)

# -----------------------------------------------------------------------------------------------------------------

    if licznik == czas:                                                                                                 # jeżeli granica (prawo, lewo, dół)
        if czy_moze_tu_byc(aktualna_poz_x, aktualna_poz_y + 1, aktualna_figura):
            aktualna_poz_y = aktualna_poz_y + 1
            licznik = 0
        else:
            tablica = dodaj_do_tablicy(aktualna_figura, aktualna_poz_x, aktualna_poz_y)
            licznik = 0
            stop = True

    wyswietl_tablice()
    end = 0
    pokaz_figure(aktualna_figura, aktualna_poz_x, aktualna_poz_y)
    if stop:
        wyb_fig = next_fig
        next_fig = random.randint(1, 7)
        aktualna_figura = fig(wyb_fig)
        aktualna_poz_x = 4
        aktualna_poz_y = 0
     #   if czy_moze_tu_byc(aktualna_poz_x, aktualna_poz_y, aktualna_figura) == 0:
     #       end = 1
        stop = False

    if czy_moze_tu_byc(4, 0, aktualna_figura) == 0:
        end = 1

    if end:
        pygame.draw.rect(okienko, BLACK, [0, 0, szerokosc, wysokosc])
        pygame.draw.rect(okienko, GREYDARK, [0, wysokosc / 2 - 200, szerokosc, 430])
        pygame.draw.rect(okienko, GREYLIGHT, [0, wysokosc / 2 - 100, szerokosc, 230])

        okienko.blit(dark1, (200 + 2, wysokosc / 2 - 190 + 2))
        okienko.blit(light1, (200, wysokosc / 2 - 190))

        okienko.blit(darklevel, (200 + 2, wysokosc / 2 - 150 + 2))
        okienko.blit(lightlevel, (200, wysokosc / 2 - 150))

        okienko.blit(rzedydark, (430 + 2, wysokosc / 2 - 190 + 2))
        okienko.blit(rzedylight, (430, wysokosc / 2 - 190))

        okienko.blit(darkrzedy, (430 + 2, wysokosc / 2 - 150 + 2))
        okienko.blit(lightrzedy, (430, wysokosc / 2 - 150))

        okienko.blit(ribdark, (int(szerokosc / 2 + 2 - 180), int(wysokosc / 2 + 2 - 30)))           # napis u lose
        okienko.blit(riblight, (int(szerokosc / 2 - 180), int(wysokosc / 2 - 30)))

        okienko.blit(dark, (315 + 2, wysokosc / 2 + 140 + 2))
        okienko.blit(light, (315, wysokosc / 2 + 140))

        okienko.blit(darkpunkty, (315 + 2, wysokosc / 2 + 180 + 2))
        okienko.blit(lightpunkty, (315, wysokosc / 2 + 180))

    licznik = licznik + 1
    pygame.display.update()
