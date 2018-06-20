from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Washington Vélez'

doc = """
App para obtener detalle de pagos de las tareas/apps de la sesión bienes públicos
"""



class Constants(BaseConstants):
    name_in_url = 'tar_fin_ses_bp'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    num_maquina = models.PositiveIntegerField()
    matricula = models.PositiveIntegerField()
    pago_de_sesion = models.FloatField()
    pago_bp = models.FloatField()
    pago_bret = models.FloatField()
    pago_total = models.FloatField()


    def info_de_pagos(self):

        self.num_maquina = self.participant.vars.get('maquina')        
        self.matricula = self.participant.vars.get('matricula')
        #self.participant.vars['participacion'] = 3
        self.pago_de_sesion = 2.00
        if self.participant.vars.get('pago_bp') == None:
            self.participant.vars["pago_bp"] = 0
        if self.participant.vars.get('pago_bret') == None:
            self.participant.vars["pago_bret"] = 0
        
        self.pago_bp = round(self.participant.vars.get('pago_bp'), 1)
        print('pago bp: ', self.pago_bp, type(self.pago_bp))
        self.pago_bret = float(self.participant.vars.get('pago_bret'))
        print('pago bret: ', self.pago_bret, type(self.pago_bret))
        self.pago_total = round(self.pago_de_sesion + self.pago_bp + self.pago_bret, 1)
        print('pago total: ', self.pago_total, type(self.pago_total))
