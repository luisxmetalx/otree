from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Washington Vélez'

doc = """
Cuestionario demográfico
"""


class Constants(BaseConstants):
    name_in_url = 'cuest_demografico'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    c4_pregunta_1 = models.PositiveIntegerField(min=15, verbose_name="1)\t¿Cuál es su edad?")#edad
    c4_p2_op = ("Masculino", "Femenino")
    c4_pregunta_2 = models.CharField(choices=c4_p2_op, widget=widgets.RadioSelectHorizontal(),verbose_name = "2)\t¿Cuál es su género?")
    c4_p3_op = ("Centro de Guayaquil", "Sur de Guayaquil", "Norte de Guayaquil", "Otra Ciudad")#vivienda
    c4_pregunta_3 = models.CharField(choices=c4_p3_op, verbose_name = "3)\t¿Dónde vive?")
    c4_p4_op = ("Casa Propia", "Departamento Propio", "Arrienda Casa", "Arrienda Departamento", "Casa familiar", "Renta Cuarto")
    c4_pregunta_4 = models.CharField(choices=c4_p4_op, verbose_name = "4)\t¿En qué tipo de residencia vive?")#tipo residencia
    c4_p5_op = ("Estudiar", "Trabajar")
    c4_pregunta_5 = models.CharField(choices=c4_p5_op, verbose_name = "5)\t¿Cuál ha sido su principal ocupación durante los últimos 12 meses? La principal ocupación se define como el tipo de ocupación donde se gasta la mayor parte de su tiempo de trabajo.")
    c4_p6_op = (("Pobre", "Menos de US$ 364"), ("Media Baja", "Entre US$ 365 y US$ 600"), ("Media", "Entre US$ 601 y US$ 1000"), ("Media Alta", "Entre US$ 1000 y US$ 1600"), ("Alta", "Más de US$ 1601"))
    c4_pregunta_6 = models.CharField(choices=c4_p6_op, verbose_name = "6)\t¿Aproximadamente cuánto es el ingreso familiar en su hogar?")
    c4_pregunta_7 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name = ("7)\t¿Ha adquirido usted algún producto o servicio a crédito por lo cual esté actualmente pagando su valor?"))
    c4_pregunta_8 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name = "8)\t¿Tiene y usa usted tarjeta de crédito?")

    c4_pregunta_9 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name="9)\t¿Tiene usted hijos/as?")  # hijos

    c4_p10_op = ("Usted", "Padre", "Madre", "Otro")
    c4_pregunta_10 = models.CharField(choices=c4_p10_op, verbose_name = "10)\t¿Quién considera usted es el principal encargado de las decisiones de gasto del hogar?")
    c4_pregunta_11 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name = "11)\t¿Tiene usted seguro médico privado?")#seguro medico privado
    c4_pregunta_12 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name = "12)\t¿Tiene usted seguro de vida?")#seguro de vida
    c4_pregunta_13 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name = "13)\t¿Asiste con frecuencia a chequeos médicos de rutina, o a medicina preventiva?")#chequeos rutinarios
    c4_pregunta_14 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name = "14)\t¿Practica usted deportes extremos o deportes de aventura (ej. Motociclismo, bicicleta de montaña, andinismo, etc.)?")#deportes extremos
    c4_pregunta_15 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name="15)\t¿Tiene o realiza usted inversiones financieras (ej. pólizas de acumulación, certificados de depósito, acciones en la bolsa de valores, bonos,  etc.)  En cualquier institución o banco?")  # inversiones financieras
    c4_pregunta_16 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name="16)\t¿En el último año jugó o compró usted la lotería (cualquier marca de lotería)?")  # compra loteria
    c4_pregunta_17 = models.BooleanField(widget=widgets.RadioSelectHorizontal(), verbose_name="17)\t¿Fuma usted cigarrillo?")  # fuma
    c4_p18_op = ("1", "2", "3", "4", "5")
    c4_pregunta_18 = models.CharField(choices=c4_p18_op, verbose_name="18)\tEn una escala del 1 al 5 donde: 1 es nada paciente y 5 es muy paciente, usted es:")  # paciencia--> escala del 1 al 5

    c4_p19_op = ("Fiscal", "Particular")
    c4_pregunta_19 = models.CharField(choices=c4_p19_op, verbose_name="19)\t¿En qué clase de colegio usted se graduó?") # clase de colegio

    c4_p20_op = (
        ("FCNM", "FCNM - FACULTAD DE CIENCIAS NATURALES Y MATEMATICAS"),
        ("FCSH", "FCSH - FACULTAD DE CIENCIAS SOCIALES Y HUMANISTICAS"),
        ("FICT", "FICT - FACULTAD DE INGENIERIA EN CIENCIAS DE LA TIERRA"),
        ("FIEC", "FIEC - FACULTAD DE INGENIERIA EN ELECTRICIDAD Y COMPUTACIÓN"),
        ("FIMCP", "FIMCP - FACULTAD DE INGENIERIA EN MECÁNICA Y CIENCIAS DE LA PRODUCCION"),
        ("FIMCBOR", "FIMCBOR - FACULTAD DE INGENIERIA MARITIMA, CIENCIAS BIOLOGICAS, OCEANICAS Y RECURSOS NATURALES"),
        ("EDCOM", "EDCOM - ESCUELA DE DISEÑO Y COMUNICACION VISUAL"),
        ("FCV", "FCV - FACULTAD DE CIENCIAS DE LA VIDA"))

    c4_pregunta_20 = models.CharField(choices=c4_p20_op, verbose_name="20)\t¿En qué facultad estudia?") # facultad

    c4_pregunta_21 = models.FloatField(min=1.30, max=2.30, verbose_name="21)\tAproximadamente, ¿Cuánto es su estatura (en metros)?")

