from math import *
import tkinter
from random import *
import time

size = 4
windowWidth = 600
windowHeight = 600
gridx = int(windowWidth/size)
gridy = int(windowHeight/size)
timestep = 0.01
partlist = []
num = 50
vel = 10

window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=windowWidth,height=windowHeight, bg="black")
canvas.pack()


class Particle:
    def __init__(self,ID,posx,posy,velx,vely,col):
        self.ID = ID
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely
        self.col = col

def create(posx,posy,velx,vely):
    newPart = Particle(canvas.create_oval(posx-5,posy-5,posx+5,posy+5,fill="red",outline="white"),posx,posy,velx,vely,False)
    return newPart

def collision(part1,part2):
    phi = atan((part1.posy-part2.posy)/(part1.posx-part2.posx))
    theta1 = atan(part1.vely/part1.velx)
    theta2 = atan(part2.vely/part2.vely)
    vel1 = sqrt(part1.velx*part1.velx+part1.vely*part1.vely)
    vel2 = sqrt(part2.velx*part2.velx+part2.vely*part2.vely)
    vel1x = ((2*vel2*cos(theta2-phi)*cos(phi))/2)+(vel1*sin(theta1-phi)*cos(phi+1.5708))
    vel1y = (((2*vel2*cos(theta2-phi)*sin(phi))/2)+(vel1*sin(theta1-phi)*sin(phi+1.5708)))
    vel2x = ((2*vel1*cos(theta1-phi)*cos(phi))/2)+(vel2*sin(theta2-phi)*cos(phi+1.5708))
    vel2y = (((2*vel1*cos(theta1-phi)*sin(phi))/2)+(vel2*sin(theta2-phi)*sin(phi+1.5708)))
    return vel1x,vel1y,vel2x,vel2y

def mover(part,timestep):
    part.posx = part.posx + timestep*part.velx
    part.posy = part.posy + timestep*part.vely
    return part

def colCheck(partlist,boundx,boundy,partcount):
    for x in range(0,partcount):
        if partlist[x].col == False:
            for y in range(0,partcount):
                if partlist[x].ID != partlist[y].ID and partlist[y].col == False:
                    if ((partlist[x].posx-partlist[y].posx)**2)+((partlist[x].posy-partlist[y].posy)**2) <= 100:
                        partlist[y].col = True
                        partlist[x].col = True
                        newvel = collision(partlist[x],partlist[y])
                        partlist[x].velx = newvel[0]
                        partlist[x].vely = newvel[1]
                        partlist[y].velx = newvel[2]
                        partlist[y].vely = newvel[3]
            if partlist[x].posx <= 0 or partlist[x].posx >= boundx:
                partlist[x].col = True
                partlist[x].velx = -partlist[x].velx
            if partlist[x].posy <= 0 or partlist[x].posy >= boundy:
                partlist[x].col = True
                partlist[x].vely = -partlist[x].vely
    return partlist

def randomcreate(num,vel,partlist,boundx,boundy):
    for x in range(0,num):
        theta = random()*2*3.14159265
        partlist.append(create(randint(0,boundx),randint(0,boundy),vel*cos(theta),vel*sin(theta)))
    return partlist

def main(partlist,timestep,boundx,boundy,partcount,canvas):
    partlist = colCheck(partlist,boundx,boundy,partcount)
    for x in range(0,partcount):
        partlist[x] = mover(partlist[x],timestep)
        partlist[x].col = False
        canvas.moveto(partlist[x].ID,round(partlist[x].posx),round(partlist[x].posy))
    canvas.update()


partlist = randomcreate(num,vel,partlist,windowWidth,windowHeight)

while True:
    main(partlist,timestep,windowWidth,windowHeight,num,canvas)