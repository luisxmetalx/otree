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

    #preguntas para democracia
    pregunta1 = models.LongStringField(label="¿Qué información fue más relevante para su decisión sobre el administrador del grupo?(¿Qué le hizo decidirse por el administrador seleccionado?).",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))
    pregunta2 = models.LongStringField(label="¿Se comportó el administrador del grupo de acuerdo con tus expectativas?.",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))
    pregunta3 = models.LongStringField(label="Estamos interesados en conocer su motivación en la votación de la fase 2. Específicamente, ¿qué información tomó en cuenta para votar por el administrador del grupo?.",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))

    #preguntas para leviatan
    pregunta4 = models.LongStringField(label="¿Qué opinas sobre el mecanismo de selección del administrador?",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))
    pregunta5 = models.LongStringField(label="¿Se comportó el administrador del grupo de acuerdo con tus expectativas?",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))
    pregunta6 = models.LongStringField(label="¿Qué opina del mecanismo de selección del administrador? Si tuviera que volver a diseñar el mecanismo de selección, ¿qué regla o reglas elegiría?.",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))

    #preguntas comunes
    pregunta7 = models.LongStringField(label="¿Cómo esperaba que los administradores tomaran sus decisiones en cada ronda?.",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))
    pregunta8 = models.LongStringField(label="¿Los administradores se comportaron de acuerdo con sus expectativas?. Explique",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))
    pregunta9 = models.LongStringField(label="¿Qué efecto, en su caso, cree que tuvieron los administradores sobre los resultados de su grupo?.",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))
    pregunta10 = models.LongStringField(label="Si tuviéramos que agregar una tercera fase al experimento, ¿preferiría que se usen las reglas de la fase 1 ó fase 2?.",widget=widgets.Textarea(attrs={'cols': '20', 'rows': '5'}))


    def info_de_pagos(self):

        self.num_maquina = self.participant.vars.get('maquina')        
        self.matricula = self.participant.vars.get('matricula')
        #self.participant.vars['participacion'] = 3
        self.pago_de_sesion = 2.00
        if self.participant.vars.get('pago_bp') == None:
            self.participant.vars["pago_bp"] = 0
        if self.participant.vars.get('bret_payoff') == None:
            self.participant.vars["bret_payoff"] = 0
        
        self.pago_bp = round(self.participant.vars.get('pago_bp'), 1)
        print('pago bp: ', self.pago_bp, type(self.pago_bp))
        self.pago_bret = float(self.participant.vars.get('bret_payoff'))
        print('pago bret: ', self.pago_bret, type(self.pago_bret))
        self.pago_total = round(self.pago_de_sesion + self.pago_bp + self.pago_bret, 1)
        print('pago total: ', self.pago_total, type(self.pago_total))
