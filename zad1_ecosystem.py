import random as rn
import math
import matplotlib.pyplot as plt
import pygame
import time
import numpy as np
import sys
import os.path
from pygame.locals import *
import os

w_screen=800
h_screen=500
animal_size=6
screen=pygame.display.set_mode((w_screen, h_screen))

def normalny(mu=0,sig=4, ilosc=100):
    '''Funkcja zwraca liczbę z rozkładu normalnego'''
    w=[]
    if sig<=0:
        return 'Wartość argumentu sigma musi być większa od 0!!!'
    else:
        for i in range(ilosc):
            w.append(rn.normalvariate(mu,sig))
        return w

def wykładniczy(lam=1/70):
    '''Funkcja zwraca liczbę z rozkładu wykładniczego'''
    if lam<=0:
        return 'Argument musi byś większy od 0!!!'
    else:
        return -1/lam*math.log(rn.random())

def poisson(lam=5,T=2):
    I=0
    t=0
    time=[0]
    S=[0]
    while True:
        U=rn.random()
        t=t-(1/lam)*math.log(U)
        if t>T:
            return S
            break
        else:
            I=I+1
            S.insert(I,t)

def brown(sig,x=0,y=0,n=10,m=10,dryfx=0,dryfy=0):
    X=[x]
    Y=[y]
    Z=[]
    N=[]
    h=1/n
    for j in range(1,m):
        while True:
            Z.append(normalny(0,1,1))
            N.append(normalny(0,1,1))
            if 0<=(sig*(X[-1]+math.sqrt(h)*Z[-1][-1]))<=w_screen-animal_size and 0<=(sig*(Y[-1]+math.sqrt(h)*N[-1][-1]))<=h_screen-animal_size:
                X.append((sig*(X[-1]+math.sqrt(h)*Z[-1][-1])+dryfx))
                Y.append((sig*(Y[-1]+math.sqrt(h)*N[-1][-1])+dryfy))
                break
            else:
                if 0<=(sig*(X[-1]+math.sqrt(h)*Z[-1][-1])+2*(np.sign(X[-1]-(sig*(X[-1]+math.sqrt(h)*Z[-1][-1])))))<=w_screen-animal_size and 0<=(sig*(Y[-1]+math.sqrt(h)*N[-1][-1])+2*(np.sign(Y[-1]-(sig*(Y[-1]+math.sqrt(h)*N[-1][-1])))))<=h_screen-animal_size:
                    X.append(sig*(X[-1]+math.sqrt(h)*Z[-1][-1])+2*(np.sign(X[-1]-(sig*(X[-1]+math.sqrt(h)*Z[-1][-1])))))
                    Y.append(sig*(Y[-1]+math.sqrt(h)*N[-1][-1])+2*(np.sign(Y[-1]-(sig*(Y[-1]+math.sqrt(h)*N[-1][-1])))))
                    break
        return X,Y 

