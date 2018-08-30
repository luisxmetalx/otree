from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Introduction)
        yield (pages.Desicion, {"desicion":"Confesar"})
        assert 'Si ambos escogen Confesar' in self.html
        assert self.player.payoff == Constants.pago_ambos_confiesan
        yield (pages.Results)
