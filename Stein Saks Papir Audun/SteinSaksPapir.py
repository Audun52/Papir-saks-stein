import pygame as pg
import math as m

pg.init()
WIDTH = 800
HEIGHT  = 600
vindu = pg.display.set_mode([WIDTH, HEIGHT])
font = pg.font.Font("freesansbold.ttf", 32)

# Lager en houvedklasse som alle de andre klassene er basert på
class Ball:
    def __init__(self, xfart, yfart, bilde, x, y,):
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
        
    
    def finSaks(self, saks): # Alle subclassene har en funksjon som finner den klassen de er svake mot med pytagoras setningen
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