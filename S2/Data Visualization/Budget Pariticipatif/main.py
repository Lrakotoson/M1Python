# coding: utf-8

__author__ = 'Lrakotoson'
__maintainer__ = 'Loïc Rakotoson'
__email__ = 'contact@loicrakotoson.com'
__status__ = 'planning'


import pandas as pd

from scripts.filterdata import Data
from scripts.plotmap import mapPlot
from scripts.plotbar import barPlot, stackPlot
from scripts.markups import *

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Button, CheckboxGroup, CheckboxButtonGroup
from bokeh.events import ButtonClick
from bokeh.layouts import row, column, widgetbox

######################### DONNEES #########################

qt = pd.read_json("data/formated_quartiers.json")
bd = pd.read_csv("data/formated_budget.csv")

df_data = Data(bd, qt)

qt_source = ColumnDataSource(df_data.qt) # Quartiers
qt_source.remove('index')
bd_source = ColumnDataSource(df_data.bd) # Budgets
bd_source.remove('index')
pj_source = ColumnDataSource(df_data.proj) # Projets
pj_source.remove('index')
et_source = ColumnDataSource(df_data.etat) # Statuts
et_source.remove('index')

######################### MODELS ##########################

m_header = header()
m_footer = footer()
m_css = style()
m_blank = blank()
m_text = textInit()
m_year = textTitle('Année de campagne')
m_quartier = textTitle('Choix de quartiers')
m_status = textTitle('Statut des projets')

######################### WIDGETS #########################

f_year = CheckboxButtonGroup(
        labels = ['2016', '2017', '2018', '2019'])

f_quartier = CheckboxGroup(
        labels = [i for i in df_data.brut_qt.q_nom.unique().tolist()]
        )

f_etat = CheckboxButtonGroup(
    labels = ['Réalisé', 'Non réalisable', "A l'étude", 'En cours']
)

f_reset = Button(
    label = "Réinitialiser",
    button_type = "success")

widget = widgetbox(
    m_year, f_year,
    m_quartier, f_quartier,
    m_status, f_etat,
    f_reset,
    sizing_mode = "stretch_width"
)

sidebar = column(m_css, m_text, widget, width = 350)

######################## CALLBACKS ########################

def reset(event):
    """
    Réinitialise tous les filtres
    """
    f_year.active = []
    f_etat.active = []
    f_quartier.active = []
    df_data.reset()
    bd_source.data.update(df_data.bd.to_dict(orient = 'list'))
    qt_source.data.update(df_data.qt.to_dict(orient = 'list'))
    pj_source.data.update(df_data.proj.to_dict(orient = 'list'))
    et_source.data.update(df_data.etat.to_dict(orient = 'list'))


def update(attr,old,new):
    """
    Evalue l'ensemble des filtres actifs
    """
    yearChoose = f_year.active
    etatChoose = f_etat.active
    quartierChoose = f_quartier.active
    df_data.query(yearChoose, etatChoose, quartierChoose)
    bd_source.data.update(df_data.bd.to_dict(orient = 'list'))
    qt_source.data.update(df_data.qt.to_dict(orient = 'list'))
    pj_source.data.update(df_data.proj.to_dict(orient = 'list'))
    et_source.data.update(df_data.etat.to_dict(orient = 'list'))


f_year.on_change('active', update)
f_etat.on_change('active', update)
f_quartier.on_change('active', update)
f_reset.on_event(ButtonClick, reset)

########################## GRAPHS #########################

g_map = mapPlot(bd_source, qt_source)
g_bar = barPlot(pj_source)
g_stack = stackPlot(et_source)

graphs = column(
    g_map,
    row(
        g_bar, g_stack,
        sizing_mode = "stretch_width"),
    sizing_mode = "stretch_width")

########################## LAYOUT #########################

layout = column(
    m_header,
    row(sidebar, graphs, m_blank),
    m_footer,
    sizing_mode = "stretch_both")

curdoc().add_root(layout)