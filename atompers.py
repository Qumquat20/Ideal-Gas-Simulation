from tkinter import *
from random import choice, randint
import math

root = Tk()

winWidth = 750
winHeight = 375 

canvas = Canvas(root, width=winWidth, height=winHeight, bg='white')
canvas.pack()

def mouseEnter(event):
    # ?
    canvas.itemconfig(CURRENT)

def mouseDown(event):
    # remember where the mouse went down
    global lastx,lasty
    lastx = event.x
    lasty = event.y

def mouseMove(event):
    # does something maybe? or maybe useless but won't remove just in case
    global lastx,lasty
    canvas.move(CURRENT, event.x - lastx, event.y - lasty)
    lastx = event.x
    lasty = event.y


Widget.bind(canvas, "<Button-1>", mouseDown)
Widget.bind(canvas, "<B1-Motion>", mouseMove)

def distance_between_two_points(p1,p2):
    return math.sqrt( (p2.x-p1.x)**2 + (p2.y-p1.y)**2 )

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
# These two same same but different name
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Atom:
    def __init__(self, xPos, yPos):
        self.a = xPos
        self.b = yPos
        self.colors = ["black", "red", "green", "blue", "cyan", "yellow", "magenta"]        

        self.atom = canvas.create_oval(xPos-5, yPos-5, xPos+5, yPos+5, fill=choice(self.colors), tags='bruh')

    def randpoint(self):
        rad = randint(2,5)
        t = randint(0,360)
        self.x = self.a + rad*math.cos(t)
        self.y = self.b + rad*math.sin(t)
        
    def getComponents(self):
        self.dx = self.x-self.a
        self.dy = self.y-self.b 

    def centerCoords(self):
        x = canvas.bbox(self.atom)[2] - 5
        y = canvas.bbox(self.atom)[3] - 5
        return (x,y)

    def checkSide(self,P,Q,ball):
        O = Point(ball.centerCoords()[0],ball.centerCoords()[1])
        distOP = distance_between_two_points(O,P)
        distOQ = distance_between_two_points(O,Q)
        maxDist = max(distOP,distOQ)
        OP = Vector(P.x-O.x,P.y-O.y)
        OQ = Vector(Q.x-O.x,Q.y-O.y)
        QP = Vector(P.x-Q.x,P.y-Q.y)
        crossProduct = OP.x * OQ.y - OP.y * OQ.x
        triangleArea = abs(crossProduct)/2
        dotOP_QP = OP.x * QP.x + OP.y * QP.y
        dotOQ_PQ = OQ.x * (-QP.x) + OQ.y * (-QP.y)

        if dotOP_QP > 0 and dotOQ_PQ > 0:
            minDist = (2*triangleArea)/distance_between_two_points(P,Q)
        else:
            minDist = min(distance_between_two_points(O,P),distance_between_two_points(O,Q))

        return minDist,maxDist

    def wallColCheck(self):
        for wall in walls:
            wall.updatePos()
            
            # Check left side collision
            if self.checkSide(wall.TOP_LEFT,wall.BOTTOM_LEFT,self)[0] <= 5 and self.checkSide(wall.TOP_LEFT,wall.BOTTOM_LEFT,self)[1] >= 5:
                self.dx = -1 * self.dx
            # Check right side collision
            if self.checkSide(wall.TOP_RIGHT,wall.BOTTOM_RIGHT,self)[0] <= 5 and self.checkSide(wall.TOP_RIGHT,wall.BOTTOM_RIGHT,self)[1] >= 5:
                self.dx = -1 * self.dx
            # Check top side collision
            if self.checkSide(wall.TOP_LEFT,wall.TOP_RIGHT,self)[0] <= 5 and self.checkSide(wall.TOP_LEFT,wall.TOP_RIGHT,self)[1] >= 5:
                self.dy = -1 * self.dy
            # Check bottom side collision
            if self.checkSide(wall.BOTTOM_LEFT,wall.BOTTOM_RIGHT,self)[0] <= 5 and self.checkSide(wall.BOTTOM_LEFT,wall.BOTTOM_RIGHT,self)[1] >= 5:
                self.dy = -1 * self.dy
    

    isMoving = False
    t = 41

    def movement(self):
        if canvas.coords(self.atom)[3] > winHeight or canvas.coords(self.atom)[1] < 0:
            self.dy = -1 * self.dy
        if canvas.coords(self.atom)[2] > winWidth or canvas.coords(self.atom)[0] < 0:
            self.dx = -1 * self.dx
        canvas.move(self.atom,self.dx,self.dy)

        self.wallColCheck()

        root.after(self.t,self.movement)
        

particles = []

