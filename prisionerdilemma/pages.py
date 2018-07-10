from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

class Results(Page):
    def vars_for_template(self):
        yo = self.player
        oponente = yo.other_player()
        return {
            'mi_decision': yo.decision,
            'oponente_decision': oponente.decision,
            'misma_eleccion': yo.decision == oponente.decision,
        }


page_sequence = [
    Introduction,
    Decision,
    ResultsWaitPage,
    Results
]
