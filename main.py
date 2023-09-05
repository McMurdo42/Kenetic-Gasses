from math import *
import tkinter
from random import *
import time
import numpy as np

size = 5
windowWidth = 600
windowHeight = 600
gridx = int(windowWidth/size)
gridy = int(windowHeight/size)
timestep = 0.05
partlist = []
num = 50
vel = 10

window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=windowWidth,height=windowHeight, bg="white")
text = canvas.create_text(windowWidth/2,10,text=vel,fill="black",font=('Helvetica 15 bold'))
canvas.pack()


class Particle:
    def __init__(self,ID,posx,posy,velx,vely,col):
        self.ID = ID
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely
        self.col = col

def create(posx,posy,velx,vely,size):
    newPart = Particle(canvas.create_oval(posx-size,posy-size,posx+size,posy+size,fill="red",outline="white"),posx,posy,velx,vely,False)
    return newPart

def collision(part1,part2,size):
    pos1 = [part1.posx,part1.posy]
    pos2 = [part2.posx,part2.posy]
    vel1 = [part1.velx,part1.vely]
    vel2 = [part2.velx,part2.vely]
    disp = np.subtract(pos2,pos1)
    dispperp = [disp[1],-disp[0]]
    dispmag = sqrt((disp[0]**2)+(disp[1]**2))
    velb = np.add(np.multiply(np.dot(vel1,np.divide(disp,dispmag)),(np.divide(disp,dispmag))),np.multiply(np.dot(vel2,np.divide(dispperp,dispmag)),np.divide(dispperp,dispmag)))
    vela = np.add(np.multiply(np.dot(vel2,np.divide(disp,dispmag)),(np.divide(disp,dispmag))),np.multiply(np.dot(vel1,np.divide(dispperp,dispmag)),np.divide(dispperp,dispmag)))
    if np.dot(disp,np.subtract(vel2,vel1)) > 0:
        vel1x = part1.velx
        vel1y = part1.vely
        vel2x = part2.velx
        vel2y = part2.vely
    else:
        vel1x = vela[0]
        vel1y = vela[1]
        vel2x = velb[0]
        vel2y = velb[1]
    pos1x = part1.posx
    pos1y = part1.posy
    pos2x = part2.posx
    pos2y = part2.posy
    return vel1x,vel1y,vel2x,vel2y,pos1x,pos1y,pos2x,pos2y

def mover(part,timestep):
    part.posx = part.posx + timestep*part.velx
    part.posy = part.posy + timestep*part.vely
    return part

def colCheck(partlist,boundx,boundy,partcount,size):
    for x in range(0,partcount):
        if partlist[x].col == False:
            for y in range(0,partcount):
                if partlist[x].ID != partlist[y].ID and partlist[y].col == False:
                    if ((partlist[x].posx-partlist[y].posx)**2)+((partlist[x].posy-partlist[y].posy)**2) <= (size*2)**2:
                        partlist[y].col = True
                        partlist[x].col = True
                        newvel = collision(partlist[x],partlist[y],size)
                        partlist[x].velx = newvel[0]
                        partlist[x].vely = newvel[1]
                        partlist[y].velx = newvel[2]
                        partlist[y].vely = newvel[3]
                        partlist[x].posx = newvel[4]
                        partlist[x].posy = newvel[5]
                        partlist[y].posx = newvel[6]
                        partlist[y].posy = newvel[7]
            if partlist[x].posx <= 0 or partlist[x].posx >= boundx - size*2:
                partlist[x].col = True
                partlist[x].velx = -partlist[x].velx
                if partlist[x].posx <= 0:
                    partlist[x].posx = 0
                else:
                    partlist[x].posx = boundx - size*2
            if partlist[x].posy <= 20 or partlist[x].posy >= boundy - size*2:
                partlist[x].col = True
                partlist[x].vely = -partlist[x].vely
                if partlist[x].posy <= 20:
                    partlist[x].posy = 20
                else:
                    partlist[x].posy = boundy - size*2
    return partlist

def randomcreate(num,vel,partlist,boundx,boundy,size):
    for x in range(0,num):
        theta = random()*2*3.14159265
        xpos = randint(0,boundx)
        ypos = randint(0,boundy)
        for part in partlist:
            while ((xpos-part.posx)**2)+((ypos-part.posy)**2) < size*2:
                xpos = randint(0,boundx)
                ypos = randint(0,boundy)
        partlist.append(create(xpos,ypos,vel*cos(theta),vel*sin(theta),size))
    return partlist

def main(partlist,timestep,boundx,boundy,partcount,canvas,size,text):
    total = 0
    partlist = colCheck(partlist,boundx,boundy,partcount,size)
    for x in range(0,partcount):
        partlist[x] = mover(partlist[x],timestep)
        partlist[x].col = False
        canvas.moveto(partlist[x].ID,round(partlist[x].posx),round(partlist[x].posy))
    for x in range(0,partcount):
        total += sqrt((partlist[x].velx*partlist[x].velx)+(partlist[x].vely*partlist[x].vely))
    mean = total/partcount
    canvas.itemconfigure(text,text=(mean))
    canvas.update()


partlist = randomcreate(num,vel,partlist,windowWidth,windowHeight,size)

while True:
    main(partlist,timestep,windowWidth,windowHeight,num,canvas,size,text)