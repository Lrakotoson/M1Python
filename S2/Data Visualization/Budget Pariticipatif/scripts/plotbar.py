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
        plot = figure(title = "Projets par quartiers (VIDE)")
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