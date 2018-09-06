from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Quiz(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = 'player'
    form_fields = ['genero','edad']


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

class ExpTeorico(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class CharWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    body_text = "Esperando a que todos los participantes terminen"
    wait_for_all_groups = True


class Charts(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        lista_colores = ['','#d73027','#f46d43','#fdae61','#fee08b','#ffffbf','#d9ef8b','#a6d96a','#66bd63','#1a9850','#150EF4','#6A6895','#8F02F4','#3F7F04','#804005','#036F21','#170633','#625F66','#625F66']
        

        #se saca lista de edad y de genero 
        l_edades_mujeres = []
        l_edades_hombres = []
        l_generos = []
        for p in self.subsession.get_players():
            l_generos.append(p.in_round(Constants.num_rounds).genero)
            if p.in_round(Constants.num_rounds).genero == "Masculino":
                l_edades_hombres.append(p.in_round(Constants.num_rounds).edad)
            if p.in_round(Constants.num_rounds).genero == "Femenino":
                l_edades_mujeres.append(p.in_round(Constants.num_rounds).edad)
        
        #se saca numero de hombres y mujeres
        total_mujeres = l_generos.count('Femenino')
        total_hombres = l_generos.count('Masculino')


        ganancia_prom_total = []
        ganancias_total = []
        ganancia_prom_hom = []
        ganancias_hom = []
        ganancia_prom_muj = []
        ganancias_muj = []
        cantidad_prom_producida_group = []
        cantidades_producidas_group = []
        cantidad_producida_prom_hom = []
        cantidades_producidas_hom = []
        cantidad_producida_prom_muj = []
        cantidades_producidas_muj = []
        precio_prom_group = []
        precios_group = []
        grupos = self.subsession.get_groups()
        #se saca el precio promedio y ganancia maxima del grupo para cada ronda
        for k in range(1,Constants.num_rounds+1):
            tmp1 = 0
            tmp2 = 0
            ganancia = []
            ganancia_hom = []
            ganancia_muj = []
            cantidad_producida = []
            cantidad_producida_hom = []
            cantidad_producida_muj = []
            precio_group = []
            for j in grupos:
                players = j.get_players()
                yo = players[0]
                oponente = yo.other_player()
                tmp1 = yo.in_round(k).payoff
                tmp2 = oponente.in_round(k).payoff
                ganancia.append( tmp1 + tmp2 )
                ganancias_total.append(tmp1)
                ganancias_total.append(tmp2)
                precio_group.append(yo.in_round(k).group.unit_price)
                precios_group.append(float(yo.in_round(k).group.unit_price))
                precios_group.append(float(oponente.in_round(k).group.unit_price))
                cantidad_producida.append(yo.in_round(k).group.total_units)
                cantidades_producidas_group.append(yo.in_round(k).group.total_units)
                cantidades_producidas_group.append(oponente.in_round(k).group.total_units)
                if(yo.in_round(Constants.num_rounds).genero == 'Masculino'):
                    ganancia_hom.append(float(tmp1))
                    ganancias_hom.append(float(tmp1))
                    cantidad_producida_hom.append(yo.in_round(k).unidades)
                    cantidades_producidas_hom.append(yo.in_round(k).unidades)
                if(yo.in_round(Constants.num_rounds).genero == 'Femenino'):
                    ganancia_muj.append(float(tmp1))
                    ganancias_muj.append(float(tmp1))
                    cantidad_producida_muj.append(yo.in_round(k).unidades)
                    cantidades_producidas_muj.append(yo.in_round(k).unidades)
                if(oponente.in_round(Constants.num_rounds).genero == 'Masculino'):
                    ganancia_hom.append(float(tmp2))
                    ganancias_hom.append(float(tmp2))
                    cantidad_producida_hom.append(oponente.in_round(k).unidades)
                    cantidades_producidas_hom.append(oponente.in_round(k).unidades)
                if(oponente.in_round(Constants.num_rounds).genero == 'Femenino'):
                    ganancia_muj.append(float(tmp2))
                    ganancias_muj.append(float(tmp2))
                    cantidad_producida_muj.append(oponente.in_round(k).unidades)
                    cantidades_producidas_muj.append(oponente.in_round(k).unidades)
            ganancia_prom_total.append(round(sum([float(i) for i in ganancia])/len(self.subsession.get_players()),2))
            ganancia_prom_hom.append(round(sum([float(i) for i in ganancia_hom])/total_hombres,2))
            ganancia_prom_muj.append(round(sum([float(i) for i in ganancia_muj])/total_mujeres,2))
            cantidad_prom_producida_group.append(round(sum([i for i in cantidad_producida])/len(grupos),2))
            cantidad_producida_prom_hom.append(round(sum([i for i in cantidad_producida_hom])/total_hombres,2))
            cantidad_producida_prom_muj.append(round(sum([i for i in cantidad_producida_muj])/total_mujeres,2))
            precio_prom_group.append(round(sum([float(i) for i in precio_group])/len(grupos),2))    
        
        #porcentaje de hombres y mujeres
        if(total_mujeres != 0):
            porc_femenino = round((total_mujeres/len(self.subsession.get_players()))*100,2)
        else:
            porc_femenino = 0
        if(total_hombres != 0):
            porc_masculino = round((total_hombres/len(self.subsession.get_players()))*100,2)
        else:
            porc_masculino = 0

        #se saca edades promedio de hombres y mujeres
        suma1 = 0
        suma2 = 0

        for i in l_edades_mujeres:
            suma1 += i

        for i in l_edades_hombres:
            suma2 += i
        if (total_mujeres != 0):
            prom_edad_mujer = round(suma1/len(l_edades_mujeres),len(self.subsession.get_players()))
        else:
            prom_edad_mujer = 0
        if(total_hombres != 0):
            prom_edad_hombre = round(suma2/len(l_edades_hombres),len(self.subsession.get_players()))
        else:
            prom_edad_hombre = 0
        #Guardando edades
        edades=[]
        edades.append(round(prom_edad_hombre,2))
        edades.append(round(prom_edad_mujer,2))

        total_grupos = []
        rondas_cajas = []
        rondas_cajas_hom = []
        rondas_cajas_muj = []
        rondas_cajas_grupal = []
        c = 0
        for i in range(Constants.num_rounds):
            c += 1
            total_grupos.append("Ronda "+str(c))
            for j in range(len(self.subsession.get_groups())*2):
                rondas_cajas.append("Ronda "+str(c))
            for j in range(total_hombres):
                rondas_cajas_hom.append("Ronda "+str(c))
            for j in range(total_mujeres):
                rondas_cajas_muj.append("Ronda "+str(c))
            for j in range(len(self.subsession.get_groups())):
                rondas_cajas_grupal.append("Ronda "+str(c))
                
        return{
            'ganancia_prom_total' : ganancia_prom_total,
            'ganancias_total' : ganancias_total,
            'ganancia_prom_hom' : ganancia_prom_hom,
            'ganancias_hom' : ganancias_hom,
            'ganancia_prom_muj' : ganancia_prom_muj,
            'ganancias_muj' : ganancias_muj,
            'cant_prom_total' : cantidad_prom_producida_group,
            'cant_producida' : cantidades_producidas_group,
            'cant_prom_hom' : cantidad_producida_prom_hom,
            'cant_hom' : cantidades_producidas_hom,
            'cant_prom_muj' : cantidad_producida_prom_muj,
            'cant_muj' : cantidades_producidas_muj,
            'precio_prom_group' : precio_prom_group,
            'precios_group' : precios_group,
            'edades' : edades,
            'f' : porc_femenino,
            'm' : porc_masculino,
            'total_grupos' : total_grupos,
            'rondas_cajas' : rondas_cajas,
            'rondas_cajas_hom' : rondas_cajas_hom,
            'rondas_cajas_muj' : rondas_cajas_muj,
            'rondas_cajas_grupal' : rondas_cajas_grupal,
        }

page_sequence = [
    Introduction,
    Decide,
    ResultsWaitPage,
    Results,
    TotalResults,
    Quiz,
    ExpTeorico,
    CharWaitPage,
    Charts,
]
