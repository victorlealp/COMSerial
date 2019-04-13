from tkinter import *
def Cumprimente():
    hello.set("Olá, você!")

janela = Tk()
janela.title("E.B Master")
btn = Button(janela,text="Precione",command=Cumprimente)
btn.pack()
hello = StringVar()
lbl = Label(janela, textvariable=hello)
lbl.pack()

janela.geometry("800x680+350+100")
janela.mainloop()
