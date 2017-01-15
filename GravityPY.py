#TODO

#1.Work on different intergration methods such as RK4 and Verlet.
#2:Create solar systems to higlight proof of concept.
#2.Do anything else that was highlighted on my initial objectives.
#3.Code efficiency/OOP approach to program.
#4.increase radius of planets as they consume.
#5.Code spring cleaning.
#setup
#Importing modules
from tkinter import * #enables use of the Tkinter UI, responsible for drawing of objects and generation of GUI
from tkinter import filedialog #Cannot run without this unless in IDLE
from tkinter.colorchooser import *
import time #needed for restriction of refresh rate (may not be needed)
import math #needed for physics calculation
import random #for some more fun parts of the program.
import datetime #for delta time calculations
#functions and variables
#many of these variables can easily be locatlised.
master = Tk() #master window
alphabet=[]
w = Canvas(master, width=1200, height=1000) #generate 1200x1000 canvas
master.resizable(width=False,height=False)
w.pack() #packdat
#master.iconbitmap("icon.ico")
currr = 0 #The row number in the 2d array "OBJECTS" that is avalible for use.
xforce = 0
yforce = 0
speed = 0.001

trail = False
starttime = time.time()
lasttime = starttime
paused = False
prevpaused = False
disco = False
imported = False
planetcolour = ((255,0,0),"#FF0000")
planetselected = 0
#constants
G = 6.673 #simplfied
#2d arrays
OBJECTS = [["n" for x in range(18)] for y in range(200)]#(Y,X) #2d array for planet variables
exclude = [] #temporary mesure

""" This is the worst way of doing this. I know OOP is a thing but that doesn't matter right now
Collums of OBJECTS:
0 = The x0
1 = The y0
2 = The x1
3 = The y1
4 = The mass
5 = The colour string
6 = The objects DELTAX
7 = The objects DELTAY
8 = LASTPOSX
9 = LASTPOSy
10 = radius of the object
11 = R
12 = G
13 = B
14 = Physical representation of the Planet on the plane
15 = time alive
16 = theta
17 = number of planets devoured
"""
tbp = False
tbpc = False
def main():
       if currr > 1:
               for mainl in range(0,currr): #for more than one object
                   if mainl not in exclude:
                       x = 0
                       alone = True
                       for lines in OBJECTS:
                           if lines[0] != "n" and lines[0] != "d":
                                if mainl != x:
                                    alone = False
                                    break
                           x+=1
                       if alone == True: solo(mainl,trail)
                       if OBJECTS[mainl][0] != "n" and OBJECTS[mainl][0] != "d":
                           objectxy = [((OBJECTS[mainl][0]+OBJECTS[mainl][2])/2),((OBJECTS[mainl][1]+OBJECTS[mainl][3])/2)]
                           calculatedeltaXY(currr,G,objectxy,mainl,exclude,OBJECTS,speed)
                           OBJECTS[mainl][8] = objectxy [0]
                           OBJECTS[mainl][9] = objectxy [1]
       if currr == 1: solo(0,trail)
def solo(no,trail):
        x = ((OBJECTS[no][0]+OBJECTS[no][2])/2)
        y = ((OBJECTS[no][1]+OBJECTS[no][3])/2)
        w.move(OBJECTS[no][14],OBJECTS[no][6],OBJECTS[no][7])
        OBJECTS[no][0],OBJECTS[no][1],OBJECTS[no][2],OBJECTS[no][3] = w.coords(OBJECTS[no][14])
        nx = ((OBJECTS[no][0]+OBJECTS[no][2])/2)
        ny = ((OBJECTS[no][1]+OBJECTS[no][3])/2)
        xy = [x,y]
        nxy = [nx,ny]
        if trail == True: drawtrail(xy,nxy,no,trail)
