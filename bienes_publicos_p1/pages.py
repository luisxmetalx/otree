from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Bienvenida(Page):
    #timeout_seconds = 15
    form_model = models.Player
    form_fields = ['matricula']
    def is_displayed(self):
        self.player.calcularNumMaquina()
        return True

    def before_next_page(self):
        
        self.player.participant.vars["matricula"] = self.player.matricula
        matricula = self.player.participant.vars["matricula"]
        self.player.participant.vars["tratamiento"] = self.group.tratamiento
        tratamiento = self.player.participant.vars["tratamiento"]
        print('pasar matricula a dicc del participante: ', matricula)
        print('pasar tratamiento a dicc del participante: ', tratamiento)


class Instrucciones(Page):
    #timeout_seconds = 15
    def is_displayed(self):
        #print('rondas fase1: ', rondas_fase1)
        return True
    
    def vars_for_template(self):
        return {
                #'rondas_fase1': rondas_fase1,
                
                #'rondas_totales': rondas_fase1 + rondas_fase2
                }


class InstruccionesFase1(Page):
    #timeout_seconds = 15
    def is_displayed(self):
        return True
    
    def vars_for_template(self):
        return {#'rondas_fase1': rondas_fase1
        }


class Test1(Page):
    form_model = models.Player
    form_fields = ['test1_p1', 'test1_p2', 'test1_p3', 'test1_p4']

    def test1_p1_error_message(self, value):
        if value != 20:
            return 'Error en la pregunta 1'
        else:
            self.player.participant.vars["test1_p1"] = 20
            print ('Respuesta correcta! --> ', self.player.participant.vars["test1_p1"])

    def test1_p2_error_message(self, value):
        if value != 52:
            return 'Error en la pregunta 2'
        else:
            self.player.participant.vars["test1_p2"] = 52
            print ('Respuesta correcta! --> ', self.player.participant.vars["test1_p2"])
    
    def test1_p3_error_message(self, value):
        if value != 26:
            return 'Error en la pregunta 3'
        else:
            self.player.participant.vars["test1_p3"] = 26
            print ('Respuesta correcta! --> ', self.player.participant.vars["test1_p3"])
    
    def test1_p4_error_message(self, value):
        if value != 16:
            return 'Error en la pregunta 4'
        else:
            self.player.participant.vars["test1_p4"] = 16
            print ('Respuesta correcta! --> ', self.player.participant.vars["test1_p4"])
    
    
    def is_displayed(self):
        return True
    
    def vars_for_template(self):
        
        ronda_actual = self.subsession.round_number
        
        sup_p1 = "Suponga que en una ronda todos los integrantes de su grupo (incluyendo usted) asignan 0 puntos a la cuenta grupal."
        preg1 = "1) ¿Cuánto ganaría usted en esa ronda?"

        sup_p2 = "Suponga que en una ronda los demás integrantes de su grupo asignan cada uno 20 puntos a la cuenta grupal."
        preg2 = "2) ¿Cuánto ganaría usted en esa ronda si asigna 0 puntos a la cuenta grupal?"

        sup_p3 = "Suponga que en una ronda todos los integrantes de su grupo (incluyendo usted) asignan, en total, 40 puntos a la cuenta del grupo."
        preg3 = "3) ¿Cuánto ganaría usted en esa ronda si asignó 10 puntos a la cuenta grupal?"
        preg4 = "4) ¿Cuánto ganaría usted en esa ronda si asignó 20 puntos a la cuenta grupal?"
        
        indices = [i for i in range(1,4)]
        supuestos = [sup_p1, sup_p2, sup_p3]
        preguntas = [preg1, preg2, preg3]

        respuestas = [20, 52, 26, 16]
        return {
                'test1': 0,
                'rondas': Constants.num_rounds,
                'ronda_actual': ronda_actual,
                'preguntas': zip(indices, supuestos, preguntas),
                'respuestas': respuestas,
                'preg4': preg4,
                }

page_sequence = [    
    Instrucciones,
    InstruccionesFase1,
    #Test1
]