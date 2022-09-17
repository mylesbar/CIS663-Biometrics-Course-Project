#imports
from typing import Text
import pygame
from pygame import mixer
import math
import button


#===========================Pygame setup===========================#
pygame.init()
sizeX,sizeY = 800,600
window_size = (sizeX,sizeY)
clock = pygame.time.Clock()
mouse = pygame.mouse.get_pos()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("CIS 663 Biometrics")
bg = pygame.image.load('C:/Users/mills/Desktop/Code Projects/Biometrics Project/Images/Syracuse-logo.jpg')
bg = pygame.transform.scale(bg,window_size)
pygame.display.set_icon(bg)


mixer.music.load("Music/55_bpm.mp3")
mixer.music.play(-1,-1,1000)


#==========================Music Switching Utils====================#
def changeMusic(musicIn):
    mixer.music.load(musicIn)
    mixer.music.play(-1)    

def crossFade(musicIn):
    mixer.music.fadeout(1000);
    mixer.music.load(musicIn)
    mixer.music.play(-1,-1,1000)
    
scaleMusic = pygame.USEREVENT + 1
scaleTrigger = pygame.event.Event(scaleMusic)

musicDict = {
    "55" : "Music/55_bpm.mp3",
    "60" : "Music/60_bpm.mp3",
    "65" : "Music/65_bpm.mp3",
    "70" : "Music/70_bpm.mp3",
    "75" : "Music/75_bpm.mp3",
    "80" : "Music/80_bpm.mp3",
    "85" : "Music/85_bpm.mp3",
    "90" : "Music/90_bpm.mp3",
    "95" : "Music/95_bpm.mp3",
    "100" : "Music/100_bpm.mp3",
    "105" : "Music/105_bpm.mp3",
    "110" : "Music/110_bpm.mp3",
    "115" : "Music/115_bpm.mp3",
    "120" : "Music/120_bpm.mp3",
    "125" : "Music/125_bpm.mp3",
    "130" : "Music/130_bpm.mp3",
    "135" : "Music/135_bpm.mp3",
    "140" : "Music/140_bpm.mp3",
    "145" : "Music/145_bpm.mp3",
    "155" : "Music/155_bpm.mp3",
    "165" : "Music/165_bpm.mp3"  
}

#State Flags
currState = 50
counter = currState


running = True
sustain = 10
stateCheck = 0
status = 0 # stop = 0 | run = 1 | calibrate = 2

#Button Coordinates
start_x,start_xend =100,100+178
calibrate_x,calibrate_xend =300,300+239
stop_x,stop_xend =550,550+172
button_ystart,button_yend=400,400+69

while running:
    
    #==============================================================event handler==============================================================#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Window Closed")
            running = False   
             
        if event.type == scaleMusic:
            print("scale key")
            musicLoader = musicDict[str(musicSelect)]
            crossFade(musicLoader)
            sustain = 15
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("click detected")
            x,y=pygame.mouse.get_pos()
            print("x,y",x,y)
            
            #stop button
            if((x >= stop_x and x <=stop_xend) and (y>=button_ystart and y<=button_yend)):
                print('stop detected')
                status = 0
            
            #calibrate button
            elif((x >= calibrate_x and x<=calibrate_xend) and (y>=button_ystart and y<=button_yend)):
                print('calibrate detected')
                status ==2
                pygame.time.wait(12000)
                status ==1
                
            #start button
            elif((x >= start_x and x<=start_xend) and (y>=button_ystart and y<=button_yend)):
                print('start detected')
                status = 1;
            
        if(event.type == pygame.KEYDOWN):
            
            #Quit
            if(event.key == pygame.K_ESCAPE):
                print("Exit event")
                running = False
                pygame.quit()
                exit()
            
            #Manual Override Test
            if event.key == pygame.K_1:
                print("manual override")
                musicLoader =  musicDict["115"]
                crossFade(musicLoader)
    
                
    #==================================================Music Switching Logic==============================================================#  
    if status == 1:
        if sustain > 0:
            
            print("sustain state")
            sustain-=1
            
        else:      
            counter+=1
        
            stateCheck = math.floor(counter/10) * 10
            print("current state:", currState)
        
        #switch sounds
        if(stateCheck != currState):
            currState = stateCheck
            musicSelect = currState + 5
            
            if str(musicSelect) in musicDict:
                print("post")
                pygame.event.post(scaleTrigger)
        pygame.time.wait(500)    
        print("runtime ctr:",counter)
        print('==================================')
        
    
    
    #==================================================Render Window==============================================================#
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    
    #TODO: Change counter to bpm
    
    button_color = (194, 204, 209)
    textFont = pygame.font.SysFont('arialblack',50) 
    Text_in_Box = "Heart Rate: " + str(counter)
    start_button = pygame.draw.rect(screen, button_color, [150, 100, 500 , 150])
    start_text = textFont.render(Text_in_Box , True , ('0x0f2e5a'))
    screen.blit(start_text , ( 200 , 140))
    
    
    #buttons
    start_img = pygame.image.load('C:/Users/mills/Desktop/Code Projects/Biometrics Project/Images/button_start.png').convert_alpha()
    start_button = button.Button(start_x,button_ystart, start_img,0.8)
    start_button.draw(screen)
     
    calibrate_img = pygame.image.load('C:/Users/mills/Desktop/Code Projects/Biometrics Project/Images/button_calibrate.png').convert_alpha()
    calibrate_button = button.Button(calibrate_x,button_ystart, calibrate_img,0.8)
    calibrate_button.draw(screen)
    
    stop_img = pygame.image.load('C:/Users/mills/Desktop/Code Projects/Biometrics Project/Images/button_stop.png').convert_alpha()
    stop_button = button.Button(stop_x,button_ystart, stop_img,0.8)
    stop_button.draw(screen)
    
    pygame.display.update()
    
        
    