from tkinter import *
from Pixel import Pixel
import time, random
import numpy as np

"""
Tetrominoes class is the tool to create tetris game, which designs a block
and baic operations that makes it move around.
"""

class Tetrominoes:

    ## to complete
    def __init__(self,canvas,nrow,ncol,scale,c=2,pattern_list=None,name="Custom"):
        self.canvas=canvas
        self.nrow=nrow
        self.ncol=ncol
        self.scale=scale
        self.c=c
        if pattern_list==None:
            pattern_list=[np.array([[2,2,2],[2,0,2],[2,2,2]])]
            name="Basic"
        self.pattern_list=pattern_list
        self.name=name
        self.nbpattern=int(len(pattern_list)) #number of pattern given by length of list
        self.h,self.w=pattern_list[0].shape #shape function returns hight and width of matrix
        self.current=0 #current counter

    def get_pattern(self):
        return self.pattern_list[self.current] #current counter give pattern in pattern list

    def activate(self,i=None,j=None): #making i j input opitonal
        if i==None or j==None: #setting initial value of i and j
            i=0
            j=random.randint(0,self.ncol-self.w) #giving random j coordinates
        self.i=i #create new attribute of i and j
        self.j=j
        self.big_pixels=[] #create new attribute of list of big pixels
        pattern=self.get_pattern() #extract pattern
        for a in range(self.h): #linear search thorugh matrix and display
            for b in range(self.w):
                if pattern[a,b]!=0: #when it is not black
                    color=pattern[a, b] #excract color profile
                    pixel=Pixel(self.canvas,int(i+a),int(j+b),self.nrow,self.ncol,self.scale,color)

                    self.big_pixels.append(pixel) # to list of big pixels

    def rotate(self):
        self.delete() #delete the original pixels
        del self.big_pixels[:] #delete from pixel tracker as well
        self.current=(self.current+1)%self.nbpattern #modulo number of patterns, so that it creates a loop
        self.activate(self.i,self.j) #display the grid

    def delete(self):
        for pixel in self.big_pixels:
            pixel.delete()       #delete pixels in the list of pixels

    #moving methods
    def left(self):
        for pixel in self.big_pixels:
            pixel.left()        #execute for each pixels
            pixel.delete()      #delete the old pixels
        self.j=(self.j-1)%self.ncol #modulo for loop
        self.activate(self.i,self.j) #display pixels with new ijvar
    def right(self):
        for pixel in self.big_pixels:
            pixel.right()
            pixel.delete()
        self.j=(self.j+1)%self.ncol
        self.activate(self.i,self.j)
    def up(self):
        for pixel in self.big_pixels:
            pixel.up()
            pixel.delete()
        self.i=(self.i-1)%self.nrow
        self.activate(self.i,self.j)
    def down(self):
        for pixel in self.big_pixels:
            pixel.down()
            pixel.delete()
        self.i=(self.i+1)%self.nrow
        self.activate(self.i,self.j)


    @staticmethod
    def random_select(canv,nrow,ncol,scale):
        t1=TShape(canv,nrow,ncol,scale)
        t2=TripodA(canv,nrow,ncol,scale)
        t3=TripodB(canv,nrow,ncol,scale)
        t4=SnakeA(canv,nrow,ncol,scale)
        t5=SnakeB(canv,nrow,ncol,scale)
        t6=Cube(canv,nrow,ncol,scale)
        t7=Pencil(canv,nrow,ncol,scale)        
        return random.choice([t1,t2,t3,t4,t5,t6,t7,t7]) #a bit more change to obtain a pencil shape
        


#########################################################
############# All Child Classes #########################
#########################################################



    ## to complete
class TShape(Tetrominoes):
    def __init__(self,canv,nrow,ncol,scale):
        self.pattern_list=[np.array([[0,3,0],[0,3,0],[3,3,3]]),
                           np.array([[3,0,0],[3,3,3],[3,0,0]]),
                           np.array([[3,3,3],[0,3,0],[0,3,0]]),
                           np.array([[0,0,3],[3,3,3],[0,0,3]])]
        super().__init__(canv,nrow,ncol,scale,c=3,pattern_list=self.pattern_list,name="TShape")

