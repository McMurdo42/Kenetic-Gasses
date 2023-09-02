from math import *
import tkinter
from random import *
import time

size = 10
windowWidth = 600
windowHeight = 600
gridx = int(windowWidth/size)
gridy = int(windowHeight/size)
timestep = 0.1
partlist = []
num = 60
vel = 5

window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=windowWidth,height=windowHeight, bg="white")
text = canvas.create_text(windowWidth/2,10,text=vel,fill="black",font=('Courier 15 bold'))
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

def colCheck(partlist,boundx,boundy,partcount,size):
    for x in range(0,partcount):
        if partlist[x].col == False:
            if partlist[x].posx <= 0 or partlist[x].posx >= boundx - size*2:
                partlist[x].col = True
                if partlist[x].posx <= 0:
                    partlist[x].velx = abs(partlist[x].velx)
                else:
                    partlist[x].velx = -abs(partlist[x].velx)
            if partlist[x].posy <= 20 or partlist[x].posy >= boundy - size*2:
                partlist[x].col = True
                if partlist[x].posy <= 20:
                    partlist[x].vely = abs(partlist[x].vely)
                else:
                    partlist[x].vely = -abs(partlist[x].vely)
    return partlist

def randomcreate(num,vel,partlist,boundx,boundy,size):
    for x in range(0,num):
        theta = random()*2*3.14159265
        partlist.append(create(randint(0,boundx-(size*2)),randint(20,boundy-(size*2)),vel*cos(theta),vel*sin(theta),size))
    return partlist



def forces(partlist, Current, size):
    currplanet = partlist[Current]
    forcex = 0
    forcey = 0
    for item in partlist:
        if currplanet.ID != item.ID:
            distance = sqrt(((partlist[Current].posx - item.posx)**2) + ((partlist[Current].posy - item.posy)**2))
            if distance > 2*size:
                ##force = (6.67428 * (10 ** -11)) * (2/((distance)**2))
                force = (1000) * (1/(((distance)**2)))
            else:
                force = (1000) * (1/(((distance)**2)))
            forcex += force * ((partlist[Current].posx-item.posx)/distance)
            forcey += force * ((partlist[Current].posy-item.posy)/distance)
    force = [forcex, forcey]
    return force

def acceleration(force, mass):
    accel = force/mass
    return accel

def velocity(accel, vel, TimeStep):
    vel = vel + (accel * TimeStep)
    return vel

def movement(velx, vely, posx, posy, timestep):
    posx = posx + (velx * timestep)
    posy = posy + (vely * timestep)
    pos = [posx, posy]
    return pos

def step(partlist, Current, forceList,timestep):
    force = forceList[Current]
    partlist[Current].velx = velocity(acceleration(force[0], 1), partlist[Current].velx,timestep)
    partlist[Current].vely = velocity(acceleration(force[1], 1), partlist[Current].vely,timestep)
    newpos = movement(partlist[Current].velx, partlist[Current].vely, partlist[Current].posx, partlist[Current].posy,timestep)
    partlist[Current].posx = newpos[0]
    partlist[Current].posy = newpos[1]
    return partlist





def main(partlist,timestep,boundx,boundy,partcount,canvas,size,text):
    total = 0
    forcelist = []
    partlist = colCheck(partlist,boundx,boundy,partcount,size)
    for current in range(0,partcount):
        forcelist.append(forces(partlist, current, size))
    for current in range(0,partcount):
        partlist = step(partlist, current, forcelist, timestep)
        partlist[current].col = False
        canvas.moveto(partlist[current].ID,round(partlist[current].posx),round(partlist[current].posy))
    for x in range(0,partcount):
        total += sqrt((partlist[x].velx*partlist[x].velx)+(partlist[x].vely*partlist[x].vely))
    mean = round((total/partcount)*100)/100
    canvas.itemconfigure(text,text=(mean))
    canvas.update()


partlist = randomcreate(num,vel,partlist,windowWidth,windowHeight,size)

while True:
    main(partlist,timestep,windowWidth,windowHeight,num,canvas,size,text)