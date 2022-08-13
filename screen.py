from tkinter import *
from PIL import ImageTk, Image
from string import ascii_lowercase as letters
from game import *
from time import sleep
root = Tk()
root.title('Chess')

bgim=PhotoImage(file="src/chess-board.png")
chess_board = Canvas(root,width=700,height=700)
chess_board.grid(row=0,column=0)
chess_board.create_image(0,5, image=bgim, anchor="nw")
possimg=PhotoImage(file="src/pmarker.png")
g=game()
g.reset()
img=[]
pie={}
possi=[]
castle=[]
enpassant=[]
def updateBoard():
    sleep(0.5)
    img.clear()
    pie.clear()
    a=0
    b=0
    c=0
    for i in range(8,0,-1):
        for j in letters[:8]:
            p=position(j,i)
            pc=g.board[p.givepos()]
            im=pc.getIm()
            if im=="":
                b+=1
                continue
            img.append(PhotoImage(file=im))
            pie[p.givepos()]=chess_board.create_image(p.x,p.y,image=img[c],anchor="nw")
            chess_board.tag_bind(pie[p.givepos()],'<Button-1>',click)
            c+=1
            b+=1
        a+=1
        b=0
def click(event):
    for c in castle:
        chess_board.delete(c)
    castle.clear()
    for a in possi:
        chess_board.delete(a)
    possi.clear()
    rank=8-int((event.y-4)/70)
    file=int((event.x-1)/70)
    file=chr(ord('a')+file)
    pos=position(file,rank)
    p=g.board[pos.givepos()]
    if(p.p=='' or p.color!=g.turn):
        pass
    else:
        if(p.piece=='p'):
            dispP(pos,p.color,p.movd)
        elif(p.piece=='r'):
            dispR(pos,p.color)
        elif(p.piece=='n'):
            dispN(pos,p.color)
        elif(p.piece=='b'):
            dispB(pos,p.color)
        elif(p.piece=='q'):
            dispQ(pos,p.color)
        else:
            dispK(pos,p.color)
def dispP(pos,color,movd):
    possibles=[]
    if color=='w':
        newpos=pos.move(0,1)
        p=g.board[newpos.givepos()]
        if(p.p==""):
            possibles.append(newpos)
            if movd==0:
                newpos=pos.move(0,2)
                p=g.board[newpos.givepos()]
                if p.p=="":
                    possibles.append(newpos)
        newpos=pos.move(1,1)
        p=g.board[newpos.givepos()]
        if(p.p!="" and p.color=='b' and newpos.file!=pos.file and newpos.rank!=pos.rank):
            possibles.append(newpos)
        newpos=pos.move(-1,1)
        p=g.board[newpos.givepos()]
        if(p.p!="" and p.color=='b' and newpos.file!=pos.file and newpos.rank!=pos.rank):
            possibles.append(newpos)
    else:
        newpos=pos.move(0,-1)
        p=g.board[newpos.givepos()]
        if(p.p==""):
            possibles.append(newpos)
            if movd==0:
                newpos=pos.move(0,-2)
                p=g.board[newpos.givepos()]
                if p.p=="":
                    possibles.append(newpos)
        newpos=pos.move(1,-1)
        p=g.board[newpos.givepos()]
        if(p.p!="" and p.color=='w' and newpos.file!=pos.file and newpos.rank!=pos.rank):
            possibles.append(newpos)
        newpos=pos.move(-1,-1)
        p=g.board[newpos.givepos()]
        if(p.p!="" and p.color=='w' and newpos.file!=pos.file and newpos.rank!=pos.rank):
            possibles.append(newpos)
    disp(possibles,pos)
    if len(enpassant)>0:
        if ord(pos.file)+1==ord(enpassant[0].file) or ord(pos.file)-1==ord(enpassant[0].file):
            if pos.rank==enpassant[0].rank:
                denp(pos)
def denp(pos):
    if enpassant[0].rank==5:
        goal=enpassant[0].move(0,1)
    else:
        goal=enpassant[0].move(0,-1)
    p=g.board[goal.givepos()]
    if p.p!='':
        return
    enpassant.append(chess_board.create_image(goal.x+10,goal.y+10,image=possimg,anchor='nw'))
    chess_board.tag_bind(enpassant[1],'<Button-1>',lambda event:enp(event,goal,pos))
