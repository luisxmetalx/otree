from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from bienes_publicos_p4 import utils
import random


class WP_contribuir(WaitPage):
    pass

class EnviarMensaje(Page):
    form_model = models.Group
    form_fields = ['contribucion_minima']

    def is_displayed(self):
        return self.session.config['control'] != 0 and self.player.id_in_group == self.player.participant.vars.get("admin")

    def vars_for_template(self):
        control = self.session.config['control']

        return {
            'control': control
        }
    
    

class Contribuir(Page):
    #timeout_seconds = 15
    #timeout_submission = {'contribucion': -1}
    form_model = models.Player
    form_fields = ['contribucion']

    def contribucion_min(self):
        if self.session.config['control'] == 1:    
            return self.group.contribucion_minima
        else:
            return 0

    def vars_for_template(self):
        ronda_actual = self.subsession.round_number
        control = self.session.config['control']        
        return {
                'rondas': Constants.num_rounds,
                'ronda_actual': ronda_actual,
                'puntos_asignados': Constants.puntos_asignados,
                'puntos_reducidos': Constants.puntos_reducidos,
                'control': control
                }

    def before_next_page(self):
        if self.player.contribucion == -1:
            self.player.contribucion = utils.contribucion_aleatoria()
       
        # acumula en cada participante las contirbuciones para VCM y VCM-Tax/Punishment
        if self.subsession.round_number > Constants.num_rounds:
            self.player.participant.vars["acumulado"] = 0
        self.player.participant.vars["acumulado"] += self.player.contribucion

        # genera una lista aleatoria con los indices de los demas participantes en su grupo y se almacena esta en el diccionario
        otros_jugadores = [p.id_in_group for p in self.player.get_others_in_group()]
        random.shuffle(otros_jugadores)
        self.player.participant.vars["jugadores_random"] = otros_jugadores
        print ('Otros jugadores: ', otros_jugadores)
        


class FinContribuciones(WaitPage):
    def after_all_players_arrive(self):
        self.group.cacularGanancias()


class EsperaCastigo(WaitPage):
    def is_displayed(self):
        print ('view EsperaCastigo --> id: ', self.player.id_in_group, ', admin : ', self.player.participant.vars.get("admin"))
        return True

class AplicarCastigo(Page):
    form_model = models.Group
    
    def get_form_fields(self):
        if self.player.id_in_group == 1:
            return ['castigo_jug2', 'castigo_jug3', 'castigo_jug4', 'castigo_jug5']
        elif self.player.id_in_group == 2:
            return ['castigo_jug1', 'castigo_jug3', 'castigo_jug4', 'castigo_jug5']
        elif self.player.id_in_group == 3:
            return ['castigo_jug1', 'castigo_jug2', 'castigo_jug4', 'castigo_jug5']
        elif self.player.id_in_group == 4:
            return ['castigo_jug1', 'castigo_jug2', 'castigo_jug3', 'castigo_jug5']
        elif self.player.id_in_group == 5:
            return ['castigo_jug1', 'castigo_jug2', 'castigo_jug3', 'castigo_jug4']
    
    def error_message(self, values):
        for k, v in values.items():
            if v == None:
                values[k] = 0
        if self.player.id_in_group == 1:
            if values["castigo_jug2"] + values["castigo_jug3"] + values["castigo_jug4"] + values["castigo_jug5"] > 10:
                return 'La suma de los puntos asignados no debe superar 10'
        elif self.player.id_in_group == 2:
            if values["castigo_jug1"] + values["castigo_jug3"] + values["castigo_jug4"] + values["castigo_jug5"] > 10:
                return 'La suma de los puntos asignados no debe superar 10'
        elif self.player.id_in_group == 3:
            if values["castigo_jug1"] + values["castigo_jug2"] + values["castigo_jug4"] + values["castigo_jug5"] > 10:
                return 'La suma de los puntos asignados no debe superar 10'
        elif self.player.id_in_group == 4:
            if values["castigo_jug1"] + values["castigo_jug2"] + values["castigo_jug3"] + values["castigo_jug5"] > 10:
                return 'La suma de los puntos asignados no debe superar 10'
        elif self.player.id_in_group == 5:
            if values["castigo_jug1"] + values["castigo_jug2"] + values["castigo_jug3"] + values["castigo_jug4"] > 10:
                return 'La suma de los puntos asignados no debe superar 10'
    

    def is_displayed(self):
        print ('view castigo --> id: ', self.player.id_in_group, ', admin : ', self.player.participant.vars.get("admin"))
        return self.player.id_in_group == self.player.participant.vars.get("admin")

    def vars_for_template(self):
        otros_jugadores = self.player.participant.vars["jugadores_random"]
        
        contribuciones = []
        ganancias = []

        for indice in otros_jugadores:
            actual = self.group.get_player_by_id(indice)
            ganancias.append(actual.ganancia)
            contribuciones.append(actual.contribucion)

        porcentajes = []        
        for con in contribuciones:
            porcentajes.append(round(con/Constants.fondo*100,2))

        ronda_actual = self.subsession.round_number
        
        puntos_disponibles = Constants.tao*Constants.players_per_group

        control = self.session.config['control']

        return {
                'puntos_disponibles': puntos_disponibles,
                'rondas': Constants.num_rounds,
                'puntos_asignados': Constants.puntos_asignados,
                'lista_jugadores': otros_jugadores,
                'contribuciones': contribuciones,
                'porcentaje_propio': round(self.player.contribucion/Constants.fondo*100,2),
                'porcentajes': porcentajes,
                'ganancias': ganancias,
                'puntos_reducidos': Constants.puntos_reducidos,
                'ronda_actual': ronda_actual,
                'control': control
                }

    def before_next_page(self):
        print('castigo jug1', self.group.castigo_jug1)
        print('castigo jug2', self.group.castigo_jug2)
        print('castigo jug3', self.group.castigo_jug3)
        print('castigo jug4', self.group.castigo_jug4)
        print('castigo jug5', self.group.castigo_jug5)

        for jugador in self.player.get_others_in_group():
            if jugador.id_in_group == 1:
                c = utils.puntosReducidos(self.group.castigo_jug1, jugador)
                jugador.castigo = c
            elif jugador.id_in_group == 2:
                c = utils.puntosReducidos(self.group.castigo_jug2, jugador)
                jugador.castigo = c
            elif jugador.id_in_group == 3:
                c = utils.puntosReducidos(self.group.castigo_jug3, jugador)
                jugador.castigo = c
            elif jugador.id_in_group == 4:
                c = utils.puntosReducidos(self.group.castigo_jug4, jugador)
                jugador.castigo = c
            elif jugador.id_in_group == 5:
                c = utils.puntosReducidos(self.group.castigo_jug5, jugador)
                jugador.castigo = c

        for p in self.group.get_players():
            print ('jugador: ', p.id_in_group, ' --> puntos recibidos: ', p.castigo)
            castigo = p.calcular_castigo()
            print ('jugador: ', p.id_in_group, ' --> tax/punish: ', castigo)
            p.aplicar_castigo()


