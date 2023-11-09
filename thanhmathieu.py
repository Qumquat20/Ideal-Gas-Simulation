from tkinter import *
from random import choice, randint
import math

root = Tk()

particules = {}
compteur = 0
def ajouter_particule():
    global compteur, particules
    x_position = randint(10,largeur_fenetre-10)
    y_position = randint(10,hauteur_fenetre-10)
    couleurs = ['magenta','black','red','blue','green','cyan','purple','yellow','orange']
    particule = canvas.create_oval(x_position-5, y_position-5, x_position+5, y_position+5, fill=choice(couleurs))

    vitesses = [str(randint(-10,10)),str(randint(-10,10))]
    v = '/'.join(vitesses)

    particules[particule]= v

def mouvement():
    for p in particules:
        xy = particules.get(p).split('/')
        x = int(xy[0])
        y = int(xy[1])

        canvas.move(p,x,y)

        if canvas.coords(p)[3] > hauteur_fenetre or canvas.coords(p)[1] < 0:
            y = -1 * y
        if canvas.coords(p)[2] > largeur_fenetre or canvas.coords(p)[0] < 0:
            x = -1 * x
        
        xy[0]=str(x)
        xy[1]=str(y)
        
        v = '/'.join(xy)
        particules[p]=v

    root.after(18,mouvement)

bouton_ajout_particule = Button(root, text='Ajouter particule',command=ajouter_particule)
bouton_ajout_particule.pack()

bouton_lancer_simu = Button(root, text='Demarrer', command=mouvement)
bouton_lancer_simu.pack()

largeur_fenetre = 375
hauteur_fenetre = 200 

canvas = Canvas(root, width=largeur_fenetre, height=hauteur_fenetre, bg='white')
canvas.pack()

root.mainloop()