#Import tkinter library
from tkinter import*

#Create an instance of frame
win= Tk()

#Set geometry
win.geometry("700x400")

#Create a text Label
Label(win, text="Notepad", font=('Poppins bold', 25)).pack(pady=20)
text= StringVar()

#Create an entry widget
test= Entry(win, textvariable=text)
test.pack(fill='x', expand=True, padx= 45, pady=45)
test.focus()

#Add a placeholder in the entry Widget
test.insert(0, "Enter any Text")
win.mainloop()