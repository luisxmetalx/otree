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
        


page_sequence = [FinalSeccion2, TareasFinalizadas]
