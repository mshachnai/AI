#MAZE RUNNER -- INTRO TO AI 198:520 -- Rutgers University


from tkinter import *
from tkinter import ttk
import random

#Function to generate maze
def maze_gen(dim, prob = 1):
    
    root = Tk()
    
    for r in range(dim): #width
        for c in range(dim): #height
            
            Prob = random.randint(1,10)
            if r == 0 and c == 0 :  
                button1 = Button(root, text = "S", relief = SOLID, borderwidth = 1, bg = "light blue", height = 1, width = 1 ).grid(row=r,column=c)

            elif r == dim-1 and c == dim-1 :  
                button2 = Button(root, text = "G", relief = SOLID, borderwidth = 1, bg = "light blue", width = 1 ).grid(row=r,column=c)

            elif Prob == 1:
                button3 = Button(root, relief = SOLID, borderwidth = 1, bg = "black", width = 1).grid(row=r,column=c)
                        
            else:
                button4 = Button(root, relief = SOLID, borderwidth = 1, bg = "white", width = 1).grid(row=r,column=c)


    root.mainloop()

    return;


dim = int(input("Enter dimension: "))
print(random.random())
maze_gen(dim)
