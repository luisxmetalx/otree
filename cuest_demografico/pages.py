from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Page1(Page):

    template_name = 'cuest_demografico/Cuestionario.html'

    form_model = models.Player
    form_fields = ['c4_pregunta_{}'.format(i) for i in range(1, 8)]

class Page2(Page):

    template_name = 'cuest_demografico/Cuestionario.html'

    form_model = models.Player
    form_fields = ['c4_pregunta_{}'.format(i) for i in range(8, 15)]

class Page3(Page):

    template_name = 'cuest_demografico/Cuestionario.html'

    form_model = models.Player
    form_fields = ['c4_pregunta_{}'.format(i) for i in range(15, 22)]


page_sequence = [
    Page1,
    Page2,
    Page3
]
