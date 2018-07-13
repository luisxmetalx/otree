from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
#rondas_fase2 = __import__('bienes_publicos_p4').models.Constants.num_rounds 
from bienes_publicos_p5 import utils
import random

class InstruccionesFase2(Page):
    #timeout_seconds = 15
    def is_displayed(self):
        return self.subsession.round_number == 1
    
    def vars_for_template(self):
        puntos_asignados = [i for i in range(11)]
        puntos_reducidos = [0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30]
        return{
            #'rondas_fase2': rondas_fase2,
            #'distribucion': 'static/bienes_publicos/distribucion.png',
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
        return self.round_number == 1
    
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
    def is_displayed(self):
        return self.round_number==1 or self.round_number==4 or self.round_number==7 or self.round_number==10

    def after_all_players_arrive(self):
        print ('...after all arrive...')
        self.group.obtenerTratamiento()
        self.group.administrador = 0
        

        if self.group.tratamiento == 'leviatan':
            print ('Leviatan --> Se sortea')
            print("el adm es: ",self.group.administrador)
            if(self.group.administrador == 0):
                self.group.sortear_admin_lev()
            else:
                print ('ya se ha sorteado administrador del grupo')
            print("el adm es: ",self.group.administrador)

class ElegirAdministrador(Page):
    form_model = models.Player
    form_fields = ['voto']

    def is_displayed(self):
        return self.round_number==1 or self.round_number==4 or self.round_number==7 or self.round_number==10

    def vars_for_template(self):
        rondas = []
        if(self.round_number==1):
            for i in range(len(self.player.participant.vars["contribuciones"])):
                rondas.append(i+1)
        else:
            for i in range(3):
                rondas.append(self.round_number-i-1)
                rondas=sorted(rondas)

        #print(rondas)
        #print(self.round_number)
        #print(sorted(rondas))
        contribuciones = []
        if(self.round_number==1):
            for i in rondas:
                cont = []
                print("el numero de participantes: ", len(self.player.get_others_in_group()))
                for otro in self.player.get_others_in_group():
                    #sc="contribucion"+str(i)+": " + str(otro.participant.vars["contribuciones"][i-1])
                    #print(sc)
                    cont.append(otro.participant.vars["contribuciones"][i-1])
                contribuciones.append(cont)
                print(contribuciones)
        else:
            
            print("el numero de participantes: ", len(self.player.get_others_in_group()))
            for otro in self.player.get_others_in_group():
                cont = []
                for j in range(3):
                    sc="contribucion"+str(j)+": " + str(otro.in_round(self.round_number - (j+1)).contribucion)
                   #print(sc)
                    cont.append(otro.in_round(self.round_number - (3-j)).contribucion)
                    #print(cont)
                contribuciones.append(cont)
                print(contribuciones)
            #sacar las contribuciones por ronda.
            lista_rondas=[]
            r1=[]
            r2=[]
            r3=[]
            #ronda1
            for i in range(len(contribuciones)):
                r1.append(contribuciones[i][0])
            #print(r1)
            lista_rondas.append(r1)
            #ronda2
            for i in range(len(contribuciones)):
                r2.append(contribuciones[i][1])
            lista_rondas.append(r2)
            #ronda3
            for i in range(len(contribuciones)):
                r3.append(contribuciones[i][2])
            lista_rondas.append(r3)
            contribuciones=lista_rondas
            print("las contribuciones por las 3 rondas son: ",contribuciones)
                


        #print ('contribuciones de otros: ', contribuciones)
        contribuciones_propias = self.player.participant.vars["contribuciones"]
        if(self.round_number==1):
            for i in range(len(contribuciones)):
                contribuciones[i].insert(0, contribuciones_propias[i])
        else:
            cont_propia=[]
            for i in range(3):
                contribuciones[i].insert(0,self.player.in_round(self.round_number - (3-i)).contribucion)
            print("las contribuciones propias son: ",cont_propia)
            print("las contribuciones por las 3 rondas son: ",contribuciones)

        #print ('contribuciones todos: ', contribuciones)
        # elegir otra letra de participante
        if(self.round_number==4 or self.round_number==7 or self.round_number==10):
            # for p in self.group.get_players():
            #     p.roleP = ''
            for jugador in self.group.get_players():
                jugador.roleP = jugador.in_round(self.round_number-3).roleP
                    
                
        return {
            'rondas': rondas,
            'acumulado': self.player.participant.vars["acumulado"],
            'contribuciones_por_ronda': zip(rondas, contribuciones),
            'playerRol': self.player.roleP
        }
    


class FinalVotacion(WaitPage):
    def is_displayed(self):
        print('self.group.tratamiento --> ', self.group.tratamiento)
        return self.group.tratamiento == 'democracia' and (self.round_number==1 or self.round_number==4 or self.round_number==7 or self.round_number==10)

    def after_all_players_arrive(self):
        print('....')
        self.group.contarVotos()
        admin = self.group.obtener_admin_dem()
        print('administrador | dem: ', admin)

class ResultadosVotacion(Page):
    #timeout_seconds = 15
    def is_displayed(self):
        #self.player.ganVCM()
        return (self.round_number==1 or self.round_number==4 or self.round_number==7 or self.round_number==10)

    def vars_for_template(self):
        rondas = []
        acumulado = []
        if(self.round_number==1):
            for i in range(len(self.player.participant.vars["contribuciones"])):
                rondas.append(i+1)
        else:
            for i in range(3):
                rondas.append(self.round_number-i-1)
                rondas=sorted(rondas)
        
        contribuciones = []
        if(self.round_number==1):
            for i in rondas:
                cont = []
                print("el numero de participantes: ", len(self.player.get_others_in_group()))
                for otro in self.player.get_others_in_group():
                    #sc="contribucion"+str(i)+": " + str(otro.participant.vars["contribuciones"][i-1])
                    #print(sc)
                    cont.append(otro.participant.vars["contribuciones"][i-1])
                contribuciones.append(cont)
                print(contribuciones)
        else:
            
            print("el numero de participantes: ", len(self.player.get_others_in_group()))
            for otro in self.player.get_others_in_group():
                cont = []
                for j in range(3):
                    sc="contribucion"+str(j)+": " + str(otro.in_round(self.round_number - (j+1)).contribucion)
                   #print(sc)
                    cont.append(otro.in_round(self.round_number - (3-j)).contribucion)
                    #print(cont)
                contribuciones.append(cont)
                print(contribuciones)
            #sacar las contribuciones por ronda.
            lista_rondas=[]
            r1=[]
            r2=[]
            r3=[]
            #ronda1
            for i in range(len(contribuciones)):
                r1.append(contribuciones[i][0])
            #print(r1)
            lista_rondas.append(r1)
            #ronda2
            for i in range(len(contribuciones)):
                r2.append(contribuciones[i][1])
            lista_rondas.append(r2)
            #ronda3
            for i in range(len(contribuciones)):
                r3.append(contribuciones[i][2])
            lista_rondas.append(r3)
            contribuciones=lista_rondas
            print("las contribuciones por las 3 rondas son: ",contribuciones)

        #print ('contribuciones de otros: ', contribuciones)
        # elegir otra letra de participante
        if(self.round_number==4 or self.round_number==7 or self.round_number==10):
            # for p in self.group.get_players():
            #     p.roleP = ''
            for jugador in self.group.get_players():
                jugador.roleP = jugador.in_round(self.round_number-3).roleP

        contribuciones_propias = self.player.participant.vars["contribuciones"]

        if(self.round_number==1):
            for i in range(len(contribuciones)):
                contribuciones[i].insert(0, contribuciones_propias[i])
        else:
            cont_propia=[]
            for i in range(3):
                contribuciones[i].insert(0,self.player.in_round(self.round_number - (3-i)).contribucion)
            print("las contribuciones propias son: ",cont_propia)
            print("las contribuciones por las 3 rondas son: ",contribuciones)

        for jugador in self.group.get_players():
            jugador.participant.vars["admin"] = self.group.administrador
            print ('jugador admin todos: ', jugador.participant.vars["admin"])

        print ('el acumulado es: ', self.player.participant.vars["acumulado"])
        print ("las contibuciones son: ", contribuciones)
        for p in self.group.get_players():
            if(p.id_in_group == self.group.administrador):
                adm = p.roleP
        
        for j in self.group.get_players():
            j.Jug_admin = adm

        return{
                'tratamiento': self.player.tratamiento,
                'rondas': rondas,
                'acumulado': self.player.participant.vars["acumulado"],
                'contribuciones_por_ronda': zip(rondas, contribuciones),
                'administrador': adm
            }

    def before_next_page(self):
        # elegir otra letra de participante
        if(self.round_number==4 or self.round_number==7 or self.round_number==10):
            if(self.player.roleP != ''):
                for p in self.group.get_players():
                    p.roleP = ''

            while(self.player.roleP == '' or self.player.roleP == None):
                acum=0            
                letra = random.choice(['A','B','C','D','E'])
                print("la letra escogida fue: ",letra)
                for jugador in self.player.get_others_in_group():
                    print("letra asignada fue: ",jugador.roleP)
                    if(jugador.roleP == letra):
                        acum+=1
                print("veces repetidas: ",acum)
                if(acum == 0):
                    print("letra no asiganada a ningunjugador")
                    self.player.roleP = letra
    # def before_next_page(self):
    #     for p in self.group.get_players():
    #         p.participant.vars["acumulado"] = 0
    #         print("entro a la parte de iniciaizar el acumulado")

class FinalFase1(Page):
    pass


# BP4
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
        #setear el acumulado a CERO en cada de las rondas
        if(self.round_number == 1 or self.round_number == 4 or self.round_number == 7 or self.round_number == 10 ):
                for p in self.group.get_players():
                    p.participant.vars["acumulado"] = 0
                    print("entro a la parte de iniciaizar el acumulado")
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
        print("la ronda de la subsesion es: ",self.subsession.round_number)
        if self.subsession.round_number > Constants.num_rounds:
            self.player.participant.vars["acumulado"] = 0
        self.player.participant.vars["acumulado"] += self.player.contribucion

        # genera una lista aleatoria con los indices de los demas participantes en su grupo y se almacena esta en el diccionario
        otros_jugadores = [p.id_in_group for p in self.player.get_others_in_group()]
        random.shuffle(otros_jugadores)
        self.player.participant.vars["jugadores_random"] = otros_jugadores
        print ('Otros jugadores: ', otros_jugadores)

        if(self.round_number==4 or self.round_number==7 or self.round_number==10):
            while(self.player.roleP == '' or self.player.roleP == None):
                acum=0            
                letra = random.choice(['A','B','C','D','E'])
                print("la letra escogida fue: ",letra)
                for jugador in self.player.get_others_in_group():
                    print("letra asignada fue: ",jugador.roleP)
                    if(jugador.roleP == letra):
                        acum+=1
                print("veces repetidas: ",acum)
                if(acum == 0):
                    print("letra no asiganada a ningunjugador")
                    self.player.roleP = letra
        


class FinContribuciones(WaitPage):
    def after_all_players_arrive(self):
        self.group.cacularGanancias()


class EsperaCastigo(WaitPage):
    def is_displayed(self):
        print ('view EsperaCastigo --> id: ', self.player.id_in_group, ', admin : ', self.player.participant.vars.get("admin"))
        return True
        
#aqui se debe de cambiar la condicon para que entre por la letra no por el id del jugador.
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
        n_ronda = 0
        for jugador in self.group.get_players():
            print("jugador seleccionados: ", jugador.in_round(1).roleP)
            print("jugador administrador: ", self.player.participant.vars.get("admin"))
            if self.round_number >= 1 and self.round_number < 4:
                n_ronda = 1
                if jugador.in_round(n_ronda).roleP == self.player.in_round(n_ronda).Jug_admin:
                    administrador = jugador.in_round(n_ronda).roleP
                    print("la letra del administrador es: ", administrador)
            elif self.round_number >= 4 and self.round_number < 7:
                n_ronda = 4
                if jugador.in_round(n_ronda).roleP == self.player.in_round(n_ronda).Jug_admin:
                    administrador = jugador.in_round(n_ronda).roleP
                    print("la letra del administrador es: ", administrador)
            elif self.round_number >= 7 and self.round_number < 10:
                n_ronda = 7
                if jugador.in_round(n_ronda).roleP == self.player.in_round(n_ronda).Jug_admin:
                    administrador = jugador.in_round(n_ronda).roleP
                    print("la letra del administrador es: ", administrador)

        return self.player.in_round(n_ronda).roleP == administrador

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
    #timeout_seconds = 60
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

class FinalFase1(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    
    def vars_for_template(self):
        print("la letra fue: ",self.player.roleP)
        # for p in self.group.get_players():
        #     p.roleP = ''
        while(self.player.roleP == '' or self.player.roleP == None):
            acum=0            
            letra = random.choice(['A','B','C','D','E'])
            print("la letra escogida fue: ",letra)
            for jugador in self.player.get_others_in_group():
                print("letra asignada fue: ",jugador.roleP)
                if(jugador.roleP == letra):
                    acum+=1
            print("veces repetidas: ",acum)
            if(acum == 0):
                print("letra no asiganada a ningunjugador")
                self.player.roleP = letra

                

        return{
            'role_participante':self.player.roleP,
        }

page_sequence = [
    FinalFase1,
    InstruccionesFase2,
    #Test2,
    EsperaVotacion,
    ElegirAdministrador,
    FinalVotacion,
    ResultadosVotacion,    
    #BP4
    EnviarMensaje,
    WP_contribuir,
    Contribuir,
    FinContribuciones,
    AplicarCastigo,
    EsperaCastigo,
    ResultadosCastigo,
    Final

]
