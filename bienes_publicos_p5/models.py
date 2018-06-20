from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import numpy as np

author = 'Luis Andrade'

doc = """
Bienes públicos: Instrucciones Fase2, Test2, Votación, Resultados de Votación
integración de las apps bienes_publico_p3 y bienes_publico_p4
"""

class Constants(BaseConstants):
    name_in_url = 'bienes_publicos_p5'
    players_per_group = 5
    num_rounds = 12
    fondo = 20
    fondo_castigo = 10
    tao = 2    

    #parte de bienes_publicos_p4
    valor_por_puntos = 0.020

    
    puntos_asignados = [i for i in range(11)]
    puntos_reducidos = [0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30]

    modalF2 = 'bienes_publicos/modalInstF2.html'

class Subsession(BaseSubsession):
    #parte de bienes_publicos_p4
    def creating_session(self):
        self.session.vars["dicc_puntos"] = {}

        for i in range(len(Constants.puntos_asignados)):
            self.session.vars["dicc_puntos"][Constants.puntos_asignados[i]] = Constants.puntos_reducidos[i]

class Group(BaseGroup):
    administrador = models.PositiveIntegerField(initial=0)

    tratamiento = models.CharField()

    def obtenerTratamiento(self):
        tratamientos = [jugador.participant.vars["tratamiento"] for jugador in self.get_players()]
        self.tratamiento = tratamientos[0]
        print ('tratamiento del grupo: ', self.id_in_subsession, ' :', self.tratamiento)

    def contarVotos(self):
        #setear valores a cero para q no escoja votos pasados
        for p in self.get_players():
            p.participant.vars["votos_recibidos"] = 0
        #suma de botos 
        for p in self.get_players():
            self.get_player_by_id(p.voto).participant.vars["votos_recibidos"] += 1
        for p in self.get_players():
            print ('id: ', p.id_in_group, 'votos recibidos: ', p.participant.vars["votos_recibidos"])
    
    # obtiene el administrador entre los votos de los participantes
    def obtener_admin_dem(self):
        votos = []
        for p in self.get_players():
            votos.append(p.voto)
        dicc_votos = {}
        for v in votos:
            if str(v) not in dicc_votos:
                dicc_votos[str(v)] = 1
            else:
                dicc_votos[str(v)] += 1

        print ('dicc_votos: ', dicc_votos)
        maximo = max(dicc_votos.values())
        print ('maximo: ', maximo)
        maximos = []
        indices_maximos = []

        for k, v in dicc_votos.items():
            print (k, ' --> ', v)
            if v == maximo:
                maximos.append(v)
                indices_maximos.append(k)

        #print ('maximos: ', indices_maximos)
        admin = random.choice(indices_maximos)
        #print ('admin --> ', admin)
        for g in self.in_rounds(1, Constants.num_rounds):
            g.administrador = admin

        return admin


    # sortea ganador con 75% de probabilidad de ser elegido el de mayor acumulado de contribuciones
    def sortear_admin_lev(self):
        prob_mayor = 0.75
        lista_contrib_acum = []
        for p in self.get_players():
            print ('Jugador: ', p.id_in_group, '  tiene: ', p.participant.vars["acumulado"])
            lista_contrib_acum.append(p.participant.vars["acumulado"])
        if sum(lista_contrib_acum) != 0:
            # hay al menos una contribución
            print ('lista contrib acum (ordenada por id de participante):', lista_contrib_acum)
            # se obtienen los indices de los valores maximos y los que no son maximo, 
            mayores = np.where(lista_contrib_acum == np.max(lista_contrib_acum))
            menores = np.where(lista_contrib_acum != np.max(lista_contrib_acum))

            indices_mayores = mayores[0].tolist()
            indices_menores = menores[0].tolist()

            sorteo = [np.max(lista_contrib_acum), -1]
            gana = np.random.choice(sorteo, p = [prob_mayor, 1 - prob_mayor])

            print('indices mayores: ', indices_mayores, type(indices_mayores))
            print('indices menores: ', indices_menores, type(indices_menores))

            #print ('gana: ', gana)
            if gana == -1:
                # gana uno que no tiene el maximo de contribuciones acumladas (p = 0.25)
                ind_ganador = np.random.choice(indices_menores)
            else:
                # gana uno que tiene el maximo de contribuciones acumladas (p = 0.75)
                ind_ganador = np.random.choice(indices_mayores)
            ganador = self.get_players()[ind_ganador]
            self.administrador = ganador.id_in_group
            admin = self.administrador
        else:
            #print ('nadie contribuyó nada')
            ganador = random.randint(1,5)
            self.administrador = ganador
            admin = self.administrador

        for g in self.in_rounds(1, Constants.num_rounds):
            g.administrador = admin
        #print ('grupo: ', self.id_in_subsession, '| administrador: ', admin)

        #BP4
        contribucion_total = models.IntegerField()

    # variables de el castigo a recibir para cada jugador
    castigo_jug1 = models.IntegerField(initial=0, min=0, max=20, blank=True)
    castigo_jug2 = models.IntegerField(initial=0, min=0, max=20, blank=True)
    castigo_jug3 = models.IntegerField(initial=0, min=0, max=20, blank=True)
    castigo_jug4 = models.IntegerField(initial=0, min=0, max=20, blank=True)
    castigo_jug5 = models.IntegerField(initial=0, min=0, max=20, blank=True)

    # variable para contribución mínima definida por el administrador
    contribucion_minima = models.IntegerField(initial=0, min=0, max=20)

    def cacularGanancias(self):
        # obtiene el acumulado de las contribuciones de cada participante y actualiza el modelo
        self.contribucion_total = sum([p.contribucion for p in self.get_players()])

        # Calcula la ganancia de cada jugador y actualiza el modelo (VCM)
        for jugador in self.get_players():
            ganancia = round(Constants.fondo - jugador.contribucion + (2/Constants.players_per_group)*self.contribucion_total, 2)
            jugador.ganancia = ganancia
        #print ('contribucion total actual: ', self.contribucion_total)

    

