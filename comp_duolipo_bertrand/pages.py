from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1
    # timeout_seconds = 150

class Quiz(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = 'player'
    form_fields = ['genero','edad']

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
        lista = {}
        
        #ganacia por ronda
        for i in self.player.in_rounds(1,self.round_number):
            lista[i.round_number] = {   'vendido' : i.vendido,
                                        'precio' : i.precio,
                                        'ganancia' : i.payoff
                                    }

        ganancia_total = sum([p.payoff for p in self.player.in_rounds(1,self.round_number)])

        return {
            'mi_ganancia' : mi_ganancia,
            'ganancia_total' : ganancia_total,
            'lista' : lista
        }

class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        ganancia_total = sum([p.payoff for p in self.player.in_all_rounds()])
        lista = {}
        #ganacia por ronda
        for i in self.player.in_rounds(1,self.round_number):
            lista[i.round_number] = {   'vendido' : i.vendido,
                                        'precio' : i.precio,
                                        'ganancia' : i.payoff
                                    }
        return {
            'ganancia_total' : ganancia_total,
            'lista' : lista
        }

class ExpTeorico(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class CharWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    wait_for_all_groups = True

class Charts(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        ganancia_prom_total = []
        ganancia_prom_group = []
        ganancias_total = []
        ganancias_group = []
        ganancia_prom_hom = []
        ganancias_hom = []
        ganancia_prom_muj = []
        ganancias_muj = []
        prom_precio = []
        precios = []
        precio_prom_hom = []
        precios_hom = []
        precio_prom_muj = []
        precios_muj = []
        
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

        grupos = self.subsession.get_groups()
        #se saca el precio promedio y ganancia maxima del grupo
        for k in range(1,Constants.num_rounds+1):
            tmp = 0
            tmp1 = 0
            tmp2 = 0
            tmp3 = 0
            ganancia = []
            precio = []
            precio_hom = []
            precio_muj = []
            ganancia_hom = []
            ganancia_muj = []
            for j in grupos:
                players = j.get_players()
                yo = players[0]
                oponente = yo.other_player()
                tmp1 = yo.in_round(k).payoff
                tmp2 = oponente.in_round(k).payoff
                tmp3 = (tmp1 + tmp2)
                p1 = yo.in_round(k).precio
                p2 = oponente.in_round(k).precio
                ganancias_total.append(tmp1)
                ganancias_total.append(tmp2)
                ganancias_group.append(tmp3)
                if(yo.in_round(Constants.num_rounds).genero == 'Masculino'):
                    precio_hom.append(p1)
                    precios_hom.append(p1)
                    ganancia_hom.append(tmp1)
                    ganancias_hom.append(tmp1)
                if(yo.in_round(Constants.num_rounds).genero == 'Femenino'):
                    precio_muj.append(p1)
                    precios_muj.append(p1)
                    ganancia_muj.append(tmp1)
                    ganancias_muj.append(tmp1)
                if(oponente.in_round(Constants.num_rounds).genero == 'Masculino'):
                    precio_hom.append(p2)
                    precios_hom.append(p2)
                    ganancia_hom.append(tmp2)
                    ganancias_hom.append(tmp2)
                if(oponente.in_round(Constants.num_rounds).genero == 'Femenino'):
                    precio_muj.append(p2)
                    precios_muj.append(p2)
                    ganancia_muj.append(tmp2)
                    ganancias_muj.append(tmp2)
                
                precios.append(p1)
                precios.append(p2)
                precio.append(p1+p2)
                ganancia.append(tmp3)

            prom_precio.append(round(sum([i for i in precio])/len(self.subsession.get_players()),2))
            ganancia_prom_total.append(round(sum([float(i.in_round(k).payoff) for i in self.subsession.get_players()])/len(self.subsession.get_players()),2))
            ganancia_prom_group.append(round(sum([float(i) for i in ganancia])/len(self.subsession.get_groups()),2))
            
            if(total_hombres != 0):
                precio_prom_hom.append(round(sum([i for i in precio_hom])/total_hombres,2))
                ganancia_prom_hom.append(round(sum([float(i) for i in ganancia_hom])/total_hombres,2))
            else:
                precio_prom_hom.append(0)
                ganancia_prom_hom.append(0)
            if(total_mujeres != 0):
                precio_prom_muj.append(round(sum([i for i in precio_muj])/total_mujeres,2))
                ganancia_prom_muj.append(round(sum([float(i) for i in ganancia_muj])/total_mujeres,2))
            else:
                precio_prom_muj.append(0)
                ganancia_prom_muj.append(0)
        
        #ganancia maxima del grupo    
        ganancia_maxima = Constants.demanda * 16 * len(self.subsession.get_groups())
        
        

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
        

        total_grupos = []
        rondas_cajas = []
        rondas_cajas_hom = []
        rondas_cajas_muj = []
        rondas_cajas_grupal = []
        cmg_const = []
        const_max = []
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
            cmg_const.append(Constants.cmg)
            const_max.append(ganancia_maxima)
        return{
            'prom_precio' : prom_precio,
            'prom_precio_hom' : precio_prom_hom,
            'prom_precio_muj' : precio_prom_muj,
            'precios' : precios,
            'precios_hom' : precios_hom,
            'precios_muj' : precios_muj,
            'ganancia_prom_total' : ganancia_prom_total,
            'ganancia_prom_group' : ganancia_prom_group,
            'ganancia_prom_hom' : ganancia_prom_hom,
            'ganancia_prom_muj' : ganancia_prom_muj,
            'ganancias_total' : ganancias_total,
            'ganancias_group' : ganancias_group,
            'ganancias_hom' : ganancias_hom,
            'ganancias_muj' : ganancias_muj,
            'const_max' : const_max,
            'f' : porc_femenino,
            'm' : porc_masculino,
            'prom_edad_hom' : prom_edad_hom,
            'prom_edad_muj' : prom_edad_muj,
            'total_grupos' : total_grupos,
            'rondas_cajas' : rondas_cajas,
            'rondas_cajas_hom' : rondas_cajas_hom,
            'rondas_cajas_muj' : rondas_cajas_muj,
            'rondas_cajas_grupal' : rondas_cajas_grupal,
            'cmg_const' : cmg_const
        }

page_sequence = [
    Introduction,
    darPrecio,
    ResultsWaitPage,
    Resultados,
    Results,
    Quiz,
    ExpTeorico,
    CharWaitPage,
    Charts
]
