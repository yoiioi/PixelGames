from tkinter import *
from Pixel import Pixel
import numpy as np
import random, time

"""
Grid class creates a black pixels on the gray background to show pixels.
When it is clicked, it turns white, and when it is right-clicked, it delects
the cell or the line.
"""

class Grid:

        def __init__(self,root,nrow,ncol,scale):
                self.root=root
                self.nrow=nrow
                self.ncol=ncol
                self.scale=scale
                self.matrix=np.zeros((nrow,ncol),dtype=int) #initialize grid with all empty cells
                self.pixels=[] #list to keep track of existing pixels
                
                #create a canvas and pack it
                self.canvas=Canvas(self.root,width=self.ncol*self.scale, height=self.nrow*self.scale, bg="black") # create a canvas width*height
                self.canvas.pack()
                
                #plot the entire grid using gray color
                for i in range(nrow):
                        for j in range(ncol):
                                x1 = j*scale
                                y1 = i*scale
                                x2 = x1+scale
                                y2 = y1+scale
                                self.canvas.create_rectangle(x1,y1,x2,y2,outline="grey")
                                
        def addij(self,i,j,c):
                if c>0:
                       
                        pix=Pixel(self.canvas,i,j,self.nrow,self.ncol,self.scale,c)
                        self.pixels.append(pix) #appending the pixel information to the list of pixels
                        self.matrix[i,j]=c

        def random_pixels(self,num_sq,c):
                for k in range(num_sq):
                        i=random.randint(0,self.nrow-1) #setting random i value
                        j=random.randint(0,self.ncol-1) #setting random j value
                        self.addij(i,j,c)
        
        def addxy(self,x,y):
                #convert x,y coordinates to i,j cell coordinates
                i=y//self.scale
                j=x//self.scale
                cell_color=self.matrix[i,j] #get the current color of the cell

                print("insert",x,y,i,j,cell_color) #display information

                #add a pixel at i,j if the cell is black
                if cell_color==0:
                        self.addij(i,j,1)
                
        def delxy(self,x,y):
                #convert x,y coordinates to i,j cell coordinates
                i=y//self.scale
                j=x//self.scale
                print("delete",x,y,j,i,self.matrix[i,j]) #display information
                self.delij(i,j)
        
        def delij(self,i,j):
                #check if the pixel is not black
                if self.matrix[i,j]!=0:
                        self.matrix[i,j]=0 #update matrix element to zero
                        
                        self.reset() #reset the grid with non-black pixels
                        #linear scan through all the matrix
                        for x in range(len(self.matrix)):
                                for y in range(len(self.matrix[x])):
                                        self.addij(x,y,self.matrix[x,y])
                                           
                else:
                        self.flush_row(i)   

        def reset(self):
                #delete everything
                for pix in self.pixels:
                        pix.delete()
                self.pixels=[]
                i=0
                for x in self.matrix:
                        j=0
                        for y in self.matrix[i]:
                                if self.matrix[i,j]!=0:
                                        self.addij(i,j,y)
                                j=j+1
                        i=i+1
                
       
        def flush_row(self, i):
                #create the purple pixels
                purple_pixels=[]

                for j in range (3):
                        pixel_left=Pixel(self.canvas,i,j,self.nrow,self.ncol,self.scale,7,[0,1])
                        pixel_right=Pixel(self.canvas,i,self.ncol-j-1,self.nrow,self.ncol,self.scale,7,[0,-1])
                        purple_pixels.append(pixel_left) 
                        purple_pixels.append(pixel_right)

                #animate the pixels
                for n in range(int(self.ncol/2)):
                        for pix in purple_pixels:
                                pix.next()
                        self.canvas.update()
                        time.sleep(0.01)
                #delete purple pixels        
                for pix in purple_pixels:
                        pix.delete()      

                #shift the matrix down
                self.matrix[1:i+1,:]=self.matrix[0:i,:]
                self.matrix[0,:]=0
                self.reset()

                #linear scan through all the matrix and redraw the pixels
                for x in range(len(self.matrix)):
                        for y in range(len(self.matrix[x])):
                                if self.matrix[x,y]!=0:
                                        self.addij(x,y,1)

#########################################################
############# Main code #################################
#########################################################

  
def main(): 
        
        ##### create a window, canvas 
        root = Tk()                # instantiate a tkinter window
        mesh = Grid(root,50,30,20) # instantiate a Grid object
        mesh.random_pixels(25,1) # generate 25 random (white) pixels in the Grid

        
        ####### Tkinter binding mouse actions
        root.bind("<Button-1>",lambda e:mesh.addxy(e.x,e.y))
        root.bind("<Button-2>",lambda e:mesh.delxy(e.x,e.y))
        root.bind("<Button-3>",lambda e:mesh.delxy(e.x,e.y))
        
        

        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
        main()