def enp(event,goal,pos):
    p=g.board[pos.givepos()]
    g.board[pos.givepos()]=pieces('')
    g.board[enpassant[0].givepos()]=pieces('')
    g.board[goal.givepos()]=p
    enpassant.clear()
    g.enpable=""
def dispR(pos,color):
    possibles=[]
    newpos=pos.move(0,1)
    p=g.board[newpos.givepos()]
    prev=pos.rank
    #move up
    while(p.p=='' and newpos.rank!=prev):
        possibles.append(newpos)
        prev=newpos.rank
        newpos=newpos.move(0,1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='':
        possibles.append(newpos)
    #move down
    newpos=pos.move(0,-1)
    prev=pos.rank
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.rank!=prev):
        possibles.append(newpos)
        prev=newpos.rank
        newpos=newpos.move(0,-1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='':
        possibles.append(newpos)
    #move right
    newpos=pos.move(1,0)
    prev=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.file!=prev):
        possibles.append(newpos)
        prev=newpos.file
        newpos=newpos.move(1,0)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='':
        possibles.append(newpos)
    #move left
    newpos=pos.move(-1,0)
    prev=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.file!=prev):
        possibles.append(newpos)
        prev=pos.file
        newpos=newpos.move(-1,0)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='':
        possibles.append(newpos)
    disp(possibles,pos)
def dispN(pos,color):
    possibles=[]
    if pos.file!='h' and pos.rank<7:
        newpos=pos.move(1,2)
        p=g.board[newpos.givepos()]
        if p.color!=color:
            possibles.append(newpos)
    if pos.file!='h' and pos.rank>2:
        newpos=pos.move(1,-2)
        p=g.board[newpos.givepos()]
        if p.color!=color:
            possibles.append(newpos)
    if pos.file!='a' and pos.rank>2:
        newpos=pos.move(-1,-2)
        p=g.board[newpos.givepos()]
        if p.color!=color:
            possibles.append(newpos)
    if pos.file!='a' and pos.rank<7:
        newpos=pos.move(-1,2)
        p=g.board[newpos.givepos()]
        if p.color!=color:
            possibles.append(newpos)
    if pos.file<'g' and pos.rank!=1:
        newpos=pos.move(2,-1)
        p=g.board[newpos.givepos()]
        if p.color!=color:
            possibles.append(newpos)
    if pos.file<'g' and pos.rank!=8:
        newpos=pos.move(2,1)
        p=g.board[newpos.givepos()]
        if p.color!=color:
            possibles.append(newpos)
    if pos.file>'b' and pos.rank!=1:
        newpos=pos.move(-2,-1)
        p=g.board[newpos.givepos()]
        if p.color!=color:
            possibles.append(newpos)
    if pos.file>'b' and pos.rank!=8:
        newpos=pos.move(-2,1)
        p=g.board[newpos.givepos()]
        if p.color!=color:
            possibles.append(newpos)
    disp(possibles,pos)
