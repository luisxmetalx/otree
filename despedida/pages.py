from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Despedida(Page):
    def vars_for_template(self):
        if self.session.config['name'] == 'Sesion_Inaguracion':
            return {
                    'ruta_imagen': 'images/despedida.gif'
                    }
        else:
            return {
                    'matricula': self.participant.vars.get('matricula')
                    }

page_sequence = [
    Despedida
]
