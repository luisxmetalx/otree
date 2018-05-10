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
    
    def before_next_page(self):
        self.group.opcionCoima == ''

class player2(Page):
    form_model = 'group'
    form_fields = ['aceptarCoima']

    def is_displayed(self):
        self.group.porcentaje =  choice(range(1000))
        return self.player.id_in_group == 2 and self.group.opciones == 1
    
    def vars_for_template(self):
        return {'prediccion': choice(range(1000)),
                'monto': int(self.group.coinsJ1*self.Constants.tasa
        }

class reparticion(Page):
    form_model = 'group'
    form_fields = ['opcionCoima']

    def is_displayed(self):
        return self.group.opciones == 1 and self.player.id_in_group== 2 and self.group.aceptarCoima <= 2
    
    def vars_for_template(self):
        return {}
    
class noReparticion(Page):
    form_model = 'group'
    form_fields = ['opcionesCogerDinero']

    def is_displayed(self):
        return self.player.id_in_group== 1 and self.group.aceptarCoima == 3




class WaitForP1(WaitPage):
    pass

class WaitForP2(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    form_model = 'group'

    def after_all_players_arrive(self):
        group = self.group
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)
        if(group.aceptarCoima == 1):
            p1.payoff = (Constants.tokens1-2)- group.coinsJ1
            p2.payoff = Constants.tokens2 + ((group.coinsJ1)*3)
            if(group.coinsJ1 == 1):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 47
                    p2.payoff = 63
                else:
                    p1.payoff = 67
                    p2.payoff = 48
            if(group.coinsJ1 == 2):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 45
                    p2.payoff = 56
                else:
                    p1.payoff = 66
                    p2.payoff = 51
            if(group.coinsJ1 == 3):
                if(group.opcionCoima == 'A'):
                    p1.payoff = p1.payoff + (group.coinsJ1*Constants.tasa)
                    p2.payoff = p2.payoff + (group.coinsJ1*Constants.tasa)
                else:
                    p1.payoff = 65
                    p2.payoff = 54
            if(group.coinsJ1 == 4):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 44
                    p2.payoff = 62
                else:
                    p1.payoff = 64
                    p2.payoff = 57
            if(group.coinsJ1 == 5):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 43
                    p2.payoff = 65
                else:
                    p1.payoff = 63
                    p2.payoff = 60
            if(group.coinsJ1 == 6):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 42
                    p2.payoff = 68
                else:
                    p1.payoff = 62
                    p2.payoff = 63
            if(group.coinsJ1 == 7):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 41
                    p2.payoff = 71
                else:
                    p1.payoff = 61
                    p2.payoff = 66
            if(group.coinsJ1 == 8):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 40
                    p2.payoff = 74
                else:
                    p1.payoff = 60
                    p2.payoff = 69
            if(group.coinsJ1 == 9):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 39
                    p2.payoff = 77
                else:
                    p1.payoff = 59
                    p2.payoff = 72
            if(group.coinsJ1 == 10):
                if(group.opcionCoima == 'A'):
                    p1.payoff = 38
                    p2.payoff = 80
                else:
                    p1.payoff = 58
                    p2.payoff = 75
        elif(group.aceptarCoima == 2):
            p1.payoff = (Constants.tokens1)-group.coinsJ1
            p2.payoff = Constants.tokens2+2 
        elif(group.aceptarCoima == 3):
            if(group.opcionesCogerDinero == 1):
                p1.payoff = (Constants.tokens1)-2
                p2.payoff = (Constants.tokens2)-3
            else:
                p1.payoff = (Constants.tokens1)-group.coinsJ1
                p2.payoff = Constants.tokens2+group.coinsJ1

        else:
            p1.payoff = Constants.tokens1
            p2.payoff = Constants.tokens2

class Results(Page):
    form_model = 'group'
    pass


page_sequence = [
    player1,
    coima,
    WaitForP1,
    player2,
    WaitForP1,
    reparticion,
    WaitForP2,
    noReparticion,
    ResultsWaitPage,
    Results
]
