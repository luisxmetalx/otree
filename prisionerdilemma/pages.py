from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
            return self.round_number == 1
    # timeout_seconds = 100

class Quiz(Page):
    def is_displayed(self):
            return self.round_number == Constants.num_rounds
    form_model = 'player'
    form_fields = ['genero','edad']

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
            
class ExpTeorico(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

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

        ronda_mujeres_c=[]
        ronda_hombres_c=[]
        ronda_mujeres_nc=[] 
        ronda_hombres_nc=[]

        pareja_conf = 0
        pareja_no_conf = 0
        pareja_dif = 0

        porc_grupos_conf = []
        porc_grupos_no_conf = []
        porc_grupos_dif = []
        
        #se saca el porcentajes de grupos que cooperaron, no cooperaron y dieron respuesta diferentes sus integrantes
        for k in range(1,Constants.num_rounds+1):
            for j in self.subsession.get_groups():
                yo = j.get_players()[0]
                oponente = yo.other_player()
                if yo.in_round(k).decision == oponente.in_round(k).decision and yo.in_round(k).decision =='cooperar':
                    pareja_conf += 1
                elif yo.in_round(k).decision == oponente.in_round(k).decision and yo.in_round(k).decision =='no cooperar':
                    pareja_no_conf += 1
                else:
                    pareja_dif += 1
            porc_grupos_conf.append(round((pareja_conf/len(self.subsession.get_groups())*100),2))
            porc_grupos_no_conf.append(round((pareja_no_conf/len(self.subsession.get_groups())*100),2))
            porc_grupos_dif.append(round((pareja_dif/len(self.subsession.get_groups())*100),2))
            pareja_conf = 0
            pareja_no_conf = 0
            pareja_dif = 0
        
        for k in range(1,Constants.num_rounds+1):
            for p in self.subsession.get_players():
                if p.in_round(k).decision=='cooperar' and p.in_round(Constants.num_rounds).genero=='Femenino':
                    mujeres_confesaron += 1
                    l_edades_mujeres.append(p.in_round(Constants.num_rounds).edad)
                elif p.in_round(k).decision=='no cooperar' and p.in_round(Constants.num_rounds).genero=='Femenino':
                    mujeres_callaron += 1
                    l_edades_mujeres.append(p.in_round(Constants.num_rounds).edad)
                elif p.in_round(k).decision=='cooperar' and p.in_round(Constants.num_rounds).genero=='Masculino':
                    hombres_confesaron += 1
                    l_edades_hombres.append(p.in_round(Constants.num_rounds).edad)
                else:
                    hombres_callaron += 1
                    l_edades_hombres.append(p.in_round(Constants.num_rounds).edad)
            #sacar número de mujer y hombres que cooperaron y no cooperaron por ronda
            ronda_mujeres_c.append(mujeres_confesaron)
            ronda_mujeres_nc.append(mujeres_callaron)
            ronda_hombres_c.append(hombres_confesaron)
            ronda_hombres_nc.append(hombres_callaron)
            mujeres_callaron=0
            mujeres_confesaron=0
            hombres_callaron=0
            hombres_confesaron=0

        #sacar los generos de los participantes
        for p in self.subsession.get_players():
            l_generos.append(p.in_round(Constants.num_rounds).genero)
        
        #se calcula total mujeres y hombres
        total_mujeres = l_generos.count('Femenino')
        print("total de mujeres: ",total_mujeres)
        total_hombres = l_generos.count('Masculino')
        #procentaje de hombres y mujeres
        porc_femenino = round((total_mujeres/len(self.subsession.get_players()))*100,2)
        porc_masculino = round((total_hombres/len(self.subsession.get_players()))*100,2)

        #calculo del promedio de mujeres coperan y no cooperan por ronda
        porc_mc=[]
        porc_mnc=[]
        porc_hc=[]
        porc_hnc=[]
        for v in ronda_mujeres_c:
            p=round((v/total_mujeres)*100,2)
            porc_mc.append(p)
        for v in ronda_mujeres_nc:
            p=round((v/total_mujeres)*100,2)
            porc_mnc.append(p)
        for v in ronda_hombres_c:
            p=round((v/total_hombres)*100,2)
            porc_hc.append(p)
        for v in ronda_hombres_nc:
            p=round((v/total_hombres)*100,2)
            porc_hnc.append(p)

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
        
        rondas = []
        rond = 0
        for i in range(Constants.num_rounds):
            rond += 1
            rondas.append("Ronda "+str(rond))
        return {
            'mc': porc_mc,
            'mnc': porc_mnc,
            'hc': porc_hc,
            'hnc': porc_hnc,
            'm' : porc_masculino,
            'f' : porc_femenino,
            'rondas': rondas,
            'edades': edades,
            'prom_edad_muj' : prom_edad_mujer,
            'prom_edad_hom' : prom_edad_hombre,
            'pair_conf' : porc_grupos_conf,
            'pair_no_conf' : porc_grupos_no_conf,
            'pair_dif' : porc_grupos_dif
        }

page_sequence = [
    Introduction,
    Decision,
    ResultsWaitPage,
    Results,
    Quiz,
    ExpTeorico,
    CharWaitPage,
    Chart
]
