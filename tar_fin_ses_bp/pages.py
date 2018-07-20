from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class TareasFinalizadas(Page):
    def is_displayed(self):
        print('\tactual: ', self.player.id_in_group)
        print('\tip: ', self.participant.ip_address)
        
        print('\tmaquina: ', self.player.participant.vars.get('maquina'))
        self.player.info_de_pagos()

        return True
    
    
class FinalSeccion2(Page):
    pass

class Contestas(Page):
    form_model = 'player'
    #form_fields=['pregunta1','pregunta2','pregunta3','pregunta4']
    def get_form_fields(self):
        if self.player.participant.vars["tratamiento"] == "leviatan":
            return ['pregunta4','pregunta5','pregunta6','pregunta7','pregunta8','pregunta9','pregunta10']
        else:
            return ['pregunta1','pregunta2','pregunta3','pregunta7','pregunta8','pregunta9','pregunta10']
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
        


page_sequence = [FinalSeccion2, TareasFinalizadas,Contestas]
