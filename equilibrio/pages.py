from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models
from .models import Constants


class Definir_precio(Page):
    form_model = models.Player
    form_fields = ['precio']

    def precio_error_message(self, value):
        if value < self.player.carta:
            return 'valor no permitido...'

    def is_displayed(self):

        return True

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

class Negociacion(Page):
    pass

class Results(Page):
    pass


page_sequence = [
    Definir_precio,
    ResultsWaitPage,
    Negociacion,
    Results
]
