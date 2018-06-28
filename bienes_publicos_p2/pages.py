from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import utils
import random


class Contribuir(Page):
    #timeout_seconds = 15
    #timeout_submission = {'contribucion': -1}
    form_model = models.Player
    form_fields = ['contribucion']

    def vars_for_template(self):
        ronda_actual = self.subsession.round_number        
        return {
                'rondas': Constants.num_rounds,
                'ronda_actual': ronda_actual,
                }

    def before_next_page(self):
        if self.player.contribucion == -1:
            self.player.contribucion = utils.contribucion_aleatoria()
        
        # acumula en cada participante las contirbuciones para VCM
        self.player.participant.vars["acumulado"] += self.player.contribucion
        print("el acumulado es: ",self.player.participant.vars["acumulado"])

        self.player.participant.vars["contribuciones"].append(self.player.contribucion)

        # genera una lista aleatoria con los indices de los demas participantes en su grupo y se almacena esta en el diccionario
        otros_jugadores = [p.id_in_group for p in self.player.get_others_in_group()]
        random.shuffle(otros_jugadores)
        self.player.participant.vars["jugadores_random"] = otros_jugadores
        print ('Otros jugadores: ', otros_jugadores)
        


class FinContribuciones(WaitPage):
    def after_all_players_arrive(self):
        self.group.cacularGanancias()


class Resultados(Page):
    #timeout_seconds = 60
    def is_displayed(self):
        if self.subsession.round_number == Constants.num_rounds:
            self.player.calcularGananciaAcumlada()
        return True

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

        print("\t*********************************")
        print("\t\tJugador: ", self.player.id_in_group, "| Grupo: ", self.group.id_in_subsession, " | Ronda: ", self.subsession.round_number)
        print('\tganancia: ', self.player.ganancia)
        print('\tfondo: ', Constants.fondo)
        print('\tcontribución hecha: ', self.player.contribucion)
        print("\t*********************************")

        return{
                'lista_jugadores': otros_jugadores,
                'ganancia': Constants.fondo - self.player.contribucion,
                'porcentaje_propio': round(self.player.contribucion/Constants.fondo*100,2),
                'ganancia_grupo': round(self.player.ganancia - Constants.fondo + self.player.contribucion,2),
                'rondas': Constants.num_rounds,
                'ronda_actual': ronda_actual,
                'contribuciones': contribuciones,
                'porcentajes': porcentajes,
                'ganancias': ganancias
                }



page_sequence = [
    Contribuir,
    FinContribuciones,
    Resultados,
]
