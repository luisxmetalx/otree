from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Page1(Page):

    form_model = models.Player
    form_fields = ['pregunta_1']

    def vars_for_template(self):
        opciones = [i for i in range(1, 11)]
        return {
                'opciones': opciones                
                }
    
class Page2(Page):

    form_model = models.Player
    form_fields = ['pregunta_{}'.format(i) for i in range(2, 8)]
    
    def vars_for_template(self):
        p_2 = "¿Mientras manejo?"
        p_3 = "¿En asuntos financieros?"
        p_4 = "¿En deportes y entrenamiento?"
        p_5 = "¿En su ocupación laboral?"
        p_6 = "¿Con su salud?"
        p_7 = "¿Su confianza en las demás personas?"
        preguntas = [p_2, p_3, p_4, p_5, p_6, p_7]

        opciones = [i for i in range(1, 11)]
        ids_preg = [i for i in range(2, 8)]
        return {
                'preguntas': preguntas,
                'opciones': opciones,
                'mult': zip(ids_preg, preguntas)
                }



page_sequence = [
    Page1, Page2
]
