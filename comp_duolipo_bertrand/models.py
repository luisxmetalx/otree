from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Jonathan Parrales'

doc = """
Este experimento consiste en que dos participantes empresarios
establecen el precio de un producto y quien proponga el mejor
precio tendra todo el mercado o la mitad.
"""


class Constants(BaseConstants):
    name_in_url = 'comp_duolipo_bertrand'
    players_per_group = 2
    num_rounds = 10
    ume = 0.01
    intructions_template = 'comp_duolipo_bertrand/instructions.html'
    demanda = 100

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #precio que pone el jugador entre 0 y 20 en cada ronda
    precio = models.IntegerField(min=0, max=20)

    #valor temporal para la ganancia actual de la ronda
    value = 0

    #matricula del jugador
    matricula = models.IntegerField(min=100000000,max=999999999)

    def other_player(self):
        return self.get_others_in_group()[0]

    def ganancia(self):
        yo = self
        oponente = self.other_player()
        value=0
        if yo.precio == oponente.precio:
            value = yo.precio*(Constants.demanda/2)*Constants.ume
        elif yo.precio < oponente.precio:
            value = yo.precio*(Constants.demanda)*Constants.ume
        else:
            value = 0
        self.payoff = value
