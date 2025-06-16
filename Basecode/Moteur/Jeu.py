import random
import numpy as np


POSITION_X_JOUEUR = 0.1
TAILLE_JOUEUR = 0.06
LARGEUR_TUYAU = 0.13
ECART_MIN = 0.05
ECART_MAX = 0.3
FENETRE_MIN = 0.2
FENETRE_MAX = 0.5
G = -2.9
G_CHUTTE_LIBRE = -G*2
FLAP = 0.8


'''
Représente le joueur dans la partie avec sa position verticale y et sa vitesse vy
L'oiseau est un carré de size x size, de centré sur y (et la position x fixe à l'écran, c'est l'environnement qui bouge)
'''
class Joueur:
    y = 0.5
    vy = 0
    def __init__(self):
        pass

class Tuyau:
    collide = 0
    xLeft = 0
    yBot = 0
    yTop = 0
    ecart = 0
    def __init__(self, xLeft: float, yBot: float, yTop: float):
        self.xLeft, self.yBot, self.yTop = xLeft, yBot, yTop

    def collision(self, joueur: Joueur):
        if POSITION_X_JOUEUR<self.xLeft or POSITION_X_JOUEUR-TAILLE_JOUEUR>=self.xLeft+LARGEUR_TUYAU: return False
        if joueur.y>=self.yBot and joueur.y+TAILLE_JOUEUR<=self.yTop: return False
        if joueur.y>=self.yBot: self.collide = 1
        else: self.collide = -1
        return True  

    def __str__(self):
        return f"xLeft={self.xLeft}, xRight={self.xLeft+LARGEUR_TUYAU}, yBot={self.yBot}, yTop={self.yTop}"


class Jeu:
    tuyaux = []
    joueur = Joueur()
    elapsedTime = 0
    speed = 1.0
    score = 0
    n = 0
    chutteLibre = False

    def __init__(self, speed: float):
        self.speed = speed
        self.reset()

    def reset(self):
        self.joueur = Joueur()
        self.elapsedTime = 0
        self.rang = 0
        self.tuyaux = []
        self.tuyaux.append(Tuyau(1.0, 0.3, 0.7))
        for _ in range(10): self.ajoutTuyau()
        self.score = 0
        self.n = 0
        self.chutteLibre = False

    def flap(self):
        self.joueur.vy = FLAP
        self.chutteLibre = False

    def setChutteLibre(self, value):
        self.chutteLibre = value

    def refresh(self, dt):
        if not self.chutteLibre: self.joueur.vy+= G*dt
        else: self.joueur.vy+= G_CHUTTE_LIBRE*dt
        self.joueur.y+=self.joueur.vy*dt
        if self.joueur.y<0: return False


        self.elapsedTime+=self.speed*dt


        for tuyau in self.tuyaux:
            tuyau.xLeft-=self.speed*dt    
        
        if self.tuyaux[0].xLeft + LARGEUR_TUYAU <=0:
            self.tuyaux = self.tuyaux[1:]
            self.ajoutTuyau()
        
        for tuyau in self.tuyaux:
            if tuyau.collision(self.joueur): return False
        
        return True
    
    def ajoutTuyau(self):
        ecart = random.random()*(ECART_MAX-ECART_MIN)+ECART_MIN
        fenetre = random.random()*(FENETRE_MAX-FENETRE_MIN)+FENETRE_MIN
        yBot = random.random()*(0.2) - 0.1 + self.tuyaux[-1].yBot
        yBot = 0.1 if yBot<0.1 else yBot
        yBot = 0.9 - fenetre if yBot>0.9 - fenetre else yBot
        
        self.tuyaux.append(Tuyau(self.tuyaux[-1].xLeft+LARGEUR_TUYAU+ecart, yBot, yBot+fenetre))
        self.score+=1

