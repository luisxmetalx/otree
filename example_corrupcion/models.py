from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'example_corrupcion'
    players_per_group = 2
    num_rounds = 1

    tokens1=c(40)
    tokens2=c(40)



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    
    opciones = models.IntegerField(
        choices=[[1,'Asignar Tokens'],[2,'No Asignar Tokens']], widget=widgets.RadioSelect,blank=True,initial=0
    )

    coinsJ1= models.IntegerField(min=1, max=10, label="Con cuanto sobornará...")

    aceptarCoima = models.BooleanField()

    opcionTokens = models.StringField(
        choices = ['Regalo','Soborno'], widget=widgets.RadioSelect,blank=True,initial=0,label="Como desea enviarlo?..."
    )

    opcionCoima = models.StringField(
        choices = ['A','B'], widget=widgets.RadioSelect,blank=True,initial=0,label="Cual es su eleccion?..."
    )



class Player(BasePlayer):
    pass


