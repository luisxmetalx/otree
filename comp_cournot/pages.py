from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Quiz(Page):
    def is_displayed(self):
        return self.round_number == 1
    form_model = 'player'
    form_fields = ['genero','edad','matricula']


class Decide(Page):
    form_model = 'player'
    form_fields = ['unidades']
    def vars_for_template(self):
        return {
            'ronda' : self.round_number
        }


class ResultsWaitPage(WaitPage):
    body_text = "Esperando a que el otro participante decida."

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {
            'other_player_units': self.player.other_player().unidades
        }

class TotalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        ganancia_total = sum([p.payoff for p in self.player.in_all_rounds()])
        #total_u_propia = sum([p.unidades for p in self.player.in_all_rounds()])
        #total_u_oponente = sum([p.other_player().unidades for p in self.player.in_all_rounds()])

        dic_ganancia = {}

        for i in self.player.in_rounds(1,self.round_number):
            lista = []
            lista.append(str(i.unidades)+ " unidades")
            lista.append(str(i.other_player().unidades)+" unidades")
            lista.append(str(i.group.total_units)+" unidades")
            lista.append(str(round(i.group.unit_price,1))+" puntos")
            lista.append(str(round(i.payoff,1))+" puntos")
            dic_ganancia[i.round_number]=lista
            
        return {
            'ganancia_total' : ganancia_total,
            'dic_ganancia' : dic_ganancia,
            #'total_u_propia': total_u_propia,
            #'total_u_oponente' : total_u_oponente,
        }

class CharWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    body_text = "Esperando a que todos los participantes terminen"
    wait_for_all_groups = True


class Charts(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        grupo1 = 'Grupo 1'
        grupo1_ganancia = []
        grupo1_unidades = []
        grupo1_pvu = []
        grupos_ganancias = {}
        grupos_pvu = {}
        grupos_units = {}
        control_grupo = 0
        lista_colores = ['','#A2CD45','#21869A','#6D36D7','#08F20C','#D8991B','#13ABF1','#E32329','#12ED4F','#E1F111','#150EF4','#6A6895','#8F02F4','#3F7F04','#804005','#036F21','#170633','#625F66','#625F66']
        cont = 1
        #se saca el precio promedio y ganancia maxima del grupo para cada ronda
        for j in self.subsession.get_groups():
            tmp = 0
            tmp1 = 0
            tmp2 = 0
            precio = []
            ganancia = []
            control_grupo += 1
            if control_grupo == 1:
                for k in range(1,Constants.num_rounds+1):
                    players = j.get_players()
                    yo = players[0]
                    oponente = yo.other_player()
                    tmp1 = yo.in_round(k).payoff
                    tmp2 = oponente.in_round(k).payoff
                    tmp = tmp1 + tmp2
                    grupo1_ganancia.append(tmp)
                    grupo1_pvu.append(yo.in_round(k).group.unit_price)
                    grupo1_unidades.append(yo.in_round(k).group.total_units)
            else:
                cont += 1
                tmp = {}
                tmp5 = {}
                tmp6 = {}
                l_tmp = []
                l_pvu = []
                l_units = []
                for k in range(1,Constants.num_rounds+1):
                    players = j.get_players()
                    yo = players[0]
                    oponente = yo.other_player()
                    tmp1 = yo.in_round(k).payoff
                    tmp2 = oponente.in_round(k).payoff
                    l_tmp.append( tmp1 + tmp2 )
                    l_pvu.append(yo.in_round(k).group.unit_price)
                    l_units.append(yo.in_round(k).group.total_units)
                    tmp[lista_colores[cont]] = l_tmp
                    tmp5[lista_colores[cont]] = l_pvu
                    tmp6[lista_colores[cont]] = l_units
                    grupos_pvu['Grupo '+str(cont)] = tmp5
                    grupos_units['Grupo '+str(cont)] = tmp6
                grupos_ganancias['Grupo '+str(cont)] = tmp
                
        
        
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

        rondas = []
        rond = 0
        for i in range(Constants.num_rounds):
            rond += 1
            rondas.append("Ronda "+str(rond))

        return{
            'grupo1_ganancia' : grupo1_ganancia,
            'grupos_ganancias' : grupos_ganancias,
            'grupo1_pvu' : grupo1_pvu,
            'grupos_pvu' : grupos_pvu,
            'grupo1_units' : grupo1_unidades,
            'grupos_units' : grupos_units,
            'prom_edad_mujer' : prom_edad_mujer,
            'prom_edad_hombre' : prom_edad_hombre,
            'f' : porc_femenino,
            'm' : porc_masculino,
            'rondas' : rondas,
        }

page_sequence = [
    Introduction,
    Quiz,
    Decide,
    ResultsWaitPage,
    Results,
    TotalResults,
    CharWaitPage,
    Charts
]
