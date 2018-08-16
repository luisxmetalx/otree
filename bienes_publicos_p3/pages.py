from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
rondas_fase2 = __import__('bienes_publicos_p4').models.Constants.num_rounds 
import utils
import random

class InstruccionesFase2(Page):
    #timeout_seconds = 15
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        puntos_asignados = [i for i in range(11)]
        puntos_reducidos = [0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30]
        return{
            'rondas_fase2': rondas_fase2,
            'distribucion': 'bienes_publicos/distribucion.png',
            'puntos_asignados': puntos_asignados,
            'puntos_reducidos': puntos_reducidos
        }

class Test2(Page):
    form_model = models.Player
    form_fields = ['test2_p1', 'test2_p2', 'test2_p3', 'test2_p4', 'test2_p5']

    def test2_p1_error_message(self, value):
        if value != 36:
            return 'Error en la pregunta 1'
        else:
            self.player.participant.vars["test2_p1"] = 36
            print ('Respuesta correcta! --> ', self.player.participant.vars["test2_p1"])

    def test2_p2_error_message(self, value):
        if value != 10:
            return 'Error en la pregunta 2'
        else:
            self.player.participant.vars["test2_p2"] = 10
            print ('Respuesta correcta! --> ', self.player.participant.vars["test2_p2"])
    
    def test2_p3_error_message(self, value):
        if value != 1:
            return 'Error en la pregunta 3'
        else:
            self.player.participant.vars["test2_p3"] = 1
            print ('Respuesta correcta! --> ', self.player.participant.vars["test2_p3"])
    
    def test2_p4_error_message(self, value):
        if value != 21:
            return 'Error en la pregunta 4'
        else:
            self.player.participant.vars["test2_p4"] = 21
            print ('Respuesta correcta! --> ', self.player.participant.vars["test2_p4"])
    
    def test2_p5_error_message(self, value):        
        if value != 35:
            return 'Error en la pregunta 5'
        else:
            self.player.participant.vars["test2_p5"] = 35
            print ('Respuesta correcta! --> ', self.player.participant.vars["test2_p5"])

    def is_displayed(self):
        
        self.player.participant.vars["test2_p1"] = None
        self.player.participant.vars["test2_p2"] = None
        self.player.participant.vars["test2_p3"] = None
        self.player.participant.vars["test2_p4"] = None
        self.player.participant.vars["test2_p5"] = None
        return self.subsession.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        ronda_actual = self.subsession.round_number
        
        sup_p1 = "Suponga que otros integrantes (A, B, C, D) de su grupo asignan 5 (A) + 10 (B) + 10 (C) + 15 (D) puntos a la cuenta grupal."
        preg1 = "1) ¿Cuánto ganaría usted en esa ronda si asigna 0 puntos a la cuenta grupal y el administrador no asigna puntos para reducir las ganancias de ningún miembro del grupo?"
    
        sup_p2 = "Suponga que usted es el administrador. Cada integrante del grupo le entrega 2 puntos que pueden ser usados para reducir las ganancias de los miembros del grupo."
        preg2 = "2) Como administrador, ¿cuántos puntos obtiene usted para reducir las ganancias de los otros miembros del grupo?"

        sup_p3 = "Suponga que usted es el administrador. Ahora usted tiene 10 puntos que puede usar para reducir las ganancias de los miembros del grupo. Cada punto que asigne a cualquier miembro del grupo reduce las ganancias del receptor (puntos reducidos) de acuerdo a la tabla señalada (ver las instrucciones). Los puntos no utilizados serán devueltos a todos los integrantes del grupo equitativamente."
        preg3 = "3) Como administrador, suponga que decide reducir 3 puntos al individuo A y 2 puntos al individuo B, en total 5 puntos asignados. ¿Cuántos puntos se devolverán a cada integrante del grupo?"

        sup_p4 = "Suponga nuevamente que usted el administrador de su grupo. Usted dispone de 10 puntos para reducir las ganancias de los demás miembros. Usted aporta 0 puntos a la cuenta grupal mientras que otros participantes (A, B, C, D) en su grupo aportan 5 (A) + 10 (B) + 10 (C) + 15 (D) puntos a la cuenta grupal.\nSuponga que usa 5 puntos para reducir las ganancias del participante A (esto quiere decir, según la tabla, que las ganancias del participante A, se reducen 9 puntos)."
        preg4 = "4) ¿Cuánto ganará el participante A?"
        preg5 = "5) ¿Cuánto ganaría usted?"

        indices = [i for i in range(1,5)]
        supuestos = [sup_p1, sup_p2, sup_p3, sup_p4]
        preguntas = [preg1, preg2, preg3, preg4]

        respuestas = [36, 10, 1, 21, 35]
        return {
                'test2': 0,
                'rondas': Constants.num_rounds,
                'ronda_actual': ronda_actual,
                'puntos_asignados': Constants.puntos_asignados,
                'puntos_reducidos': Constants.puntos_reducidos,
                'preguntas': zip(indices, supuestos, preguntas),
                'preg5': preg5,
                'indices': indices,
                'respuestas': respuestas                
                }

