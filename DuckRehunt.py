#!/usr/bin/env python
"""
Copyright 2011 Michael Bachmann

This program is distributed under the terms of the GNU
General Public License
"""

import pygame, random, sys

fullscreen = 0
for arg in sys.argv:
    if arg == "--fullscreen":
        fullscreen = 1

pygame.init()

from DuckLib import *

if fullscreen:
    screen = pygame.display.set_mode((640,480),pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((640,480))

screen_dim = screen.get_rect()


def main():

    pygame.display.set_caption("Duck Rehunt: Reckoning")
    pygame.mixer.init()
    pygame.mixer.Sound("Music.ogg").play(-1)

    background = pygame.Surface(screen.get_size())
    background.blit(pygame.image.load("Background.gif"), (0,0))
    screen.blit(background, (0,0))

    foreground = setPiece(pygame.image.load("Foreground.gif"), (0,301))
    setSprites = pygame.sprite.Group(foreground)

    dSprites.add(Dog())

    crosshair = pygame.sprite.Group(Crosshair())
                          
    keepGoing = True
    pause = 0
    delay = 60
    shotScore = 0
    global score

    scoreFont = pygame.font.Font("HelveticaWorld.ttf",20)
    scoreboard = scoreFont.render("Score: %d" % score, 1, (255,255,255))

    
    clock = pygame.time.Clock()
    
    while keepGoing:

        clock.tick(60)
        pygame.mouse.set_visible(False)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gunshot.play()
                flash.add(Flash())
                pointCollide = [sprite for sprite in dSprites.sprites() if sprite.rect.collidepoint(pygame.mouse.get_pos())]
                if pointCollide != []:
                    for sprite in pointCollide:
                        if not sprite.dog and not sprite.isDead:
                            sprite.isDead = True
                            sprite.pause = 0
                            if sprite.enemy:
                                shotScore -= 50
                            else:
                                shotScore += 5
                            sprite.setAnim()
                    shotScore *= len(pointCollide)
                    score += shotScore
                    shotScore = 0
                    scoreboard = scoreFont.render("Score: %d" % score, 1, (255,255,255))

    
        #Garbage collection        
        pause+= 1
        if pause >= delay:

            dSprites.remove([sprite for sprite in dSprites.sprites() if sprite.rect.centery >= 500])

        dSprites.clear(screen, background)
        crosshair.clear(screen, background)
        flash.clear(screen, background)

        dSprites.update()
        crosshair.update()
        flash.update()
        
        dSprites.draw(screen)
        setSprites.draw(screen)
        screen.blit(scoreboard, (500,440))
        flash.draw(screen)
        crosshair.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()

pygame.quit()
