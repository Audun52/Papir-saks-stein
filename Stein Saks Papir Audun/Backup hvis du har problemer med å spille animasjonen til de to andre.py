import pygame as pg
import math as m
import random as r
from pygame.locals import K_SPACE

pg.init()

WIDTH = 800
HEIGHT  = 600
vindu = pg.display.set_mode([WIDTH, HEIGHT])
font = pg.font.Font("freesansbold.ttf", 32)
# importerer bildene jeg skal bruke
paplr = pg.image.load("papir.png") # Har kaldt den paplr med en L fordi jeg har en liste lenger nede som heter papir
saks = pg.image.load("saks.png")
stein = pg.image.load("stein.png")
# Gjør bildene til størelsen jeg skal bruke i spillet
scaled_saks = pg.transform.scale(saks, (50, 50))
scaled_stein = pg.transform.scale(stein, (50, 50))
scaled_papir = pg.transform.scale(paplr, (50, 50))
# Gjør bildene til størelsen jeg skal bruke når animasjonen er over og vinneren er erklært
vinner_saks = pg.transform.scale(saks, (200, 200))
vinner_stein = pg.transform.scale(stein, (200, 200))
vinner_papir = pg.transform.scale(paplr, (200, 200))
# Lager en houvedklasse som alle de andre klassene er basert på
class Ball:
    def __init__(self, xfart, yfart, bilde, x, y):
        self.x = x
        self.y = y
        self.xfart = xfart
        self.yfart = yfart
        self.radius = 25
        self.hitx = self.x - self.radius
        self.hity = self.y + self.radius
        self.bilde = bilde
        # hitx og hity er laget fordi x og y verdiene til bildene er oppi venstere hjørne av bildet, derfor har jeg hitx og hity som jeg flytter til midten av bildet og bruker den til å kjekke om den treffer andre bilder eller vegen
    def tegn(self): # Tegner in bildet jeg har impotert
        vindu.blit(self.bilde, (self.x, self.y))

    
    def beveg(self): # For ballene til å flytte på deg og kjekker om de treffer veggen
        if ((self.hitx + self.radius) <= 0) or ((self.hitx + self.radius*3) >= WIDTH):
            self.xfart = -self.xfart
        if ((self.hity - self.radius)  <= 0) or ((self.hity + self.radius) >= HEIGHT):
            self.yfart = -self.yfart
        
        self.x += self.xfart
        self.y += self.yfart
        self.hitx += self.xfart
        self.hity += self.yfart
        
class Papir(Ball):
    def __init__(self, xfart, yfart, bilde, x, y):
        super().__init__(xfart, yfart, bilde, x, y)
        
    
    def finSaks(self, saks): # Alle subclassene har en funksjon som finner den klassen de er svake modt
        for i in saks:
            ax2 = (self.hitx - i.hitx)**2
            ay2 = (self.hity - i.hity)**2
            avstand = m.sqrt(ax2 + ay2)
        
            if avstand <= self.radius+i.radius:
                return True

class Saks(Ball):
    def __init__(self, xfart, yfart, bilde, x, y):
        super().__init__(xfart, yfart, bilde, x, y)
        
    def finStein(self, steiner):
        for i in steiner:
            ax2 = (self.hitx - i.hitx)**2
            ay2 = (self.hity - i.hity)**2
            avstand = m.sqrt(ax2 + ay2)
        
            if avstand <= self.radius+i.radius:
                return True
        
class Stein(Ball):
    def __init__(self, xfart, yfart, bilde, x, y):
        super().__init__(xfart, yfart, bilde, x, y)
        
    def finPapir(self, papir):
        for i in papir:
            ax2 = (self.hitx - i.hitx)**2
            ay2 = (self.hity - i.hity)**2
            avstand = m.sqrt(ax2 + ay2)
        
            if avstand <= self.radius+i.radius:
                return True
def drawGrid(): # Gridden hjelper meg å se at størrelsen på alt er riktig

    blockSize = 25

    for x in range(0, WIDTH, blockSize):

        for y in range(0, HEIGHT, blockSize):

            rect = pg.Rect(x, y, blockSize, blockSize)

            pg.draw.rect(vindu, (255, 255, 255), rect, 1)
            
def drawWiner(bilde): # Bruker denne når en vinner er erklært
    vindu.blit(bilde, (WIDTH/2-100, HEIGHT/2-100))

sakser = []
steiner = []
papir = []

vStein = font.render("STEINER VANT!!", True, (255, 0, 255))
vSaks = font.render("SAKSER VANT!!", True, (255, 0, 255))
vPapir = font.render("PAPIR VANT!!", True, (255, 0, 255))

igjen = font.render("TRYKK PÅ SPACE FOR Å SPILLE AV IGJEN", True, (0, 0, 0))

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
            for i in range(5): # Lager fem objekter fra vær klasse med tilfeldig fart, possisjonen er den samme i den samme klassen sånn at de kan starte ca. like langt vekk fra hverandre
               sakser.append(Saks(r.uniform(-2, 2), r.uniform(-2, 2), scaled_saks, WIDTH/5, HEIGHT/2))
               steiner.append(Stein(r.uniform(-2, 2), r.uniform(-2, 2), scaled_stein, WIDTH/(4/3), HEIGHT/(4/3)))
               papir.append(Papir(r.uniform(-2, 2), r.uniform(-2, 2), scaled_papir, WIDTH/(4/3), HEIGHT/5)) 
            
            begyn = False
    vindu.fill((0, 100, 100))
    clock = pg.time.Clock()
    clock.tick(fps) # Denne kolkken sårger for at det bare er 80 bilder i sekundet og ikke flere
    drawGrid()
    if spill: # Har if løkken her sånn at den skal stoppe å gå gjennom denne dellen av programmet når bevegelses delen er over
    
        for i in sakser:
            i.tegn()
            i.beveg()
            if i.finStein(steiner):
                sakser.remove(i) # fjerner fra sakselisten
                i = Stein(i.xfart, i.yfart, scaled_stein, i.x, i.y) # Gjor saksen om til stein med alle verdiene til pososjon og fart den hadde fra før av
                steiner.append(i) # legger til i steinlisten, funker det samme for de andre klassene
        for i in steiner:
            i.tegn()
            i.beveg()
            if i.finPapir(papir):
                steiner.remove(i)
                i = Papir(i.xfart, i.yfart, scaled_papir, i.x, i.y)
                papir.append(i)
        for i in papir:
            i.tegn()
            i.beveg()
            if i.finSaks(sakser):
                papir.remove(i)
                i = Saks(i.xfart, i.yfart, scaled_saks, i.x, i.y)
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
            drawWiner(vinner_stein)
            vindu.blit(vStein, (WIDTH/3, HEIGHT/1.5))
        if seier == 2:
            drawWiner(vinner_papir)
            vindu.blit(vPapir, (WIDTH/3, HEIGHT/1.5))
        if seier == 3:
            drawWiner(vinner_saks)
            vindu.blit(vSaks, (WIDTH/3, HEIGHT/1.5))
         
        vindu.blit(igjen, (75, HEIGHT/1.3))
        taster = pg.key.get_pressed()
    
        if taster[K_SPACE]:
            vinner = False
            spill = True
            begyn = True
        
    pg.display.update()
pg.quit()