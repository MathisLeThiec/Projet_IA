from Moteur.Jeu import *
from Vue.Interface import *
import pygame

FPS = 60

def main():
    pygame.init()
    fenetre = Drawer()
    clock = pygame.time.Clock()
    game  = Jeu(speed=1.0)

    run = True
    pressed = True
    while run:
        dt = clock.tick(FPS) / 1000.0  # en secondes
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        # récupérer l’entrée IA ou clavier
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            run = False
            break
        
        
        action = -1
        if not keys[pygame.K_SPACE] and not keys[pygame.K_LCTRL]:
            pressed = False
            action = 0
        elif not pressed:
            if keys[pygame.K_SPACE]:
                pressed = True
                action = 1
            elif keys[pygame.K_LCTRL]:
                pressed = True
                action = 2

        match action:
            case 0: game.setChutteLibre(False)
            case 1: game.flap()
            case 2: game.setChutteLibre(True)
            
        alive = game.refresh(dt)
        if not alive:
            game.reset()

        fenetre.draw(game)

    pygame.quit()

if __name__ == "__main__":
    main()