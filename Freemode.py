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
