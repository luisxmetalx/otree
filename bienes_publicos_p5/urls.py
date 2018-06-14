from .models import Subsession
import random


# genera una contribucion aleatoria (entre 0 y 20) y actualiza el modelo
def contribucion_aleatoria():
    ale = random.randint(0, 20)
    print ('contribucion aleatoria: ', ale)
    return ale


def puntosReducidos(puntos, player):
    dicc = player.session.vars.get("dicc_puntos")
    for k, v in dicc.items():
        print (k, v)
    return player.session.vars["dicc_puntos"][puntos]