class TripodA(Tetrominoes):
    def __init__(self, canv, nrow, ncol, scale):
        self.pattern_list=[np.array([[0,4,0],[0,4,0],[4,0,4]]),
                           np.array([[4,0,0],[0,4,4],[4,0,0]]),
                           np.array([[4,0,4],[0,4,0],[0,4,0]]),
                           np.array([[0,0,4],[4,4,0],[0,0,4]])]
        super().__init__(canv,nrow,ncol,scale,c=4,pattern_list=self.pattern_list,name="TripodA")

class TripodB(Tetrominoes):
    def __init__(self,canv,nrow,ncol,scale):
        self.pattern_list=[np.array([[0,5,0],[5,0,5],[5,0,5]]),
                           np.array([[5,5,0],[0,0,5],[5,5,0]]),
                           np.array([[5,0,5],[5,0,5],[0,5,0]]),
                           np.array([[0,5,5],[5,0,0],[0,5,5]])]
        super().__init__(canv,nrow,ncol,scale,c=5,pattern_list=self.pattern_list,name="TripodB")

class SnakeA(Tetrominoes):
    def __init__(self,canv,nrow,ncol,scale):
        self.pattern_list=[np.array([[6,6,0],[0,6,0],[0,6,6]]),
                           np.array([[0,0,6],[6,6,6],[6,0,0]])]
        super().__init__(canv,nrow,ncol,scale,c=6,pattern_list=self.pattern_list,name="SnakeA")

class SnakeB(Tetrominoes):
    def __init__(self,canv,nrow,ncol,scale):
        self.pattern_list=[np.array([[0,7,7],[0,7,0],[7,7,0]]),
                           np.array([[7,0,0],[7,7,7],[0,0,7]])]
        super().__init__(canv,nrow,ncol,scale,c=7,pattern_list=self.pattern_list,name="SnakeB")

class Cube(Tetrominoes):
    def __init__(self,canv,nrow,ncol,scale):
        self.pattern_list=[np.full((3,3),8),
                           np.array([[0,8,0],[8,8,8],[0,8,0]]),
                           np.array([[8,0,8],[0,8,0],[8,0,8]])]
        super().__init__(canv,nrow,ncol,scale,c=8,pattern_list=self.pattern_list,name="Cube")

class Pencil(Tetrominoes):
    def __init__(self,canv,nrow,ncol,scale):
        self.pattern_list=[np.array([[9,0,0],[9,0,0],[9,0,0]]),
                           np.array([[0,0,0],[0,0,0],[9,9,9]]),
                           np.array([[0,0,9],[0,0,9],[0,0,9]]),
                           np.array([[0,0,0],[0,0,0],[9,9,9]])]
        super().__init__(canv,nrow,ncol,scale,c=9,pattern_list=self.pattern_list,name="Pencil")





#########################################################
############# Testing Functions #########################
#########################################################
def delete_all(canvas):
    canvas.delete("all")
    print("Delete All")


