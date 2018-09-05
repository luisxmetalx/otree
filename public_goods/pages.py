from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    def is_displayed(self):
        return self.round_number == 1

class Quiz(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = 'player'
    form_fields = ['genero','edad']

class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}
    
    def vars_for_template(self):
        return {
            'ronda' : self.round_number
            }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute."


class Results(Page):
    """Players payoff: How much each has earned"""

    def vars_for_template(self):
        promedio = self.group.total_contribution/Constants.players_per_group
        return {
            'total_earnings': self.group.total_contribution * Constants.multiplier,
            'promedio': promedio,
        }
class Graficas(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        """
        Insertar todas las rondas jugadas de manera dinamica
        """
        rondas=[]
        cont_promedio=[]
        cont_hombre=[]
        cont_mujeres=[]
        ganancia_total=[]
        ganancia_hombre=[]
        ganancia_mujeres=[]
        genero=[]
        prom_genero=[]
        num_player=len(self.subsession.get_players())
        rond=0
        promedio=0
        ganancia=0
        edad=0
        edadH=0
        edadM=0
        cm=0
        ch=0
        prom_edad=0
        prom_edadH=0
        prom_edadM=0
        h=0
        m=0
        #rondas
        for i in range(Constants.num_rounds):
            rond += 1
            rondas.append("Ronda "+str(rond))
        #contribucion promedio
        for i in range(1,rond+1):
            promedio=(sum([p.in_round(i).total_contribution for p in self.subsession.get_groups()]))
            cont_promedio.append(round(int(promedio)/num_player,2))
            promedio=0
        #ganacia total
        for i in range(1,rond+1):
            ganancia=(sum([p.in_round(i).payoff for p in self.subsession.get_players()]))
            ganancia_total.append(round(float(ganancia),2))
            ganancia=0
        #numero de mujeres y hombres
        for p in self.subsession.get_players():
            genero.append(p.genero)
            if p.genero == 'Masculino':
                edadH+=p.edad
            else:
                edadM+=p.edad
        h=genero.count('Masculino')
        m=genero.count('Femenino')
        prom_genero.append(round((h/num_player)*100,2))
        prom_genero.append(round((m/num_player)*100,2))
        #edades de participantes
        for p in self.subsession.get_players():
            edad+=p.edad
        prom_edad=round(edad/num_player,2)
        prom_edadH=round(edadH/h,2)
        prom_edadM=round(edadM/m,2)

        #contribuciones promedio por hombres y mujeres
        for i in range(1,rond+1):
            for p in self.subsession.get_players():
                if p.genero == 'Masculino':
                    ch+=p.in_round(i).contribution
                else:
                    cm+=p.in_round(i).contribution
            cont_hombre.append(round(int(ch)/h,2))
            cont_mujeres.append(round(int(cm)/m,2))
            ch=0
            cm=0
        #ganancia total hombres y mujeres
        for i in range(1,rond+1):
            for p in self.subsession.get_players():
                if p.genero == 'Masculino':
                    ch+=p.in_round(i).payoff
                else:
                    cm+=p.in_round(i).payoff
            ganancia_hombre.append(round(int(ch),2))
            ganancia_mujeres.append(round(int(cm),2))
            ch=0
            cm=0
        #rondas para la caja
        rond1=0
        for j in range(len(self.subsession.get_groups))
        for i in range(Constants.num_rounds):
            rond1 += 1
            rondas.append("Ronda "+str(rond1))
        return {
            'rondas': rondas,
            'promedio':cont_promedio,
            'ganancia': ganancia_total,
            'genero': genero,
            'pGenero': prom_genero,
            'prom_edad': prom_edad,
            'prom_edadH': prom_edadH,
            'prom_edadM': prom_edadM,
            'con_hombres': cont_hombre,
            'con_mujeres': cont_mujeres,
            'ganancia_h': ganancia_hombre,
            'ganancia_m': ganancia_mujeres,
        }

class AllGroupsWaitPage(WaitPage):
    wait_for_all_groups = True

page_sequence = [
    Introduction,
    Contribute,
    ResultsWaitPage,
    Results,
    Quiz,
    AllGroupsWaitPage,
    Graficas
]