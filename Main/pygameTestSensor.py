#imports
from typing import Text
import pygame
from pygame import mixer
import math
import button
import logging
import traceback
from pulsesensor import Pulsesensor
import pandas as pd
import csv
import time




print("window init")
pygame.init()
sizeX,sizeY = 800,600
window_size = (sizeX,sizeY)
clock = pygame.time.Clock()
mouse = pygame.mouse.get_pos()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("CIS 663 Biometrics")
bg = pygame.image.load('/home/mills/Desktop/Biometrics_Project/Images/Syracuse-logo.jpg')
bg = pygame.transform.scale(bg,window_size)
pygame.display.set_icon(bg)

textout = "Program Start"
statusOut = "Stopped"


#==========================Music Switching Utils====================#
musicDict = {
    "45" : "Music/55_bpm.mp3",
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

def changeMusic(musicIn):
    mixer.music.load(musicIn)
    mixer.music.play(-1)    

def crossFade(musicIn):
    print("crossfade")
    
    mixer.music.fadeout(1000);
    mixer.music.load(musicIn)
    mixer.music.play(-1,1000)
    statusOut="Switching Music"

    
scaleMusic = pygame.USEREVENT + 1
scaleTrigger = pygame.event.Event(scaleMusic)

readSignal = pygame.USEREVENT +2
readTrigger = pygame.event.Event(readSignal)


def closeCSV():
    with open('dataLog.csv',"r") as DL:
        try:
            read_file = pd.read_csv(r'dataLog.csv',on_bad_lines=None)
            read_file.to_excel(r'bpmLog.xlsx',index = None, header=True, delim_whitespace=True)
        except Exception as e:
            logging.error(traceback.format_exc())
#State Flags
currState = 50
counter = currState
bpm = 50
lastBPM = 50


running = True
sustain = 10
stateCheck = 0
status = 0 # stop = 0 | run = 1 | calibrate = 2

#Button Coordinates
start_x,start_xend =100,100+178
calibrate_x,calibrate_xend =300,300+239
stop_x,stop_xend =550,550+172
button_ystart,button_yend=400,400+69

textFont = pygame.font.SysFont('arialblack',50)
statusFont = pygame.font.SysFont('arialblack',30)
start_img = pygame.image.load('/home/mills/Desktop/Biometrics_Project/Images/button_start.png').convert_alpha()
# start_button = button.Button(start_x,button_ystart, start_img,0.8)

calibrate_img = pygame.image.load('/home/mills/Desktop/Biometrics_Project/Images/button_calibrate.png').convert_alpha()
calibrate_button = button.Button(calibrate_x,button_ystart, calibrate_img,0.8)

stop_img = pygame.image.load('/home/mills/Desktop/Biometrics_Project/Images/button_stop.png').convert_alpha()
stop_button = button.Button(stop_x,button_ystart, stop_img,0.8)

#PulseSensor Init
p = Pulsesensor()
#p.startAsyncBPM()
print("starting loop")
#p.startAsyncBPM()
with open("dataLog.csv","w") as log:
    writer = csv.writer(log)
    writer.writerow(['TimeStamp   ','BPM   '])

    while running:
        #initiate Pulse Sensor Readout
        p.startAsyncBPM()
        #==============================================================event handler==============================================================#

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    p.stopAsyncBPM()
                    print("Window Closed")
                    pygame.event.clear()
                    running = False
                    closeCSV()
                    pygame.quit()
                    
                elif event.type == scaleMusic:
                    print("scale key")
                    statusOut="Transition hold"
                    musicLoader = musicDict[str(musicSelect)]
                    crossFade(musicLoader)
                    sustain = 10
                    
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #pygame.event.pump()
                    print("click detected")
                    x,y=pygame.mouse.get_pos()
                    print("x,y",x,y)
                    
                    #stop button
                    if((x >= stop_x and x <=stop_xend) and (y>=button_ystart and y<=button_yend)):
                        print('stop detected') #do not update screen
                        status = 0
                        statusOut = 'Stopped'
                        pygame.event.clear()
                        #p.stopAsyncBPM()
                    
                    #calibrate button
                    elif((x >= calibrate_x and x<=calibrate_xend) and (y>=button_ystart and y<=button_yend)):
                        print('calibrate detected')
                        status =2
                        sustaiin =10;
                        #pygame.time.wait(1000)
                        #status ==1
                        print('calibrate done')
                        #continue
                        
                    #start button
                    elif((x >= start_x and x<=start_xend) and (y>=button_ystart and y<=button_yend)):
                        print('start detected')
                        #p.stopAsyncBPM()
                        status = 1;
                                
                elif(event.type == pygame.KEYDOWN):
                    print("key detected")
                    #Quit
                    if(event.key == pygame.K_ESCAPE):
                        p.stopAsyncBPM()
                        print("Exit event")
                        running = False
                        pygame.event.clear()
                        pygame.quit()
                        exit()
                    
                    #Manual Override Test
                    elif event.key == pygame.K_1:
                        print("manual override")
                        musicLoader =  musicDict["115"]
                        crossFade(musicLoader)
        try:          
                #==================================================Music Switching Logic==============================================================#  
            
                print("current status:",status)
                #print('read post')
                try:
                    if(status != 0):
                        bpm = p.BPM
                        print("midread:",bpm)
                        print('read conclude')
                        if bpm > 0:
                            found = 1
                            print("BPM: %d" % bpm)
                            textout = str(math.floor(bpm))
                            
                        else:
                            found = 0
                            print("No Heartbeat found")
                            textout = str(lastBPM)
                            bpm = lastBPM
                        #pygame.time.wait(500)
                        
                        valid  = True if (bpm>=50 and bpm<=170) else False

                        stateCheck = math.floor(bpm/10) * 10
                        print("current state:", currState)

                        if(valid ==True):
                            print("writing to file")
                            timeIn ="{0}".format(time.strftime("%H:%M:%S"))
                            writer.writerow([str(timeIn)+' ',str(textout)+' '])
                            print("write successful")
                        else:
                            print("invalid reading, sustaining state")
                            currState=stateCheck
                            bpm = currState
                            textout=str(lastBPM)

                        if(status==1 and sustain ==0):
                            #switch sounds
                            if(stateCheck != currState):
                                currState = stateCheck
                                musicSelect = currState + 5
                                
                                if str(musicSelect) in musicDict:
                                    print("post")
                                    pygame.event.post(scaleTrigger)
                                    status = 2
                                    sustain = 10
                                else:
                                    print("no track")
                        else:
                            sustain -=1;
                        
                            print("current hold",sustain)
                            statusOut="Transition hold"
                            #pygame.time.wait(1000) 

                        
                        pygame.time.wait(1000)    
                        print("runtime bpm:",bpm)
                        print('==================================')
                        statusOut="Reading Heart Rate"
                        
                    #elif status == 2:
                        
                    
                    if(sustain ==0):
                        status=1;


                    lastBPM =math.floor(bpm)
                    #print("window display ")
                    #render window
                    screen.fill((0,0,0))
                    screen.blit(bg,(0,0))
                    
                    button_color = (194, 204, 209)
                    
                    Text_in_Box = ("Heart Rate: " + textout)
                    Status_in_Box = ("Program Status: " + statusOut)
                    start_button = pygame.draw.rect(screen, button_color, [150, 100, 500 , 150])
                    start_text = textFont.render(Text_in_Box , True , (15, 46, 90))
                    status_text= statusFont.render(Status_in_Box , True , (15, 46, 90))

                    screen.blit(start_text , ( 200 , 140)) 
                    screen.blit(status_text , ( 200 , 200)) 
                    
                    #buttons
                    #start_img = pygame.image.load('/home/mills/Desktop/Biometrics_Project/Images/button_start.png').convert_alpha()
                    start_button = button.Button(start_x,button_ystart, start_img,0.8)
                    start_button.draw(screen)
                    
                    # calibrate_img = pygame.image.load('/home/mills/Desktop/Biometrics_Project/Images/button_calibrate.png').convert_alpha()
                    # calibrate_button = button.Button(calibrate_x,button_ystart, calibrate_img,0.8)
                    calibrate_button.draw(screen)
                    
                    # stop_img = pygame.image.load('/home/mills/Desktop/Biometrics_Project/Images/button_stop.png').convert_alpha()
                    # stop_button = button.Button(stop_x,button_ystart, stop_img,0.8)
                    stop_button.draw(screen)
                    
                    pygame.display.update()
                    #p.stopAsyncBPM()
                except Exception as e:
                    print(pygame.error)
                #p.stopAsyncBPM()
                    logging.error(traceback.format_exc())
                #print('current event: ',pygame.event.event_name())
                #pygame.event.pump()
                
        except Exception as e:
            p.stopAsyncBPM()
            logging.error(traceback.format_exc())
            closeCSV()
            pygame.quit()
            exit()