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

    tokens1=40
    tokens2=40
    monto=0
    tasa=0.25



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    
    opciones = models.IntegerField(
        choices=[[1,'Asignar Tokens'],[2,'No Asignar Tokens']], widget=widgets.RadioSelect,blank=True,initial=0
    )

    coinsJ1= models.IntegerField(min=1, max=10, label="Con cuanto sobornará...")

    aceptarCoima = models.IntegerField(
        choices=[[1,'aceptar'],[2,'Denunciar'],[3,'Cogerse el dinero']], widget=widgets.RadioSelect,blank=True,initial=0,label="Elija su opcion...:"
    )

    porcentaje = models.IntegerField()

    opcionTokens = models.StringField(
        choices = ['Regalo','Soborno'], widget=widgets.RadioSelect,blank=True,initial=0,label="Como desea enviarlo?..."
    )

    opcionCoima = models.StringField(
        choices = ['A','B',''], widget=widgets.RadioSelect,blank=True,initial=0,label="Cual es su eleccion?..."
    )

    opcionesCogerDinero = models.IntegerField(
        choices=[[1,'Denunciar'],[2,'No hacer Nada']], widget=widgets.RadioSelect,blank=True,initial=0,label="cual es la opcion a escoger"
    )



class Player(BasePlayer):
    pass


