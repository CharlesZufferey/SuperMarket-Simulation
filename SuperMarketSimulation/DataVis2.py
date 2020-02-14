# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:18:53 2020

@author: Charles
"""

import numpy as np
import cv2
import time
import DataSimulation as ds
#%%
market = cv2.imread(r'C:\Users\Charles\Documents\Spiced\Week8\Market.png')
df = ds.Sim.groupby(['CustomerID'])['Path'].apply(list)
#%%
def movev(cx,cy,p,i,frame):

    c = cv2.rectangle(frame, (cx[0], cy[0]), (cx[1], cy[1]), (255, 1, 255), 10)
    cy[0]=cy[0]-i
    cy[1]=cy[1]-i
    cv2.imshow("frame", frame)#,cy[0],cy[1]

    return cy[0],cy[1]

def moveh(cx,cy,pp,j,frame):

    c = cv2.rectangle(frame, (cx[0], cy[0]), (cx[1], cy[1]), (255, 1, 255), 10)
    cx[0] = cx[0]-j
    cx[1] = cx[1]-j
    cv2.imshow("frame", frame)#,cy[0],cy[1]

    return cx[0],cx[1]

#%%
cx = [760,790]
cy = [650,680]
while True:
    i = 0
    j = 0

    fruitsy = 755,880
    fruitsx = 50,440
    drinksy = 55,170
    drinksx = 50,440
    spicesx = 525,630
    spicesy = 50,440
    drinks = (50,440),(55,130)
    spices = (50,440),(580,630)
    dairy = (50,440),(290,370)
    checkout = (510,630),(60,90)
    fruit = (50,440),(780,880)
    #p = np.random.randint(fruitsx[0],fruitsx[1])
    #pp = np.random.randint(drinksy[0],drinksy[1])

    sec = [drinks,spices,dairy,fruit,checkout]
    for s in df[:10]:#range(len(df[3])):

        for t in s:
            s = globals()[t]
            p = np.random.randint(s[0][0],s[0][1])
            pp = np.random.randint(s[1][0],s[1][1])
            #p = 400
            #pp = 400

                #while True:
            frame = market.copy()
                # fruitsy = 755,880
                # fruitsx = 50,440
                # drinksy = 55,190
                # drinksx = 50,440
        
                #cv2.imshow('frame', frame)
                #drinks = cv2.rectangle(frame, (55, 50), (190, 440), (0, 0, 255), 2)
                #dairy = cv2.rectangle(frame, (290, 50), (425, 440), (0, 0, 255), 2)
                #spices = cv2.rectangle(frame, (525, 50), (650, 440), (0, 0, 255), 2)
                #fruit = cv2.rectangle(frame, (755, 50), (880, 440), (0, 0, 255), 2)
                
            entrance = cv2.rectangle(frame, (675, 650), (890, 670), (0, 0, 255), 2)
            checkout1 = cv2.rectangle(frame, (60, 510), (150, 670), (0, 0, 255), 2)
                #checkout2 = cv2.rectangle(frame, (200, 510), (280, 670), (0, 0, 255), 2)
                #checkout3 = cv2.rectangle(frame, (350, 510), (430, 670), (0, 0, 255), 2)
                #checkout4 = cv2.rectangle(frame, (480, 510), (560, 670), (0, 0, 255), 2)
                
            if cy[0] == p and cx[0] == pp :#int(fruitsx[0]+fruitsx[1])/2:
                pass
            else:
                if cy[0] == p and cx[0] == pp :#int(fruitsx[0]+fruitsx[1])/2:
                    pass
                if cy[0] > (p+10):
                    #print("a")
                    i+=1
                    xx,yy = movev(cx,cy,p,i,frame)
                    cy[0] = xx
                    cy[1] = yy
                elif cy[1] < (p-10):
                   # print("b")
                    i-=1
                    xx,yy = movev(cx,cy,p,i,frame)
                    cy[0] = xx
                    cy[1] = yy  
                elif cx[0] > (pp+10):
                    #print("a")
                    j+=1
                    x,y = moveh(cx,cy,pp,j,frame)
                    cx[0] = x
                    cx[1] = y
                elif cx[1] < (pp-10):
                    #print ("aaaaaaaaaaaa")
                    j-=1
                    x,y = moveh(cx,cy,pp,j,frame)
                    cx[0] = x
                    cx[1] = y    
            #if cv2.waitKey(1) & 0xFF == ord('q'):
             #   break
    if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cv2.destroyAllWindows()


#%%
while True:
    edged = cv2.Canny(market, 30, 150)
    cv2.imshow("Edged", edged)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
#%%

    