def test1(canvas,nrow,ncol,scale):
    print("Generate a Tetromino (basic shape)- different options")
    
    tetro1=Tetrominoes(canvas,nrow,ncol,scale) # instantiate
    print("Tetro1",tetro1.name)
    print("  number of patterns:",tetro1.nbpattern)
    print("  current pattern:\n",tetro1.get_pattern()) # retrieve current pattern
    print("  height/width:",tetro1.h,tetro1.w)
    tetro1.activate(nrow//2,ncol//2)        # activate and put in the middle
    print("  i/j coords:  ",tetro1.i,tetro1.j)

    pattern=np.array([[0,3,0],[3,3,3],[0,3,0],[3,0,3],[3,0,3]]) # matrix motif
    tetro2=Tetrominoes(canvas,nrow,ncol,scale,3,[pattern]) # instantiate (list of patterns-- 1 item here)
    print("\nTetro2",tetro2.name)
    print("  number of patterns:",tetro2.nbpattern)
    print("  current pattern:\n",tetro2.get_pattern()) # retrieve current pattern
    print("  height/width:",tetro2.h,tetro2.w)
    tetro2.activate()        # activate and place at random at the top
    print("  i/j coords:  ",tetro2.i,tetro2.j)

    
    
def test2(root,canvas,nrow,ncol,scale):
    print("Generate a 'square' Tetromino (with double shape) and rotate")
    
    print("My Tetro")
    pattern1=np.array([[4,0,0],[0,4,0],[0,0,4]]) # matrix motif
    pattern2=np.array([[0,0,4],[0,4,0],[4,0,0]]) # matrix motif
    tetro=Tetrominoes(canvas,nrow,ncol,scale,4,[pattern1,pattern2]) # instantiate (list of patterns-- 2 items here)
    print("  number of patterns:",tetro.nbpattern)
    print("  height/width:",tetro.h,tetro.w)
    tetro.activate(nrow//2,ncol//2)        # activate and place in the middle
    print("  i/j coords:  ",tetro.i,tetro.j)

    for k in range(10): # make 10 rotations
        tetro.rotate() # rotate (change pattern)
        print("  current pattern:\n",tetro.get_pattern()) # retrieve current pattern
        root.update()
        time.sleep(0.5)
    tetro.delete() # delete tetro (delete every pixels)


def rotate_all(tetros): #auxiliary routine
    for t in tetros:
        t.rotate()
    
       
def test3(root,canvas,nrow,ncol,scale):
    print("Dancing Tetrominoes")

    t0=Tetrominoes(canvas,nrow,ncol,scale)
    t1=TShape(canvas,nrow,ncol,scale)
    t2=TripodA(canvas,nrow,ncol,scale)
    t3=TripodB(canvas,nrow,ncol,scale)
    t4=SnakeA(canvas,nrow,ncol,scale)
    t5=SnakeB(canvas,nrow,ncol,scale)
    t6=Cube(canvas,nrow,ncol,scale)
    t7=Pencil(canvas,nrow,ncol,scale)
    tetros=[t0,t1,t2,t3,t4,t5,t6,t7]

    for t in tetros:
        print(t.name)

    # place the tetrominos
    for i in range(4):
        for j in range(2):
            k=i*2+j
            tetros[k].activate(5+i*10,8+j*10)
            
    ####### Tkinter binding for this test
    root.bind("<space>",lambda e:rotate_all(tetros))     

    
      
def test4(root,canvas,nrow,ncol,scale):
    print("Moving Tetromino")
    tetro=Tetrominoes.random_select(canvas,nrow,ncol,scale) # choose at random
    print(tetro.name)
        
    ####### Tkinter binding for this test
    root.bind("<space>",lambda e:tetro.rotate())
    root.bind("<Up>",lambda e:tetro.up())
    root.bind("<Down>",lambda e:tetro.down())
    root.bind("<Left>",lambda e:tetro.left())
    root.bind("<Right>",lambda e:tetro.right())

    tetro.activate()

    

#########################################################
############# Main code #################################
#########################################################

def main():
    
        ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        nrow=45
        ncol=30
        scale=20
        canvas = Canvas(root,width=ncol*scale,height=nrow*scale,bg="black") # create a canvas width*height
        canvas.pack()

        ### general binding events to choose a testing function
        root.bind("1",lambda e:test1(canvas,nrow,ncol,scale))
        root.bind("2",lambda e:test2(root,canvas,nrow,ncol,scale))
        root.bind("3",lambda e:test3(root,canvas,nrow,ncol,scale))
        root.bind("4",lambda e:test4(root,canvas,nrow,ncol,scale))
        root.bind("<d>",lambda e:delete_all(canvas))

        
        root.mainloop() # wait until the window is closed        

if __name__=="__main__":
    main()

