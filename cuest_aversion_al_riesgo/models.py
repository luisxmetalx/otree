from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Washington Vélez'

doc = """
Cuestionario de aversión al riesgo por dominios
"""


class Constants(BaseConstants):
    name_in_url = 'cuest_aversion_al_riesgo'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
        
    # Preguntas de opción múltiple (radio buttons generados en el template) entre 1 y 10.
    pregunta_1 = models.PositiveSmallIntegerField()
    pregunta_2 = models.PositiveSmallIntegerField()
    pregunta_3 = models.PositiveSmallIntegerField()
    pregunta_4 = models.PositiveSmallIntegerField()
    pregunta_5 = models.PositiveSmallIntegerField()
    pregunta_6 = models.PositiveSmallIntegerField()
    pregunta_7 = models.PositiveSmallIntegerField()