class Player(BasePlayer):
    tratamiento = models.CharField()
    voto = models.IntegerField()
    
    # test2_p1 = models.IntegerField(initial=0)
    # test2_p2 = models.IntegerField(initial=0)
    # test2_p3 = models.IntegerField(initial=0)
    # test2_p4 = models.IntegerField(initial=0)
    # test2_p5 = models.IntegerField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        elif self.id_in_group == 2:
            return 'B'
        elif self.id_in_group == 3:
            return 'C'
        elif self.id_in_group == 4:
            return 'D'
        else:
            return 'E'

    # BP4
    contribucion = models.IntegerField(min=0, max=20)
    ganancia = models.FloatField(initial=0)
    gan_tp = models.FloatField(initial=0)
    ganancias_totales = models.FloatField()

    # puntos asignados por el administrador
    castigo = models.IntegerField(initial=0)

    pts_asignados = models.IntegerField(initial=0)
    # valor calculado para aplicar castigo
    tp = models.FloatField(initial=0)

    # Calucla el castigo de un jugador y actualiza el modelo (Tax/Punishment)
    def calcular_castigo(self):
        acum_castigo = self.group.castigo_jug1 + self.group.castigo_jug2 + self.group.castigo_jug3 + self.group.castigo_jug4 + self.group.castigo_jug5

        if self.id_in_group == 1:
            self.pts_asignados = self.group.castigo_jug1
        elif self.id_in_group == 2:
            self.pts_asignados = self.group.castigo_jug2
        elif self.id_in_group == 3:
            self.pts_asignados = self.group.castigo_jug3
        elif self.id_in_group == 4:
            self.pts_asignados = self.group.castigo_jug4

        elif self.id_in_group == 5:
            self.pts_asignados = self.group.castigo_jug5
        
        #acum_castigo = sum([p.castigo for p in self.group.get_players()])
        print ('total de pts asignados: ', acum_castigo)
        pts_no_asignados = 10 - acum_castigo
        print('ptos no asignados: ', pts_no_asignados)
        tp = -Constants.tao - self.castigo  + ((1/Constants.players_per_group) * (Constants.fondo_castigo - acum_castigo))
        print ('tax/punish: ', tp)
        self.tp = round(tp,2)
        return tp
       
    # Aplica el castigo calculado sobre la ganancia (VCM - Tax/Punishment)
    def aplicar_castigo(self):
        print ('ganancia sin castigo: ', self.ganancia)
        ganancia = self.ganancia + self.tp
        acum_castigo = self.group.castigo_jug1 + self.group.castigo_jug2 + self.group.castigo_jug3 + self.group.castigo_jug4 + self.group.castigo_jug5
        print ('total de pts asignados: ', acum_castigo)
        self.gan_tp = max (-self.pts_asignados, round(ganancia, 1))
        print ('ganancia con castigo: ', self.gan_tp)

    # Calcula el pago del jugador de acuerdo a sus ganancias
    def calcular_pago(self):
        ganVCM = self.participant.vars.get("ganVCM")
        ganancias_totales = ganVCM + sum([p.gan_tp for p in self.in_all_rounds()])

        if ganancias_totales < 0:
            self.ganancias_totales = 0
        else:
            self.ganancias_totales = round(ganancias_totales,2)
        
        self.payoff = ganancias_totales    
        print('ganacias totales: ', self.ganancias_totales)
        pago = round(self.ganancias_totales * Constants.valor_por_puntos, 2)
        #self.payoff = pago
        print('pago final: ', c(pago))
        self.participant.vars["pago_bp"] = pago
        #self.participant.vars["matricula"] = self.matricula
        print('pago final $: ', c(self.payoff))
        return pago
