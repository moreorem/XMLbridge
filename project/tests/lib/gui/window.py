from tkinter import *

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.button1 = Button(self, text="Create new window", command=self.New_Window)
        self.button1.pack(fill=BOTH)

    def New_Window(self):
        win = Toplevel(self)
        win.title("New Window")
        etiquette1 = Label(root, text = "Text shenanigans")
        etiquette1.pack()
        

if __name__ == "__main__":
    root = Tk()
    main = Window(root)
    main.New_Window()
    main.mainloop()