def clearPlaceholder(entry,event):
    entry.delete(0,END)
    entry.configure(fg='black')

def putPlaceholder(entry,text,*args):
    entry.delete(0,END)
    entry.configure(fg='grey')
    entry.insert(0,text)

particleNum = Entry(root)
particleNum.configure(bg='white',fg='grey')
putPlaceholder(particleNum,'  # of particles to add')
particleNum.bind("<FocusIn>",lambda ev: clearPlaceholder(particleNum,ev))
particleNum.bind("<FocusOut>",lambda ev: putPlaceholder(particleNum,'  # of particles to add',ev))
particleNum.pack()

def addAtom():
    global particles
    if particleNum.get() == '':
        x = randint(5,winWidth-5)
        y = randint(5,winHeight-5)

        particles.append(Atom(x, y))

        particles[-1].randpoint()
        particles[-1].getComponents()
    else:
        for x in range(int(particleNum.get())):
            x = randint(5,winWidth-5)
            y = randint(5,winHeight-5)

            particles.append(Atom(x, y))

            particles[-1].randpoint()
            particles[-1].getComponents()

addParticleButton = Button(root, text='Add particle',command=addAtom)
addParticleButton.configure(bg='white',fg='black')
addParticleButton.pack()

walls = []

class Wall:
    # Add movement method maybe?
    def __init__(self,x,y,length,width):
        self.wall = canvas.create_rectangle(x,y-length/2,x+width,y+length/2,fill='black')

        canvas.tag_bind(self.wall, "<Any-Enter>", mouseEnter)
        self.updatePos()

    def updatePos(self):
        self.TOP_LEFT = Point(canvas.coords(self.wall)[0],canvas.coords(self.wall)[3])
        self.TOP_RIGHT = Point(canvas.coords(self.wall)[2],canvas.coords(self.wall)[3])
        self.BOTTOM_LEFT = Point(canvas.coords(self.wall)[0],canvas.coords(self.wall)[1])
        self.BOTTOM_RIGHT = Point(canvas.coords(self.wall)[2],canvas.coords(self.wall)[1])

    isSqueezer = False

    def moveLeft(self):
        canvas.move(self.wall,-winWidth*0.05,0)
        for ball in particles:
            if ball.checkSide(self.TOP_LEFT,self.BOTTOM_LEFT,ball)[0] <= 5 and ball.checkSide(self.TOP_LEFT,self.BOTTOM_LEFT,ball)[1] >= 5:
                self.dx = -1 * self.dx
                ball.lastdx, ball.lastdy = ball.dx, ball.dy
                ball.dx, ball.dy = 0,0
                ball.isMoving = False
                canvas.move(ball,-winWidth*0.05,0)


wallLen = Entry(root)
wallLen.configure(bg='white',fg='grey')
putPlaceholder(wallLen,'  Length of wall to add')
wallLen.bind("<FocusIn>",lambda event: clearPlaceholder(wallLen,event))
wallLen.bind("<FocusOut>",lambda event: putPlaceholder(wallLen,'Length of wall to add',event))
wallLen.pack()

def addWall():
    global walls
    if wallLen.get() != '':
        walls.append(Wall(winWidth/2,winHeight/2,int(wallLen.get()),10))

addWallButton = Button(root, text='Add wall',command=addWall)
addWallButton.configure(bg='white',fg='black')
addWallButton.pack()

def addSqueezer():
    global walls
    walls.append(Wall(winWidth,winHeight/2,winHeight,3))

addSqueezerButton = Button(root, text='Spawn squeezer',command=addSqueezer)
addSqueezerButton.pack()

paused = False
def simStart():
    global paused
    if paused:
        for atom in particles:
            if hasattr(atom, 'lastdx'):
                atom.dx = atom.lastdx
                atom.dy = atom.lastdy
                atom.isMoving = True
                paused = False
            else:
                atom.movement()
    else:
        for atom in particles:
            if atom.isMoving == False:
                atom.isMoving = True
                atom.movement()

startButton = Button(root, text='Start', command=simStart)
startButton.configure(bg='white',fg='black')
startButton.pack()

def simStop():
    global paused
    paused = True
    for atom in particles:
        if not (atom.dx == 0 and atom.dy == 0):
            atom.lastdx = atom.dx
            atom.lastdy = atom.dy
            atom.dx = 0
            atom.dy = 0
            atom.isMoving = False

stopButton = Button(root, text='Pause', command=simStop)
stopButton.configure(bg='white',fg='black')
stopButton.pack()

exitButton = Button(root, text='Quit', command=root.destroy)
exitButton.configure(bg='white',fg='black')
exitButton.pack()

root.configure(background='grey')

root.title('Ideal Gas Simulation')
root.mainloop()