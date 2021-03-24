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