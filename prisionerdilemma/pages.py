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

class Decision_tratamiento(Page):
    def is_displayed(self):
            return self.round_number == 1
    form_model = 'player'
    form_fields = ['decision_tratamiento']

    def vars_for_template(self):
        return {
            'ronda' : self.round_number
            }

class ResultsWaitFase1(WaitPage):
    def is_displayed(self):
            return self.round_number == 1

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.escoger_decision_tratamiento()

class ResultadosFase1(Page):
    def is_displayed(self):
            return self.round_number == 1

    def vars_for_template(self):
        yo = self.player
        oponente = yo.other_player()

        puntos = int(yo.payoff)

        return {
            'mi_decision' : yo.decision_tratamiento,
            'oponente_decision' : oponente.decision_tratamiento,
            'misma_eleccion' : yo.decision_tratamiento == oponente.decision_tratamiento,
            'puntos' : puntos
        }

class Fase2(Page):
    def is_displayed(self):
            return self.round_number == 1

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return {
            'ronda' : self.round_number
            }

class ResultsWaitFase2(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.escoger_decision()

class Results(Page):
    def vars_for_template(self):
        yo = self.player
        oponente = yo.other_player()

        puntos = int(yo.payoff)

        return {
            'mi_decision' : yo.decision,
            'oponente_decision' : oponente.decision,
            'misma_eleccion' : yo.decision == oponente.decision,
            'puntos' : puntos
        }

class FinalResults(Page):
    def is_displayed(self):
            return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        yo = self.player
        puntos_perdidos = 0
        for i in range(1, Constants.num_rounds+1):
            puntos_perdidos += int(yo.in_round(i).payoff)
        puntos_total = 100 - puntos_perdidos

        return {
            'puntos_perdidos' : puntos_perdidos,
            'puntos_total' : puntos_total
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
        mujeres_conf_tratamiento = 0
        mujeres_callaron_tratamiento = 0
        hombres_conf_tratamiento = 0
        hombres_callaron_tratamiento = 0

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

        porc_grupos_conf_tratamiento = 0 
        porc_grupos_no_conf_tratamiento = 0
        porc_grupos_dif_tratamiento = 0
        porc_hom_conf_tratamiento = 0
        porc_muj_conf_tratamiento = 0
        porc_hom_no_conf_tratamiento = 0
        porc_muj_no_conf_tratamiento = 0

        
        
        #se saca el porcentajes de grupos que confesaron, no confesaron y dieron respuesta diferentes sus integrantes
        for k in range(1,Constants.num_rounds+1):
            if k == 1:
                for j in self.subsession.get_groups():
                    yo = j.get_players()[0]
                    oponente = yo.other_player()
                    if yo.in_round(k).decision_tratamiento == oponente.in_round(k).decision_tratamiento and yo.in_round(k).decision_tratamiento =='confesar':
                        pareja_conf += 1
                    elif yo.in_round(k).decision_tratamiento == oponente.in_round(k).decision_tratamiento and yo.in_round(k).decision_tratamiento =='no confesar':
                        pareja_no_conf += 1
                    else:
                        pareja_dif += 1
                porc_grupos_conf_tratamiento = round((pareja_conf/len(self.subsession.get_groups())*100),2)
                porc_grupos_no_conf_tratamiento = round((pareja_no_conf/len(self.subsession.get_groups())*100),2)
                porc_grupos_dif_tratamiento = round((pareja_dif/len(self.subsession.get_groups())*100),2)
                pareja_conf = 0
                pareja_no_conf = 0
                pareja_dif = 0
            for j in self.subsession.get_groups():
                yo = j.get_players()[0]
                oponente = yo.other_player()
                if yo.in_round(k).decision == oponente.in_round(k).decision and yo.in_round(k).decision =='confesar':
                    pareja_conf += 1
                elif yo.in_round(k).decision == oponente.in_round(k).decision and yo.in_round(k).decision =='no confesar':
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
            if k ==1:
                for p in self.subsession.get_players():
                    if p.in_round(k).decision_tratamiento == 'confesar' and p.in_round(Constants.num_rounds).genero=='Femenino':
                        mujeres_confesaron += 1
                    elif p.in_round(k).decision_tratamiento == 'no confesar' and p.in_round(Constants.num_rounds).genero=='Femenino':
                        mujeres_callaron += 1
                    elif p.in_round(k).decision_tratamiento == 'confesar' and p.in_round(Constants.num_rounds).genero=='Masculino':
                        hombres_confesaron += 1
                    else:
                        hombres_callaron += 1
                mujeres_callaron_tratamiento = mujeres_callaron
                mujeres_conf_tratamiento = mujeres_confesaron
                hombres_callaron_tratamiento = hombres_callaron
                hombres_conf_tratamiento = hombres_confesaron
                mujeres_callaron=0
                mujeres_confesaron=0
                hombres_callaron=0
                hombres_confesaron=0
            for p in self.subsession.get_players():
                if p.in_round(k).decision=='confesar' and p.in_round(Constants.num_rounds).genero=='Femenino':
                    mujeres_confesaron += 1
                elif p.in_round(k).decision=='no confesar' and p.in_round(Constants.num_rounds).genero=='Femenino':
                    mujeres_callaron += 1
                elif p.in_round(k).decision=='confesar' and p.in_round(Constants.num_rounds).genero=='Masculino':
                    hombres_confesaron += 1
                else:
                    hombres_callaron += 1
                    
            #sacar número de mujer y hombres que confesaron y no confesaron por ronda
            ronda_mujeres_c.append(mujeres_confesaron)
            ronda_mujeres_nc.append(mujeres_callaron)
            ronda_hombres_c.append(hombres_confesaron)
            ronda_hombres_nc.append(hombres_callaron)
            mujeres_callaron=0
            mujeres_confesaron=0
            hombres_callaron=0
            hombres_confesaron=0

        #sacar los generos de los participantes y edades de hombres y mujeres
        for p in self.subsession.get_players():
            l_generos.append(p.in_round(Constants.num_rounds).genero)
            if p.in_round(Constants.num_rounds).genero=='Masculino':
                l_edades_hombres.append(p.in_round(Constants.num_rounds).edad)
            if p.in_round(Constants.num_rounds).genero=='Femenino':
                l_edades_mujeres.append(p.in_round(Constants.num_rounds).edad)
        
        #se calcula total mujeres y hombres
        total_mujeres = l_generos.count('Femenino')
        total_hombres = l_generos.count('Masculino')
        
        #porcentaje de hombres y mujeres, aprovechando los condicionales
        #se saca para la ronda de tratamiento 
        if(total_mujeres != 0):
            porc_femenino = round((total_mujeres/len(self.subsession.get_players()))*100,2)
            mujeres_callaron_tratamiento = round((mujeres_callaron_tratamiento/total_mujeres)*100,2)
            mujeres_conf_tratamiento = round((mujeres_conf_tratamiento/total_mujeres)*100,2)
        else:
            porc_femenino = 0
        if(total_hombres != 0):
            porc_masculino = round((total_hombres/len(self.subsession.get_players()))*100,2)
            hombres_callaron_tratamiento = round((hombres_callaron_tratamiento/total_hombres)*100,2)
            hombres_conf_tratamiento = round((hombres_conf_tratamiento/total_hombres)*100,2)
        else:
            porc_masculino = 0

        #calculo del promedio de mujeres coperan y no cooperan por ronda

        porc_mc=[]
        porc_mnc=[]
        porc_hc=[]
        porc_hnc=[]
        for v in ronda_mujeres_c:
            if(total_mujeres != 0):
                p=round((v/total_mujeres)*100,2)
            else:
                p = 0
            porc_mc.append(p)
        for v in ronda_mujeres_nc:
            if(total_mujeres != 0):
                p=round((v/total_mujeres)*100,2)
            else:
                p = 0
            porc_mnc.append(p)
        for v in ronda_hombres_c:
            if(total_hombres != 0):
                p=round((v/total_hombres)*100,2)
            else:
                p = 0
            porc_hc.append(p)
        for v in ronda_hombres_nc:
            if(total_hombres != 0):
                p=round((v/total_hombres)*100,2)
            else:
                p = 0
            porc_hnc.append(p)

        #se saca edades promedio de hombres y mujeres
        suma1 = 0
        suma2 = 0
        prom_edad_hom = 0
        prom_edad_muj = 0 
        for i in l_edades_mujeres:
            suma1 += i

        for i in l_edades_hombres:
            suma2 += i
        
        #se saca la edad promedio de hombres y mujeres 
        if (total_mujeres != 0):
            prom_edad_muj = round(suma1/total_mujeres,2)
        if(total_hombres != 0):
            prom_edad_hom = round(suma2/total_hombres,2)

        
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
            'prom_edad_muj' : prom_edad_muj,
            'prom_edad_hom' : prom_edad_hom,
            'pair_conf' : porc_grupos_conf,
            'pair_no_conf' : porc_grupos_no_conf,
            'pair_dif' : porc_grupos_dif,
            'pair_conf_tratamiento' : porc_grupos_conf_tratamiento,
            'pair_no_conf_tratamiento' : porc_grupos_no_conf_tratamiento,
            'pair_dif_tratamiento' : porc_grupos_dif_tratamiento,
            'hom_conf_tratamiento' : hombres_conf_tratamiento,
            'hom_no_conf_tratamiento' : hombres_callaron_tratamiento,
            'muj_conf_tratamiento' : mujeres_conf_tratamiento,
            'muj_no_conf_tratamiento' : mujeres_callaron_tratamiento
        }

page_sequence = [
    Introduction,
    Decision_tratamiento,
    ResultsWaitFase1,
    ResultadosFase1,
    Fase2,
    Decision,
    ResultsWaitFase2,
    Results,
    FinalResults,
    Quiz,
    ExpTeorico,
    CharWaitPage,
    Chart
]
