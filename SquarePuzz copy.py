from cmu_112_graphics import *
#Citation: CMU 15-112-s20 version 0.8.7 [Source code]cmu_112_graphics.py
from PIL import Image
import copy
import random
import os
import math


class LearnBoard():
    def __init__(self,board,mode):
        """each food has x,y coordinate"""
        self.bluh=[]
        self.board=board
        self.mode=mode

    def add(self,piece):
        self.bluh.append(piece)

    def shuffle(self):
        self.piecesize=133
        i=0
        random.shuffle(self.bluh)
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                self.bluh[i].y=100+row*self.piecesize
                self.bluh[i].x=300+col*self.piecesize 
                i+=1

    def show(self,canvas):
        """renders the image of our piece""" 
        for piece in self.bluh:
            piece.render(canvas)

        #create vertical and horizontal bold outline
        for i in range(len(self.board)+1):
            x0=300+self.piecesize*i
            y0=100
            x1=300+self.piecesize*i
            y1=900
            canvas.create_line(x0,y0,x1,y1,width=5,fill=self.mode.color1)
        for a in range(len(self.board)+1):
            for i in range(len(self.board)+1):
                x2=300
                y2=100+self.piecesize*i
                x3=1100
                y3=100+self.piecesize*i
                canvas.create_line(x2,y2,x3,y3,width=5,fill=self.mode.color1)
        for piece in self.bluh:
            if piece.isselected==True:
                piece.dropShadow(canvas)
                piece.render(canvas)
            #print(piece.__repr__())

