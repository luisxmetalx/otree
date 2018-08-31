from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
            return self.round_number == 1
    # timeout_seconds = 100

class Quiz(Page):
    def is_displayed(self):
            return self.round_number == 1
    form_model = 'player'
    form_fields = ['genero','edad','matricula']

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return {
            'ronda' : self.round_number
            }

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
    def is_displayed(self):
            return self.round_number == Constants.num_rounds
    wait_for_all_groups = True
            

class Chart(Page):
    def is_displayed(self):
            return self.round_number==Constants.num_rounds

    def vars_for_template(self):
        acum = 0
        l_generos = []
        l_edades_mujeres = []
        l_edades_hombres = []
        mujeres_confesaron = 0
        mujeres_callaron = 0
        hombres_confesaron = 0
        hombres_callaron = 0

        pareja_conf = 0
        pareja_no_conf = 0
        pareja_dif = 0
        
        for k in range(1,Constants.num_rounds+1):
            for j in self.subsession.get_groups():
                for p in j.get_players():
                    yo = p
                    oponente = yo.other_player()
                    if yo.in_round(k).decision == oponente.in_round(k).decision and yo.in_round(k).decision =='cooperar':
                        pareja_conf += 1
                    elif yo.in_round(k).decision == oponente.in_round(k).decision and yo.in_round(k).decision =='no cooperar':
                        pareja_no_conf += 1
                    else:
                        pareja_dif += 1
                   
        #se rellena la lista de edades 
        for k in range(1,Constants.num_rounds+1):
            for p in self.subsession.get_players():
                #l_generos.append(p.in_round(1).genero)
                if p.in_round(k).decision=='cooperar' and p.in_round(1).genero=='Femenino':
                    mujeres_confesaron += 1
                    l_edades_mujeres.append(p.in_round(1).edad)
                elif p.in_round(k).decision=='no cooperar' and p.in_round(1).genero=='Femenino':
                    mujeres_callaron += 1
                    l_edades_mujeres.append(p.in_round(1).edad)
                elif p.in_round(k).decision=='cooperar' and p.in_round(1).genero=='Masculino':
                    hombres_confesaron += 1
                    l_edades_hombres.append(p.in_round(1).edad)
                else:
                    hombres_callaron += 1
                    l_edades_hombres.append(p.in_round(1).edad)
        #sacar los generos de los participantes
        for p in self.subsession.get_players():
            l_generos.append(p.in_round(1).genero)
        print(l_generos)
        print(mujeres_confesaron)
        #se calcula total mujeres y hombres
        total_mujeres = l_generos.count('Femenino')
        total_hombres = l_generos.count('Masculino')
        #procentaje de hombres y mujeres
        porc_femenino = (total_mujeres/len(self.subsession.get_players()))*100
        porc_masculino = (total_hombres/len(self.subsession.get_players()))*100
        #porcentaje de hombres y mujeres que callaron o confesaron
        porc_muj_confesaron = (mujeres_confesaron/total_mujeres)*100
        porc_muj_callaron = (mujeres_callaron/total_mujeres)*100
        porc_hom_confesaron = (hombres_confesaron/total_hombres)*100
        porc_hom_callaron = (hombres_callaron/total_hombres)*100
        #procentaje de grupos que ambos callaron o confesaron o difirieron
        pair_conf = ((pareja_conf/2)/((total_hombres+total_mujeres)/2))*100
        pair_no_conf = ((pareja_no_conf/2)/((total_hombres+total_mujeres)/2))*100
        pair_dif = ((pareja_dif/2)/((total_hombres+total_mujeres)/2))*100

        #se saca edades promedio de hombres y mujeres
        suma1 = 0
        suma2 = 0

        for i in l_edades_mujeres:
            suma1 += i

        for i in l_edades_hombres:
            suma2 += i
        
        prom_edad_mujer = round(suma1/len(l_edades_mujeres),len(self.subsession.get_players()))
        prom_edad_hombre = round(suma2/len(l_edades_hombres),len(self.subsession.get_players()))
        #Guardando edades
        edades=[]
        edades.append(round(prom_edad_hombre,2))
        edades.append(round(prom_edad_mujer,2))
        
        return {
            'm' : porc_masculino,
            'f' : porc_femenino,
            'edades': edades,
            'porc_muj_con' : porc_muj_confesaron,
            'porc_muj_cal' : porc_muj_callaron,
            'porc_hom_con' : porc_hom_confesaron,
            'porc_hom_cal' : porc_hom_callaron,
            'prom_edad_muj' : prom_edad_mujer,
            'prom_edad_hom' : prom_edad_hombre,
            'pair_conf' : pair_conf,
            'pair_no_conf' : pair_no_conf,
            'pair_dif' : pair_dif
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
