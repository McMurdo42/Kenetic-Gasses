from math import *
import tkinter
from random import *
import time

size = 3
windowWidth = 600
windowHeight = 600
gridx = int(windowWidth/size)
gridy = int(windowHeight/size)
timestep = 0.1
partlist = []
num = 10
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
    phi = -(atan2((part1.posy-part2.posy),(part1.posx-part2.posx)))
    theta1 = atan2(part1.vely,part1.velx)
    theta2 = atan2(part2.vely,part2.vely)
    vel1 = sqrt(part1.velx*part1.velx+part1.vely*part1.vely)
    vel2 = sqrt(part2.velx*part2.velx+part2.vely*part2.vely)
    if part1.velx == 0:
        m = part1.vely
    else:
        m = part1.vely/part1.velx
    x = ((part1.velx/m)+part1.vely)/(m+(1/m))
    y = (-x/m)+(part1.velx/m)+part1.vely
    
    '''
    vel1x = ((2*vel2*cos(theta2-phi)*cos(phi))/2)+(vel1*sin(theta1-phi)*cos(phi+1.5708))
    vel1y = (((2*vel2*cos(theta2-phi)*sin(phi))/2)+(vel1*sin(theta1-phi)*sin(phi+1.5708)))
    vel2x = ((2*vel1*cos(theta1-phi)*cos(phi))/2)+(vel2*sin(theta2-phi)*cos(phi+1.5708))
    vel2y = (((2*vel1*cos(theta1-phi)*sin(phi))/2)+(vel2*sin(theta2-phi)*sin(phi+1.5708)))
    midx = (part1.posx+part2.posx)/2
    midy = (part1.posy+part2.posy)/2
    pos1x = size*cos(phi)+midx
    pos1y = size*sin(phi)+midy
    pos2x = -size*cos(phi)+midx
    pos2y = -size*sin(phi)+midy
    '''
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
        partlist.append(create(randint(0,boundx),randint(0,boundy),vel*cos(theta),vel*sin(theta),size))
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