class LearnPiece():
    def __init__(self,image,pos,app):
        (self.x,self.y)=pos
        print(pos)
        self.app=app
        self.piecesize=self.app.piecesize
        self.col,self.row=self.x//self.piecesize,self.y//self.piecesize
        self.image=image
        self.isselected=False
        (self.finalc,self.finalr)=pos

    def __repr__(self):
        return f"col={self.col},row={self.row}"
    def clicked(self):
        print("clicked")
    def drag(self,x,y):
        """drag to move a selected piece"""
        self.x=x
        self.y=y

    def render(self,canvas):
        #print("x,y",self.x,self.y)
        x0,y0=self.x,self.y
        x1=x0+self.piecesize
        y1=y0+self.piecesize
        canvas.create_rectangle(x0,y0,x1,y1,fill="white",
        outline="antiquewhite",onClick=self.clicked)
        canvas.create_image((x0+x1)//2,(y0+y1)//2,image=self.image)
        # canvas.create_rectangle(x0,y0,x1,y1,fill="cyan",
        # outline="antiquewhite",onClick=self.clicked)
    
    def dropShadow(self,canvas):
        margin=20
        a0,b0=self.x+margin,self.y+margin
        a1=a0+self.piecesize
        b1=b0+self.piecesize
        canvas.create_rectangle(a0,b0,a1,b1,fill="darkgrey",
        width=0)
 
from PIL import Image
class LearnMode(Mode):
    def appStarted(self):
        """take in a start board, initializes data"""
        self.color1=self.app.colorset[0]
        self.color2=self.app.colorset[1]
        self.color3=self.app.colorset[2]
        self.rows=6
        self.cols=6
        self.squaresize=800
        self.piecesize=int(self.squaresize/self.cols)
        self.square=([[0]*self.cols for row in range(self.rows)])
        self.side=[0]*self.cols
        
        self.doubleclick=None
        self.temp=None
        self.s=None
        self.imagesize=self.squaresize
        self.image=self.loadImage('level4.png')
        w,h=self.image.size
        scale=min(w,h)
        self.image=self.scaleImage(self.image,self.imagesize/scale)
        self.image=self.image.crop((0,0,self.squaresize,self.squaresize))
        self.imageW,self.imageH=self.image.size
        self.smol=self.scaleImage(self.image,300/scale)

        self.pieces=self.createPiece()
        self.pieces.shuffle()
        self.start=False
        self.timer=0
        self.timers=0
        self.timerm=0
    
    def modeActivated(self):
        print("In Learn Mode...")
    def timerFired(self):
        self.timer+=1
        if self.timer%10==0:
            self.timers+=1
        if self.timer%600==0:
            self.timers=0
            self.timerm+=1

    def createPiece(self):
        pieces=LearnBoard(self.square,self)
        for row in range(self.rows):
            for col in range(self.cols):
                x0=col*self.piecesize
                y0=row*self.piecesize
                x1=x0+self.piecesize
                y1=y0+self.piecesize
                iImage=ImageTk.PhotoImage(self.image.crop((x0,y0,x1,y1)))
                piece=LearnPiece(iImage,(x0+300,y0+100),self)
                pieces.add(piece)
        return pieces
 
    def mouseDragged(self, event):
        for piece in self.pieces.bluh:
            if piece.isselected:
                piece.drag(event.x,event.y)

    def mousePressed(self, event):
        for piece in self.pieces.bluh:
            if piece.isselected==True:
                return False
        x,y=event.x-300,event.y-100
        clickedrow=int(y//self.piecesize)
        clickedcol=int(x//self.piecesize)
        print("CCCCCCCC=",clickedrow,clickedcol)
        for piece in self.pieces.bluh:
            if clickedrow==int((piece.y-100)//self.piecesize)and clickedcol==int((piece.x-300)//self.piecesize):
                self.temp=(clickedrow,clickedcol)
                print('mousePressedTemp:', self.temp)
                piece.isselected=True

    def mouseReleased(self,event):
        print("Board==",self.pieces.bluh)
        """release mouse to release the piece"""
        if self.temp!=None:
            newrow,newcol=int((event.y-100)//self.piecesize),int((event.x-300)//self.piecesize)
            newx=300+self.piecesize*newcol
            newy=100+self.piecesize*newrow
            if newrow == self.temp[0] and newcol == self.temp[1]:
                for piece in self.pieces.bluh:
                    if piece.isselected:#selected piece
                        (crow,ccol)=self.temp
                        piece.x,piece.y=300+self.piecesize*ccol,100+self.piecesize*crow
                        piece.isselected=False
                        return
            #Swapping#######################
            for piece in self.pieces.bluh:
                if piece.x==newx and piece.y==newy and self.temp != None:#piece@newlocation
                    (crow,ccol)=self.temp
                    # print('mouseReleasedTemp:', self.temp)
                    # print("x,y,crow,ccol",newrow,newcol,crow,ccol)
                    piece.x,piece.y=300+self.piecesize*ccol,100+self.piecesize*crow
                    piece.isselected=False
                    #break
                if piece.isselected:#selected piece
                    print("CHECK ISSELECTED")
                    piece.x,piece.y=newx,newy
                    piece.isselected=False
        self.temp=None
    def swap(self,piece,other):
        self.s=(piece.x,piece.y)
        piece.x,piece.y=other.x,other.y
        (other.x,other.y)=self.s
        piece.isselected=False
        other.isselected=False
        self.s=None

    def checkEnd(self):
        for piece in self.pieces.pieces:
            if piece.row!=int(piece.y//self.piecesize) or piece.col!=int(piece.x//self.piecesize):
                return False
        return True

    def recursionHelper(self, bluh, startIdx, record):
        print("record: ", record)
        print("checkEnd: ", self.checkEnd is True)
        ################ TODO: checkEnd is broken, fix it plz #####################
        if self.checkEnd is True:
            return record
        if startIdx >= len(bluh):
            return record
        piece = bluh[startIdx]
        if piece.row!=int(piece.y//self.piecesize) or piece.col!=int(piece.x//self.piecesize):
            for otherpiece in bluh:
                if piece is not otherpiece and otherpiece.row!=int(otherpiece.y//self.piecesize) or otherpiece.col!=int(otherpiece.x//self.piecesize):
                    print("swapping: ", piece, " and ", otherpiece)
                    self.swap(piece,otherpiece)
                    #we want to wait a little
                    if self.recursionHelper(bluh, startIdx + 1, record + [[piece, otherpiece]]) is None:
                        print("swapping back: ", piece, " and ", otherpiece)
                        self.swap(piece,otherpiece)
        return self.recursionHelper(bluh, startIdx + 1, record)

    def Start(self):
        res = self.recursionHelper(self.pieces.bluh, 0, [])
        
        print("RES!!!!!: ", res)
       
    def setStart(self):
        self.start=True
    
    def onClick(self):
        """When the Back button is clicked, set active mode
        to start mode"""
        self.app.setActiveMode("start")

    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,1500,1000,fill=self.color1,width=0)
        canvas.create_rectangle(300,100,1100,900,fill=self.color2,width=0)
        canvas.create_image(1300,150,image=ImageTk.PhotoImage(self.smol))
        
        self.pieces.show(canvas)
        drawButton(canvas, 1300, self.height-130, 150, 60, 
        self.onClick,"Back",self.color3) 
        drawButton(canvas, 1300, self.height-400, 150, 60, 
        self.Start,"setStart",self.color3) 
        canvas.create_rectangle(1250,400,1350,500,fill="sandybrown",width=0)
        if self.timers<10:
            canvas.create_text(1300,450,text=f"{self.timerm}:0{self.timers}",fill="lightsteelblue",
            font="Helvetica 30 bold",width=0)
        elif self.timers>=10:
            canvas.create_text(1300,450,text=f"{self.timerm}:{self.timers}",fill="lightsteelblue",
            font="Helvetica 30 bold",width=0)
##########################################################################        
def drawButton(canvas,cx,cy,w,h,onClick,text,color)->None:
    """draw a Button with the given coordinate and size"""
    canvas.create_rectangle(cx-w/2, cy-h/2, cx+w/2, cy+h/2,
    fill=color,onClick=onClick,width=0)
    canvas.create_text(cx, cy, text=text, font="Helvetica 40 bold",fill="white")
def drawButton2(canvas,cx,cy,w,h,onClick,text,color)->None:
    """draw a Button with the given coordinate and size"""
    canvas.create_oval(cx-w/2, cy-h/2, cx+w/2, cy+h/2,
    fill=color,onClick=onClick,width=0)
    canvas.create_text(cx, cy, text=text, font="Helvetica 40 bold",fill="white")

class Board():
    def __init__(self,board,mode):
        """each food has x,y coordinate"""
        self.piecesMainBoard=[]
        self.pieces=[]#SideBar
        self.board=board
        self.mode=mode
        self.totalpage=self.mode.cols
        self.numPage=0
        self.piecesize=mode.piecesize

    def add(self,piece):
        self.pieces.append(piece)

    def shuffle(self):
        i=0
        random.shuffle(self.pieces)
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                self.pieces[i].y=100+row*self.piecesize
                self.pieces[i].x=50
                i+=1

    def flipForward(self):
        """flip one Page forward"""
        if self.numPage<self.totalpage - 1:
            self.numPage+=1
            return True
        if self.numPage==self.totalpage:
            return False

    def flipBackward(self):
        """flip one Page backward"""
        if self.numPage==0:
            return False
        else:
            self.numPage-=1
            return True

    def showSideBar(self,canvas):
        """renders the image of our piece""" 
        currenty=100
        for piece in self.pieces:
            if piece!="":
                piece.y=50
                piece.x=-100
        start=self.numPage*self.totalpage
        for i in range(start,start+self.totalpage):
            if self.pieces[i]=="":
                pass
            else:
                self.pieces[i].y=currenty
                self.pieces[i].x=50
                currenty+=self.piecesize
                self.pieces[i].render(canvas)
        for piece in self.pieces:
            if piece!="":
                if piece.isselected==True:
                    piece.dropShadow(canvas)
                    piece.render(canvas)
        if self.numPage!=self.totalpage-1: 
            drawButton2(canvas, 150, 950, 60, 60,self.flipForward,"⬇",self.mode.color3) 
        if self.numPage!=0:
            drawButton2(canvas, 150, 50, 60, 60,self.flipBackward,"⬆",self.mode.color3) 
        canvas.create_text(300, 950, text=f"Page {self.numPage+1}/{self.totalpage}", font="Helvetica 40 bold",fill="white")


    def showMainBoard(self,canvas):
        for piece in self.piecesMainBoard:
            piece.render(canvas)
            ############display in side bar according to page num

            #draw Sidebar horizontal lines
        for i in range(len(self.board)+1):
            x2=50
            y2=100+self.piecesize*i
            x3=50+self.piecesize
            y3=100+self.piecesize*i
            canvas.create_line(x2,y2,x3,y3,width=5,fill=self.mode.color1)
        for piece in self.piecesMainBoard:
            if piece.isselected==True:
                piece.dropShadow(canvas)
                piece.render(canvas)


class Piece():
    def __init__(self,image,dirs,pos,app):
        (self.x,self.y)=pos
        (self.row,self.col)=dirs
        self.app=app
        self.piecesize=self.app.piecesize
        self.image=image
        self.isselected=False
        self.neighbors=[]
        self.diff=(0,0)
        (self.finalc,self.finalr)=pos

        (self.rx,self.ry)=(self.x,self.y)


    def clicked(self):
        print("clicked")

    def getneighbours(self):
        self.neightbours=[]
        offsets=((-1,0),(1,0),(0,-1),(0,1))

    def drag(self,x,y):
        """drag to move a selected piece"""
        (diffx, diffy)=self.diff
        self.x=x+diffx
        self.y=y+diffy
    def display(self,canvas):
        x0,y0=self.x,self.y


    def render(self,canvas):
        #print("x,y",self.x,self.y)
        x0,y0=self.x,self.y
        x1=x0+self.piecesize
        y1=y0+self.piecesize
        canvas.create_rectangle(x0,y0,x1,y1,fill="white",
        outline="antiquewhite",onClick=self.clicked)
        canvas.create_image((x0+x1)//2,(y0+y1)//2,image=self.image)
        # canvas.create_rectangle(x0,y0,x1,y1,fill="cyan",
        # outline="antiquewhite",onClick=self.clicked)

    def dropShadow(self,canvas):
        margin=20
        a0,b0=self.x+margin,self.y+margin
        a1=a0+self.piecesize
        b1=b0+self.piecesize
        canvas.create_rectangle(a0,b0,a1,b1,fill="darkgrey",
        width=0)


class StartMode(Mode):
    def appStarted(self):
        self.color1=self.app.colorset[0]
        self.color2=self.app.colorset[1]
        self.color3=self.app.colorset[2]
        self.image=self.loadImage('B.png')
        self.imagesize=1500
        w,h=self.image.size
        scale=min(w,h)
        self.image=self.scaleImage(self.image,self.imagesize/scale)
        self.image=self.image.crop((0,0,1000,1000))
        self.imageW,self.imageH=self.image.size
    
    def modeActivated(self):
        self.appStarted()
        print("In Start Mode...")
    def onClick(self):
        self.app.setActiveMode("level")
    def onlick(self):
        self.app.setActiveMode("learn")
    def onick(self):
        self.app.setActiveMode("help")
    def onCck(self):
        self.app.setActiveMode("custom")
    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,1500,1000,fill=self.color1,width=0)
        canvas.create_image(750,500,image=ImageTk.PhotoImage(self.image))
        drawButton(canvas, 300, self.height-220, 230, 60, 
        self.onClick,"Free Mode",self.color3) 
        drawButton(canvas, 600, self.height-220, 230, 60, 
        self.onlick,"Learn Mode",self.color3) 
        drawButton(canvas, 900, self.height-220, 230, 60, 
        self.onick,"Help Mode",self.color3)
        drawButton(canvas, 1200, self.height-220, 230, 60, 
        self.onCck,"Customize",self.color3) 
        canvas.create_text(375,400,text="Square",fill="white",font="Helvetica 120 bold")
        canvas.create_text(435,520,text="Puzz",fill="white",font="Helvetica 120 bold")
        canvas.create_text(380,400,text="Square",fill="lightsteelblue2",font="Helvetica 120 bold")
        canvas.create_text(440,520,text="Puzz",fill="lightsteelblue2",font="Helvetica 120 bold")
        canvas.create_text(600,640,text="select a mode",fill="lightgrey",font="Helvetica 45 bold")
images=None
class LevelMode(Mode):
    def appStarted(self):
        self.color1=self.app.colorset[0]
        self.color2=self.app.colorset[1]
        self.color3=self.app.colorset[2]
        self.levels=[]
        self.generateLevel()
        self.text=""
    def modeActivated(self):
        self.appStarted()
        print("In Level Mode...")

    def generateLevel(self):
        self.levels=[]
        for f in os.listdir('.'):
            if f.endswith(".png"):
                image=self.loadImage(f)
                w,h=image.size
                scale=min(w,h)
                imagesize=800
                image=self.scaleImage(image,imagesize/scale)
                image=image.crop((0,0,800,800))
                imageW,imageH=image.size
                smol=self.scaleImage(image,300/imageW)
                images,imageh=smol.size
                self.levels.append((smol,images,f))
        return self.levels
    def onClick(self):
        self.app.setActiveMode("play")
    def onlick(self):
        self.app.setActiveMode("start")
    def keyPressed(self,event):
        if event.key=="e":
            self.text=self.getUserInput("Name your level:")
            self.app.text=self.text
    def mousePressed(self,event):
        global images
        image=None
        w=300
        h=300
        margin=300
        marginy=300
        i=(event.x-margin+w/2)/300
        if 300+marginy-h/2<=event.y<=300+marginy+h/2:
            i=int(i)+4
        i=int(i)
        images=self.levels[i][2]
        print(images)
        self.app.rowcol=6
  

    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,1500,1000,fill=self.color1,width=0)
        for i in range(len(self.levels)):
            w=300
            h=300
            margin=300
            marginy=300
            if i<2:
                canvas.create_rectangle(i*300+margin-w/2,marginy-h/2,i*300+margin+w/2,marginy+h/2,fill=self.color2)
                canvas.create_image(i*300+margin,marginy,image=ImageTk.PhotoImage(self.levels[i][0]))
                canvas.create_text(i*300+margin,marginy-h/2+20,text=f"level{i}",font="Helvetica 40 bold")
                
            if 2<=i<=3:
                canvas.create_rectangle(i*300+margin-w/2,marginy-h/2,i*300+margin+w/2,marginy+h/2,fill="white")
                canvas.create_image(i*300+margin,marginy,image=ImageTk.PhotoImage(self.levels[i][0]))
                canvas.create_text(i*300+margin,marginy-h/2+20,text=f"level{i}",font="Helvetica 40 bold")
            if i==4:
                n=i%4
                canvas.create_rectangle(n*300+margin-w/2,300+marginy-h/2,n*300+margin+w/2,300+marginy+h/2,fill="white")
                canvas.create_image(n*300+margin,300+marginy,image=ImageTk.PhotoImage(self.levels[i][0]))
                canvas.create_text(n*300+margin,marginy+h/2+50,text=f"level{i}",font="Helvetica 40 bold")
            if i>4:
                n=i%4
                canvas.create_rectangle(n*300+margin-w/2,300+marginy-h/2,n*300+margin+w/2,300+marginy+h/2,fill="white")
                canvas.create_image(n*300+margin,300+marginy,image=ImageTk.PhotoImage(self.levels[i][0]))
                canvas.create_text(n*300+margin,marginy+h/2+50,text=self.app.text,font="Helvetica 40 bold")
        drawButton(canvas, 300, self.height-130, 150, 60, 
        self.onlick,"Back",self.color3) 
        drawButton(canvas, 1300, self.height-130, 150, 60, 
        self.onClick,"Start",self.color3) 
        




from PIL import Image
from PIL import Image
class PlayMode(Mode):
    def appStarted(self):
        """take in a start board, initializes data"""
        global images
        self.color1=self.app.colorset[0]
        self.color2=self.app.colorset[1]
        self.color3=self.app.colorset[2]
        self.rows=self.cols=self.app.rowcol
        self.squaresize=800
        self.piecesize=int(self.squaresize/self.cols)
        self.square=([[0]*self.cols for row in range(self.rows)])
        self.hint=False

        self.doubleclick=None
        self.temp=None
        self.imagesize=self.squaresize
        self.image=self.loadImage(images)
        w,h=self.image.size
        scale=min(w,h)
        self.image=self.scaleImage(self.image,self.imagesize/scale)
        self.image=self.image.crop((0,0,self.squaresize,self.squaresize))
        self.imageW,self.imageH=self.image.size
        self.smol=self.scaleImage(self.image,300/scale)
        self.temploc=None

        self.pieces=self.createPiece()
        self.pieces.shuffle()

        self.pieceschain = [[]]


    def modeActivated(self):
        print("In Play Mode...")
        self.appStarted()
    def check(self):
        for piece in self.pieces.pieces:
            if piece!="":
                if 1100>=piece.x>=300 and 100<=piece.y<=900:
                    self.pieces.pieces.remove(piece)
                    self.pieces.pieces.append("")
                    self.pieces.piecesMainBoard.append(piece)
                    break

        for piece in self.pieces.piecesMainBoard:
            if piece.x<250:
                self.pieces.piecesMainBoard.remove(piece)
                self.pieces.pieces.append(piece)
                break
    def createPiece(self):
        pieces=Board(self.square,self)
        for row in range(self.rows):
            for col in range(self.cols):
                x0=col*self.piecesize
                y0=row*self.piecesize
                x1=x0+self.piecesize
                y1=y0+self.piecesize
                iImage=ImageTk.PhotoImage(self.image.crop((x0,y0,x1,y1)))
                piece=Piece(iImage,(row,col),(x0+300,y0+100),self)
                pieces.add(piece)
        return pieces
    def mouseDragged(self, event):
        #Move All Neib of selected piece
        for piece in self.pieces.piecesMainBoard:
            if piece.isselected:
                piece.drag(event.x,event.y)
                for chain in self.pieceschain:
                    if piece in chain:
                        for neighbor in chain:
                            if neighbor is not piece:
                                neighbor.drag(event.x, event.y)
            self.check()
        #Move selected piece
        for piece in self.pieces.pieces:
            if piece!="":
                if piece.isselected:
                    piece.drag(event.x,event.y)
                self.check()#Update Sidebar&
    
    def mousePressed(self, event):
        for piece in self.pieces.piecesMainBoard:
            if piece.isselected==True:
                return False
        for piece in self.pieces.pieces:
            if piece!="":
                if piece.isselected==True:
                    return False
        x,y=event.x,event.y
        for piece in self.pieces.piecesMainBoard:
            if piece.y<=y<=piece.y+self.piecesize and piece.x<=x<=piece.x+self.piecesize:
                self.temploc=(piece.x,piece.y)
                print('mousePressedTemp:', self.temploc)
                piece.isselected=True
                piece.diff=(piece.x-x,piece.y-y)
                for chain in self.pieceschain:
                    if piece in chain:
                        for neighbor in chain:
                            if neighbor is not piece:
                                neighbor.diff=(neighbor.x-x,neighbor.y-y)
                # for neighbor in piece.neighbors:
                #     neighbor.isSelected=True
                #     neighbor.diff=(neighbor.x-x,neighbor.y-y)
                break
        for piece in self.pieces.pieces:
            if piece!="":
                if piece.y<=y<=piece.y+self.piecesize and piece.x<=x<=piece.x+self.piecesize:
                    self.temploc=(piece.x,piece.y)
                    print('mousePressedTemp:', self.temploc)
                    piece.isselected=True
                    piece.diff=(piece.x-x,piece.y-y)
    
    def canBeNeib(self,piece,otherpiece):
        if otherpiece is piece:
            return False
        print("Looking for neighb")
        oneThird = piece.piecesize//3
        maxDist = piece.piecesize + oneThird
        minDist = piece.piecesize - oneThird
        if piece.col==otherpiece.col:
            if piece.row == otherpiece.row + 1:
                if minDist<=piece.y-otherpiece.y<=maxDist and abs(piece.x-otherpiece.x)<=oneThird:
                    oldx, oldy = piece.x, piece.y
                    piece.x=otherpiece.x
                    piece.y=otherpiece.y+piece.piecesize
                    self.alignNeibWithMerge(piece,oldx,oldy)
                    return True
            elif piece.row == otherpiece.row - 1:
                if minDist<=otherpiece.y-piece.y<=maxDist and abs(piece.x-otherpiece.x)<=oneThird:
                    oldx, oldy = piece.x, piece.y
                    piece.x=otherpiece.x
                    piece.y=otherpiece.y-piece.piecesize
                    self.alignNeibWithMerge(piece,oldx,oldy)
                    return True
        if piece.row==otherpiece.row:
            if piece.col == otherpiece.col + 1:
                if abs(piece.y-otherpiece.y)<=oneThird and minDist<=piece.x-otherpiece.x<=maxDist:
                    oldx, oldy = piece.x, piece.y
                    piece.x=otherpiece.x+piece.piecesize
                    piece.y=otherpiece.y
                    self.alignNeibWithMerge(piece,oldx,oldy)
                    return True
            elif piece.col == otherpiece.col - 1:
                if abs(piece.y-otherpiece.y)<=oneThird and minDist<=otherpiece.x-piece.x<=maxDist:
                    oldx, oldy = piece.x, piece.y
                    piece.x=otherpiece.x-piece.piecesize
                    piece.y=otherpiece.y
                    self.alignNeibWithMerge(piece,oldx,oldy)
                    return True
        return False

    def alignNeibWithMerge(self,piece,oldx,oldy):
        for chain in self.pieceschain:
            if piece in chain:
                for neighbor in chain:
                    if neighbor is not piece:
                        neighbor.x = neighbor.x + (piece.x - oldx)
                        neighbor.y = neighbor.y + (piece.y - oldy)

    def mouseReleased(self,event):
        print("Board==",self.pieces.piecesMainBoard)
        """release mouse to release the piece"""

        x,y=event.x,event.y
        if x<300:
            ##### Do nothing for now
            print("Not allowed to put pieces back to sidebar")
            return

        for piece in (self.pieces.piecesMainBoard + self.pieces.pieces):
            if piece!="":
                if piece.isselected:
                    piece.isselected=False

                    (diffx,diffy)=piece.diff
                    #diffx, diffy = x - piece.rx, y - piece.ry
                    (piece.rx,piece.ry)=(x,y)

                    thisChain = []
                    for chain in self.pieceschain:
                        if piece in chain:
                            thisChain = chain

                    ####### See if we can nail any pieces together
                    for otherpiece in self.pieces.piecesMainBoard:
                        for chainpiece in thisChain+[piece]:
                            if otherpiece not in thisChain and self.canBeNeib(chainpiece,otherpiece):
                                print("Found Neighb: ", otherpiece.x, " , ", otherpiece.y)

                                ###### Merge with neighbor chain
                                otherChain = []
                                for chain in self.pieceschain:
                                    if otherpiece in chain:
                                        otherChain = chain
                                print("thisChain is: ", thisChain)
                                print("otherChain is: ", otherChain)

                                if thisChain == [] and otherChain ==[]:
                                    self.pieceschain.append([piece, otherpiece])
                                elif thisChain == []:
                                    otherChain.append(piece)
                                elif otherChain == []:
                                    thisChain.append(otherpiece)
                                else:
                                    thisChain.extend(otherChain)
                                    self.pieceschain.remove(otherChain)
                    break
        self.check()

        # print("Board=",self.pieces.piecesMainBoard)
        # print("Side=",self.pieces.pieces)
        print("Chains=",len(self.pieceschain))
        # self.temploc=None


    def onClick(self):
        """When the Back button is clicked, set active mode
        to level mode"""
        self.app.setActiveMode("level")


    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,1500,1000,fill=self.color1,width=0)
        canvas.create_rectangle(50,100,50+self.piecesize,900,fill=self.color2,width=0)
        canvas.create_rectangle(300,100,1100,900,fill=self.color2,width=0)
        canvas.create_image(1300,150,image=ImageTk.PhotoImage(self.smol))

        self.pieces.showSideBar(canvas)
        self.pieces.showMainBoard(canvas)
        drawButton(canvas, 1300, self.height-130, 150, 60,
        self.onClick,"Back",self.color3)

class HelpMode(Mode):
    def appStarted(self):
        self.color1=self.app.colorset[0]
        self.color2=self.app.colorset[1]
        self.color3=self.app.colorset[2]
        self.image=self.loadImage('H.jpg')
        self.imagesize=800
        w,h=self.image.size
        scale=min(w,h)
        self.image=self.scaleImage(self.image,self.imagesize/scale)
        self.image=self.image.crop((0,0,800,800))
        self.imageW,self.imageH=self.image.size
    def Clicked(self):  
        self.app.setActiveMode("start")
    def modeActivated(self):
        print("In help Mode...")
        self.appStarted()
    def redrawAll(self,canvas):
        canvas.create_rectangle(0,0,1500,1000,fill=self.color1,width=0)
        canvas.create_image(750,500,image=ImageTk.PhotoImage(self.image))
        drawButton(canvas, 1300, self.height-130, 150, 60, 
        self.Clicked,"Back",self.color3) 

class CustomMode(Mode):
    def appStarted(self):
        self.color1=self.app.colorset[0]
        self.color2=self.app.colorset[1]
        self.color3=self.app.colorset[2]
    def modeActivated(self):
        print("In Background Mode...")
        self.appStarted()
    def onClick(self):
        self.app.colorset=("antiquewhite","snow3","skyblue2")
    def onClick1(self):
        self.app.colorset=("lightgrey","lightpink","burlywood3")
    def onClick2(self):
        self.app.colorset=("slategrey","snow3","darkslategrey")
    def onClick3(self):
        self.app.colorset=("lightcoral","snow3","darkcyan")
    def onClick4(self):
        self.app.colorset=("aquamarine","azure","darksalmon")
    def onClick5(self):
        self.app.colorset=("deepskyblue","snow3","cadetblue")
    def onClick6(self):
        self.app.colorset=("mistyrose","azure","darkseagreen")
    def onClick7(self):
        self.app.colorset=("chocolate","azure","burlywood")
    def Clicked(self):  
        self.app.setActiveMode("start")
    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,1500,1000,fill=self.color1,width=0)
        drawButton(canvas, 1300, self.height-130, 150, 60, 
        self.Clicked,"Back",self.color3) 
    
        canvas.create_rectangle(200,300,350,450,fill="antiquewhite",onClick=self.onClick,width=50, outline="skyblue2")

        canvas.create_rectangle(450,300,600,450,fill="lightgrey",onClick=self.onClick1,width=50,outline="burlywood3")

        canvas.create_rectangle(800,300,950,450,fill="slategrey",onClick=self.onClick2,width=50,outline="darkslategrey")

        canvas.create_rectangle(1050,300,1200,450,fill="lightcoral",onClick=self.onClick3,width=50,outline="darkcyan")

        canvas.create_rectangle(200,550,350,700,fill="aquamarine",onClick=self.onClick4,width=50,outline="darksalmon")

        canvas.create_rectangle(450,550,600,700,fill="deepskyblue",onClick=self.onClick5,width=50,outline="cadetblue")

        canvas.create_rectangle(800,550,950,700,fill="mistyrose",onClick=self.onClick6,width=50,outline="darkseagreen")

        canvas.create_rectangle(1050,550,1200,700,fill="chocolate",onClick=self.onClick7,width=50,outline="burlywood")
        canvas.create_text(705,150,text="Click to Choose Your Favorite Theme",font="Helvetica 50 bold",fill=self.color2)
        canvas.create_text(700,150,text="Click to Choose Your Favorite Theme",font="Helvetica 50 bold",fill=self.color3)


class SquarePal(ModalApp):
    def appStarted(self):
        """Add all three modes to the Agar Game,
        set inital mode to play mode"""
        self.addMode(PlayMode(name="play"))
        self.addMode(StartMode(name="start"))
        self.addMode(LevelMode(name="level"))
        self.addMode(LearnMode(name="learn"))
        self.addMode(CustomMode(name="custom"))
        self.addMode(HelpMode(name="help"))
        self.rowcol=6
        self.colorset=("antiquewhite","snow3","skyblue2")
        self.text=""

        self.setActiveMode("level")


    def getState(self):
        pass
SquarePal(width=1500,height=1000)