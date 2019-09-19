# Mode Template: http://www.cs.cmu.edu/~112/notes/notes-animations-demos.html
#https://colorswitch.co/  Recreating this game
#http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html used starter code
#For the run function
import random
from tkinter import *
from twoPlayer import *
#Functions to write and read file from 
#http://www.cs.cmu.edu/~112/notes/notes-strings.html

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "a") as f:
        f.write(contents)
        
#Class for players object
class Ball(object):
    
    def __init__(self, color, cx, cy):
        self.color=color
        self.cx=cx
        self.cy=cy
        self.r=10
        
    #Function to draw the object
    def draw(self, canvas):
        canvas.create_oval(self.cx-self.r, self.cy-self.r, self.cx+self.r, self.cy+self.r, \
        fill=self.color)

#Superclass for all obstacles
class Obstacle(object):
    
    def __init__(self, cx, cy):
        self.cx=cx
        self.cy=cy
        
class pointCounter(Obstacle):
    def __init__(self, cx, cy, r):
        super().__init__(cx, cy)
        self.r=r
        
    def draw(self, canvas, scrollY):
        canvas.create_rectangle(self.cx-self.r, self.cy-self.r+scrollY, 
        self.cx+self.r, self.cy+self.r+scrollY, fill="white")
        
    def collision(self, other, scrollY):
        if other.cy==self.cy+scrollY:
            return True
        return False

class ColorChanger(Obstacle):
    
    def __init__(self, cx, cy,r):
        super().__init__(cx,cy)
        self.color="yellow"
        self.r=r
        self.turn=0
        
    def draw(self, canvas, scrollY):
        canvas.create_arc(self.cx-self.r, self.cy-self.r+scrollY, self.cx+self.r, 
        self.cy+self.r+scrollY, start=0-self.turn, fill="red")
        canvas.create_arc(self.cx-self.r, self.cy-self.r+scrollY, self.cx+self.r, 
        self.cy+self.r+scrollY, start=90-self.turn, fill="yellow")
        canvas.create_arc(self.cx-self.r, self.cy-self.r+scrollY, self.cx+self.r, 
        self.cy+self.r+scrollY, start=180-self.turn, fill="green")
        canvas.create_arc(self.cx-self.r, self.cy-self.r+scrollY, self.cx+self.r, 
        self.cy+self.r+scrollY, start=270-self.turn, fill="blue")
        
    def updateTurn(self):
        self.turn+=5
    
    #Checks if ball collided with obstacle    
    def collision(self, other, scrollY):
        if other.cy==self.cy+scrollY:
            return True
        return False
#Class for the circle obstacle
class Circle(Obstacle):
    
    def __init__(self, cx, cy, r):
        super().__init__(cx,cy)
        self.r=r
        self.turn=0
        self.a=0
        self.b=0
        self.c=0
        self.d=0
        
    #http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_arc.html  Used 
    #this link to draw arcs
    #https://stackoverflow.com/questions/31385036/getting-the-fill-color-or-any
    #-other-property-of-a-item-drawn-in-a-canvas-in-tkin  Learnt about 
    # itemcget from here
    def draw(self, canvas, scrollY):
        self.a = canvas.create_arc(self.cx-self.r, self.cy-self.r + scrollY, 
        self.cx+self.r, self.cy+self.r+scrollY, start = 0-self.turn, 
        style = "arc",outline="red", width = 10)
        self.b = canvas.create_arc(self.cx-self.r, self.cy-self.r+scrollY, 
        self.cx+self.r, self.cy+self.r+scrollY, start = 90-self.turn, 
        style = "arc",outline="yellow", width = 10)
        self.c = canvas.create_arc(self.cx-self.r, self.cy-self.r+scrollY, 
        self.cx+self.r, self.cy+self.r+scrollY, start = 180-self.turn, 
        style = "arc",outline="green", width = 10)
        self.d = canvas.create_arc(self.cx-self.r, self.cy-self.r+scrollY, 
        self.cx+self.r, self.cy+self.r+scrollY, start = 270-self.turn, 
        style = "arc",outline="blue", width = 10)
        
    def updateTurn(self):
        self.turn+=5
    
    #Checks if ball collides with obstacle and if color that section is same as 
    #color of ball
    def collision(self, other, canvas, scrollY):
        l=[self.a, self.b, self.c, self.d]
        if other.cy in range(self.cy+self.r+scrollY-5, self.cy+self.r+scrollY+5):
            for i in l:
                if canvas.itemcget(i, "outline")==other.color:
                    if 180 in range(int(float(canvas.itemcget(i, "start")))-90,int(float(canvas.itemcget(i, "start")))):
                        return False
                if canvas.itemcget(i, "outline")!=other.color:
                    if 180 in range( int(float(canvas.itemcget(i, "start")))-90,int(float(canvas.itemcget(i, "start")))):
                        return True
        elif other.cy in range(self.cy-self.r+scrollY-5, self.cy-self.r+scrollY+5):
            for i in l:
                if canvas.itemcget(i, "outline")==other.color:
                    if 0 in range(int(float(canvas.itemcget(i, "start")))-90,int(float(canvas.itemcget(i, "start")))):
                        return False
                if canvas.itemcget(i, "outline")!=other.color:
                    if 0 in range( int(float(canvas.itemcget(i, "start")))-90,int(float(canvas.itemcget(i, "start")))):
                        return True
        return None