def ro(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


#####################
#
#PARDWA SAMIEC
#
#####################

class pardwa_male():
    """Tworzenie samca pardwy"""
    def __init__(self):
        self.x=rn.randint(0,w_screen-10)
        self.y=rn.randint(0,h_screen-10)
        self.pardwamimage = pygame.Surface((animal_size, animal_size))
        self.pardwamimage.fill((0, 0, 255))
        self.L=wykładniczy()
        self.dryfy=0
        self.dryfx=0
        self.time=time.time()
        self.timec=0

    def adult(self):
        if time.time()-self.time>=15: return True
        else: return False

    def move(self,sig=1):
        position=brown(sig,x=self.x,y=self.y,n=10,m=2,dryfx=self.dryfx,dryfy=self.dryfy)
        self.x=position[0][1]
        self.y=position[1][1]
        screen.blit(self.pardwamimage, (self.x,self.y))

    def femalepardwa(self,P): 
        if self.adult()==True and P.adult()==True and P.c==False:
            if 150>ro(self.x,self.y,P.x,P.y)>5:
                self.dryfx=self.dryfx+1.5*(np.sign(-self.x-P.x))
                self.dryfy=self.dryfy+1.5*(np.sign(-self.y-P.y))
            elif 5>=ro(self.x,self.y,P.x,P.y):
                self.dryfx=0.4*(np.sign(self.x-P.x))
                self.dryfy=0.4*(np.sign(self.y-P.y))
                if self.timec==0:
                    self.timec = time.time()
        if self.time!=0 and time.time()-self.timec>1:
            self.dryfx=0
            self.dryfy=0
            self.timec=0
                

    def malepardwa(self,P):
        for z in P:
            if 0<ro(self.x,self.y,z.x,z.y)<=150:
                self.dryfx=self.dryfx+(-3/ro(self.x,self.y,z.x,z.y))*(-np.sign(self.x-z.x))
                self.dryfy=self.dryfy+(-3/ro(self.x,self.y,z.x,z.y))*(-np.sign(self.y-z.y))

    def ucieczka(self,W):
        for z in W:
            if 20<=ro(self.x,self.y,z.x,z.y)<=150:
                self.dryfx=self.dryfx+0.1*(np.sign(self.x-z.x))
                self.dryfy=self.dryfy+0.1*(np.sign(self.y-z.y))

    def kill(self,P,Pm):
        for z in P:
            if ro(self.x,self.y,z.x,z.y)<20:
                self.L=0
                if self in Pm:
                    Pm.remove(self)
           
 
########################
#
# PARDWA SAMICA
#
########################

class pardwa_female():
    """Tworzenie samicy pardwy"""
    def __init__(self):
        self.x=rn.randint(0,w_screen-10)
        self.y=rn.randint(0,h_screen-10)
        self.pardwamimage = pygame.Surface((animal_size, animal_size))
        self.pardwamimage.fill((255, 0, 0))
        self.L=wykładniczy()
        self.time=time.time()
        self.dryfy=0
        self.dryfx=0
        self.timec=0
        self.jajko=0
        self.c=False

    def adult(self):
        if time.time()-self.time>=15: return True
        else: return False

    def male(self,P):
        if self.adult()==True and P.adult()==True and self.c==False:
            if 40>ro(self.x,self.y,P.x,P.y)>5:
                self.dryfx=self.dryfx+5*(np.sign(-self.x-P.x))
                self.dryfy=self.dryfy+5*(np.sign(-self.y-P.y))
            elif 5>=ro(self.x,self.y,P.x,P.y):
                self.dryfx=self.dryfx-13*(np.sign(-self.x-P.x))
                self.dryfy=self.dryfy-13*(np.sign(-self.y-P.y))
                if self.timec==0:
                    self.timec = time.time()
                    self.timec2 = time.time()
                    self.c=True
                    self.jajko=len(poisson(lam=6,T=1))
        if time.time()-self.timec>5:
            self.dryfx=0
            self.dryfy=0            

    def move(self):
        position=brown(sig=1,x=self.x,y=self.y,n=10,m=2)
        self.x=position[0][1]
        self.y=position[1][1]
        screen.blit(self.pardwamimage, (self.x,self.y))

    def kill(self,P,Pf):
        for z in P:
            if ro(self.x,self.y,z.x,z.y)<15:
                self.L=0
                if self in Pf:
                    Pf.remove(self)

    def baby_pardwa(self,Pm,Pf):
        if self.jajko==0:
            if time.time()-self.timec>16:
                self.c=False
                self.timec=0
        if self.jajko>0:
            if time.time()-self.timec>11:
                self.jajko=self.jajko-1
                U=rn.random()
                if U<0.5:
                    a=pardwa_male()
                    Pm.append(a)
                    a.x=self.x
                    a.y=self.y
                    pygame.init()
                    screen.blit(a.pardwamimage, (a.x,a.y))
                else:
                    a=pardwa_female()
                    Pf.append(a)
                    a.x=self.x
                    a.y=self.y
                    pygame.init()
                    screen.blit(a.pardwamimage, (a.x,a.y))

    def ucieczka(self,W):
        for z in W:
            if 20<=ro(self.x,self.y,z.x,z.y)<=150:
                self.dryfx=self.dryfx+0.9*(np.sign(self.x-z.x))
                self.dryfy=self.dryfy+0.9*(np.sign(self.y-z.y))

#####################
#
# WILK SAMICA
#
#####################

class wolf_female():
    """Tworzenie samicy wilka"""
    def __init__(self):
        self.x=rn.randint(0,w_screen-10)
        self.y=rn.randint(0,h_screen-10)
        self.pardwamimage = pygame.Surface((animal_size, animal_size))
        self.pardwamimage.fill((255, 255, 255))
        self.L=wykładniczy(1/200)
        self.dryfy=0
        self.dryfx=0
        self.time=time.clock()
        self.timec=0
        self.baby=1
        selfc=0
        self.c=False

    def adult(self): 
        if self.time-time.time()>=30: return True
        else: return False

    def move(self):
        position=brown(sig=1,x=self.x,y=self.y,n=10,m=2)
        self.x=position[0][1]
        self.y=position[1][1]
        screen.blit(self.pardwamimage, (self.x,self.y))

    def polowanie(self,P):
        for z in P:
            if ro(self.x,self.y,z.x,z.y)<=70 and z.L!=0:
                self.dryfx=self.dryfx+(-np.sign(self.x-z.x))*(1+min(0.3,3/(ro(self.x,self.y,z.x,z.y))**2))
                self.dryfy=self.dryfy+(-np.sign(self.y-z.y))*(1+min(0.3,3/(ro(self.x,self.y,z.x,z.y))**2))

    def samiec(self,P):
        if self.adult()==True and P.adult()==True and self.c==False:
            if 180>ro(self.x,self.y,P.x,P.y)>5:
                self.dryfx=self.dryfx+5*(np.sign(-self.x-P.x))
                self.dryfy=self.dryfy+5*(np.sign(-self.y-P.y))
            elif 5>=ro(self.x,self.y,P.x,P.y):
                self.dryfx=self.dryfx-13*(np.sign(-self.x-P.x))
                self.dryfy=self.dryfy-13*(np.sign(-self.y-P.y))
                if self.timec==0:
                    self.timec = time.time()
                    self.c=True
                    self.baby=len(poisson(lam=2,T=1))
                    print(self.baby)
        if time.time()-self.timec>8:
            self.dryfx=0
            self.dryfy=0

    def baby_wilczek(self,Wm,Wf):
        if self.baby==0:
            if time.time()-self.timec>21:
                self.c=False
                self.timec=0
        if self.baby>0:
            if time.time()-self.timec>18:
                self.baby=self.baby-1
                U=rn.random()
                if U<0.5:
                    a=wolf_male()
                    Wm.append(a)
                    a.x=self.x
                    a.y=self.y
                    pygame.init()
                    screen.blit(a.pardwamimage, (a.x,a.y))
                else:
                    a=wolf_female()
                    Wf.append(a)
                    a.x=self.x
                    a.y=self.y
                    pygame.init()
                    screen.blit(a.pardwamimage, (a.x,a.y))

#######################
#
#WILK SAMIEC
#
#######################

class wolf_male():
    """Tworzenie samca wilka"""
    def __init__(self):
        U=rn.random()
        if U<=0.05:
            colour=(250, 250, 0)
            self.alpha=1
        else:
            colour=(0, 0, 0)
            self.alpha=0
        self.x=rn.randint(0,w_screen-10)
        self.y=rn.randint(0,h_screen-10)
        self.pardwamimage = pygame.Surface((animal_size, animal_size))
        self.pardwamimage.fill(colour)
        self.L=wykładniczy(1/200)
        self.dryfx=0
        self.dryfy=0
        self.timec=0
        self.time=time.clock()

    def adult(self): 
        if self.time-time.time()>=30: return True
        else: return False

    def move(self):
        position=brown(sig=1,x=self.x,y=self.y,n=10,m=2,dryfx=self.dryfx,dryfy=self.dryfy)
        self.x=position[0][1]
        self.y=position[1][1]
        screen.blit(self.pardwamimage, (self.x,self.y))

    def wolf_male(self,P):
        for z in P:
            if 25<=ro(self.x,self.y,z.x,z.y)<=70 and z.alpha==0 and self.alpha==0 and self.adult==True:
                self.dryfx=self.dryfx+0.1*(-np.sign(self.x-z.x))*(ro(self.x,self.y,z.x,z.y)-0.1)
                self.dryfy=self.dryfy+0.1*(-np.sign(self.y-z.y))*(ro(self.x,self.y,z.x,z.y)-0.1)
            elif 25<=ro(self.x,self.y,z.x,z.y)<=70 and z.alpha==1 and self.alpha==0 and self.adult==True:
                self.dryfx=self.dryfx+0.15*(-np.sign(self.x-z.x))
                self.dryfy=self.dryfy+0.15*(-np.sign(self.y-z.y))
            elif 25<=ro(self.x,self.y,z.x,z.y)<=70 and z.alpha==1 and self.alpha==1 and self.adult==True:
                self.dryfx=self.dryfx+(np.sign(self.x-z.x))
                self.dryfy=self.dryfy+(np.sign(self.y-z.y))

    def wolf_female(self,P):
        if self.adult()==True and P.adult()==True and P.c==False:
            if 250>ro(self.x,self.y,P.x,P.y)>5:
                self.dryfx=self.dryfx+7.5*(-np.sign(self.x-P.x))
                self.dryfy=self.dryfy+7.5*(-np.sign(self.y-P.x))
            elif 5>=ro(self.x,self.y,P.x,P.y):
                self.dryfx=self.dryfx-3*(-np.sign(self.x-P.x))
                self.dryfy=self.dryfy-3*(-np.sign(self.y-P.y))
                if self.timec==0:
                    self.timec = time.time()
        if time.time()-self.timec>8:
            self.dryfx=0
            self.dryfy=0
            
    def polowanie(self,P):
        for z in P:
            if ro(self.x,self.y,z.x,z.y)<=70 and z.L!=0:
                self.dryfx=self.dryfx+(-np.sign(self.x-z.x))*0.1
                self.dryfy=self.dryfy+(-np.sign(self.y-z.y))*0.1


####################
#
#SYMULACJA
#
####################

Pf=[]
Pm=[]
Wf=[]
Wm=[]

ilosc_wilkow=21
ilosc_wilczyc=19
ilosc_pardw_male=40
ilosc_pardw_female=45

for i in range(ilosc_wilkow):
    Wm.append(wolf_male())

for i in range(ilosc_wilczyc):
    Wf.append(wolf_female())

for i in range(ilosc_pardw_male):
    Pm.append(pardwa_male())

for i in range(ilosc_pardw_female):
    Pf.append(pardwa_female())
    
pygame.init()
pygame.display.set_caption('Forest')
clock = pygame.time.Clock()
f = pygame.font.SysFont('Arial', 15)
screen.fill((0, 255, 0))

for i in Pf:
    screen.blit(i.pardwamimage, (i.x,i.y))
for i in Pm:
    screen.blit(i.pardwamimage, (i.x,i.y))
for i in Wf:
    screen.blit(i.pardwamimage, (i.x,i.y))
for i in Wm:
    screen.blit(i.pardwamimage, (i.x,i.y))
    
pygame.display.flip()
clock.tick(7)

while True:

    screen.fill((0, 255, 0))
    
    for i in Pm:
        i.dryfx=0
        i.dryfy=0
        if time.clock()<i.time+i.L:
            for y in Pf:
                i.femalepardwa(P=y)
            i.malepardwa(P=Pm)
            i.ucieczka(W=Wm)
            i.ucieczka(W=Wf)
            i.kill(P=Wm,Pm=Pm)
            i.kill(P=Wf,Pm=Pm)
            if i.L!=0:
                i.move()
                                
    for i in Pf:
        i.dryfx=0
        i.dryfy=0
        if time.clock()<i.time+i.L:
            i.baby_pardwa(Pm=Pm,Pf=Pf)
            for k in Pm:
                i.male(P=k)
            i.ucieczka(W=Wm)
            i.ucieczka(W=Wf)
            i.kill(P=Wm,Pf=Pf)
            i.kill(P=Wf,Pf=Pf)
            if i.L!=0:
                i.move()
            
    for i in Wm:
        i.dryfx=0
        i.dryfy=0
        if time.clock()>i.time+i.L:
            Wm.remove(i)
        if time.clock()<i.time+i.L:
            for w in Wf:
                i.wolf_female(P=w)
            i.polowanie(P=Pf)
            i.polowanie(P=Pm)
            i.wolf_male(P=Wm)
            i.move()
            
    for i in Wf:
        i.dryfx=0
        i.dryfy=0
        if time.clock()>i.time+i.L:
            Wf.remove(i)
        if time.clock()<i.time+i.L:
            for w in Wm:
                i.samiec(P=w)
            i.polowanie(P=Pm)
            i.polowanie(P=Pf)
            i.baby_wilczek(Wm=Wm,Wf=Wf)
            i.move()

#LICZNIKI ZWIERZĄT
    t=f.render("Pardwy samce: " + str(len(Pm)), True, (0, 0, 0));
    screen.blit(t, (10, 10));
    c=f.render("Pardwy samice: " + str(len(Pf)), True, (0, 0, 0));
    screen.blit(c, (10, 27));
    c1=f.render("Wilki: " + str(len(Wm)), True, (0, 0, 0));
    screen.blit(c1, (10, 44));
    c2=f.render("Wilczyce: " + str(len(Wf)), True, (0, 0, 0));
    screen.blit(c2, (10, 61));
    
    pygame.display.flip()
    pygame.display.update()
