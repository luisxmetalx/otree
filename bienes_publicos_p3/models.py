from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import numpy as np

author = 'Washington Vélez'

doc = """
Bienes públicos: Instrucciones Fase2, Test2, Votación, Resultados de Votación
"""

class Constants(BaseConstants):
    name_in_url = 'bienes_publicos_p3'
    players_per_group = 5
    num_rounds = 1
    fondo = 20
    fondo_castigo = 10
    tao = 2    
    
    puntos_asignados = [i for i in range(11)]
    puntos_reducidos = [0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30]

    modalF2 = 'bienes_publicos/modalInstF2.html'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    administrador = models.PositiveIntegerField(initial=0)

    tratamiento = models.CharField()

    def obtenerTratamiento(self):
        tratamientos = [jugador.participant.vars["tratamiento"] for jugador in self.get_players()]
        self.tratamiento = tratamientos[0]
        print ('tratamiento del grupo: ', self.id_in_subsession, ' :', self.tratamiento)

    def contarVotos(self):
        for p in self.get_players():
            self.get_player_by_id(p.voto).participant.vars["votos_recibidos"] += 1
        for p in self.get_players():
            print ('id: ', p.id_in_group, 'votos recibidos: ', p.participant.vars["votos_recibidos"])
    
    # obtiene el administrador entre los votos de los participantes
    def obtener_admin_dem(self):
        votos = []
        for p in self.get_players():
            votos.append(p.voto)
        dicc_votos = {}
        for v in votos:
            if str(v) not in dicc_votos:
                dicc_votos[str(v)] = 1
            else:
                dicc_votos[str(v)] += 1

        print ('dicc_votos: ', dicc_votos)
        maximo = max(dicc_votos.values())
        print ('maximo: ', maximo)
        maximos = []
        indices_maximos = []

        for k, v in dicc_votos.items():
            print (k, ' --> ', v)
            if v == maximo:
                maximos.append(v)
                indices_maximos.append(k)

        #print ('maximos: ', indices_maximos)
        admin = random.choice(indices_maximos)
        #print ('admin --> ', admin)
        for g in self.in_rounds(1, Constants.num_rounds):
            g.administrador = admin

        return admin


    # sortea ganador con 75% de probabilidad de ser elegido el de mayor acumulado de contribuciones
    def sortear_admin_lev(self):
        prob_mayor = 0.75
        lista_contrib_acum = []
        for p in self.get_players():
            print ('Jugador: ', p.id_in_group, '  tiene: ', p.participant.vars["acumulado"])
            lista_contrib_acum.append(p.participant.vars["acumulado"])
        if sum(lista_contrib_acum) != 0:
            # hay al menos una contribución
            print ('lista contrib acum (ordenada por id de participante):', lista_contrib_acum)
            # se obtienen los indices de los valores maximos y los que no son maximo, 
            mayores = np.where(lista_contrib_acum == np.max(lista_contrib_acum))
            menores = np.where(lista_contrib_acum != np.max(lista_contrib_acum))

            indices_mayores = mayores[0].tolist()
            indices_menores = menores[0].tolist()

            sorteo = [np.max(lista_contrib_acum), -1]
            gana = np.random.choice(sorteo, p = [prob_mayor, 1 - prob_mayor])

            print('indices mayores: ', indices_mayores, type(indices_mayores))
            print('indices menores: ', indices_menores, type(indices_menores))

            #print ('gana: ', gana)
            if gana == -1:
                # gana uno que no tiene el maximo de contribuciones acumladas (p = 0.25)
                ind_ganador = np.random.choice(indices_menores)
            else:
                # gana uno que tiene el maximo de contribuciones acumladas (p = 0.75)
                ind_ganador = np.random.choice(indices_mayores)
            ganador = self.get_players()[ind_ganador]
            self.administrador = ganador.id_in_group
            admin = self.administrador
        else:
            #print ('nadie contribuyó nada')
            ganador = random.randint(1,5)
            self.administrador = ganador
            admin = self.administrador

        for g in self.in_rounds(1, Constants.num_rounds):
            g.administrador = admin
        #print ('grupo: ', self.id_in_subsession, '| administrador: ', admin)
    

class Player(BasePlayer):
    tratamiento = models.CharField()
    voto = models.IntegerField()
    
    test2_p1 = models.IntegerField(initial=0)
    test2_p2 = models.IntegerField(initial=0)
    test2_p3 = models.IntegerField(initial=0)
    test2_p4 = models.IntegerField(initial=0)
    test2_p5 = models.IntegerField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        elif self.id_in_group == 2:
            return 'B'
        elif self.id_in_group == 3:
            return 'C'
        elif self.id_in_group == 4:
            return 'D'
        else:
            return 'E'