def calculatedeltaXY(currr,G,objectxy,mainl,exclude,OBJECTS,speed):
        for planets in range(0,currr):
            if OBJECTS[planets][0] != "n" and OBJECTS[planets][0] != "d" and planets not in exclude:
                object2xy = [((OBJECTS[planets][0]+OBJECTS[planets][2])/2),((OBJECTS[planets][1]+OBJECTS[planets][3])/2)]
                if object2xy != objectxy:
                       ###Essentialy the collision detection###
                       if planets not in exclude and mainl not in exclude:
                           radius,theta,xn,yn = maths(objectxy,object2xy)
                           if colide(mainl,planets,radius) == True:
                                  if OBJECTS[mainl][10] >= OBJECTS[planets][10]:
                                         tbd = planets
                                         OBJECTS[mainl][4] += OBJECTS[planets][4]
                                         OBJECTS[mainl][17] += 1
                                  else:
                                         tbd = mainl
                                         OBJECTS[planets][4] += OBJECTS[mainl][4]
                                         OBJECTS[planets][17] += 1
                                  exclude.append(tbd)
                                  w.delete(OBJECTS[tbd][14])
                                  for x in range(0,len(OBJECTS[tbd])): OBJECTS[tbd][x] = "d"

                           ###Calculate variables###
                                   ###EULER###
                           else:
                                  if default.get() == "Euler 8x" or default.get() == "Euler":
                                         if default.get() == "Euler": step = 0
                                         if default.get() == "Euler 4x": step = 4
                                         Euler(objectxy,object2xy,mainl,planets,step,exclude,OBJECTS,speed)
                                  if default.get() == "Trapezium": Trapeziumrule(objectxy,object2xy)
                                  if default.get() == "Verlet": xforce,yforce = Verlet(yn,xn,yforce,xforce,force,theta,step,planets)
                                  if default.get() == "Runge-Kutta": Runge()
                                  if default.get() == "RK4": RK4()

def maths(objectxy,object2xy):
        a = int(objectxy[0] - object2xy[0])
        b = int(objectxy[1] - object2xy[1])
        xn = False
        yn = False
        radius = math.sqrt((a**2) + (b**2)) #Pythagorus theorem
        if radius != 0:
               if a == 0 : theta = 0 #change in x is 0 and we dont want an error to be thrown.
               else: theta = abs(math.atan(b/a))
        else: theta = 0
        if radius == 0:
               radius = 1
        if b > 0: yn = True
        else: yn = False
        if a > 0: xn = True
        else: xn = False
        return(radius,theta,xn,yn)
def physics(mainl,planets,objectxy,object2xy,step,exclude,OBJECTS,speed):
       radius,theta,xn,yn = maths(objectxy,object2xy)
       if radius == 0: pass #no div by 0
       Fgrav = ((G*(int(OBJECTS[mainl][4])*(int(OBJECTS[planets][4]))))/radius**2) / OBJECTS[mainl][4]
       if xn == True:accelerationx = -(Fgrav*math.cos(theta))
       else:accelerationx = Fgrav*math.cos(theta)
       if yn == True: accelerationy = -(Fgrav*math.sin(theta))
       else: accelerationy = Fgrav*math.sin(theta)
       cspeed = speed.get()
       #Resolving (Right) (positive x)
       vx = accelerationx*cspeed / (step+1)
       vy = accelerationy*cspeed / (step+1)
       #Resolving (Down) (positive y)
       return(vx,vy)

def Euler(objectxy,object2xy,mainl,planets,step,exclude,OBJECTS,speed):
       prevxy = objectxy
       for hop in range(0,step+1):
              vx,vy = physics(mainl,planets,objectxy,object2xy,step,exclude,OBJECTS,speed)
              OBJECTS[mainl][6] += vx
              OBJECTS[mainl][7] += vy
       #if trail == True: drawtrail(prevxy,objectxy,mainl)
       colour = toggle()
       if colour != "White":
              w.itemconfig(OBJECTS[mainl][14],fill = colour)
              colour = toggle()
              OBJECTS[mainl][5] = colour

