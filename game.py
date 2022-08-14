from string import ascii_lowercase as letters
from curses.ascii import isupper
from tkinter import *
from PIL import ImageTk, Image

class pieces:
    movd=0
    def __init__(self,p):
        self.p = p
        if p=='':
            self.color=""
        elif isupper(p):
            self.color="w"
        else:
            self.color="b"
        if p=='p' or p=='P':
            self.piece= 'p'
        elif p=='b' or p=='B':
            self.piece='b'
        elif p=='r' or p=='R':
            self.piece='r'
        elif p=='n' or p=='N':
            self.piece='n'
        elif p=='q' or p=='Q':
            self.piece='q'
        elif p=='':
            self.piece=""
        else:
            self.piece='k'
    def getIm(self):
        if self.p=="":
            return ""
        return ("src/"+self.piece+self.color+".png")

class position:
    def __init__(self,file,rank):
        self.file=file
        self.rank=rank
        self.x=1
        self.y=4
        file=ord(file)-ord('a')
        self.x+=file*70
        rank=8-rank
        self.y+=rank*70

    def move(self,fmove,rmove):
        i=0
        file=self.file
        rank=self.rank
        while i<fmove:
            if(file!='h'):
                file=chr(ord(file)+1)
            i+=1
        i=0
        while i<rmove:
            if(rank!=8):
                rank+=1
            i+=1
        i=0
        while i>fmove:
            if(file!='a'):
                file=chr(ord(file)-1)
            i-=1
        i=0
        while i>rmove:
            if(rank!=1):
                rank-=1
            i-=1
        p=position(file,rank)
        return p
    def givepos(self):
        self.pos=self.file+str(self.rank)
        return self.pos

class game:
    def __init__(self):
        self.board={}
    def reset(self):
        self.turn='w'
        self.ht=0
        self.mc=0
        self.k=True
        self.K=True
        self.q=True
        self.Q=True
        self.enpable=""
        for i in range(8,0,-1):
            for j in letters[:8]:
                p=position(j,i)
                if i==7:
                    self.board[p.givepos()]=pieces("p")
                elif i==2:
                    self.board[p.givepos()]=pieces("P")
                elif i==1:
                    if j=='a' or j=='h':
                       self.board[p.givepos()]=pieces("R") 
                    elif j=='b' or j=='g':
                        self.board[p.givepos()]=pieces("N")
                    elif j=='c' or j=='f':
                        self.board[p.givepos()]=pieces("B")
                    elif j=='d':
                        self.board[p.givepos()]=pieces("Q")
                    else:
                        self.board[p.givepos()]=pieces("K")
                elif i==8:
                    if j=='a' or j=='h':
                       self.board[p.givepos()]=pieces("r") 
                    elif j=='b' or j=='g':
                        self.board[p.givepos()]=pieces("n")
                    elif j=='c' or j=='f':
                        self.board[p.givepos()]=pieces("b")
                    elif j=='d':
                        self.board[p.givepos()]=pieces("q")
                    else:
                        self.board[p.givepos()]=pieces("k")
                else:
                    self.board[p.givepos()]=pieces("")
    def toFn(self):
        self.fen=""
        c=0
        for i in range(8,0,-1):
            for j in letters[:8]:
                pos=position(j,i)
                p=self.board[pos.givepos()]
                if p.p=='':
                    c+=1
                elif c!=0:
                    self.fen+=str(c)
                    self.fen+=p.p
                    c=0
                else:
                    self.fen+=p.p
            if c>0:
                self.fen+=str(c)
                c=0
            if i!=1:
                self.fen+="/"
        self.fen+=" "
        self.fen+=self.turn
        self.fen+=" "
        if self.K:
            self.fen+="K"
        if self.Q:
            self.fen+="Q"
        if self.k:
            self.fen+="k"
        if self.q:
            self.fen+="q"
        self.fen+=" "
        if self.enpable!="":
            self.fen+=self.enpable
        else:
            self.fen+="-"
        self.fen+=" "
        self.fen+=str(self.ht)
        self.fen+=" "
        self.fen+=str(self.mc)        
    def fromfn(self,fen):
        self.fen=fen
        c=0
        for i in range(8,0,-1):
            for j in letters[:8]:
                if c==0:
                    piece=fen[0]
                    if piece>'0' and piece<'9':
                        c=int(piece)
                        pos=position(j,i)
                        p=pieces('')

                        c-=1
                    else:
                        pos=position(j,i)
                        p=pieces(piece)
                    self.board[pos.givepos()]=p
                    fen=fen[1:]
                else:
                    pos=position(j,i)
                    self.board[pos.givepos()]=pieces('')
                    c-=1
            fen=fen[1:]
        self.turn=fen[0]
        fen=fen[2:]
        while fen[0]!=' ':
            if fen[0]=='K':
                self.K=True
            elif fen[0]=='Q':
                self.Q=True
            elif fen[0]=='q':
                self.q=True
            elif fen[0]=='k':
                self.k=True
            fen=fen[1:]
        fen=fen[1:]
        if fen[0]!='-':
            self.enpable=fen[0:2]
            fen=fen[3:]
        else:
            self.enpable=""
            fen=fen[2:]
        self.ht=int(fen[0:fen.index(" ")])
        fen=fen[fen.index(" ")+1:]
        fp=fen.find(" ")
        if fp!=-1:
            fen=fen[:fp]
        self.mc=int(fen)