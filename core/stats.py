import pygal
from pygal.style import LightColorizedStyle, Style
from datetime import date, datetime
import calendar
from core.objects import Donation, DonationType
from sqlalchemy import extract
from dateutil.rrule import rrule, MONTHLY


# def gen_month(inc):
    # actuel = date.today().month + inc   # on récupère le mois actuel (en chiffre) et on lui additionne le parametre 'inc'
#   actuel = 5 + inc                   # test à partir d'un autre mois que l'actuel
    # 
    # if actuel > 12 :                            # si on dépasse le nombre de mois dans une année (12), on soustrait 12, pour retrouver une valeur cohérente
        # actuel = actuel - 12
    # nom_actuel = calendar.month_name[actuel]    # on transforme la valeur du mois en son nom
    # return nom_actuel                           # on balance le résultat >:3


# https://stackoverflow.com/a/6064267
def gen_months(start_month, start_year, end_month, end_year):
    start = datetime(start_year, start_month, 1)
    end = datetime(end_year, end_month, 1)
    return [(d.month, d.year) for d in rrule(MONTHLY, dtstart=start, until=end)]


def monthlysum_monthly(month, year):
    crawl_recurring = (Donation.query
        .filter(Donation.type == DonationType.monthly)
        .filter(Donation.hidden == False)
        .filter(extract('month', Donation.updated) <= month)
        .filter(extract('year', Donation.updated) <= year)
        .filter(extract('month', Donation.created) >= month)
        .filter(extract('year', Donation.created) >= year)
    )
    recurring_count = crawl_recurring.count()
    recurring_sum = sum([d.amount for d in crawl_recurring]) / 100
    return recurring_sum


def monthlysum_onetime(month, year):
    month_onetime = (Donation.query
        .filter(Donation.type == DonationType.one_time)
        .filter(extract('month', Donation.created) == month)
        .filter(extract('year', Donation.created) == year))
    onetime_count = month_onetime.count()
    onetime_sum = sum([d.amount for d in month_onetime]) / 100
    return onetime_sum


# génération du graphique
def gen_chart():
    custom_style = Style(
        label_font_size=15.0,
        background='transparent')

    line_chart = pygal.Line(fill=True, style=custom_style, x_label_rotation=25, y_title='en €', y_title_size=17, x_title='mois', disable_xml_declaration=True, dots_size=5, show_x_guides=True )
    line_chart.title = 'Évolution des donations'

    today = date.today()
    xlabels, onetime, monthly = [], [], []
    for month in gen_months(today.month + 0, today.year - 1, today.month, today.year): # génération des 12 mois passés (incluant l'actuel et l'année des mois)
        xlabels.append(calendar.month_name[month[0]] + " " + str(month[1]))
        onetime.append(monthlysum_onetime(month[0], month[1]))
        monthly.append(monthlysum_monthly(month[0], month[1]))

    line_chart.x_labels = xlabels
    line_chart.add('Ponctuels', onetime)
    line_chart.add('Mensuels', monthly)
 
#    line_chart.add('Mensuel', [ monthlysum_monthly(month, 2019) for month in range(0, 12)[::-1] ])

#    line_chart.add('Objectif', [ 13.12, None, None, None, None, None, None, None, None, None, None, None, 13.12 ], fill=False)
    line_chart.render_to_file('static/chart.svg')



