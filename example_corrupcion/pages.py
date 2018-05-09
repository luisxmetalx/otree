from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import choice,random


class player1(Page):
    form_model = 'group'
    form_fields = ['opciones']

    def is_displayed(self):
        return self.player.id_in_group == 1

class coima(Page):

    form_model = 'group'
    form_fields =['coinsJ1','opcionTokens']
    def is_displayed(self):
        return self.player.id_in_group == 1 and self.group.opciones == 1

class player2(Page):
    form_model = 'group'
    form_fields = ['coinsJ1']
    form_fields =['aceptarCoima']

    def is_displayed(self):
        return self.player.id_in_group == 2 
    
    def vars_for_template(self):
        return {'prediccion': choice(range(1000))}

class reparticion(Page):
    form_model = 'group'
    form_fields = ['opcionCoima']

    def is_displayed(self):
        return self.group.opciones == 1 and self.player.id_in_group== 2 and self.group.aceptarCoima == True

class MyPage(Page):
    pass

class WaitForP1(WaitPage):
    pass

class ResultsWaitPage(WaitPage):
    

    def after_all_players_arrive(self):
        group = self.group
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)
        if(group.aceptarCoima == 1):
            p1.payoff = (Constants.tokens1-2)- group.coinsJ1
            p2.payoff = Constants.tokens2 + ((group.coinsJ1)*3)
        else:
            p1.payoff = (Constants.tokens1-2)- group.coinsJ1
            p2.payoff = Constants.tokens2 
        
            




class Results(Page):
    pass


page_sequence = [
    player1,
    coima,
    WaitForP1,
    player2,
    reparticion,
    ResultsWaitPage,
    Results
]
