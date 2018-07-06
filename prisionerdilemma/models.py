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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
