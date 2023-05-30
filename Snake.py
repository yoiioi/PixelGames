from tkinter import *
from Grid import Grid
from Pixel import Pixel
import time
"""
SNAKE CLASS, is a child class of grid. using Piel and Grid class, it generates
a snake game."""
class Snake(Grid):
    def __init__(self,root,n_obstacle,n_fruit,nrow=50,ncol=30,scale=20):
        super().__init__(root,nrow,ncol,scale)

        self.root=root
        self.n_obstacle=n_obstacle
        self.n_fruit=n_fruit
        self.random_pixels(n_obstacle,1)
        self.random_pixels(n_fruit,3)
        self.__gameover=False
        self.__pause=False
        
        #list storing pixels for snake
        self.snake_list=[]
        for num in range(3):
            self.snake_list.append(Pixel(self.canvas,nrow//2,self.ncol//2+num,self.nrow,self.ncol,self.scale,5,[0,1]))
        self.snake_list.append(Pixel(self.canvas,nrow//2,self.ncol//2+3,self.nrow,self.ncol,self.scale,4,[0,1]))
        
    def left(self):
        head=self.snake_list[-1]
        #can only turn left if not going left or right
        if head.vector!=[0,1] or head.vector!=[0,-1]:
            head.vector=[0,-1]
            """for pix in self.snake_list:
                pix.vector=head.vector #set direction"""
            self.matrix[head.i,head.j]=-1

    def right(self):
        head=self.snake_list[-1]
        #can only turn right if not going left or right
        if head.vector!=[0,-1] or head.vector!=[0,1]:
            head.vector=[0,1]
            """for pix in self.snake_list:
                pix.vector=head.vector #set direction"""
            self.matrix[head.i,head.j]=-2  
   
    def up(self):
        head=self.snake_list[-1]
        #can only turn up if not going up or down
        if head.vector!=[-1,0] or head.vector!=[1,0]:
            head.vector=[-1,0]
            """for pix in self.snake_list:
                pix.vector=head.vector #set direction"""
            self.matrix[head.i,head.j]=-3

    def down(self):
        head=self.snake_list[-1]
        if head.vector!=[-1,0] or head.vector!=[1,0]:
            head.vector=[1,0]
            """for pix in self.snake_list:
                pix.vector=head.vector #set direction"""
            self.matrix[head.i,head.j]=-4
            
    def next(self):
        snake_store=[]
        for pix in range (len(self.snake_list)-1,-1,-1):
            snake_store.append(self.snake_list[pix])
        head=self.snake_list[-1]
        for pix in snake_store:                       #moves from head pixel
            if self.matrix[pix.i,pix.j]==-1:          #check if matrix is going left
                if head.vector!=[0,1] or head.vector!=[0,-1]:
                    pix.left()
                    if pix == self.snake_list[0]:       #check if pixel is the last pixel of snake
                        self.matrix[pix.i,pix.j]=0      #set matrix as 0 when every pixel is moved
                    
            elif self.matrix[pix.i,pix.j]==-2:          #check if matrix is going right
                if head.vector!=[0,1] or head.vector!=[0,-1]:
                    pix.right()
                    if pix == self.snake_list[0]:       #check if pixel is the last pixel of snake
                        self.matrix[pix.i,pix.j]=0      #set matrix as 0 when every pixel is moved
                    
            elif self.matrix[pix.i,pix.j]==-3:          #check if matrix is going right
                if head.vector!=[-1,0] or head.vector!=[1,0]:
                    pix.up()
                    if pix == self.snake_list[0]:       #check if pixel is the last pixel of snake
                        self.matrix[pix.i,pix.j]=0      #set matrix as 0 when every pixel is moved
                    
            elif self.matrix[pix.i,pix.j]==-4:          #check if matrix is going right
                if head.vector!=[-1,0] or head.vector!=[1,0]:
                    pix.down()
                    if pix == self.snake_list[0]:       #check if pixel is the last pixel of snake
                        self.matrix[pix.i,pix.j]=0      #set matrix as 0 when every pixel is moved
                    
        for x in snake_store:
            x.next()

        #check if the head of the snake has hit a fruit
        head_i,head_j=self.snake_list[-1].i,self.snake_list[-1].j
        dir_last=self.snake_list[0].vector

        #if the head has hit the fruit
        if self.matrix[head_i,head_j]==3:           
            self.snake_list.insert(0,Pixel(self.canvas,self.snake_list[0].i-self.snake_list[0].vector[0], self.snake_list[0].j-self.snake_list[0].vector[1],self.nrow,self.ncol,self.scale,5,dir_last)) #add pixel at the end of the snake_list
            self.delij(head_i,head_j)
            self.n_fruit+=-1

        #game over cases
        if self.matrix[head_i,head_j]==1 or self.n_fruit==0 :         #if the head has hit the obstacle
            if self.matrix[head_i,head_j]==1:
                self.canvas.create_text(self.ncol//2*self.scale,self.nrow//2*self.scale,fill="white",font="Times 40 italic bold",
                                        text="GAME OVER",width=0)
                self.__gameover=True
            elif self.n_fruit==0:
                self.canvas.create_text(self.ncol//2*self.scale,self.nrow//2*self.scale,fill="white",font="Times 40 italic bold",
                                        text="GAME OVER",width=0)
                self.__gameover=False

    def is_game_over(self):
        return self.__gameover
    
    def pause(self):
        self.__pause= not self.__pause

    def is_pause(self):
        return self.__pause

#########################################################
############# Main code #################################
#########################################################

def main(): 
        
        ##### create a window, canvas 
        root = Tk()                     # instantiate a tkinter window
        python = Snake(root,20,20)      #20 obstacles, and 20 fruits
        #python = Snake(root,5,5,25,25,30) # 5 obstacles/fruits, 25 row, 25 column, 30 scale
        
        
        ####### Tkinter binding mouse actions
        root.bind("<Right>",lambda e:python.right())
        root.bind("<Left>",lambda e:python.left())
        root.bind("<Up>",lambda e:python.up())
        root.bind("<Down>",lambda e:python.down())
        root.bind("<p>",lambda e:python.pause())
       
        while True:
            if not python.is_pause(): python.next()
            root.update()
            time.sleep(0.5)  # wait few second (simulation)
            if python.is_game_over(): break
        
        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
    main()

