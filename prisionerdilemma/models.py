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
    num_rounds = 1
    introduction_template = 'prisionerdilemma/Introduction.html'
    #Pago cuando ambos jugadores confiesan o callan
    pago_ambos_confiesan = c(300)
    pago_ambos_callan = c(100)
    #Pago cuando un juigador confiesa y el otro coopera
    pago_jugador_confiesa = c(300)
    pago_jugador_calla = c(0)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.StringField(
        choices=['Confesarr', 'Callar'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):

        matriz_pagos = {
            'Confiesan':
                {
                    'Confesar': Constants.pago_ambos_confiesan,
                    'Callar': Constants.pago_jugador_calla
                },
            'Callan':
                {
                    'Confesar': Constants.pago_jugador_confiesa,
                    'Callar': Constants.pago_ambos_callan
                }
        }

        self.payoff = matriz_pagos[self.decision][self.other_player().decision]