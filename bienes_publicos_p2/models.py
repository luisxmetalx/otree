from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import numpy as np

author = 'Washington Vélez'

doc = """
Bienes Públicos: Contribuir, Calcular VCM, Mostrar Resultados
"""


class Constants(BaseConstants):
    name_in_url = 'bienes_publicos_p2'
    players_per_group = 5
    num_rounds = 2
    fondo = 20
        
    modalF1 = 'bienes_publicos_p2/modalInstF1.html'

class Subsession(BaseSubsession):
    def creating_session(self):

        if self.round_number == 1:        
            for grupo in self.get_groups():
                for jugador in grupo.get_players():
                    jugador.participant.vars["contribuciones"] = []
                    jugador.participant.vars["acumulado"] = 0
                    jugador.participant.vars["votos_recibidos"] = 0
                    lista = jugador.participant.vars["contribuciones"]      
                    #print ('jugador ', jugador.id_in_group, '--> lista de contr: ', lista)

class Group(BaseGroup):
    contribucion_total = models.IntegerField()
    
    def cacularGanancias(self):
        # obtiene el acumulado de las contribuciones de cada participante y actualiza el modelo
        self.contribucion_total = sum([p.contribucion for p in self.get_players()])

        # Calcula la ganancia de cada jugador y actualiza el modelo (VCM)
        for jugador in self.get_players():
            ganancia = round(Constants.fondo - jugador.contribucion + (2/Constants.players_per_group)*self.contribucion_total, 2)
            jugador.ganancia = ganancia
        #print ('contribucion total actual: ', self.contribucion_total)

class Player(BasePlayer):
    contribucion = models.IntegerField(min=0, max=20)
    tratamiento = models.CharField()
    ganancia = models.FloatField(initial=0)
    ganVCM = models.FloatField(initial=0)

    # calcula la suma de las ganacias de cada ronda y lo guarda en la variable del dicc "ganVCM"
    def calcularGananciaAcumlada(self):
        ganancias_totales = sum([p.ganancia for p in self.in_all_rounds()])
        self.participant.vars["ganVCM"] = ganancias_totales
        self.ganVCM = ganancias_totales
        return ganancias_totales