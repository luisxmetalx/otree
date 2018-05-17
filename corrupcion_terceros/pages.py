from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import choice,random

class reglas_experimento(Page):
    form_model = 'group'
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        return {'id_player_1': self.player.id_in_group
                }

class player1(Page):
    form_model = 'group'
    form_fields = ['opciones']

    def is_displayed(self):
        return self.player.id_in_group == 1
    
    def vars_for_template(self):
        #choice(range(1000))
        self.group.porcentaje =  choice(range(1000))
        if(self.round_number==1):
            token=Constants.tokens1
        else:
            p1=self.group.get_player_by_id(1)
            token=p1.in_round(self.round_number - 1).payoff
        return{'num_jugadores':len(self.group.get_players()),
            'num_grupo': len(self.subsession.get_groups()),
            'num_player_gruop':len(self.subsession.get_players()),
            'token':token,
        'porcentaje':self.group.porcentaje}

class coima(Page):
    form_model = 'group'
    form_fields =['coinsJ1','opcionTokens']
    def is_displayed(self):
        return self.player.id_in_group == 1 and self.group.opciones == 1

class player2(Page):
    form_model = 'group'
    form_fields = ['aceptarCoima']

    def is_displayed(self):
        
        return self.player.id_in_group == 2 and self.group.opciones == 1 
    
    def vars_for_template(self):

        valor = int(self.group.coinsJ1)
        if(valor >1):
            self.group.monto = valor
        else:
            self.group.monto = (valor +1)
        return {
                'monto': self.group.monto,
                'valor': valor,  
                }
        
    print(Constants.monto)

class reparticion(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.group.opciones == 1 and self.player.id_in_group== 2 and self.group.aceptarCoima <= 2 and self.group.porcentaje > 4
    
    def vars_for_template(self):
        return {}
    
class noReparticion(Page):
    form_model = 'group'
    form_fields = ['opcionesCogerDinero']

    def is_displayed(self):
        return self.player.id_in_group== 1 and self.group.aceptarCoima == 3 and self.group.porcentaje > 4

class mensajes(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.group.opciones == 0 or self.group.porcentaje < 4


class WaitForP1(WaitPage):
    pass

class WaitForP2(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    form_model = 'group'

    def after_all_players_arrive(self):
        group = self.group
        #jugador firma p1
        p1 = group.get_player_by_id(1)
        print("el id del jugador es ",p1.id_in_group)
        #jugador servidor público p2
        p2 = group.get_player_by_id(2)
        print("el jugador es ",p2.id_in_group)
        if(group.opciones == 0):
            if(self.round_number == 1):
                p1.payoff = Constants.tokens1
                p2.payoff = Constants.tokens2
            else:
                p1.payoff = Constants.tokens1
                p2.payoff = Constants.tokens2

        if(self.round_number >= 1 and group.opciones == 1 ):
            if(group.aceptarCoima == 1 or group.aceptarCoima == 0):
                if(group.porcentaje < 4):
                    p1.payoff = (Constants.tokens1)-5
                    p2.payoff = (Constants.tokens1)-5
                else:
                    #formula
                    p1.payoff = (Constants.tokens1)+ (group.monto*2) - group.coinsJ1 + 2
                    p2.payoff = Constants.tokens2 + (group.monto)

            elif(group.aceptarCoima == 2):
                p1.payoff = (Constants.tokens1)-group.coinsJ1-5
                p2.payoff = (Constants.tokens2)+2 
            elif(group.aceptarCoima == 3 or group.aceptarCoima == 0 ):
                if(group.opcionesCogerDinero == 1):
                    p1.payoff = (Constants.tokens1)-(group.coinsJ1)-2
                    p2.payoff = (Constants.tokens2)-5
                elif(group.porcentaje < 4):
                    p1.payoff = (Constants.tokens1)-5
                    p2.payoff = (Constants.tokens1)-5
                else:
                    p1.payoff = (Constants.tokens1)-group.coinsJ1
                    p2.payoff = Constants.tokens2+group.coinsJ1
        

class Results(Page):
    form_model = 'group'
    def is_displayed(self):
        return self.player.id_in_group== 1 or self.player.id_in_group== 2
    
    def vars_for_template(self):
        self.group.total_pagar= sum([p.payoff for p in self.player.in_all_rounds()])
        return {
            'total_pagar': sum([p.payoff for p in self.player.in_all_rounds()]),
            'player_in_all_rounds': self.player.in_all_rounds(),
        }


page_sequence = [
    reglas_experimento,
    player1,
    coima,
    WaitForP2,
    mensajes,
    WaitForP1,
    player2,
    WaitForP1,
    reparticion,
    WaitForP2,
    noReparticion,
    ResultsWaitPage,
    Results
]
