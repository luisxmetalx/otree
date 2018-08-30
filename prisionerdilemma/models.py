from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Jonathan Parrales'

doc = """
Two people have been arrested separately, and are held in separate cells. 
and depending on what they tell to police could have more o less years of
prision.
"""


class Constants(BaseConstants):
    name_in_url = 'prisionerdilemma'
    players_per_group = 2
    num_rounds = 10
    intructions_template = 'prisionerdilemma/instructions.html'
    #Pago cuando ambos jugadores confiesan o callan
    pago_ambos_confiesan = c(300)
    pago_ambos_callan = c(100)
    #Pago cuando un juigador confiesa y el otro coopera
    pago_jugador_confiesa = c(0)
    pago_jugador_calla = c(300)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    #Se crea un campo para almacenar la decisión del jugador
    decision = models.StringField(
        choices=['Confiesa', 'No Confiesa'],
        doc="""Esto es la decisión del jugador""",
        widget=widgets.RadioSelect
    )

    #Se crea un campo para almacenar el género del jugador
    genero = models.StringField(
        choices=['Masculino', 'Femenino'],
        doc="""Esto es el género del jugador""",
        widget=widgets.RadioSelect
    )

    #La edad del jugador
    edad = models.IntegerField(min=18)
    
    #matricula del jugador
    matricula = models.IntegerField(min=100000000,max=999999999)
    

    def other_player(self):
        return self.get_others_in_group()[0]

    def escoger_decision(self):
        matriz_pagos = {
            'Confiesa':
                {
                    'Confiesa': Constants.pago_ambos_confiesan,
                    'No Confiesa': Constants.pago_jugador_confiesa
                },
            'No Confiesa':
                {
                    'Confiesa': Constants.pago_jugador_calla,
                    'No Confiesa': Constants.pago_ambos_callan
                }
        }

        self.payoff = matriz_pagos[self.decision][self.other_player().decision]


