__author__ = 'Nobody'

import random, sys, time, pygame
from pygame.locals import *

FPS=30
WINDOWWIDTH=640
WINDOWHEIGHT=480
FLASHSPEED=500
FLASHDELAY=200
BUTTONSIZE=200
BUTTONGAPSIZE=20
TIMEOUT=4  #seconds before game over if no button is pushed

WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
BRIGHTRED=(255, 0, 0)
RED=(155, 0 ,0)
BRIGHTGREEN=(0, 255, 0)
GREEN=(0, 155, 0)
BRIGHTBLUE=(0, 0, 255)
BLUE=(0, 0, 155)
BRIGHTYELLOW=(255, 255, 0)
YELLOW=(155, 155, 0)
DARKGRAY=(40, 40, 40)
bgColor=BLACK

XMARGIN=int((WINDOWWIDTH-(2*BUTTONSIZE)-BUTTONGAPSIZE)/2)
YMARGIN=int((WINDOWHEIGHT-(2*BUTTONSIZE)-BUTTONGAPSIZE)/2)

#Rect objects for each of the four buttons
YELLOWRECT=pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT=pygame.Rect(XMARGIN+BUTTONSIZE+BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT=pygame.Rect(XMARGIN, YMARGIN+BUTTONSIZE+BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT=pygame.Rect(XMARGIN+BUTTONSIZE+BUTTONGAPSIZE, YMARGIN+BUTTONSIZE+BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT=pygame.font.Font('freesansbold.ttf', 16)
    infoSurf=BASICFONT.render('Match the pattern by clicking on the button or using QWA keys.', 1, DARKGRAY)
    infoRect=infoSurf.get_rect()
    infoRect.topleft=(10, WINDOWHEIGHT-25)
    #load the sound files
    BEEP1=pygame.mixer.Sound('beep1.ogg')
    BEEP2=pygame.mixer.Sound('beep2.ogg')
    BEEP3=pygame.mixer.Sound('beep3.ogg')
    BEEP4=pygame.mixer.Sound('beep4.ogg')

    #Initialize some variables for a new game
    pattern=[]  #stores the pattern of colors
    currentStep=0 #the color the player must push next
    lastClickTime=0 #timestamp of the player's last button push
    score=0
    #when false,the pattern is playing .when True,waiting for the player to click a colored button
    waitingForInput=False

    while True:
        clickedButton=None  #button that was clicked(set to YELLOW,RED,GREEN or BLUE)
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf=BASICFONT.render('Score:'+str(score), 1, WHITE)
        scoreRect=scoreRect.get_rect()
        scoreRect.topleft=(WINDOWWIDTH-100, 10)
        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():  #event handling loop
            if event.type==MOUSEBUTTONUP:
                mousex, mousey=event.pos
                clickedButton=getButtonClicked(mousex, mousey)
            elif event.type==KEYDOWN:
                if event.key==K_q:
                    clickedButton=YELLOW
                elif event.key==K_w:
                    clickedButton=BLUE
                elif event.key==K_a:
                    clickedButton=RED
                elif event.key==K_s:
                    clickedButton=GREEN
        if not waitingForInput:
            #play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput=True

        else:
            #wait for the player to enter buttons
            if clickedButton and clickedButton==pattern[currentStep]:
                #pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep+=1
                lastClickTime=time.time()

                if currentStep==len(pattern):
                    #pushed the last button in the pattern
                    changeBackgroundAnimation()
                    score+=1
                    waitingForInput=False
                    currentStep=0  #reset back to first step
            elif (clickedButton and clickedButton!=pattern[currentStep]) or (currentStep!=0 and time.time()-TIMEOUT>lastClickTime):
                #push the incorrect button, or has time out
                gameOverAnimation()
                #reset the variables for a new game:
                pattern=[]
                currentStep=0
                waitingForInput=False
                score=0
                pygame.time.wait(1000)
                changeBackgroundAnimation()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): #get all the QUIT events
        terminate()
    for event in pygame.event.get(KEYUP):  #get all the KEYUP events
        if event.key==K_ESCAPE:
            terminate()
        pygame.event.post(event)

def flashButtonAnimation(color, animationSpeed=50):
    if color==YELLOW:
        sound=BEEP1
        flashColor=BRIGHTYELLOW
        rectangle=YELLOWRECT
    elif color==BLUE:
        sound=BEEP2
        flashColor=BRIGHTBLUE
        rectangle=BLUERECT
    elif color==RED:
        sound=BEEP3
        flashColor=BRIGHTRED
        rectangle=REDRECT
    elif color==GREEN:
        sound=BEEP4
        flashColor=BRIGHTGREEN
        rectangle=GREENRECT
    origSurf=DISPLAYSURF.copy()
    flashSurf=pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf=flashSurf.convert_alpha()
    r, g, b=flashColor
    sound.play()
    for start, end, step in ((0, 255, 1),(255, 0, -1)):
        for alpha in range(start, end, animationSpeed*step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0,0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))
    
