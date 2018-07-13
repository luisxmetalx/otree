from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100

class Quiz(Page):
    form_model = 'player'
    form_fields = ['genero','edad']

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.escoger_decision()

class Results(Page):
    def vars_for_template(self):
        yo = self.player
        oponente = yo.other_player()
        return {
            'mi_decision' : yo.decision,
            'oponente_decision' : oponente.decision,
            'misma_eleccion' : yo.decision == oponente.decision
        }

class CharWaitPage(WaitPage):
    wait_for_all_groups = True
            

class Chart(Page):
    def vars_for_template(self):
        acum = 0
        l_edades = []
        l_edades_mujeres = []
        l_edades_hombres = []
        l_generos = []
        mujeres_confesaron = 0
        mujeres_callaron = 0
        hombres_confesaron = 0
        hombres_callaron = 0
        for p in self.subsession.get_players():
            l_edades.append(p.edad)
            l_generos.append(p.genero)
            if p.decision=='Confesar' and p.genero=='Femenino':
                mujeres_confesaron += 1
                l_edades_mujeres.append(p.edad)
            elif p.decision=='Callar' and p.genero=='Femenino':
                mujeres_callaron += 1
                l_edades_mujeres.append(p.edad)
            elif p.decision=='Confesar' and p.genero=='Masculino':
                hombres_confesaron += 1
                l_edades_hombres.append(p.edad)
            else:
                hombres_callaron += 1
                l_edades_hombres.append(p.edad)
        
        total_mujeres = l_generos.count('Femenino')
        total_hombres = l_generos.count('Masculino')
        porc_femenino = (total_mujeres/len(self.subsession.get_players()))*100
        porc_masculino = (total_hombres/len(self.subsession.get_players()))*100
        porc_muj_confesaron = (mujeres_confesaron/total_mujeres)*100
        porc_muj_callaron = (mujeres_callaron/total_mujeres)*100
        porc_hom_confesaron = (hombres_confesaron/total_hombres)*100
        porc_hom_callaron = (hombres_callaron/total_hombres)*100

        suma1 = 0
        suma2 = 0

        for i in l_edades_mujeres:
            suma1 += i

        for i in l_edades_hombres:
            suma2 += i
        
        prom_edad_mujer = suma1/len(l_edades_mujeres)
        prom_edad_hombre = suma2/len(l_edades_hombres)
        return {
            'm' : porc_masculino,
            'f' : porc_femenino,
            'porc_muj_con' : porc_muj_confesaron,
            'porc_muj_cal' : porc_muj_callaron,
            'porc_hom_con' : porc_hom_confesaron,
            'porc_hom_cal' : porc_hom_callaron,
            'prom_edad_muj' : prom_edad_mujer,
            'prom_edad_hom' : prom_edad_hombre
        }

page_sequence = [
    Introduction,
    Quiz,
    Decision,
    ResultsWaitPage,
    Results,
    CharWaitPage,
    Chart
]
