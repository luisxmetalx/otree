from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100

class Quiz(Page):
    form_model = 'player'
    form_fields = ['genero','edad']

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.escoger_decision()

class Results(Page):
    def vars_for_template(self):
        yo = self.player
        oponente = yo.other_player()
        return {
            'mi_decision': yo.decision,
            'oponente_decision': oponente.decision,
            'misma_eleccion': yo.decision == oponente.decision,
        }

class CharWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass
            

class Chart(Page):
    def vars_for_template(self):
        acum=0
        l_edades=[]
        l_generos=[]
        for p in self.subsession.get_players():
            l_edades.append(p.edad)
            l_generos.append(p.genero)
        
        femenino=((l_generos.count('Femenino')/len(self.subsession.get_players())))*100
        masculino=(l_generos.count('Masculino')/len(self.subsession.get_players()))*100
        
        n_jugador=len(self.group.get_players())
        return {
            'm':masculino,
            'f':femenino
        }

page_sequence = [
    Introduction,
    Quiz,
    # Decision,
    # ResultsWaitPage,
    # Results,
    CharWaitPage,
    Chart
]
