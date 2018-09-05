from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    def is_displayed(self):
        return self.round_number == 1

class Quiz(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = 'player'
    form_fields = ['genero','edad','matricula']

class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}
    
    def vars_for_template(self):
        return {
            'ronda' : self.round_number
            }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute."


class Results(Page):
    """Players payoff: How much each has earned"""

    def vars_for_template(self):
        promedio = self.group.total_contribution/Constants.players_per_group
        return {
            'total_earnings': self.group.total_contribution * Constants.multiplier,
            'promedio': promedio,
        }
class Graficas(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Introduction,
    Contribute,
    ResultsWaitPage,
    Results,
    Quiz,
    Graficas
]