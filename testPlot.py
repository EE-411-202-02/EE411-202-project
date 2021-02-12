import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from tkinter import *

root = Tk()
l0 = Label(root, text="Hello world!").grid(row=0, column=0)
l0 = Label(root, text="DEEZ NUTZ!").grid(row=1, column=0)

root.mainloop()


#t = np.linspace(0, 8 * np.pi, 200)
#s = np.cos(t)

#plt.figure(1)
#plt.plot(t, s)
#plt.show()
