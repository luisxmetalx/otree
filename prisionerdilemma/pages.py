from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100

class Decision(Page):
    form_model = 'player'
    form_field = ['decision']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    pass


page_sequence = [
    Introduction,
    Decision,
    ResultsWaitPage,
    Results
]
