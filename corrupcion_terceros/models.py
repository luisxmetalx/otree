from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Luis Andrade'

doc = """
Tratamiento de corrupcion con agentes externos
"""


class Constants(BaseConstants):
    name_in_url = 'corrupcion_terceros'
    players_per_group = 2
    num_rounds = 10

    tokens1=15
    tokens2=15
    token_Espol=50
    monto=0
    #tasa=0.25



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    
    opciones = models.IntegerField(
        choices=[[1,'1) Enviar un mensaje ofreciéndole una cantidad de tokens (entre 3 y 15) al servidor público'],[0,'2)	No enviar ningún mensaje al servidor público']], widget=widgets.RadioSelect,blank=True,initial=0
    )

    coinsJ1= models.IntegerField(min=3, max=10, label="Con cuanto sobornará...")

    aceptarCoima = models.IntegerField(
        choices=[[1,'1)	Acepta los tokens '],[2,'2) Reportar el mensaje a su agencia.'],[3,'3)	Recibe los tokens, pero no favorece a su firma'],[0,'']], widget=widgets.RadioSelect,blank=True,initial=0,label="Elija su opcion...:"
    )

    porcentaje = models.IntegerField()

    opcionTokens = models.IntegerField(
        choices = [[0,'Regalo'],[1,'Soborno']], widget=widgets.RadioSelect,blank=True,initial=0,label="Como desea enviarlo?..."
    )

    total_pagar = models.IntegerField()

    opcionesCogerDinero = models.IntegerField(
        choices=[[1,'Denunciar'],[2,'No hacer Nada']], widget=widgets.RadioSelect,blank=True,initial=0,label="cual es la opcion a escoger"
    )

    ganancia_espol=models.IntegerField()   
    
    monto=models.IntegerField()



class Player(BasePlayer):
    pass
