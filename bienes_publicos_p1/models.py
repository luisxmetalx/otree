from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import numpy as np

author = 'Washington Vélez'

doc = """
Bienes públicos: Bienvenida, Instrucciones, Test1
"""

def generar_Dicc_Ip():
    dicc_ip = {}
    indice = 194
    for i in range(1, 36):
        dicc_ip[indice] = i
        indice += 1
    #for k, v in dicc_ip.items():
        #print (k, ' --> ', v)
    return dicc_ip


class Constants(BaseConstants):
    name_in_url = 'bienes_publicos_p1'
    players_per_group = 5
    num_rounds = 1
    fondo = 20
        
    modalF1 = 'bienes_publicos/modalInstF1.html'
    

class Subsession(BaseSubsession):
    def creating_session(self):
        # se guarda el diccionario de ip's como variable de sesión
        self.session.vars['dicc_ip'] = generar_Dicc_Ip()
        
        total_grupos = len([g for g in self.get_groups()])
        print('Grupos en la sesión: ', total_grupos)
        grupos_leviatan = self.session.config['grupos_leviatan']
        grupos_democracia = self.session.config['grupos_democracia']

        if grupos_democracia + grupos_leviatan == 0 or grupos_democracia + grupos_leviatan > total_grupos:
            # Mayor o menor cantidad de tratamientos por grupos que los grupos totales o
            # Suma de grupos asignados por tratamientos igual a cero
            print ('\nCanitdad incorrecta de grupos ingresados. Se asignarán los tratamientos de manera aleatoria\n')
            for g in self.get_groups():
                # se asigna para los grupos impares 'democracia' y para los pares 'leviatan'
                for actual in g.in_all_rounds():
                    if actual.id % 2 == 1:
                        actual.tratamiento = 'democracia'
                    else:
                        actual.tratamiento = 'leviatan'
                    print('Grupo: ', actual.id_in_subsession, '| tratamiento: ', actual.tratamiento)
        
        elif grupos_democracia + grupos_leviatan == total_grupos:
            for g in self.get_groups()[:grupos_democracia]:
                print('Grupo asignado a tratamiento democracia: ', g.id_in_subsession)
                for actual in g.in_all_rounds():
                    actual.tratamiento = 'democracia'
            for g in self.get_groups()[-grupos_leviatan:]:
                print('Grupo asignado a tratamiento leviatan: ', g.id_in_subsession)
                for actual in g.in_all_rounds():
                    actual.tratamiento = 'leviatan'
        
        elif grupos_democracia + grupos_leviatan == total_grupos and grupos_democracia == 0:
            for g in self.get_groups():
                print('Grupo asignado a tratamiento leviatan: ', g.id_in_subsession)
                for actual in g.in_all_rounds():
                    actual.tratamiento = 'leviatan'
        
        elif grupos_democracia + grupos_leviatan == total_grupos and grupos_leviatan ==0:
            for g in self.get_groups():
                print('Grupo asignado a tratamiento democracia: ', g.id_in_subsession)
                for actual in g.in_all_rounds():
                    actual.tratamiento = 'democracia'
        
        elif grupos_democracia + grupos_leviatan < total_grupos:
            sub_grupo = [grupo.id_in_subsession for grupo in self.get_groups()[:grupos_democracia + grupos_leviatan]]
            print('sub grupo: ', sub_grupo)

            sub_grupo_demo = [grupo.id_in_subsession for grupo in self.get_groups()[:grupos_democracia]]
            print('sub grupo demo: ', sub_grupo_demo)
            for g in self.get_groups()[:grupos_democracia]:
                print('Grupo asignado a tratamiento democracia: ', g.id_in_subsession)
                for actual in g.in_all_rounds():
                    actual.tratamiento = 'democracia'
            sub_grupo_lev = [grupo.id_in_subsession for grupo in self.get_groups()[grupos_democracia: grupos_democracia + grupos_leviatan]]
            print('sub grupo lev: ', sub_grupo_lev)
            for g in self.get_groups()[grupos_democracia: grupos_democracia + grupos_leviatan]:
                print('Grupo asignado a tratamiento leviatan: ', g.id_in_subsession)
                for actual in g.in_all_rounds():
                    actual.tratamiento = 'leviatan'

            for g in self.get_groups()[grupos_democracia + grupos_leviatan:]:
                # se asigna para los grupos impares 'democracia' y para los pares 'leviatan'
                for actual in g.in_all_rounds():
                    if actual.id % 2 == 1:
                        actual.tratamiento = 'democracia'
                    else:
                        actual.tratamiento = 'leviatan'
                    print('Grupo: ', actual.id_in_subsession, '| tratamiento: ', actual.tratamiento)


        for g in self.get_groups():    
            for jugador in g.get_players():
                jugador.tratamiento = g.tratamiento
                jugador.participant.vars['tratamiento'] = jugador.tratamiento
                

class Group(BaseGroup):
    tratamiento = models.CharField()        

class Player(BasePlayer):
    matricula = models.PositiveIntegerField(min=199000000, max=201799999)
    
    maquina = models.PositiveIntegerField()
        
    tratamiento = models.CharField()
    
    # test1_p1 = models.IntegerField(initial=0)
    # test1_p2 = models.IntegerField(initial=0)
    # test1_p3 = models.IntegerField(initial=0)
    # test1_p4 = models.IntegerField(initial=0)

    def calcularNumMaquina(self):
        ip = str(self.participant.ip_address)
        if not ip.startswith('200.126.3.'):
            self.maquina = 0
        else:
            maq = int(ip[-3:])
            self.maquina = self.session.vars['dicc_ip'][maq]