# Mode Template: http://www.cs.cmu.edu/~112/notes/notes-animations-demos.html
#https://colorswitch.co/  Recreating this game
#http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html used starter code
#For the run function
import random
from tkinter import *
        
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
        self.shiftX1 = -self.cx//8
        self.shiftR1 = 0
        self.shiftY1 = self.cx//8
        self.shiftG1 = self.cx//4
        self.shiftB1 = 3*self.cx//8
        self.a1 =0
        self.b1=0
        self.c1=0
        self.d1=0
        self.e1=0
        
        self.shiftX2 = self.cx//2
        self.shiftR2 = 5*self.cx//8
        self.shiftY2 = 6*self.cx//8
        self.shiftG2 = 7*self.cx//8
        self.shiftB2 = self.cx
        self.a2 =0
        self.b2=0
        self.c2=0
        self.d2=0
        self.e2=0
        
    def shift(self):
        if self.shiftX1+5<self.cx:
            self.shiftX1+=5
        else:
            self.shiftX1=-self.cx//8
        if self.shiftR1+5< self.cx:
            self.shiftR1+=5
        else:
             self.shiftR1 = -self.cx//8
             self.curColor="red"
        if self.shiftY1+5 < self.cx:
            self.shiftY1+=5
        else:
            self.shiftY1 = -self.cx//8
            self.curColor="yellow"
        if self.shiftG1+5 < self.cx:
            self.shiftG1+=5
        else:
            self.shiftG1 = -self.cx//8
            self.curColor="green"
        if self.shiftB1+5 < self.cx:
            self.shiftB1+=5
        else:
            self.shiftB1 = -self.cx//8
            self.curColor="blue"
            
            
        if self.shiftX2+5<self.cx:
            self.shiftX2+=5
        else:
            self.shiftX2=-self.cx//8
        if self.shiftR2+5< self.cx:
            self.shiftR2+=5
        else:
             self.shiftR2 = -self.cx//8
             self.curColor="red"
        if self.shiftY2+5 < self.cx:
            self.shiftY2+=5
        else:
            self.shiftY2 = -self.cx//8
            self.curColor="yellow"
        if self.shiftG2+5 < self.cx:
            self.shiftG2+=5
        else:
            self.shiftG2 = -self.cx//8
            self.curColor="green"
        if self.shiftB2+5 < self.cx:
            self.shiftB2+=5
        else:
            self.shiftB2 = -self.cx//8
            self.curColor="blue"
        
    def draw(self, canvas, scroll):
        self.a1 = canvas.create_rectangle(self.shiftR1,self.cy+scroll,self.shiftR1+self.cx//8, 
        self.cy+scroll+10, fill="red", width=0)
        self.b1 = canvas.create_rectangle(self.shiftY1,self.cy+scroll, self.shiftY1+self.cx//8, 
        self.cy+scroll+10, fill="yellow",width=0)
        self.c1 = canvas.create_rectangle(self.shiftG1, self.cy+scroll, self.shiftG1+self.cx//8, 
        self.cy+scroll+10, fill="green",width=0)
        self.d1 = canvas.create_rectangle(self.shiftB1, self.cy+scroll, self.shiftB1+self.cx//8, 
        self.cy+scroll+10, fill="blue",width=0)
        self.e1 = canvas.create_rectangle(self.shiftX1, self.cy+scroll, self.shiftX1+self.cx//8,
        self.cy+scroll+10, fill="yellow", width=0)
        self.a2 = canvas.create_rectangle(self.shiftR2,self.cy+scroll,self.shiftR2+self.cx//8, 
        self.cy+scroll+10, fill="red", width=0)
        self.b2 = canvas.create_rectangle(self.shiftY2,self.cy+scroll, self.shiftY2+self.cx//8, 
        self.cy+scroll+10, fill="yellow",width=0)
        self.c2 = canvas.create_rectangle(self.shiftG2, self.cy+scroll, self.shiftG2+self.cx//8, 
        self.cy+scroll+10, fill="green",width=0)
        self.d2 = canvas.create_rectangle(self.shiftB2, self.cy+scroll, self.shiftB2+self.cx//8, 
        self.cy+scroll+10, fill="blue",width=0)
        self.e2 = canvas.create_rectangle(self.shiftX2, self.cy+scroll, self.shiftX2+self.cx//8,
        self.cy+scroll+10, fill="yellow", width=0)
        
    def collision(self, other, canvas, scroll):
        l=[self.a1, self.b1, self.c1, self.d1, self.e1, self.a2, self.b2, self.c2, self.d2, self.e2]
        shifts = [self.shiftR1, self.shiftY1, self.shiftG1, self.shiftB1, self.shiftX1, 
        self.shiftR2, self.shiftY2, self.shiftG2, self.shiftB2, self.shiftX2]
        if self.cy+10+scroll>=other.cy and self.cy+scroll<=other.cy:
            for i in range(len(l)):
                if canvas.itemcget(l[i], "fill")==other.color:
                    if self.cx//4 in range(shifts[i], shifts[i]+self.cx//8):
                        return False
                if canvas.itemcget(l[i], "fill")!=other.color:
                    if self.cx//4 in range(shifts[i], shifts[i]+self.cx//8):
                        return True
        return None
            
