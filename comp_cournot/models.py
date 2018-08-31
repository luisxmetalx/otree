from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Jonthan Parrales'

doc = """
En la competencia de Cournot, las empresas deciden simultáneamente 
las unidades de productos que se fabricarán. El precio de venta de 
la unidad depende del total de unidades producidas. 
En esta implementación, hay 2 empresas que compiten por 1 período.
"""


class Constants(BaseConstants):
    name_in_url = 'cournot'
    players_per_group = 2
    num_rounds = 3

    instructions_template = 'comp_cournot/Instructions.html'

    # Total production capacity of all players
    total_capacity = 60
    max_units_per_player = int(total_capacity / players_per_group)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    unit_price = models.CurrencyField()

    total_units = models.FloatField(
        doc="""Total unidades producidas por todos los jugadores."""
    )

    def set_payoffs(self):
        players = self.get_players()
        self.total_units = sum([p.unidades for p in players])
        self.unit_price = Constants.total_capacity - self.total_units
        for p in players:
            p.payoff = self.unit_price * p.unidades


class Player(BasePlayer):
    #genero de los participante
    genero = models.StringField(
        choices=['Masculino', 'Femenino'],
        doc="""Esto es el género del jugador""",
        widget=widgets.RadioSelect
    )

    #edad del participante
    edad = models.IntegerField(min=18)
    
    #matricula del jugador
    matricula = models.IntegerField(min=100000000,max=999999999)

    #unidades que produce el jugador
    unidades = models.FloatField(
        min=0, max=Constants.max_units_per_player,
        doc="""Quantity of units to produce"""
    )

    def other_player(self):
        return self.get_others_in_group()[0]

