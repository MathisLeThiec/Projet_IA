import pygame
from Moteur.Jeu import POSITION_X_JOUEUR, TAILLE_JOUEUR, LARGEUR_TUYAU
import json

class Drawer:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 30)
        self.height, self.width = 600, 600
        self.game_window = pygame.display.set_mode((600, 600))
        self.spritesFond = []
        self.spritesSol = []
        self.spritesJoueur = []
        self.spritesTuyau = []
        self.extract()
        self.decalageFond = 0
        self.decalageSol = 0

    def extract(self):
        self.sheet = pygame.image.load("Ressources/sprites.png").convert()
        with open('Ressources/descripteur.json') as f: descripteur = json.load(f)
        for objet in descripteur['objets']:
            for coord in objet['coords']:
                rect = pygame.Rect(int(coord['x']), int(coord['y']), int(coord['w']), int(coord['h']))
                sprite = pygame.Surface(rect.size).convert()
                sprite.blit(self.sheet, (0, 0), rect)
                match objet['nom']:
                    case 'fond': self.spritesFond.append(pygame.transform.scale(sprite, (300, 600)))
                    case 'tuyau':
                        if coord['id']%2==0: self.spritesTuyau.append(pygame.transform.scale(sprite, (78, 32)))
                        else: self.spritesTuyau.append(pygame.transform.scale(sprite, (66, 600)))
                    case 'sol': self.spritesSol.append(pygame.transform.scale(sprite, (300, 100)))
                    case 'joueur':
                        colorkey = sprite.get_at((0,0))
                        sprite.set_colorkey(colorkey, pygame.RLEACCEL)
                        self.spritesJoueur.append(pygame.transform.scale(sprite, (int(600*TAILLE_JOUEUR),int(600*TAILLE_JOUEUR))))
    
    def draw(self, jeu):
        color = pygame.Color(0,0,0)
        pygame.draw.rect(self.game_window, color, pygame.Rect(0, 0, self.height, self.width))
        if self.decalageFond>=0.5:
            self.decalageFond = 0
        if self.decalageSol>=0.5:
            self.decalageSol = 0

        self.game_window.blit(self.spritesFond[0], (0-int(600*self.decalageFond), 0))
        self.game_window.blit(self.spritesFond[0], (300-int(600*self.decalageFond), 0))
        self.game_window.blit(self.spritesFond[0], (600-int(600*self.decalageFond), 0))
        #self.game_window.blit(self.spritesFond[0], (300, 0))
        self.decalageFond+=0.001
        self.game_window.blit(self.spritesSol[0], (0-int(600*self.decalageSol), 500))
        self.game_window.blit(self.spritesSol[0], (300-int(600*self.decalageSol), 500))
        self.game_window.blit(self.spritesSol[0], (600-int(600*self.decalageSol), 500))
        self.decalageSol+=0.005

        for tuyau in jeu.tuyaux:
            x, y = tuyau.xLeft*600, (1.0-tuyau.yBot)*500
            
            if tuyau.collide<0:
                self.game_window.blit(pygame.transform.scale(self.spritesTuyau[5], (66, 500-y)), (x, y))
                self.game_window.blit(self.spritesTuyau[4], (x-6, y))
            else:
                self.game_window.blit(pygame.transform.scale(self.spritesTuyau[3], (66, 500-y)), (x, y))
                self.game_window.blit(self.spritesTuyau[2], (x-6, y))

            y = (1.0-tuyau.yTop)*500
            if tuyau.collide>0:
                self.game_window.blit(pygame.transform.scale(self.spritesTuyau[7], (66, y)), (x, 0))
                self.game_window.blit(self.spritesTuyau[6], (x-6, y-32))
            else:
                self.game_window.blit(pygame.transform.scale(self.spritesTuyau[3], (66, y)), (x, 0))
                self.game_window.blit(self.spritesTuyau[0], (x-6, y-32))

        if jeu.chutteLibre:
            self.game_window.blit(self.spritesJoueur[0], (60, int((1.0 - jeu.joueur.y-TAILLE_JOUEUR)*500)))
        else:
            if jeu.joueur.vy>0.08:
                self.game_window.blit(self.spritesJoueur[2], (60, int((1.0 - jeu.joueur.y-TAILLE_JOUEUR)*500)))
            else:
                self.game_window.blit(self.spritesJoueur[1], (60, int((1.0 - jeu.joueur.y-TAILLE_JOUEUR)*500)))

        text_surface = self.font.render(f'Score : {jeu.score}', False, (0, 0, 0))
        self.game_window.blit(text_surface, (0,0))
        #pygame.draw.rect(self.game_window, pygame.Color(255, 255, 255, 0), pygame.Rect(245, 10, 110, 30))
        #pygame.draw.rect(self.game_window, pygame.Color(255, 0, 0, 0), pygame.Rect(250, 15, 100, 20))
        #pygame.draw.rect(self.game_window, pygame.Color(0, 255, 0, 0), pygame.Rect(250, 15, int(100*jeu.endurance/ENDURANCE_MAX), 20))
        pygame.display.update()