def createplanet(rad,mass,x,y,R,G,B,cx,cy,theta):
    global planetcolour
    global currr
    OBJECTS[currr] = [x-rad,y-rad,x+rad,y+rad,mass,0,cx,cy,x,y,rad,R,G,B,0,time.time(),theta,0]
    colour = toggle()
    if imported == True: colour = '#%02x%02x%02x' % ((int(OBJECTS[currr][11]//1), int(OBJECTS[currr][12]//1), int(OBJECTS[currr][13]//1)))
    if colour == "White": OBJECTS[currr][5] = planetcolour[1]
    else: OBJECTS[currr][5] = colour
    OBJECTS[currr][14] = w.create_oval(OBJECTS[currr][0],OBJECTS[currr][1],OBJECTS[currr][2],OBJECTS[currr][3],fill=OBJECTS[currr][5],tags="oval")
    currr +=1
    w.lower("oval")
    w.lower("star")


def colide(mainl,planets,radius):
    if radius < OBJECTS[mainl][10]:
        w.lower(OBJECTS[planets][14])
        if radius < OBJECTS[mainl][10]: return True
    elif radius < OBJECTS[planets][10]:
        w.lower(OBJECTS[mainl][14])
        if radius < OBJECTS[planets][10]: return True
    else: return False

###UI Related subroutines###
def fml():
	global disco
	disco = not disco
	w.configure(background="Black")
def trailtoggle():
    global trail
    if trailbutton["text"] == "Toggle trail on":
           trailbutton["text"] = "Toggle trail off"
    else:
           trailbutton["text"] = "Toggle trail on"
    trail = not trail


def drawtrail(prevxy,objectxy,mainl,planetcolour):
       if trail == True:
           colour = toggle()
           if colour == "White":
                colour = planetcolour [1]
           w.create_line(prevxy[0],prevxy[1],objectxy[0],objectxy[1],fill=OBJECTS[mainl][5])

def playpause(colourc):
       global paused
       if colourc == True:
           if paused != True:
                  prevpaused = paused
                  playp["text"] = " ► "
                  paused = True
       elif colourc ==  False:
           if playp["text"] == "▐▐  ": playp["text"] = " ► "
           else: playp["text"] = "▐▐  "
           paused = not paused
       w.update()

def safetypause(colourc):
       global tbp
       if paused == True:
              playpause(colourc)
              tbp = False
       else: tbp = True
def clickfunct(event):
       global ox
       global oy
       global mass
       global density
       global planetcolour
       nmass = int(mass.get())
       ndensity = int(density.get())
       if event.x < 1000:
              ox = event.x
              oy = event.y
              w.create_oval(event.x+(nmass/ndensity),event.y+(nmass/ndensity),event.x-(nmass/ndensity),event.y-(nmass/ndensity),fill=planetcolour[1],tags="shotoval")

def motion(event):
       w.delete("shot")
       global planetcolour
       colour = toggle()
       if colour == "White": colour = planetcolour[1]
       if event.x < 1000:
              w.create_line(ox,oy,event.x,event.y,fill=colour,tags="shot")
def release(event):
    if event.x < 1000:
       global planetcolour
       x = event.x
       y = event.y
       cx = event.x - ox
       cy = event.y - oy
       w.delete("shot")
       lmass = int(mass.get())
       ldensity = int(density.get())
       if lmass < ldensity: lmass = ldensity *2
       radius = lmass / ldensity
       end = [x,y]
       start = [ox,oy]
       rad,theta,xneg,yneg= maths(start,end)
       vx = cx/((lmass)*5)
       vy = cy/((lmass)*5)
       createplanet(round(radius),lmass,ox,oy,planetcolour[0][0],planetcolour[0][1],planetcolour[0][2],vx,vy,theta)
    w.delete("shotoval")
def toggle():
     if disco == True: return('#%02x%02x%02x' % (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
     else: return("White")
def getcolour(prevpaused):
    global paused
    global planetcolour
    global tbpc
    prevpaused = paused
    if paused == True:
           askcolour(prevpaused)
           tbpc = False
    else: tbpc = True

def askcolour(prevpaused):
       global planetcolour
       planetcolour = askcolor()
def startoggle(): #make these shift all in one direction at some point
    if stary["text"] == "Toggle Stars off":
        w.delete("star")
        stary["text"] = "Toggle Stars on"
    else:
        for i in range(0,1000):
            for x in range(0,1): #make this variable
                ran = random.randint(0,1000)
                w.create_oval(ran,i,ran,i,outline="White",tags="star")
        w.lower("star")
        stary["text"] = "Toggle Stars off"

###LOAD AND SAVE SYSTEM###
def load():
       global currr
       global imported
       global OBJECTS
       global exclude
       file = filedialog.askopenfilename(filetypes=[(".gpy Format","*.gpy")],title="Choose a file to load")
       currr = 0
       imported = True
       exclude = []
       with open(file,'r') as load:
             for dely in range(0,len(OBJECTS)):
                    for delx in range(0,len(OBJECTS[dely])):
                           OBJECTS[dely][delx] = "n"
             lines = [line.split() for line in load]
             OBJECTS = lines
             w.delete("oval")
             for y in range(0,len(OBJECTS)):
                     if OBJECTS[y][0] == "n": break
                     for x in range(0,18):
                            try: OBJECTS[y][x] = float(OBJECTS[y][x])
                            except: pass
             OBJECTS = lines
       i = 0
       for lines in range(0,len(OBJECTS)):
            print(lines)
            if OBJECTS[lines][0] == "n":
                     currr = lines
                     break
            if OBJECTS[lines][0] != "d": createplanet(OBJECTS[lines][10],OBJECTS[lines][4],((OBJECTS[lines][0]+OBJECTS[lines][2])/2),((OBJECTS[lines][1]+OBJECTS[lines][3])/2),OBJECTS[lines][11],OBJECTS[lines][12],OBJECTS[lines][13],OBJECTS[lines][6],OBJECTS[lines][7],0)
def save():
       file = filedialog.asksaveasfile(filetypes=[(".gpy Format","*.gpy")],title="Choose a file to save")
       for lines in OBJECTS:
              for entity in lines:
                     file.write(str(entity))
                     file.write(" ")
                     if lines[0] == "n": break
              file.write("\n")
       file.close()

def selectobject(event):
       x = event.x
       y = event.y
       closest = w.find_closest(x,y)
       try:
              if w.gettags(closest)[0] == "oval":
                     coords = w.coords(closest)
                     for i in range(0,currr):
                            if coords == [OBJECTS[i][0],OBJECTS[i][1],OBJECTS[i][2],OBJECTS[i][3]]:
                                         global planetselected
                                         planetselected = i
              else: print("There's no planets around here!")
       except: pass

#------------------------------------------UI SECTION------------------------------------------#
w.configure(background="Black")
b1 = w.create_rectangle(1001,0,1205,1000,fill="white")

playp = Button(master,text="▐▐  ", command =lambda:safetypause(False),font=("Helvetica", 12))
playp.place(x=1150,y=5,width=30,height=30)

trailbutton = Button(master, text="Toggle Trail on", command=trailtoggle)
trailbutton.place(x=1040,y=120,width=120)

discotrail = Button(master,command=fml)
discotrail.place(x=1190,y=0,width=10,height=10)

colourchoose = Button(master,text="Select colour",command=lambda:getcolour(prevpaused))
colourchoose.place(x=1040,y=300,width = 120)


loadfunct = Button(master,text="Load file",command=load)
loadfunct.place(x=1060,y=415,width=80)

savefunct = Button(master,text="Save file",command=save)
savefunct.place(x=1060,y=385,width=80)

stary = Button(master, text="Toggle Stars on", command=startoggle)
stary.place(x=1040,y=150,width=120)

curtime = w.create_text(50,30,fill = "White")
fps =     w.create_text(150,30,fill = "White")
###Planet specific variables###
w.create_rectangle(1020,90,1180,190,fill="Light Grey")
w.create_rectangle(1020,200,1180,340,fill="Light Grey")
w.create_rectangle(1020,350,1180,450,fill="Light Grey")
w.create_rectangle(1001,460,1250,470,fill="BLACK")
w.create_rectangle(1020,480,1180,660,fill="Light Grey")
w.create_text(1100,105,text="Toggle Functions",font=("Helvetica",10,"bold underline"))
w.create_text(1100,366,text="Load and save",font=("Helvetica",10,"bold underline"))
w.create_text(1040,63,text="Intergration \nMethod",font=("Helvetica",10))
w.create_text(1100,215,text="Planet Properties",font=("Helvetica",10,"bold underline"))
#Mass#
mass = IntVar()
mass.set(100)
w.create_text(1060,247,text= "Mass",font=("Helvetica", 10))
Mass = Entry(master,width=10,textvariable=mass)
Mass.place(x=1100,y=240)
#Density#
density = IntVar()
density.set(20)
w.create_text(1065,277,text= "Density",font=("Helvetica",10))
Density = Entry(master,width=10, textvariable=density)
Density.place(x=1100,y = 270)


#Planet variable showing#

w.create_text(1100,495,text="Planet Information",font=("Helvetica",10,"bold underline"))

w.create_text(1062,520,text="Velocity")
planetvelocity = IntVar()
showoffvelocity = Entry(master,width=6,textvariable=planetvelocity)
showoffvelocity.place(x=1100,y=513)
planetvelocity.set(0)
showoffvelocity.configure(state="disabled")

w.create_text(1062,550,text="Mass")
planetmass = IntVar()
showoffmass = Entry(master,width=6,textvariable=planetmass)
showoffmass.place(x=1100,y=540)
planetmass.set(0)
showoffmass.configure(state="disabled")

w.create_text(1062,572,text="Density")
planetdensity = IntVar()
showoffdensity = Entry(master,width=6,textvariable=planetdensity)
showoffdensity.place(x=1100,y=567)
planetdensity.set(0)
showoffdensity.configure(state="disabled")

w.create_text(1062,605,text="Devorered\n  planets")
omlettedevourer = IntVar()
showoffdevoured = Entry(master,width=6,textvariable=omlettedevourer)
showoffdevoured.place(x=1100,y=595)
omlettedevourer.set(0)
showoffdevoured.configure(state="disabled")

w.create_text(1062,635,text="Time alive")
planetalivetime = IntVar()
showoffalive = Entry(master,width=6,textvariable=planetalivetime)
showoffalive.place(x=1100,y=625)
planetalivetime.set(0)
showoffalive.configure(state="disabled")


w.create_text(1035,20,text="Force amp")
speed = Scale(master,from_=0.001,to=0.1,resolution=0.001,variable=speed,orient=HORIZONTAL,bg="white",length = 50,width=20)
speed.place(x=1085,y=5)




###    TITLE    ###

for alpha in range (65,91): alphabet.append(chr(alpha))  #something like that
systemname = ("Gravitpy - System: {}{}-{}{}{}".format(alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],random.randint(0,9),random.randint(0,9),random.randint(0,9))) #Standard string consentraition methods leave ugly curly brackets.
master.wm_title(systemname)

###Dropdown  box###
default = StringVar(master)
default.set("Euler")
integration = OptionMenu(master,default,"Euler","Euler 4x","Euler legacy","RK4","Verlet")
integration.config(bg = "White",bd=0,fg="BLACK",activeforeground="BLACK")
integration["menu"].config(bg="White",fg="Black")
integration.place(x=1085,y=50,width=105)

##Startoggle##
startoggle()
#------------------------------------------UI SECTION END--------------------------------------#
#keybinds
w.bind("<Button-1>",clickfunct) #initial click
w.bind("<B1-Motion>",motion) #click and drag
w.bind("<ButtonRelease-1>",release) #release of click
w.bind("<Button-3>",selectobject)
while True:
    if paused != True:
           colour = toggle()
           if colour != "White": colour = toggle()
           try: w.itemconfig(curtime,text=("Time",round(time.time() - starttime,2)))
           except TclError: pass
           otime = time.time()
           main()
           try: w.itemconfig(fps,text=("FPS:", round(1/(time.time()-otime))))
           except ZeroDivisionError: pass
           if tbp == True or tbpc == True:
                  if tbpc == True:
                         playpause(True)
                         askcolour(prevpaused)
                         playpause(False)
                         tbpc = False
                  else: playpause(False)
           if currr > 0 and OBJECTS[planetselected][0] != "d":
                  planetvelocity.set(math.sqrt(((OBJECTS[planetselected][6])**2) +  ((OBJECTS[planetselected][7])**2))*100)
                  planetmass.set(OBJECTS[planetselected][4])
                  planetdensity.set(OBJECTS[planetselected][4] / OBJECTS[planetselected][10])
                  planetalivetime.set(round(time.time() - OBJECTS[planetselected][15]))
                  omlettedevourer.set(OBJECTS[planetselected][17])

    
           for number in range(0,currr):
                  if OBJECTS[number][0] != "d" and OBJECTS[number][0] != "n":
                     w.move(OBJECTS[number][14],OBJECTS[number][6],OBJECTS[number][7])
                     oldxy = [((OBJECTS[number][0]+OBJECTS[number][2])/2),((OBJECTS[number][1]+OBJECTS[number][3])/2)]
                     try: OBJECTS[number][0],OBJECTS[number][1],OBJECTS[number][2],OBJECTS[number][3] = w.coords(OBJECTS[number][14])
                     except ValueError: pass
                     newxy = [((OBJECTS[number][0]+OBJECTS[number][2])/2),((OBJECTS[number][1]+OBJECTS[number][3])/2)]
                     if trail==True: drawtrail(oldxy,newxy,number,planetcolour)
    else: w.update()
    w.update()
