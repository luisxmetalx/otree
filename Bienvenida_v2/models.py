from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import datetime

author = 'Luis Andrade'

doc = """
App para mostrar el mensaje de bienvenida General para sesiones con múltiples apps.
"""
# funcion para generar diccionario de ips, las claves son indices del 194 al 228,
# los valores, números del 1 al 35 respectivamente
def generar_Dicc_Ip():
    dicc_ip = {}
    indice = 194
    for i in range(1, 36):
        dicc_ip[indice] = i
        indice += 1
    
    return dicc_ip

class Constants(BaseConstants):
    name_in_url = 'Bienvenida_v2'
    players_per_group = None
    num_rounds = 1
    anio_max = datetime.datetime.now().year * 100000 + 99999


class Subsession(BaseSubsession):

    def before_session_starts(self):
        # se guarda el diccionario de ip's como variable de sesión
        self.session.vars['dicc_ip'] = generar_Dicc_Ip()

        print('nombre de sesion: ', self.session.config['name'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    matricula = models.PositiveIntegerField(min=199000000, max=Constants.anio_max)
    maquina = models.IntegerField()

    def calcularNumMaquina(self):
        ip = str(self.participant.ip_address)
        if not ip.startswith('200.126.3.'):
            self.maquina = 0
        else:
            maq = int(ip[-3:])
            self.maquina = self.session.vars['dicc_ip'][maq]
        self.participant.vars['maquina'] = self.maquina