def dispB(pos,color):
    possibles=[]
    newpos=pos.move(1,1)
    p=g.board[newpos.givepos()]
    prevr=pos.rank
    prevf=pos.file
    #upright
    while(p.p=='' and newpos.rank!=prevr and newpos.file!=prevf):
        possibles.append(newpos)
        prevr=newpos.rank
        prevf=newpos.file
        newpos=newpos.move(1,1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!=''and newpos.rank!=prevr and newpos.file!=prevf:
        possibles.append(newpos)
    #downrite
    newpos=pos.move(1,-1)
    prevr=pos.rank
    prevf=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.rank!=prevr and newpos.file!=prevf):
        possibles.append(newpos)
        prevr=newpos.rank
        prevf=newpos.file
        newpos=newpos.move(1,-1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!=''and newpos.rank!=prevr and newpos.file!=prevf:
        possibles.append(newpos)
    #upleft
    newpos=pos.move(-1,1)
    prevr=pos.rank
    prevf=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.rank!=prevr and newpos.file!=prevf):
        possibles.append(newpos)
        prevr=newpos.rank
        prevf=newpos.file
        newpos=newpos.move(-1,1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='' and newpos.rank!=prevr and newpos.file!=prevf:
        possibles.append(newpos)
    #downleft
    newpos=pos.move(-1,-1)
    prevr=pos.rank
    prevf=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.rank!=prevr and newpos.file!=prevf):
        possibles.append(newpos)
        prevr=newpos.rank
        prevf=newpos.file
        newpos=newpos.move(-1,-1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!=''and newpos.rank!=prevr and newpos.file!=prevf:
        possibles.append(newpos)
    disp(possibles,pos)
def dispQ(pos,color):
    possibles=[]
    newpos=pos.move(1,1)
    p=g.board[newpos.givepos()]
    prevr=pos.rank
    prevf=pos.file
    #upright
    while(p.p=='' and newpos.rank!=prevr and newpos.file!=prevf):
        possibles.append(newpos)
        prevr=newpos.rank
        prevf=newpos.file
        newpos=newpos.move(1,1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!=''and newpos.rank!=prevr and newpos.file!=prevf:
        possibles.append(newpos)
    #downrite
    newpos=pos.move(1,-1)
    prevr=pos.rank
    prevf=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.rank!=prevr and newpos.file!=prevf):
        possibles.append(newpos)
        prevr=newpos.rank
        prevf=newpos.file
        newpos=newpos.move(1,-1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!=''and newpos.rank!=prevr and newpos.file!=prevf:
        possibles.append(newpos)
    #upleft
    newpos=pos.move(-1,1)
    prevr=pos.rank
    prevf=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.rank!=prevr and newpos.file!=prevf):
        possibles.append(newpos)
        prevr=newpos.rank
        prevf=newpos.file
        newpos=newpos.move(-1,1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='' and newpos.rank!=prevr and newpos.file!=prevf:
        possibles.append(newpos)
    #downleft
    newpos=pos.move(-1,-1)
    prevr=pos.rank
    prevf=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.rank!=prevr and newpos.file!=prevf):
        possibles.append(newpos)
        prevr=newpos.rank
        prevf=newpos.file
        newpos=newpos.move(-1,-1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!=''and newpos.rank!=prevr and newpos.file!=prevf:
        possibles.append(newpos)
    newpos=pos.move(0,1)
    p=g.board[newpos.givepos()]
    prev=pos.rank
    
    #move up
    while(p.p=='' and newpos.rank!=prev):
        possibles.append(newpos)
        prev=newpos.rank
        newpos=newpos.move(0,1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='':
        possibles.append(newpos)
    #move down
    newpos=pos.move(0,-1)
    prev=pos.rank
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.rank!=prev):
        possibles.append(newpos)
        prev=newpos.rank
        newpos=newpos.move(0,-1)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='':
        possibles.append(newpos)
    #move right
    newpos=pos.move(1,0)
    prev=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.file!=prev):
        possibles.append(newpos)
        prev=newpos.file
        newpos=newpos.move(1,0)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='':
        possibles.append(newpos)
    #move left
    newpos=pos.move(-1,0)
    prev=pos.file
    p=g.board[newpos.givepos()]
    while(p.p=='' and newpos.file!=prev):
        possibles.append(newpos)
        prev=pos.file
        newpos=newpos.move(-1,0)
        p=g.board[newpos.givepos()]
    if p.color!=color and p.p!='':
        possibles.append(newpos)
    disp(possibles,pos)
def dispK(pos,color):
    b=True
    possibles=[]
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            newpos=pos.move(i,j)
            p=g.board[newpos.givepos()]
            if p.color!=color and pos.givepos()!=newpos.givepos():
                possibles.append(newpos)
    if color=='w':
        if g.K:
            newpos=pos.move(1,0)
            while(newpos.file!='h'):
                p=g.board[newpos.givepos()]
                if p.p!='':
                    b=False
                newpos=newpos.move(1,0)
            p=g.board[newpos.givepos()]
            if p.p!='R':
                b=False
            if b:
                newpos=newpos.move(-1,0)
                castle.append(chess_board.create_image(newpos.x+10,newpos.y+10,image=possimg,anchor='nw'))
        if g.Q:
            newpos=pos.move(-1,0)
            while(newpos.file!='a'):
                p=g.board[newpos.givepos()]
                if p.p!='':
                    b=False
                newpos=newpos.move(-1,0)
            p=g.board[newpos.givepos()]
            if p.p!='R':
                b=False
            if b:
                newpos=newpos.move(2,0)
                castle.append(chess_board.create_image(newpos.x+10,newpos.y+10,image=possimg,anchor='nw'))
    elif color=='b':
        if g.k:
            newpos=pos.move(1,0)
            while(newpos.file!='h'):
                p=g.board[newpos.givepos()]
                if p.p!='':
                    b=False
                newpos=newpos.move(1,0)
            p=g.board[newpos.givepos()]
            if p.p!='r':
                b=False
            if b:
                newpos=newpos.move(-1,0)
                castle.append(chess_board.create_image(newpos.x+10,newpos.y+10,image=possimg,anchor='nw'))
        if g.q:
            newpos=pos.move(-1,0)
            while(newpos.file!='a'):
                p=g.board[newpos.givepos()]
                if p.p!='':
                    b=False
                newpos=newpos.move(-1,0)
            p=g.board[newpos.givepos()]
            if p.p!='r':
                b=False
            if b:
                newpos=newpos.move(2,0)
                castle.append(chess_board.create_image(newpos.x+10,newpos.y+10,image=possimg,anchor='nw'))
    dispc(pos)     
    disp(possibles,pos)
def dispc(pos):
    for c in castle:
        chess_board.tag_bind(c,'<Button-1>',lambda event:castl(event,pos))
def castl(event,pos):
    enpassant.clear()
    g.enpable=""
    p=g.board[pos.givepos()]
    g.board[pos.givepos()]=pieces('')
    for c in castle:
        chess_board.delete(c)
    castle.clear()
    for a in possi:
        chess_board.delete(a)
    possi.clear()
    rank=8-int((event.y-4)/70)
    file=int((event.x-1)/70)
    file=chr(ord('a')+file)
    pos1=position(file,rank)
    p.movd+=1
    g.ht+=1
    g.board[pos1.givepos()]=p
    if file=='c':
        pos2=position('a',rank)
        p=g.board[pos2.givepos()]
        g.board[pos2.givepos()]=pieces('')
        pos3=position('d',rank)
        g.board[pos3.givepos()]=p
    elif file=='g':
        pos2=position('h',rank)
        p=g.board[pos2.givepos()]
        g.board[pos2.givepos()]=pieces('')
        pos3=position('f',rank)
        g.board[pos3.givepos()]=p
    if g.turn=='w':
        g.turn='b'
    else:
        g.turn='w'
        g.mc+=1
    if p.p=='k':
        g.k=False
        g.q=False
    elif p.p=='K':
        g.K=False
        g.Q=False
    updateBoard()
def disp(possibles,p):
    for pos in possibles:
        possi.append(chess_board.create_image(pos.x+10,pos.y+10,image=possimg,anchor="nw"))
    for pos in possi:
        chess_board.tag_bind(pos,'<Button-1>',lambda event:go(event,p))
def go(event,pos):
    enpassant.clear()
    g.enpable=""
    p=g.board[pos.givepos()]
    g.board[pos.givepos()]=pieces('')
    for a in possi:
        chess_board.delete(a)
    possi.clear()
    for c in castle:
        chess_board.delete(c)
    castle.clear()
    rank=8-int((event.y-4)/70)
    file=int((event.x-1)/70)
    file=chr(ord('a')+file)
    pos1=position(file,rank)
    if p.p=='p':
        if pos.rank-pos1.rank==2 or pos.rank-pos1.rank==-2:
            enpassant.append(pos1)
            g.enpable=pos1.givepos()
        g.ht=0
    p.movd+=1
    g.ht+=1
    p1=g.board[pos1.givepos()]
    if p1.p!=" ":
        g.ht=0
    g.board[pos1.givepos()]=p
    if g.turn=='w':
        g.turn='b'
    else:
        g.turn='w'
        g.mc+=1
    if p.p=='k':
        g.k=False
        g.q=False
    elif p.p=='K':
        g.K=False
        g.Q=False
    elif p.p=='r':
        if pos.file=='a':
            g.q=False
        elif pos.file=='h':
            g.k=False
    elif p.p=='R':
        if pos.file=='a':
            g.Q=False
        elif pos.file=='h':
            g.K=False
    if pos1.givepos()=="a1":
        g.Q=False
    if pos1.givepos()=="h1":
        g.K=False
    if pos1.givepos()=="a8":
        g.q=False
    if pos1.givepos()=="h8":
        g.K=False
    updateBoard()
updateBoard()

frame=Frame(root,width=300,height=700)
frame.grid(row=0,column=1)
Fen=Entry(frame,width=100)
Fen.pack()
def fen():
    g.toFn()
    Fen.delete(0,END)
    Fen.insert(0,g.fen)

fbutton=Button(frame,text="Convert To FEN",command=fen)
fbutton.pack()
root.mainloop()