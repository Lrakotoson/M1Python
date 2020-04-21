import numpy as np
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, FactorRange
from bokeh.plotting import figure

def minQuartier(quartiers):
    """
    Le nom de quartier le plus court
    quartiers: valeur de DataFrame
    :return: str ou quartiers
    """
    if isinstance(quartiers, str):
        quartiers = quartiers.split(' - ')
        q_min = min(quartiers, key = len).strip()
        return q_min

def barPlot(bd_source):
    """
    Barplot des projets par quartier et par état de projet
    bd_source: budget ColumnDataSource
    :return: bokeh figure
    """

    colormap = {
        'Réalisé': '#2ecc71',
        'Non réalisable': '#c0392b',
        "A l'étude": '#f0932b',
        'En cours': '#f1c40f'
    }
    
    bd_frame = pd.DataFrame(bd_source.data)
    
    if bd_frame.shape[0] == 0: # Absence de projet
        plot = figure(title = "Projets par quartiers (vides)")
        plot.vbar(0, 0)
        return plot
    
    ########################## DONNEES ##########################
    """
    Calcul de nombre de projet par quartier et par état de projet
    Création d'une nouvelle ColumnDataSource
    """
    bd_frame.b_quartier = bd_frame.b_quartier.apply(minQuartier)
    

    dico = bd_frame.groupby(['b_quartier', 'b_realise'
                             ]).size().unstack().fillna(0).stack().to_dict()

    
    x = list(dico.keys())
    counts = list(dico.values())
    legends = [legend[1] for legend in x]
    quartiers = [quartier[0] for quartier in x]
    color = [colormap[legend] for legend in legends]
    
    source = ColumnDataSource(data = dict(
        x = x, counts = counts,
        quartiers = quartiers,
        legends = legends, color = color
    ))
    
    ########################### PLOT ###########################
    """
    Barplot par groupe
    """
    plot = figure(
        x_range = FactorRange(*x),
        title = "Projets par quartiers",
        tools = " "
    )
    
    plot.vbar(
        x = 'x', top = 'counts', source = source,
        fill_color = 'color', legend_field = 'legends',
        width = 1, line_alpha = 0
    )
    
    hover_bar = HoverTool(
        tooltips = [
            ('Quartier', '@quartiers'),
            ('Etat', '@legends'),
            ('Nombre', '@counts')
        ]
    )
    
    plot.add_tools(hover_bar)
    
    plot.toolbar.logo = None
    plot.y_range.start = 0
    plot.xgrid.grid_line_color = None
    plot.xaxis.major_label_text_font_size = "0px"
    plot.xaxis.major_tick_line_width = 0
    plot.xaxis.axis_line_width = 0
    plot.xaxis.group_label_orientation = np.pi/2
    plot.legend.orientation = "horizontal"
    plot.legend.background_fill_alpha = 0.5
    
    return plot