#Double circle obstacle
class doubleCircle(Circle):
    
    def __init__(self, cx, cy, r):
        super().__init__(cx,cy,r)
        self.c1 = Circle(cx-r, cy, r)
        self.c2 = Circle(cx+r, cy, r)
        self.a=0
        self.b=0
        self.c=0
        self.d=0
        
    def draw(self, canvas, scrollY):
        self.c1.draw(canvas, scrollY)
        self.a = canvas.create_arc(self.c2.cx-self.c2.r, self.c2.cy-self.c2.r + scrollY, 
        self.c2.cx+self.c2.r, self.c2.cy+self.c2.r+scrollY, start = 0+self.c2.turn, 
        style = "arc",outline="yellow", width = 10)
        self.b = canvas.create_arc(self.c2.cx-self.c2.r, self.c2.cy-self.c2.r+scrollY, 
        self.c2.cx+self.c2.r, self.c2.cy+self.c2.r+scrollY, start = 90+self.c2.turn, 
        style = "arc",outline="red", width = 10)
        self.c = canvas.create_arc(self.c2.cx-self.c2.r, self.c2.cy-self.c2.r+scrollY, 
        self.c2.cx+self.c2.r, self.c2.cy+self.c2.r+scrollY, start = 180+self.c2.turn, 
        style = "arc",outline="blue", width = 10)
        self.d = canvas.create_arc(self.c2.cx-self.c2.r, self.c2.cy-self.c2.r+scrollY, 
        self.c2.cx+self.c2.r, self.c2.cy+self.c2.r+scrollY, start = 270+self.c2.turn, 
        style = "arc",outline="green", width = 10)
        
    def updateTurn(self):
        self.c1.turn+=5
        self.c2.turn+=5
        
    def collision(self, other, canvas, scrollY):
        collide=0
        l=[self.c1.a, self.c1.b, self.c1.c, self.c1.d]
        if other.cy<=self.c1.cy+self.c1.r+scrollY and \
        other.cy>=self.c1.cy-self.c1.r+scrollY:
            for i in l:
                    if canvas.itemcget(i, "outline")==other.color:
                        if (float(canvas.itemcget(i, "start"))<=315 and \
                        float(canvas.itemcget(i, "start"))>=225):
                            return False
            return True
        return None

