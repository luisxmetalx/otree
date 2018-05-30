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
    num_rounds = 3

    tokens1=15
    tokens2=15
    token_Espol=50
    monto=0
    #tasa=0.25



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    
    opciones = models.IntegerField(
        choices=[[1,'1) Enviar un mensaje ofreciéndole una cantidad de tokens (entre 3 y 10) al servidor público.'],[0,'2)	No enviar ningún mensaje al servidor público.']], widget=widgets.RadioSelect
    )

    coinsJ1= models.IntegerField(min=3, max=10, label="Cantidad de Tokens (3-10)")

    aceptarCoima = models.IntegerField(
        choices=[[1,'1)	Reportar el mensaje a la entidad reguladora de compras públicas. '],[2,'2) Recibe los tokens, pero no favorece a ESPOL.'],[3,'3)	Acepta los tokens. Entrega 2 tokens a sus colegas y  garantiza el contrato a la empresa menos eficiente.'],[0,'']], widget=widgets.RadioSelect,label=""
    )

    porcentaje = models.IntegerField()

    opcionTokens = models.IntegerField(
        choices = [[0,'Regalo'],[1,'Soborno']], widget=widgets.RadioSelect, label=""
    )

    total_pagar = models.CurrencyField()
    total_pagar_firma = models.IntegerField()
    total_pagar_sp = models.IntegerField()

    opcionesCogerDinero = models.IntegerField(
        choices=[[1,'No hacer nada y pasar a la siguiente ronda.'],[0,'Denunciar al servidor público. Si decide denunciar al servidor público, a usted le costará 2 tokens que serán descontados de su ganancias, pero al servidor público se le confiscará los tokens enviados y se le castigará con una multa de 3 tokens.']], widget=widgets.RadioSelect,label="¿Qué decide hacer al respecto?"
    )
    #Ganancias para la ESPOL
    espol_firma=models.CurrencyField()
    espol_sp=models.CurrencyField()   
    
    

    grupos_auditado=models.IntegerField()
    auditado=models.BooleanField()




class Player(BasePlayer):
    Beneficio_espol=models.CurrencyField()
    
