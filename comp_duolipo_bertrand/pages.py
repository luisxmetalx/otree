from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1
    timeout_seconds = 100
    form_model = 'player'
    form_fields = ['matricula']

class darPrecio(Page):
    form_model = 'player'
    form_fields = ['precio']
    def vars_for_template(self):
        return {
            'ronda' : self.round_number
        }

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.ganancia()

class Resultados(Page):
    def vars_for_template(self):
        yo = self.player
        oponente = yo.other_player()
        mi_ganancia = yo.payoff
        opon_ganancia = oponente.payoff
        lista = {}
        for i in self.player.in_rounds(1,self.round_number):
            lista[i.round_number]=i.payoff;
        ganancia_total = sum([p.payoff for p in self.player.in_rounds(1,self.round_number)])
        return {
            'mi_ganancia' : mi_ganancia,
            'ganancia_total' : ganancia_total,
            'lista' : lista,
            'round' : self.round_number
        }

class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        ganancia_total = sum([p.payoff for p in self.player.in_all_rounds()])
        lista = {}
        for i in self.player.in_rounds(1,self.round_number):
            lista[i.round_number]=i.payoff;
        return {
            'ganancia_total' : ganancia_total,
            'lista' : lista
        }


page_sequence = [
    Introduction,
    darPrecio,
    ResultsWaitPage,
    Resultados,
    Results
]