class ResultadosCastigo(Page):
    timeout_seconds = 60
    def is_displayed(self):
        print ('view ResultadosCastigo --> id: ', self.player.id_in_group, ', admin : ', self.player.participant.vars.get("admin"))
        return True

    def vars_for_template(self):
        otros_jugadores = self.player.participant.vars["jugadores_random"]
        
        contribuciones = []
        ganancias = []

        for indice in otros_jugadores:
            actual = self.group.get_player_by_id(indice)
            ganancias.append(actual.gan_tp)
            contribuciones.append(actual.contribucion)

        porcentajes = []        
        for con in contribuciones:
            porcentajes.append(round(con/Constants.fondo*100,2))

        ronda_actual = self.subsession.round_number
                
        ganancia_grupo = self.player.ganancia - Constants.fondo + self.player.contribucion

        return {
                'rondas': Constants.num_rounds,
                'ronda_actual': ronda_actual,
                'lista_jugadores': otros_jugadores,
                'contribuciones': contribuciones,
                'ganancia_grupo': round(ganancia_grupo,2),
                'total_puntos_asignados': sum([ p.pts_asignados for p in self.group.get_players() ]),
                'porcentaje_propio': round(self.player.contribucion/Constants.fondo*100,2),
                'porcentajes': porcentajes,
                'ganancias': ganancias,
                'ganancia_sin_tp': round(self.player.ganancia + self.player.tp, 1),
                'puntos_asignados': Constants.puntos_asignados,
                'puntos_reducidos': Constants.puntos_reducidos
                }

    def before_next_page(self):
        if self.subsession.round_number == Constants.num_rounds:
            self.player.calcular_pago()
            print ('Ganancias totales de jugador:', self.player.id_in_group, ' --> ', self.player.ganancias_totales)
            print ('Valor en USD ganado: ', self.player.payoff)


class Final(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        pago = self.player.calcular_pago()
        self.player.participant.vars["pago_bp"] = pago
        print ('pago: ', pago)
        return {'pago': pago}

page_sequence = [
    EnviarMensaje,
    WP_contribuir,
    Contribuir,
    FinContribuciones,
    AplicarCastigo,
    EsperaCastigo,
    ResultadosCastigo,
    Final
]
