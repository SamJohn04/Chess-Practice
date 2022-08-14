from asyncio.windows_events import NULL
from tkinter import *
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

def check(color):
    possible=[]
    for i in range(8,0,-1):
        for j in letters[:8]:
            p=position(j,i)
            pc=g.board[p.givepos()]
            if pc.piece=='k' and pc.color==color:
                pos=p
    for i in range(8,0,-1):
        for j in letters[:8]:
            p=position(j,i)
            pc=g.board[p.givepos()]
            if pc.color!=color and pc.p!="":
                if pc.piece=='p':
                    possible.extend(dispP(p,pc.color,pc.movd,False))
                if pc.piece=='r':
                    possible.extend(dispR(p,pc.color,False))
                if pc.piece=='n':
                    possible.extend(dispN(p,pc.color,False))
                if pc.piece=='b':
                    possible.extend(dispB(p,pc.color,False))
                if pc.piece=='q':
                    possible.extend(dispQ(p,pc.color,False))
    for po in possible:
        if po.givepos()==pos.givepos():
            return True
    return False
def click(event):
    for c in castle:
        chess_board.delete(c)
    castle.clear()
    for a in possi:
        chess_board.delete(a)
    possi.clear()
    for e in enpassant:
        chess_board.delete(e)
    enpassant.clear()
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
def dispP(pos,color,movd,show=True):
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
    if show:
        disp(possibles,pos)
        if g.enpable!="":
            if color=='w':
                pos10=pos.move(1,1)
                pos11=pos.move(-1,1)
                if pos10.givepos()==g.enpable:
                    denp(pos,pos10)
                if pos11.givepos()==g.enpable:
                    denp(pos,pos11)
            else:
                pos10=pos.move(1,-1)
                pos11=pos.move(-1,-1)
                if pos10.givepos()==g.enpable:
                    denp(pos,pos10)
                if pos11.givepos()==g.enpable:
                    denp(pos,pos11)
    return possibles
def denp(pos,goal):
    p=g.board[goal.givepos()]
    if p.p!='':
        return
    enpassant.append(chess_board.create_image(goal.x+10,goal.y+10,image=possimg,anchor='nw'))
    chess_board.tag_bind(enpassant[0],'<Button-1>',lambda event:enp(event,goal,pos))
def enp(event,goal,pos):
    pos1=position(goal.file,pos.rank)
    g.board[pos1.givepos()]=pieces('')
    go(event,pos)
def dispR(pos,color,show=True):
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
    if show:
        disp(possibles,pos)
    return possibles
def dispN(pos,color,show=True):
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
    if show:
        disp(possibles,pos)
    return possibles
def dispB(pos,color,show=True):
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
    if show:
        disp(possibles,pos)
    return possibles
def dispQ(pos,color,show=True):
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
    if show:
        disp(possibles,pos)
    return possibles
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
    if check(g.turn):
        checkMessage()
        return
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
def checkMessage():
    lmsg=Label(frame,text="Your King!!?!")
    lmsg.pack()
    lmsg.after(1000,lmsg.destroy)
def go(event,pos):
    rank=8-int((event.y-4)/70)
    file=int((event.x-1)/70)
    file=chr(ord('a')+file)
    p=g.board[pos.givepos()]
    g.board[pos.givepos()]=pieces('')
    pos1=position(file,rank)
    p1=g.board[pos1.givepos()]
    g.board[pos1.givepos()]=p
    if check(g.turn):
        checkMessage()
        g.board[pos.givepos()]=p
        g.board[pos1.givepos()]=p1
        for a in possi:
            chess_board.delete(a)
        possi.clear()
        for c in castle:
            chess_board.delete(c)
        castle.clear()
        for e in enpassant:
            chess_board.delete(e)
        enpassant.clear()
        return
    for e in enpassant:
        chess_board.delete(e)
    enpassant.clear()
    g.enpable=""
    for a in possi:
        chess_board.delete(a)
    possi.clear()
    for c in castle:
        chess_board.delete(c)
    castle.clear()
    if p.piece=='p':
        if pos.rank-pos1.rank==2:
            pos2=pos1.move(0,1)
            g.enpable=pos2.givepos()
        if pos.rank-pos1.rank==-2:
            pos2=pos1.move(0,-1)
            g.enpable=pos2.givepos()
        g.ht=0
    p.movd+=1
    g.ht+=1
    if p1.p!="":
        g.ht=0
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