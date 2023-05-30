from tkinter import *
from Grid import Grid
from Tetrominoes import Tetrominoes
import numpy as np
import time

"""
Class tetris is actual runs the actual tetris game, 
using grid class, tetrominoes, and pixel class.
"""

class Tetris(Grid):  #Class Tetris inheriting from Grid
    def __init__(self,root,nrow,ncol,scale):
            super().__init__(root,nrow,ncol,scale)
            self.block=None   
            self.__game_over=False
            self.__paused=False

    #function to handle the next movement of the active block
    def next(self):
        #checks if there is an active block. If not, create one
        if self.block == None:          #instantiate block as new tetromino when no block is active
            self.block=Tetrominoes.random_select(self.canvas,self.nrow,self.ncol,self.scale)
            self.block.activate()       #activating block with new (i,j) coordinates
        
        self.block.down() #move the block downwards
        newi=self.block.i
        newj=self.block.j

        #if the block has reached the bottom or is overlapping with other blocks
        if (newi+1+self.block.h>self.nrow) or (self.is_overlapping(newi+1,newj)==True):
            current_pattern=self.block.pattern_list[self.block.current] #get current pattern from tetrominoes
            self.block.delete()
            #add the block to the grid
            for row in range(current_pattern.shape[0]):                 #iterates over the rows of the current pattern
                for col in range(current_pattern.shape[1]):
                    if current_pattern[row,col]>0:
                        self.addij(row+newi,col+newj,current_pattern[row,col])
            self.block=None        #set the active block to None as it's now part of the grid

        #check if a row is filled
        counter=0 #initialization
        for row in range(self.nrow):
            for col in range(self.ncol):
                if self.matrix[row,col]>0:
                    counter+=1
            if counter==self.ncol:      #if a row is filled
                self.flush_row(row)     #remove the row
            else:
                counter=0

        #check if the game is over (if any block has reached the top of the grid)
        for row in range(3):
            if np.any(self.matrix[row,:]>0):
                self.__game_over=True #set game over to True
                print("Game over!")
                #display a "game over" message on the screen
                self.canvas.create_text(self.ncol*self.scale//2,self.nrow*self.scale//2,text="***GAME OVER***",fill="orange",font=("deafult",25))

    #functions for different block movements
    def up(self):
        self.block.rotate()
    def down(self):
        self.next()
    def left(self):
        #if the block can move to the left without overlapping or going out of bounds, move it to the left
        if self.block and self.block.j>0 and not self.is_overlapping(self.block.i,self.block.j-1):
            self.block.left()
    def right(self):
        #if the block can move to the right without overlapping or going out of bounds, move it to the right
        if self.block and self.block.j+self.block.w<self.ncol and not self.is_overlapping(self.block.i,self.block.j+1):
            self.block.right()

    #check if the block is overlapping with another block
    def is_overlapping(self, ii, jj):
        if self.block is None:
            return False
        current_pattern=self.block.pattern_list[self.block.current]
        for row in range(self.block.h):
            for col in range(self.block.w):
                if self.matrix[ii+row,jj+col]>0 and current_pattern[row,col]>0:
                    return True

    #getter for private variable game_over and paused
    def is_game_over(self):
        return self.__game_over
    def is_pause(self):
        return self.__paused
    
    #function to pause the game
    def pause(self):
        self.__paused = not self.__paused
        return self.__paused

#########################################################
############# Main code #################################
#########################################################
    
def main():
    ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        game=Tetris(root,36,12,25) 
        
        ####### Tkinter binding mouse actions
        root.bind("<Up>",lambda e:game.up())
        root.bind("<Left>",lambda e:game.left())
        root.bind("<Right>",lambda e:game.right())
        root.bind("<Down>",lambda e:game.down())
        root.bind("<p>",lambda e:game.pause())        

        while True:
            if not game.is_pause(): game.next()
            root.update()   # update the graphic
            time.sleep(0.2)  # wait few second (simulation)
            if game.is_game_over(): break
        
        root.mainloop() # wait until the window is closed


if __name__=="__main__":
    main()

