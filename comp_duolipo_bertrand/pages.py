from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1
    timeout_seconds = 100

class Quiz(Page):
    def is_displayed(self):
        return self.round_number == 1
    form_model = 'player'
    form_fields = ['genero','edad','matricula']

class darPrecio(Page):
    form_model = 'player'
    form_fields = ['precio']
    def vars_for_template(self):
        return {
            'ronda' : self.round_number
        }

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.ganancia()

class Resultados(Page):
    def is_displayed(self):
        return self.round_number != Constants.num_rounds

    def vars_for_template(self):
        yo = self.player
        oponente = yo.other_player()
        mi_ganancia = yo.payoff
        opon_ganancia = oponente.payoff
        lista = {}
        for i in self.player.in_rounds(1,self.round_number):
            lista[i.round_number]=i.payoff;
        ganancia_total = sum([p.payoff for p in self.player.in_rounds(1,self.round_number)])
        return {
            'mi_ganancia' : mi_ganancia,
            'ganancia_total' : ganancia_total,
            'lista' : lista,
            'round' : self.round_number
        }

class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        ganancia_total = sum([p.payoff for p in self.player.in_all_rounds()])
        lista = {}
        for i in self.player.in_rounds(1,self.round_number):
            lista[i.round_number]=i.payoff;
        return {
            'ganancia_total' : ganancia_total,
            'lista' : lista
        }

class CharWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    wait_for_all_groups = True

class Charts(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        ganancia_total = []
        prom_precio = []
        #se saca el precio promedio y ganancia maxima del grupo
        for k in range(1,Constants.num_rounds+1):
            tmp = 0
            tmp1 = 0
            tmp2 = 0
            tmp3 = 0
            grupos = self.subsession.get_groups()
            precio = []
            ganancia = []
            for j in grupos:
                players = j.get_players()
                yo = players[0]
                oponente = yo.other_player()
                tmp1 = yo.in_round(k).payoff
                tmp2 = oponente.in_round(k).payoff
                tmp3 = (tmp1 + tmp2)
                tmp = ((tmp1 + tmp2))
                precio.append(tmp)
                ganancia.append(tmp3)
            #print('jugador 1: '+str(tmp1)+'jugador 2: '+str(tmp2))
            
                
            prom_precio.append(sum([i for i in ganancia])/len(grupos))
            ganancia_total.append(sum([i for i in precio]))
        
        #ganancia maxima del grupo    
        ganancia_maxima = Constants.demanda * 20 * Constants.ume * Constants.num_rounds
        
        #se saca lista de edad y de genero 
        l_edades_mujeres = []
        l_edades_hombres = []
        l_generos = []
        for p in self.subsession.get_players():
            l_generos.append(p.in_round(1).genero)
            if p.in_round(1).genero == "Masculino":
                l_edades_hombres.append(p.in_round(1).edad)
            if p.in_round(1).genero == "Femenino":
                l_edades_mujeres.append(p.in_round(1).edad)
        
        #se saca numero de hombres y mujeres
        total_mujeres = l_generos.count('Femenino')
        total_hombres = l_generos.count('Masculino')

        #se saca el porcentaje de mujeres y hombres
        porc_femenino = round((total_mujeres/len(self.subsession.get_players()))*100,2)
        porc_masculino = round((total_hombres/len(self.subsession.get_players()))*100,2)

        #se saca edades promedio de hombres y mujeres
        suma1 = 0
        suma2 = 0

        for i in l_edades_mujeres:
            suma1 += i

        for i in l_edades_hombres:
            suma2 += i
        
        prom_edad_mujer = round(suma1/len(l_edades_mujeres),2)
        prom_edad_hombre = round(suma2/len(l_edades_hombres),2)

        total_grupos = []
        cmg_const = []
        c = 0
        for i in range(Constants.num_rounds):
            c += 1
            total_grupos.append("Ronda "+str(c))
            cmg_const.append(Constants.cmg)

        return{
            'prom_precio' : prom_precio,
            'cmg' : Constants.cmg,
            'ganancia_total' : ganancia_total,
            'ganancia_max' : ganancia_maxima,
            'prom_edad_mujer' : prom_edad_mujer,
            'prom_edad_hombre' : prom_edad_hombre,
            'f' : porc_femenino,
            'm' : porc_masculino,
            'total_grupos' : total_grupos,
            'cmg_const' : cmg_const
        }

page_sequence = [
    Introduction,
    Quiz,
    darPrecio,
    ResultsWaitPage,
    Resultados,
    Results,
    CharWaitPage,
    Charts
]