####################################
# init
####################################

def init(data):
    # There is only one init, not one-per-mode
    data.mode = "startScreen"
    data.startR=60
    data.side=40
    data.gravity=10
    data.player1= Ball("red", data.width//4, data.height)
    data.player2 = Ball("red", 3*data.width//4, data.height)
    data.scrollY1=0
    data.scrollY2=0
    data.worldHeight = 100*data.height
    data.prev=0
    data.l=["Circle", "doubleCircle", "colorChanger", "pointCounter"]
    data.obstacles1=[ColorChanger(data.width//4, 3*data.height//4, 20),
    Circle(data.width//4, data.height//2, 45), 
    doubleCircle(data.width//4, 0,45)]
    data.obstacles2=[ColorChanger(3*data.width//4, 3*data.height//4, 20),
    Circle(3*data.width//4, data.height//2, 45), 
    doubleCircle(3*data.width//4, 0,45)]
    data.obstacleY=data.height/2
    data.timer=0
    data.startCircle=Circle(data.width//2, data.height//2, data.startR+10)
    data.startLine1=line(data.width, data.height-20)
    data.startLine2 = line(data.width, 20)
    data.winner=0
    
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
    data.startCircle.draw(canvas, data.scrollY1)
    data.startLine1.draw(canvas, data.scrollY1)
    data.startLine2.draw(canvas, data.scrollY1)
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
    text="Player 1: Press \"tab\" to make the ball jump", 
    font=("courier",10), justify="center")
    canvas.create_text(data.width//2, data.height//2-60, 
    text="Player 2: Press \"Up arow\" to make the ball jump", 
    font=("courier",10), justify="center")
    canvas.create_text(data.width//2, data.height//2-30, 
    text="The ball can only pass through \nobstacles of same color", font=("courier", 10),
    justify="center")
    canvas.create_text(data.width//2, data.height//2, 
    text="Game ends when one player collides", font=("courier",10), justify="center")
    canvas.create_text(data.width//2, data.height//2+30, 
    text="Player who collides first looses, and the other player wins", 
    font=("courier",10), justify="center")
    canvas.create_text(data.width//2, data.height//2+60, 
    text="Press any key to return to start screen", font=("courier",10))

####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
    pass

def playGameKeyPressed(event, data):
    if data.player1.cy<data.height//2:
        data.scrollY1+=15
    elif event.keysym=="Tab":
        data.player1.cy-=45
    if data.player2.cy<data.height//2:
        data.scrollY2+=15
    elif event.keysym=="Up":
        data.player2.cy-=45

def playGameTimerFired(data):
    data.timer+=100
    if data.timer%1000==0:
        #Generates random obstacles
        obstacle=random.choice(data.l) 
        if obstacle == "Circle":
            r=random.randint(45,60)
            data.obstacles1.append(Circle(data.width//4, data.prev-data.height//3\
            , r))
            data.obstacles2.append(Circle(3*data.width//4, data.prev-data.height//3\
            , r))
        elif obstacle=="doubleCircle":
            data.obstacles1.append(doubleCircle(data.width//4, data.prev-data.height//3, 45))
            data.obstacles2.append(doubleCircle(3*data.width//4, data.prev-data.height//3, 45))
        elif obstacle=="colorChanger":
            data.obstacles1.append(ColorChanger(data.width//4, data.prev-data.height//3, 20))
            data.obstacles2.append(ColorChanger(3*data.width//4, data.prev-data.height//3, 20))
    if len(data.obstacles1)!=0:
        data.prev=data.obstacles1[-1].cy
    #Constantly moving the obstacles and player
    data.player1.cy+=data.gravity
    data.player2.cy+=data.gravity
    for i in data.obstacles1:
        if isinstance(i, Circle) or isinstance(i, doubleCircle) or \
        isinstance(i, ColorChanger):
            i.updateTurn()
        elif isinstance(i, line):
            i.shift()
    for i in data.obstacles2:
        if isinstance(i, Circle) or isinstance(i, doubleCircle) or \
        isinstance(i, ColorChanger):
            i.updateTurn()
        elif isinstance(i, line):
            i.shift()
        
    if data.player1.cy+10>data.height:
        data.player1.cy=data.height-data.gravity
    if data.player2.cy+10>data.height:
        data.player2.cy=data.height-data.gravity

def playGameRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height)
    canvas.create_rectangle(0, data.scrollY1-data.worldHeight, data.width, 
    data.height+data.scrollY1, fill="black")
    canvas.create_rectangle(data.width//2, data.scrollY2-data.worldHeight, data.width, 
    data.height+data.scrollY2, fill="black")
    data.player1.draw(canvas)
            
    #Draws all obtacles
    for i in data.obstacles1:
        i.draw(canvas, data.scrollY1)
    data.player2.draw(canvas)
    for i in data.obstacles2:
        i.draw(canvas, data.scrollY2)
    #Checking for collisions
    i=0
    l1=[]
    for i in data.obstacles1:
        if isinstance(i, ColorChanger):
            if i.collision(data.player1, data.scrollY1)==True:
                data.player1.color=random.choice(["red", "yellow", "blue", "green"])
            else:
                l1.append(i)
        if isinstance(i, Circle) and not isinstance(i, doubleCircle):
            if i.collision(data.player1, canvas, data.scrollY1)==True:
                l1.append(i)
                data.winner=2
                data.mode="endScreen"
            else:
                l1.append(i)
        if isinstance(i, doubleCircle):
            if i.collision(data.player1, canvas, data.scrollY1)==True:
                l1.append(i)
                data.winner=2
                data.mode="endScreen"
            else:
                l1.append(i)
    data.obstacles1=l1
    
    l2=[]
    for i in data.obstacles2:
        if isinstance(i, ColorChanger):
            if i.collision(data.player2, data.scrollY2)==True:
                data.player2.color=random.choice(["red", "yellow", "blue", "green"])
            else:
                l2.append(i)
        if isinstance(i, Circle) and not isinstance(i, doubleCircle):
            if i.collision(data.player2, canvas, data.scrollY2)==True:
                l2.append(i)
                data.winner=1
                data.mode="endScreen"
            else:
                l2.append(i)
        if isinstance(i, doubleCircle):
            if i.collision(data.player2, canvas, data.scrollY2)==True:
                l2.append(i)
                data.winner=1
                data.mode="endScreen"
            else:
                l2.append(i)
    data.obstacles2=l2
    canvas.create_line(data.width//2, 0, data.width//2, data.height, fill="white")

####################################
# End screen
####################################

def endScreenMousePressed(event, data):
    pass
    
def endScreenKeyPressed(event, data):
    if event.keysym=="s":
        data.winner=0
        data.mode="playGame"
        data.player1.cy=data.height
        data.player1.cx=data.width//4
        data.player1.color="red"
        data.scrollY1=0
        data.obstacles1=[ColorChanger(data.width//4, 3*data.height//4, 20),
        Circle(data.width//4, data.height//2, 45), 
        doubleCircle(data.width//4, 0,45)]
    
        
        data.player2.cy=data.height
        data.player2.cx=3*data.width//4
        data.player2.color="red"
        data.scrollY2=0
        data.obstacles2=[ColorChanger(3*data.width//4, 3*data.height//4, 20),
        Circle(3*data.width//4, data.height//2, 45), 
        doubleCircle(3*data.width//4, 0,45)]
    
def endScreenTimerFired(data):
    data.startLine1.shift()
    data.startLine2.shift()
    
def endScreenRedrawAll(canvas, data):
    pos=70
    data.scrollY1=0
    canvas.create_rectangle(0,0, data.width, data.height, fill="black")
    data.startLine1.draw(canvas, data.scrollY1)
    data.startLine2.draw(canvas, data.scrollY1)
    canvas.create_text(data.width//2, data.height-50, text="Press 's' to restart game", 
    font=("courier", 10), fill="white")
    canvas.create_text(data.width/2, data.height//2-40, text="The winner is", 
    font=("system", 20), fill="yellow")
    if data.winner==1:
        canvas.create_text(data.width/2, data.height//2, text="Player 1",
        font=("system", 40), fill="green")
    else:
        canvas.create_text(data.width/2, data.height//2, text="Player 2",
        font=("system", 40), fill="green")
####################################
# use the run function as-is
####################################

def doublePlayerRun(width=300, height=300):
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

# doublePlayerRun(800, 600)

