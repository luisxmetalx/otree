from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models


class Bienvenida(Page):
    
    form_model = models.Player
    form_fields = ['matricula']
    
    def before_next_page(self):
        self.player.calcularNumMaquina()
        self.participant.vars['maquina'] = self.player.maquina
        print ('maquina: ', self.player.maquina)

        self.participant.vars['matricula'] = self.player.matricula

        print('matricula: ', self.participant.vars['matricula'])


page_sequence = [
    Bienvenida
]
