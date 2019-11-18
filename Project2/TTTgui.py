from tkinter import *
root=Tk()
cv = Canvas(root)
cv.create_rectangle(10,10,50,50)
cv.pack()

cv.update()
cv.postscript(file='/home/hodropetsos/Documents/Artificial-Intelligence/Project2/file.ps')
# root.mainloop()