class EsperaVotacion(WaitPage):
    def after_all_players_arrive(self):
        print ('...after all arrive...')
        self.group.obtenerTratamiento()
        if self.group.tratamiento == 'leviatan':
            print ('Leviatan --> Se sortea')
            if self.group.administrador == 0:
                self.group.sortear_admin_lev()
            else:
                print ('ya se ha sorteado administrador del grupo')


class ElegirAdministrador(Page):
    form_model = models.Player
    form_fields = ['voto']

    def vars_for_template(self):
        rondas = []
        for i in range(len(self.player.participant.vars["contribuciones"])):
            rondas.append(i+1)
        
        contribuciones = []
        for i in rondas:
            cont = []
            for otro in self.player.get_others_in_group():
                cont.append(otro.participant.vars["contribuciones"][i-1])
            contribuciones.append(cont)

        #print ('contribuciones de otros: ', contribuciones)
        contribuciones_propias = self.player.participant.vars["contribuciones"]

        for i in range(len(contribuciones)):
            contribuciones[i].insert(0, contribuciones_propias[i])

        #print ('contribuciones todos: ', contribuciones)
        
        return {
            'rondas': rondas,
            'acumulado': self.player.participant.vars["acumulado"],
            'contribuciones_por_ronda': zip(rondas, contribuciones)
        }


class FinalVotacion(WaitPage):
    def is_displayed(self):
        print('self.group.tratamiento --> ', self.group.tratamiento)
        return self.group.tratamiento == 'democracia'

    def after_all_players_arrive(self):
        print('....')
        self.group.contarVotos()
        admin = self.group.obtener_admin_dem()
        print('administrador | dem: ', admin)

class ResultadosVotacion(Page):
    #timeout_seconds = 15
    def is_displayed(self):
        #self.player.ganVCM()
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        rondas = []
        for i in range(len(self.player.participant.vars["contribuciones"])):
            rondas.append(i+1)
        
        contribuciones = []
        for i in rondas:
            cont = []
            for otro in self.player.get_others_in_group():
                cont.append(otro.participant.vars["contribuciones"][i-1])
            contribuciones.append(cont)

        #print ('contribuciones de otros: ', contribuciones)
        contribuciones_propias = self.player.participant.vars["contribuciones"]

        for i in range(len(contribuciones)):
            contribuciones[i].insert(0, contribuciones_propias[i])

        for jugador in self.group.get_players():
            jugador.participant.vars["admin"] = self.group.administrador

        #print ('contribuciones todos: ', contribuciones)

        return{
                'tratamiento': self.player.tratamiento,
                'rondas': rondas,
                'acumulado': self.player.participant.vars["acumulado"],
                'contribuciones_por_ronda': zip(rondas, contribuciones)
            }

class FinalFase1(Page):
    pass


page_sequence = [
    FinalFase1,
    InstruccionesFase2,
    Test2,
    EsperaVotacion,
    ElegirAdministrador,
    FinalVotacion,
    ResultadosVotacion    
]
