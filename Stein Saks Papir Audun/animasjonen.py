import pygame as pg
import random as r
import SteinSaksPapir as st
from pygame.locals import K_SPACE

pg.init()

WIDTH = 800
HEIGHT  = 600
# importerer bildene jeg skal bruke
paplr = pg.image.load("papir.png") # Har kaldt den paplr med en L fordi jeg har en liste lenger nede som heter papir
saks = pg.image.load("saks.png")
stein = pg.image.load("stein.png")

# Gjør bildene til størelsen jeg skal bruke i spillet
scaled_saks = pg.transform.scale(saks, (50, 50))
scaled_stein = pg.transform.scale(stein, (50, 50))
scaled_papir = pg.transform.scale(paplr, (50, 50))

sakser = []
steiner = []
papir = []

vStein = st.font.render("STEINER VANT!!", True, (0, 0, 0))
vSaks = st.font.render("SAKSER VANT!!", True, (0, 0, 0))
vPapir = st.font.render("PAPIR VANT!!", True, (0, 0, 0))

igjen = st.font.render("TRYKK PÅ SPACE FOR Å SPILLE AV IGJEN", True, (0, 0, 0))

# Gjør bildene til størelsen jeg skal bruke når animasjonen er over og vinneren er erklært
vinner_saks = pg.transform.scale(saks, (200, 200))
vinner_stein = pg.transform.scale(stein, (200, 200))
vinner_papir = pg.transform.scale(paplr, (200, 200))


spill = True
vinner = False
begyn = True
fps = 80 # fps står for "frames per second" gjo flere fps gjo fortere går spillet
run = True
while run:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        
    if begyn:
            for i in range(10): # Lager fem objekter fra vær klasse med tilfeldig fart, possisjonen er den samme i den samme klassen sånn at de kan starte ca. like langt vekk fra hverandre
               sakser.append(st.Saks(r.uniform(-2, 2), r.uniform(-2, 2), scaled_saks, WIDTH/5, HEIGHT/2))
               steiner.append(st.Stein(r.uniform(-2, 2), r.uniform(-2, 2), scaled_stein, WIDTH/(4/3), HEIGHT/(4/3)))
               papir.append(st.Papir(r.uniform(-2, 2), r.uniform(-2, 2), scaled_papir, WIDTH/(4/3), HEIGHT/5)) 
            
            begyn = False
    st.vindu.fill((0, 100, 100))
    clock = pg.time.Clock()
    clock.tick(fps) # Denne kolkken sårger for at det bare er 80 bilder i sekundet og ikke flere
    st.drawGrid()
    if spill: # Har if løkken her sånn at den skal stoppe å gå gjennom denne dellen av programmet når bevegelses delen er over
    
        for i in sakser:
            i.tegn()
            i.beveg()
            if i.finStein(steiner):
                sakser.remove(i) # fjerner fra sakselisten
                i = st.Stein(i.xfart, i.yfart, scaled_stein, i.x, i.y) # Gjor saksen om til stein med alle verdiene til pososjon og fart den hadde fra før av
                steiner.append(i) # legger til i steinlisten, funker det samme for de andre klassene
        for i in steiner:
            i.tegn()
            i.beveg()
            if i.finPapir(papir):
                steiner.remove(i)
                i = st.Papir(i.xfart, i.yfart, scaled_papir, i.x, i.y)
                papir.append(i)
        for i in papir:
            i.tegn()
            i.beveg()
            if i.finSaks(sakser):
                papir.remove(i)
                i = st.Saks(i.xfart, i.yfart, scaled_saks, i.x, i.y)
                sakser.append(i)
    
        # Under her kjekker den om en av klassene har vunnet med å se om det ikke er noen igjenn av de andre klassene 
        if len(sakser) == 0 and len(papir) == 0: 
            steiner = []
            seier = 1 # Bruker denne for å huske hvem som har vunnet
            vinner = True # starter vinner delen av while løkken
            spiller = False # slutter spill delen av while løkken
        elif len(steiner) == 0 and len(sakser) == 0: # Disse to funker på samme måte som den over bare med en annen seier
            papir = []
            seier = 2
            vinner = True
            spill = False
        elif len(papir) == 0 and len(steiner) == 0:
            sakser = []
            seier = 3
            vinner = True
            spill = False
    
    if vinner: # husker hvem som vant med seier variabelen og tegner in riktig vinner.
        if seier == 1: 
            st.drawWiner(vinner_stein)
            st.vindu.blit(vStein, (WIDTH/3, HEIGHT/1.5))
        if seier == 2:
            st.drawWiner(vinner_papir)
            st.vindu.blit(vPapir, (WIDTH/3, HEIGHT/1.5))
        if seier == 3:
            st.drawWiner(vinner_saks)
            st.vindu.blit(vSaks, (WIDTH/3, HEIGHT/1.5))
         
        st.vindu.blit(igjen, (75, HEIGHT/1.3))
        taster = pg.key.get_pressed()
    
        if taster[K_SPACE]:
            vinner = False
            spill = True
            begyn = True
        
    pg.display.update()
pg.quit()