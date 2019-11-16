from copy import deepcopy
import learningtkinter as ltk
from time import time
from PIL import Image
L=[]
for i in range(9):
    l=[]
    L.append(l)
    for j in range(9):
        if i==j:
            l.append(1)
        else:
            l.append(0)

# for item in L:
#     # print(item)

L2= []
for state in L:
    # L2.append(state)
    for i in range(9):
        l=deepcopy(state)
        if state[i]!=1:
            l[i]=2
            L2.append(l)

# for index,item in enumerate(L2):
#     # print(item,'index',index+1)

root = ltk.Tk()
ex = ltk.Example()
root.geometry("400x250+300+300")
for ind,item in enumerate(L2):
    root.destroy()
    root = ltk.Tk()
    ex = ltk.Example()
    root.geometry("250x250+300+300")
    ex.getCanvas().update()
    for index,it in enumerate(item):
        if it == 1:
            ex.cross(index+1)
        elif it ==2:
            ex.circle(index+1)
    ex.getCanvas().postscript(file="/home/hodropetsos/Documents/Artificial-Intelligence/Project2/state"+str(ind+1)+".ps",colormode='color')
    img = Image.open("state"+str(ind+1)+'.ps')
    img.save("state"+str(ind+1)+'.png', 'png')