#Class for the line obstacle
class line(Obstacle):
    def __init__(self, cx, cy):
        super().__init__(cx,cy)
        self.shiftX = -self.cx//4
        self.shiftR = 0
        self.shiftY = self.cx//4
        self.shiftG = self.cx//2
        self.shiftB = 3*self.cx//4
        self.a =0
        self.b=0
        self.c=0
        self.d=0
        self.e=0
        
    def shift(self):
        if self.shiftX+5<self.cx:
            self.shiftX+=5
        else:
            self.shiftX=-self.cx//4
        if self.shiftR+5< self.cx:
            self.shiftR+=5
        else:
             self.shiftR = -self.cx//4
             self.curColor="red"
        if self.shiftY+5 < self.cx:
            self.shiftY+=5
        else:
            self.shiftY = -self.cx//4
            self.curColor="yellow"
        if self.shiftG+5 < self.cx:
            self.shiftG+=5
        else:
            self.shiftG = -self.cx//4
            self.curColor="green"
        if self.shiftB+5 < self.cx:
            self.shiftB+=5
        else:
            self.shiftB = -self.cx//4
            self.curColor="blue"
        
    def draw(self, canvas, scroll):
        self.a = canvas.create_rectangle(self.shiftR,self.cy+scroll,self.shiftR+self.cx//4, 
        self.cy+scroll+10, fill="red", width=0)
        self.b = canvas.create_rectangle(self.shiftY,self.cy+scroll, self.shiftY+self.cx//4, 
        self.cy+scroll+10, fill="yellow",width=0)
        self.c = canvas.create_rectangle(self.shiftG, self.cy+scroll, self.shiftG+self.cx//4, 
        self.cy+scroll+10, fill="green",width=0)
        self.d = canvas.create_rectangle(self.shiftB, self.cy+scroll, self.shiftB+self.cx//4, 
        self.cy+scroll+10, fill="blue",width=0)
        self.e = canvas.create_rectangle(self.shiftX, self.cy+scroll, self.shiftX+self.cx//4,
        self.cy+scroll+10, fill="yellow", width=0)
        
    def collision(self, other, canvas, scroll):
        l=[self.a, self.b, self.c, self.d, self.e]
        shifts = [self.shiftR, self.shiftY, self.shiftG, self.shiftB, self.shiftX]
        if self.cy+10+scroll>=other.cy and self.cy+scroll<=other.cy:
            for i in range(len(l)):
                if canvas.itemcget(l[i], "fill")==other.color:
                    if self.cx//2 in range(shifts[i], shifts[i]+self.cx//4):
                        return False
                if canvas.itemcget(l[i], "fill")!=other.color:
                    if self.cx//2 in range(shifts[i], shifts[i]+self.cx//4):
                        return True
        return None
            
####################################
# init
####################################

