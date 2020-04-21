import numpy as np
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure

def barPlot(pj_source):
    """
    Barplot des projets par quartier et par état de projet
    pj_source: projet ColumnDataSource
    :return: bokeh figure
    """
    if len(pj_source.data) <= 1: # Filtre restreint
        plot = figure(title = "Projets par quartiers (VIDE)", tools = "")
        plot.vbar(0, 0)
        return plot

    plot = figure(
        x_range = [],
        title = "Projets par quartiers",
        tools = " "
    )
    
    plot.vbar(
        x = 'x', top = 'counts', source = pj_source,
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
    
    plot.x_range.factors = list(pj_source.data['x'])
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


def stackPlot(et_source):
    """
    Stack barplot de l'état des projets par année
    et_source: etat ColumnDataSource
    :return: bokeh figure
    """
    
    if len(et_source.data) <= 1: # Filtre restreint
        plot = figure(title = "Etat des projets par année (VIDE)", tools = "")
        plot.vbar(0, 0)
        return plot
    
    colormap = {
        'Realise': '#2ecc71',
        'Non_realisable': '#c0392b',
        "Etude": '#f0932b',
        'En_cours': '#f1c40f'
    }
    
    etats = [ # Pour l'ésthétique, dans cet ordre
        etat for etat in ['Realise', "Etude", 'En_cours', 'Non_realisable']
        if etat in et_source.data.keys()
    ]

    colors = [colormap[etat] for etat in etats]

    plot = figure(
        x_range = [],
        title = "Etat des projets par année",
        tools = ""
    )

    renderers = plot.vbar_stack(
        etats, x = 'b_year', color = colors,
        source = et_source, legend_label = etats,
        width = 0.9, name = etats
    )

    for r in renderers:
        etat = r.name
        hover = HoverTool(
            tooltips = [
                ("%s total" % etat, "@%s" % etat),
                ("Année", "@b_year")
            ],
            renderers = [r]
        )
        plot.add_tools(hover)


    plot.x_range.factors = list(et_source.data['b_year'])
    plot.toolbar.logo = None
    plot.xgrid.grid_line_color = None
    plot.legend.orientation = "horizontal"
    plot.legend.background_fill_alpha = 0.5
    
    return plot