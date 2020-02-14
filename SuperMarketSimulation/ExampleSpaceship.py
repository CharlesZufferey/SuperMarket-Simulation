# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:18:53 2020

@author: Charles
"""

import numpy as np
import cv2
#%%
spaceship = cv2.imread(r'C:\Users\Charles\Documents\Spiced\Week8\A10.png')
#%%
def star_background():
    bg = np.zeros((800,1200,3),dtype=np.uint8)
    for i in range(100):
        x,y = np.random.randint(0,1199),np.random.randint(0,799)
        bg[y,x] = 255
    return bg

bg = star_background()
i = 0
sp1 = 100,100
sp2 = 200,1000
vec1 = 1,1
vec2 = 0,-2
while True:
    frame = bg.copy()
    #
    sp1 = sp1[0] + vec1[0], sp1[1]+vec1[1]
    sp2 = sp2[0] + vec2[0], sp2[1]+vec2[1]
    
    #check boundaries
    if sp1[0]<0:
        sp1 = 0,sp1[1]
    if sp2[1]>1080:
        sp2 = sp2[0],1080
    
    if i == np.random.randint(100,400):
        i = 0
        vec1 = -vec1[0],-vec1[1]
        vec2 = -vec2[0],-vec2[1]
    
    frame[sp1[0]:sp1[0]+112, sp1[1]:sp1[1]+118] = spaceship   
    frame[sp2[0]:sp2[0]+112, sp2[1]:sp2[1]+118] = spaceship  
    i+=1
    cv2.imshow('frame',frame)
    #cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()