def init(data):
    # There is only one init, not one-per-mode
    data.mode = "startScreen"
    data.score = 0
    data.startR=60
    data.side=40
    data.gravity=10
    data.player= Ball("red", data.width//2, data.height)
    data.scrollY=0
    data.worldHeight = 100*data.height
    data.prev=0
    data.l=["Circle", "line", "doubleCircle", "colorChanger", "pointCounter"]
    data.obstacles=[ColorChanger(data.width//2, 3*data.height//4, 20),
    Circle(data.width//2, data.height//2, 45),
    pointCounter(data.width//2, data.height//2, 10),
    line(data.width, data.height//4), 
    doubleCircle(data.width//2, 0,45)]
    data.obstacleY=data.height/2
    data.timer=0
    data.startCircle=Circle(data.width//2, data.height//2, data.startR+10)
    data.startLine1=line(data.width, data.height-20)
    data.startLine2 = line(data.width, 20)
    data.endLine=line(data.width, 120)
    
####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "startScreen"): startScreenMousePressed(event, data)
    elif (data.mode == "playGame"):   playGameMousePressed(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)
    elif (data.mode== "endScreen"): endScreenMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "startScreen"): startScreenKeyPressed(event, data)
    elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)
    elif(data.mode== "endScreen"): endScreenKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "startScreen"): startScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)
    elif(data.mode == "endScreen"): endScreenTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "startScreen"): startScreenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)
    elif(data.mode == "endScreen"): endScreenRedrawAll(canvas, data)

####################################
# startScreen mode
####################################

def startScreenMousePressed(event, data):
    if event.x<=data.width//2+data.startR and event.x>=data.width//2-data.startR:
        if event.y<=data.height//2+data.startR and event.y>=data.height//2-data.startR:
            data.mode="playGame"
    if event.x<=45 and event.x>=10:
        if event.y<=45 and event.y>=10:
            data.mode="help"

def startScreenKeyPressed(event, data):
    pass

def startScreenTimerFired(data):
    data.startCircle.updateTurn()
    data.startLine1.shift()
    data.startLine2.shift()

def startScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height, fill="black")
    canvas.create_text(data.width//2, data.height//4, 
    text="Welcome to ColorSwitch", fill="white", font=("system",20))
    canvas.create_oval(data.width//2-data.startR, data.height//2-data.startR, 
    data.width//2+data.startR, data.height//2+data.startR, fill="grey")
    canvas.create_polygon(data.width//2-data.side+10, data.height//2-data.side, 
    data.width//2-data.side+10, data.height//2+data.side, data.width//2+data.side+10, 
    data.height//2, fill="white")
    data.startCircle.draw(canvas, data.scrollY)
    data.startLine1.draw(canvas, data.scrollY)
    data.startLine2.draw(canvas, data.scrollY)
    canvas.create_rectangle(10, 10, 45, 45, fill="white")
    canvas.create_text(27.5, 27.5, text="Help", font=("courier", 10))
####################################
# help mode
####################################

#Still need to make the help mode

def helpMousePressed(event, data):
    pass

def helpKeyPressed(event, data):
    data.mode="startScreen"

def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    canvas.create_text(data.width//2, data.height//2-90, 
    text="Press the spacebar to make the ball jump", 
    font=("courier",10), justify="center")
    canvas.create_text(data.width//2, data.height//2-60, 
    text="The ball can only pass through \nobstacles of same color", font=("courier", 10),
    justify="center")
    canvas.create_text(data.width//2, data.height//2-30, 
    text="Pass through white squares to earn points", font=("courier",10), justify="center")
    canvas.create_text(data.width//2, data.height//2, 
    text="Press any key to return to start screen", font=("courier",10))

####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
    data.score = 0

def playGameKeyPressed(event, data):
    if data.player.cy<data.height//2:
        data.scrollY+=15
    elif event.keysym=="space":
        data.player.cy-=45

def playGameTimerFired(data):
    data.timer+=100
    if data.timer%1000==0:
        #Generates random obstacles
        obstacle=random.choice(data.l) 
        if obstacle == "Circle":
            r=random.randint(45,60)
            data.obstacles.append(Circle(data.width//2, data.prev-data.height//3\
            , r))
            data.obstacles.append(pointCounter(data.width//2, data.prev-data.height//3, 10))
        elif obstacle=="line":
            data.obstacles.append(line(data.width, data.prev-data.height//3))
        elif obstacle=="doubleCircle":
            data.obstacles.append(doubleCircle(data.width//2, data.prev-data.height//3, 45))
        elif obstacle=="colorChanger":
            data.obstacles.append(ColorChanger(data.width//2, data.prev-data.height//3, 20))
        elif obstacle=="pointCounter":
            data.obstacles.append(pointCounter(data.width//2, data.prev-data.height//3, 10))
    if len(data.obstacles)!=0:
        data.prev=data.obstacles[-1].cy
    #Constantly moving the obstacles and player
    data.player.cy+=data.gravity
    for i in data.obstacles:
        if isinstance(i, Circle) or isinstance(i, doubleCircle) or \
        isinstance(i, ColorChanger):
            i.updateTurn()
        elif isinstance(i, line):
            i.shift()
        
    if data.player.cy+10>data.height:
        data.player.cy=data.height-10

def playGameRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height)
    canvas.create_rectangle(0, data.scrollY-data.worldHeight, data.width, 
    data.height+data.scrollY, fill="black")
    data.player.draw(canvas)
            
    #Draws all obtacles
    for i in data.obstacles:
        i.draw(canvas, data.scrollY)
    #Checking for collisions
    i=0
    l=[]
    for i in data.obstacles:
        if isinstance(i, ColorChanger):
            if i.collision(data.player, data.scrollY)==True:
                data.player.color=random.choice(["red", "yellow", "blue", "green"])
            else:
                l.append(i)
        elif isinstance(i, pointCounter):
            if i.collision(data.player, data.scrollY)==True:
                data.score+=1
            else:
                l.append(i)
        elif isinstance(i, Circle) and not isinstance(i, doubleCircle):
            if i.collision(data.player, canvas, data.scrollY)==True:
                l.append(i)
                data.mode="endScreen"
                writeFile("scores.txt", str(data.score)+" ")
            else:
                l.append(i)
        elif isinstance(i, doubleCircle):
            if i.collision(data.player, canvas, data.scrollY)==True:
                l.append(i)
                data.mode="endScreen"
                writeFile("scores.txt", str(data.score)+" ")
            else:
                l.append(i)
        elif isinstance(i, line):
            if i.collision(data.player, canvas, data.scrollY)==True:
                l.append(i)
                data.mode="endScreen"
                writeFile("scores.txt", str(data.score)+" ")
                
            else:
                l.append(i)
        if data.scrollY>0:
            if data.player.cy+data.player.r>=data.height:
                data.mode="endScreen"
                writeFile("scores.txt", str(data.score)+" ")
            
    data.obstacles=l
    
    canvas.create_text(0, 0, text="Score="+str(data.score), anchor=NW, fill="white")

####################################
# End screen
####################################

def endScreenMousePressed(event, data):
    pass
    
def endScreenKeyPressed(event, data):
    if event.keysym=="s":
        data.mode="playGame"
        data.score=0
        data.player.cy=data.height
        data.player.cx=data.width//2
        data.scrollY=0
        data.obstacles=[ColorChanger(data.width//2, 3*data.height//4, 20),
        Circle(data.width//2, data.height//2, 45), line(data.width, data.height//4), 
        doubleCircle(data.width//2, 0,45)]
    
def endScreenTimerFired(data):
    data.startLine1.shift()
    data.startLine2.shift()
    data.endLine.shift()
    
def endScreenRedrawAll(canvas, data):
    scores = readFile("scores.txt")
    s=scores.split()
    for i in range(len(s)):
        s[i]=int(s[i])
    pos=70
    data.scrollY=0
    canvas.create_rectangle(0,0, data.width, data.height, fill="black")
    canvas.create_text(data.width//2, data.height//4+20, text="Score", fill="white",
    font=("system", 60))
    canvas.create_text(data.width//2, data.height//2+20, text = data.score, fill="white",
    font=("system", 60))
    data.startLine1.draw(canvas, data.scrollY)
    data.startLine2.draw(canvas, data.scrollY)
    canvas.create_text(data.width//2, data.height-50, text="Press 's' to restart game", 
    font=("courier", 10), fill="white")
    canvas.create_text(data.width//2, 50, text="Leaderboard", 
    font=("system", 20), fill="yellow")
    if len(s)>=3:
        canvas.create_text(data.width//2, pos, text=sorted(s)[len(s)-1], 
        fill="white", font=("system", 10))
        canvas.create_text(data.width//2, pos+20, text=sorted(s)[len(s)-2], 
        fill="white", font=("system", 10))
        canvas.create_text(data.width//2, pos+40, text=sorted(s)[len(s)-3], 
        fill="white", font=("system", 10))
    else:
        for i in range(len(s)):
            canvas.create_text(data.width//2, pos, text=sorted(s)[len(s)-i-1], 
            fill="white")
            pos+=20
    data.endLine.draw(canvas, data.scrollY)
####################################
# use the run function as-is
####################################

def singlePlayerRun(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

print("Choose a mode: ")
print("1. Single Player")
print("2. Two Player")
mode=input("Enter 1 or 2: ")
if int(mode)==1:
    singlePlayerRun(400, 600)
elif int(mode)==2:
    doublePlayerRun(800, 600)
