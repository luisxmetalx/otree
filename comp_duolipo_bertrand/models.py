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
    num_rounds = 5
    ume = 0.01
    intructions_template = 'comp_duolipo_bertrand/Instructions.html'
    demanda = 10
    cmg = 4

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #genero de los participante
    genero = models.StringField(
        choices=['Masculino', 'Femenino'],
        doc="""Esto es el género del jugador""",
        widget=widgets.RadioSelect
    )

    #edad del participante
    edad = models.IntegerField(min=18)
    
    #precio que pone el jugador entre 0 y 20 en cada ronda
    precio = models.FloatField(min=0.00, max=20.00)

    #valor temporal para la ganancia actual de la ronda
    value = models.IntegerField(initial=0)

    #cantidad que vende el jugador 0, 5 o 10
    vendido = models.IntegerField(initial=0)

    def other_player(self):
        return self.get_others_in_group()[0]

    def ganancia(self):
        yo = self
        oponente = self.other_player()
        value = 0
        vendido = 0
        if yo.precio == oponente.precio:
            value = (yo.precio-4)*(Constants.demanda/2)
            vendido = 5
        elif yo.precio < oponente.precio:
            value = (yo.precio-4)*(Constants.demanda)
            vendido = 10
        else:
            value = 0
            vendido = 0
        self.payoff = value
        self.vendido = vendido
