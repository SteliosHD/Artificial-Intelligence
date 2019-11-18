from tkinter import *
import math
from PIL import Image

class Example(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.initUI()

    def initUI(self):
        self.master.title("Tic-Tac-Toe")
        self.pack(fill=BOTH, expand=1)
        squaresize = 50
        _color = '#3c5b97'
        _width = 3
        square = squaresize+_width
        self.canvas = Canvas(self)

        #horizontal.
        x1a,y1a,x1b,y1b=50,100,206,100
        self.canvas.create_line(x1a,y1a,x1b,y1b,fill=_color,width=_width)
        self.canvas.create_line(x1a,y1a+square,x1b,y1b+square,fill=_color,width=_width)


        #vertical
        x2a,y2a,x2b,y2b=100,50,100,206
        self.canvas.create_line(x2a,y2a,x2b,y2b,fill=_color,width=_width)
        self.canvas.create_line(x2a+square,y2a,x2b+square,y2b,fill=_color,width=_width)


        self.canvas.pack(fill=BOTH, expand=1)

    def circle(self,place):
        r = math.sqrt(450)
        x,y = self.getCenterCoordinates(place)
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r
        self.canvas.create_oval(x0,y0,x1,y1,width=3)

    def cross(self,place):
        x,y = self.getCenterCoordinates(place)
        x0 = x-15
        y0 = y+15
        x1 = x+15
        y1 = y-15
        x2 = x-15
        y2 = y-15
        x3 = x+15
        y3 = y+15
        self.canvas.create_line(x0,y0,x1,y1,fill='red',width=3)
        self.canvas.create_line(x2,y2,x3,y3,fill='red',width=3)

    @staticmethod
    def getCenterCoordinates(place):
        if place==1:
            return 75,75
        elif place ==2:
            return 126.5,75
        elif place ==3:
            return 181,75
        elif place ==4:
            return 75,126.5
        elif place ==5:
            return 126.5,126.5
        elif place ==6:
            return 181,126.5
        elif place ==7:
            return 75,181
        elif place ==8:
            return 126.5,181
        elif place ==9:
            return 181,181

    def getCanvas(self):
        return self.canvas

def main():
    root=Tk()
    ex = Example()
    # for i in range(1,10):
    #     ex.cross(i)
    #     ex.circle(i)
    ex.circle(2)
    ex.cross(4)
    root.geometry("400x250+300+300")

    ex.getCanvas().update()
    ex.getCanvas().postscript(file="/home/hodropetsos/Documents/Artificial-Intelligence/Project2/file.ps",colormode='color')

    root.mainloop()

if __name__ == '__main__':
    main()
