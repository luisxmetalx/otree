from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint


author = 'Kuis Andrade'

doc = """
Equilibrio, 2.	Muestra que la teoría que explicamos proporciona conclusiones empíricamente validadas. De hecho, es más probable que crean que los resultados son ciertos, si se han comportado de la manera en que la teoría predice.
"""


class Constants(BaseConstants):
    name_in_url = 'equilibrio'
    players_per_group = 2
    num_rounds = 3


class Subsession(BaseSubsession):
    def creating_session(self):
        for g in self.get_groups():
            # se asigna para los grupos impares 'vendedor' y para los pares 'comprador'
            for p in g.get_players():
                if p.id % 2 == 1:
                    p.tratamiento = 'vendedor'
                else:
                    p.tratamiento = 'comprador'
        #colorar la carta para todos los turnos
        for p in self.get_players():
            for actual in p.in_all_rounds():
                actual.elegir_Carta()           



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    tratamiento = models.CharField()
    carta = models.IntegerField(initial=0)

    precio=models.IntegerField(initial=0)

    def elegir_Carta(self):
        num_v=randint(1, 15)
        num_c=randint(5, 20)
        if self.in_round(1).carta==0 and self.tratamiento=='comprador':
            self.carta=num_c
        elif self.in_round(1).carta==0 and self.tratamiento=='vendedor':
            self.carta=num_v
        else:
            self.carta=self.in_round(1).carta

        

