from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import choice,random
import random

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
        'porcentaje':self.group.porcentaje,
        #'matricula':self.participant.vars['matricula'],
        'id_grupo':self.group.id_in_subsession}

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

    
        return {
                'monto': self.group.coinsJ1,
                }
        

class mensaje_token(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.group.opciones == 1 and self.player.id_in_group== 2 and self.group.aceptarCoima <= 2 and self.group.aceptarCoima >0  and self.group.porcentaje > 4 or self.player.id_in_group== 1 
    
    def vars_for_template(self):
        return {}
    
class noReparticion(Page):
    form_model = 'group'
    form_fields = ['opcionesCogerDinero']

    def is_displayed(self):
        return self.player.id_in_group== 1 and self.group.aceptarCoima == 2 and self.group.porcentaje > 4

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
        
        '''
        No Enviar coima ya sea como soborno o como regalo
        '''
        if(group.opciones == 0):
            if(self.round_number >= 1):
                p1.payoff = Constants.tokens1
                p2.payoff = Constants.tokens2
                self.group.espol_firma = 0
                self.group.espol_sp = 20
        '''
        Enviar coima ya sea como soborno o como regalo
        '''
        if(self.round_number >= 1 and group.opciones == 1 ):
            """
            Cuando se acepta el soborno.
            """
            if(group.aceptarCoima == 3 or group.aceptarCoima == 0):
                if(group.porcentaje < 4):
                    p1.payoff = (Constants.tokens1)-5
                    p2.payoff = (Constants.tokens1)-5
                    self.group.espol_firma = 0
                    self.group.espol_sp = 20

                else:
                    p1.payoff = (Constants.tokens1)+ group.coinsJ1 - 2
                    p2.payoff = Constants.tokens2 + group.coinsJ1 - 2
                    self.group.espol_firma = Constants.token_Espol - (2*group.coinsJ1)
                    self.group.espol_sp = 0
            elif(group.aceptarCoima == 1):
                """
                Denuncia el soborno.
                """
                p1.payoff = (Constants.tokens1)-5
                p2.payoff = (Constants.tokens2)+2 
                self.group.espol_firma = 0
                self.group.espol_sp = 20
            elif(group.aceptarCoima == 2 or group.aceptarCoima == 0 ):
                """
                cuando la firma denucia al servidor publico
                """
                if(group.opcionesCogerDinero == 0):
                    p1.payoff = (Constants.tokens1)-group.coinsJ1-2
                    p2.payoff = (Constants.tokens2)-3
                    self.group.espol_firma = 0
                    self.group.espol_sp = 20
                elif(group.porcentaje < 4):
                    p1.payoff = (Constants.tokens1)-5
                    p2.payoff = (Constants.tokens1)-5
                    self.group.espol_firma = 0
                    self.group.espol_sp = 20
                else:
                    """
                    cuando la firma no hace nada al respecto
                    """
                    p1.payoff = (Constants.tokens1)-group.coinsJ1
                    p2.payoff = Constants.tokens2+group.coinsJ1
                    self.group.espol_firma = 0
                    self.group.espol_sp = 20
        

class Results(Page):
    form_model = 'group'
    def is_displayed(self):
        return self.player.id_in_group== 1 or self.player.id_in_group== 2
    
    def vars_for_template(self):
        self.group.total_pagar= sum([p.payoff for p in self.player.in_all_rounds()])
        #self.group.total_pagar_firma= sum([p.total_pagar_firma for p in self.subsession.get_groups()])
        #self.group.total_pagar_sp= sum([p.total_pagar_sp for p in self.subsession.get_groups()])
        return {
            'total_pagar': sum([p.payoff for p in self.player.in_all_rounds()]),
            #'total_pagar_firma': self.group.total_pagar_firma,
            #'total_pagar_sp': self.group.total_pagar_sp,
            'player_in_all_rounds': self.player.in_all_rounds(),
        }

class auditoria(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.player.id_in_group== 1 or self.player.id_in_group== 2 

    def vars_for_template(self):
        cachados=[]
        self.group.total_pagar= sum([p.payoff for p in self.player.in_all_rounds()])
        #self.group.total_pagar_firma= sum([p.total_pagar_firma for p in self.subsession.get_groups()])
        #self.group.total_pagar_sp= sum([p.total_pagar_sp for p in self.subsession.get_groups()])
        if(self.round_number == 1):
            auditados=5
        else:
            auditados=self.group.in_round(self.round_number - 1).grupos_auditado
        lista_all=self.subsession.get_groups()
        for grupo in lista_all:
            if(grupo.auditado == True):
                idGrupo=grupo.id_in_subsession
                cachados.append(grupo)
        return{
            'auditados': auditados,
            'gAuditados':self.group.grupos_auditado,
            'detenidos': len(cachados),
            #'grupos_pasados': self.group.in_round(self.round_number - 1).grupos_auditado,
            #'id_auditado':idGrupo,
            'total_pagar': sum([p.payoff for p in self.player.in_all_rounds()]),
            'total_pagar_firma': self.group.total_pagar_firma,
            'total_pagar_sp': self.group.total_pagar_sp,
            'player_in_all_rounds': self.player.in_all_rounds(),
        }

class  AllGroupsWaitPage ( WaitPage ): 
    wait_for_all_groups  =  True

class Resulado_auditoria(WaitPage):
    form_model = 'group'

    def after_all_players_arrive(self):
        lista_grupo=[]
        grupos_auditados=[]
        lista_all=self.subsession.get_groups()

        #operaciones
        if(self.round_number == 1):
            lista_grupo=random.sample(lista_all,k=5)
            #lista_grupo=choice(lista_all)
            for grupo in lista_grupo:
                print("\n el id del grupo escogido es : ", grupo.id_in_subsession)                
                if(grupo.aceptarCoima == 3):
                    print("\n el id del grupo auditado es : ", grupo.id_in_subsession)
                    grupo.auditado = True
                    grupos_auditados.append(grupo)

            if(len(grupos_auditados)>=3):
                self.group.grupos_auditado=8
                for grupo in lista_all:
                    grupo.total_pagar_firma= grupo.espol_firma
                    grupo.total_pagar_sp= grupo.espol_sp
                    grupo.grupos_auditado=8
            elif(len(grupos_auditados)==2):
                self.group.grupos_auditado=5
                for grupo in lista_all:
                    grupo.total_pagar_firma= grupo.espol_firma
                    grupo.total_pagar_sp= grupo.espol_sp
                    grupo.grupos_auditado=5
            elif(len(grupos_auditados)<=1):
                self.group.grupos_auditado=3
                for grupo in lista_all:
                    grupo.total_pagar_firma= grupo.espol_firma
                    grupo.total_pagar_sp= grupo.espol_sp
                    grupo.grupos_auditado=3
        else:
            '''
            k siempre ira cambiando en las rondas, ya que va a depender de las auditorias que se esten haciendo presentes.
            '''
            #self.player.in_round(self.round_number - 1).payoff
            lista_grupo=random.sample(lista_all,k=self.group.in_round(self.round_number - 1).grupos_auditado)
            print("el numero de participantes a auditar: ",self.group.in_round(self.round_number - 1).grupos_auditado)
            #lista_grupo=choice(lista_all)
            for grupo in lista_grupo:
                print("\n el id del grupo escogido es : ", grupo.id_in_subsession) 
                if(grupo.aceptarCoima == 3):
                    print("\n el id del grupo auditado es : ", grupo.id_in_subsession)
                    grupo.auditado = True
                    grupos_auditados.append(grupo)

            if(len(grupos_auditados)>=3):
                self.group.grupos_auditado=8
                for grupo in lista_all:
                    grupo.total_pagar_firma= grupo.espol_firma + grupo.in_round(self.round_number - 1).total_pagar_firma
                    grupo.total_pagar_sp= grupo.espol_sp + grupo.in_round(self.round_number - 1).total_pagar_sp
                    grupo.grupos_auditado=8
            elif(len(grupos_auditados)==2):
                self.group.grupos_auditado=5
                for grupo in lista_all:
                    grupo.total_pagar_firma= grupo.espol_firma + grupo.in_round(self.round_number - 1).total_pagar_firma
                    grupo.total_pagar_sp= grupo.espol_sp + grupo.in_round(self.round_number - 1).total_pagar_sp
                    grupo.grupos_auditado=5
            elif(len(grupos_auditados)<=1):
                self.group.grupos_auditado=3
                for grupo in lista_all:
                    grupo.total_pagar_firma= grupo.espol_firma + grupo.in_round(self.round_number - 1).total_pagar_firma
                    grupo.total_pagar_sp= grupo.espol_sp + grupo.in_round(self.round_number - 1).total_pagar_sp
                    grupo.grupos_auditado=3

    def is_displayed(self):
        return self.group.id_in_subsession == 2

class Multa_Auditoria(WaitPage):
    form_model = 'group'

    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)

        #multa
        p1.payoff = p1.payoff - 8
        p2.payoff = p2.payoff - 8
        if(p1.payoff <0):
            p1.payoff = 0
        if(p2.payoff < 0):
            p2.payoff = 0

    def is_displayed(self):
        return self.group.auditado == 1



page_sequence = [
    reglas_experimento,
    player1,
    coima,
    WaitForP2,
    mensajes,
    WaitForP1,
    player2,
    WaitForP1,
    mensaje_token,
    WaitForP2,
    noReparticion,
    ResultsWaitPage,
    Results,
    Resulado_auditoria,
    AllGroupsWaitPage,
    Multa_Auditoria,
    auditoria
]
