from time import time
import pickle
import string
from random import choice
#hangman work
class Player(object):
    def __init__(self,pname):
        self.name=pname
        self.movie=''        
        self.done=[]
        self.tried=[]
        self.creationtime=time()
    
    def reset(self):
        self.movie=self.fetchmovie()
        self.tried=[]
        self.done=['-']
        self.lastaction=time()
    
    def fetchmovie(self):
        movlist=pickle.load(open("movielist.p","rb"))
        self.lastaction=time()
        return string.strip(string.lower(choice(movlist)))
    
    def getstat(self):
        self.lastaction=time()
        return 'name = '+self.name+' movie= '+self.movie+' tried list='+str(self.tried)+' done list='+str(self.done)
    
    def displaytext(self):
        self.lastaction=time()
        rs=''
        for i in range(len(self.movie)):
            if self.movie[i] in self.done : rs=rs+self.movie[i]
            else:
                if self.movie[i]==' ': rs=rs+'/'
                else: rs=rs+'__'+' '
        return rs



class Game(object):
    def __init__(self):
        self.playertable={}
    
    def register_player(self,newplayer):
        self.playertable[newplayer]=Player(newplayer)        
    
    def delete_player(self,playername):
        self.playertable.pop(playername,None)
        return 'Hangman session Ended!'
        
    def startgame(self,f):
        self.playertable[f].reset()
        return '\n************Game Started!***********\n'+self.playertable[f].displaytext()
    
    def gameresponse(self,q,f):
        q=q.replace(' ','')
        if q:
            if len(q)>1: q=q[0].lower()
            if q in self.playertable[f].movie:
                self.playertable[f].done.append(q)
                response='\n'+self.playertable[f].displaytext()+'\n'+'HANGMAN'[:len(self.playertable[f].tried)]
            else:
                if q in self.playertable[f].tried:
                    response='Already tried!\n'+self.playertable[f].displaytext()+'\n'+'HANGMAN'[:len(self.playertable[f].tried)]
                else: 
                    self.playertable[f].tried.append(q)
                    response='INCORRECT, Try Again!\n'+self.playertable[f].displaytext()+'\n'+'HANGMAN'[:len(self.playertable[f].tried)]
            if len(self.playertable[f].tried)==len('HANGMAN'):
                response='HANGMAN\n Game Over, You lost. The answer was '+self.playertable[f].movie+self.startgame(f)
                
            if '_' not in self.playertable[f].displaytext():
                response=self.playertable[f].movie+'\nVICTORY!!!!\n\n\n'+self.startgame(f)
                
        else: response='WTF?'
        return response
    
    def cleanup(self):
        for n in self.playertable:
            if (self.playertable[n].lastaction-self.playertable[n].creationtime)>(30*60):
                self.delete_player(n)        
