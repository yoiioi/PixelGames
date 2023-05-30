from tkinter import *
import time
import random

"""
Pixel class becomes a fundamental tools in creating and presenting pixels
"""

class Pixel:
    color=['black','white','yellow','red','blue','green','orange','purple','brown','cyan']
    
    def __init__(self,canvas,i,j,nrow,ncol,scale,c,vector=[0,0]):
        self.nrow=nrow
        self.ncol=ncol
        self.i=i%self.nrow      #ensure i within the valid range
        self.j=j%self.ncol      #ensure j within the valid range
        self.scale=scale
        self.c=c
        self.vector=vector
        
        x1=self.j*self.scale
        x2=(self.j+1)*self.scale
        y1=self.i*self.scale
        y2=(self.i+1)*self.scale

        self.canvas=canvas
        self.id=self.canvas.create_rectangle(x1,y1,x2,y2,fill=self.color[c])

    def __str__(self):
        return "(%s, %s) %s"%(self.i,self.j,self.color[self.c])
    
    def next(self):
        #update pixel position based on the current vector
        self.i+=self.vector[0]
        self.j+=self.vector[1]

        #check if the pixel has gone out of bounds and wrap around if needed
        if self.i<0:
            self.i=self.nrow-1
        elif self.i>=self.nrow:
            self.i=0
        if self.j<0:
            self.j=self.ncol-1
        elif self.j>=self.ncol:
            self.j=0
        
        #update the rectangle on the canvas to reflect the new position
        x1=self.j*self.scale
        x2=(self.j+1)*self.scale
        y1=self.i*self.scale
        y2=(self.i+1)*self.scale
        self.canvas.coords(self.id,x1,y1,x2,y2)

    def delete(self):
        self.canvas.delete(self.id)
        
    #functions for different block movements
    def right(self):
        self.vector=[0,1]
    def left(self):
        self.vector=[0,-1]
    def up(self):
        self.vector=[-1,0]
    def down(self):
        self.vector=[1,0]

#################################################################
########## TESTING FUNCTION
#################################################################
def delete_all(canvas):
    canvas.delete("all")
    print("Delete All")

def test1(canvas,nrow,ncol,scale):
    print("Generate 10 points at random")
    random.seed(4) # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1) 
        j=random.randint(0,ncol-1)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(pix)

def test2(canvas,nrow,ncol,scale):
    print("Generate 10 points at random (using modulo)")
    random.seed(5) # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1)*34
        j=random.randint(0,ncol-1)*13
        ij=str(i)+","+str(j)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(ij,"->",pix)

def test3(root,canvas,nrow,ncol,scale):
    print("Move one point along a square")

    pix=Pixel(canvas,35,35,nrow,ncol,scale,3)
    pix.vector=[-1,0]    # set up direction (up)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[0,-1]    # set up new direction (left)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[1,0]     # set up new direction (down)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[0,1]     # set up new direction (right)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)

    #delete point
    pix.delete()


  
def test4(root,canvas,nrow,ncol,scale):
    print("Move four point along a square")

    pixs=[]
    pixs.append(Pixel(canvas,35,35,nrow,ncol,scale,3,[-1,0]))
    pixs.append(Pixel(canvas,5,35,nrow,ncol,scale,4,[0,-1]))
    pixs.append(Pixel(canvas,5,5,nrow,ncol,scale,5,[1,0]))
    pixs.append(Pixel(canvas,35,5,nrow,ncol,scale,6,[0,1]))
    
    print("Starting coords")
    for p in pixs: print(p)

    for i in range(30):
        for p in pixs:
            p.next()       # next move in the simulation     
        root.update()      # update the graphic
        time.sleep(0.05)   # wait in second (simulation)

    print("Ending coords")
    for p in pixs:
        print(p)
        p.delete()


        
def test5(root,canvas,nrow,ncol,scale):
    print("Move one point any direction -use arrow commands")

    pix=Pixel(canvas,20,20,nrow,ncol,scale,2)

    ### binding used by test5
    root.bind("<Right>",lambda e:pix.right())
    root.bind("<Left>",lambda e:pix.left())
    root.bind("<Up>",lambda e:pix.up())
    root.bind("<Down>",lambda e:pix.down())

    ### simulation
    while True:
        pix.next()
        root.update()     # update the graphic
        time.sleep(0.05)  # wait in second (simulation)

###################################################
#################### Main method ##################
###################################################

def main():
       
        ##### create a window, canvas
        root = Tk() # instantiate a tkinter window
        nrow=40
        ncol=40
        scale=20
        canvas = Canvas(root,width=ncol*scale,height=nrow*scale,bg="black") # create a canvas width*height
        canvas.pack()

        ### general binding events to choose a testing function
        root.bind("1",lambda e:test1(canvas,nrow,ncol,scale))
        root.bind("2",lambda e:test2(canvas,nrow,ncol,scale))
        root.bind("3",lambda e:test3(root,canvas,nrow,ncol,scale))
        root.bind("4",lambda e:test4(root,canvas,nrow,ncol,scale))
        root.bind("5",lambda e:test5(root,canvas,nrow,ncol,scale))
        root.bind("<d>",lambda e:delete_all(canvas))
        
        
        root.mainloop() # wait until the window is closed
        
if __name__=="__main__":
    main()