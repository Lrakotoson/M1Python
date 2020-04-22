# coding: utf-8

__author__ = 'Lrakotoson'
__maintainer__ = 'Loïc Rakotoson'
__email__ = 'contact@loicrakotoson.com'
__status__ = 'planning'
__all__ = ['mapPlot']


from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from bokeh.palettes import Category20
from bokeh.transform import factor_cmap


def mapPlot(bd_source, qt_source):
    """
    Renvoie une map
    bd_source, qt_source: ColumnDataSource
    :return: bokeh figure
    """

    plot = figure(x_range = (-195729.64378600637, -175690.50954609076),
                  y_range = (6119069.396713561, 6131687.895850816),
                  x_axis_type = "mercator",
                  y_axis_type = "mercator",
                  sizing_mode = "stretch_width",
                  toolbar_location = "above"
                  )

    plot.add_tile(get_provider(Vendors.CARTODBPOSITRON))
    
    ######################### QUARTIERS #########################
    """
    Contour des quartiers de la base qt_source
    """
    quartier = plot.patches(xs = "q_x",
                         ys = "q_y",
                         source = qt_source,
                         color = factor_cmap(
                             'q_nom',
                             palette = Category20[12],
                             factors = qt_source.data['q_nom']),
                         alpha = 0.3)
    
    q_hover = HoverTool(tooltips = [('Quartier', '@q_nom')],
                        renderers = [quartier])
    
    plot.add_tools(q_hover)
    plot.axis.visible = False
    
    ########################## BUDGET ###########################
    """
    Répartition géographique des projets
    """
    budget = plot.circle('b_x',
                      'b_y',
                      source = bd_source,
                      size = 10,
                      color = factor_cmap(
                          'b_realise',
                          palette = ["#2ecc71", "#c0392b", "#f0932b", "#f1c40f"],
                          factors = ['Réalisé', 'Non réalisable',
                                     "A l'étude", 'En cours'
                                      ]),     
                      alpha = 0.7)
    
    b_hover = HoverTool(
        renderers = [budget],
        tooltips = """
                    <style>
                        .button {
                            color: #fff !important;
                            text-transform: uppercase;
                            text-decoration: none;
                            background: #60a3bc;
                            padding: 20px;
                            border-radius: 50px;
                            display: inline-block;
                            border: none;
                            transition: all 0.4s ease 0s;
                            }
                    </style>
                    <div align="center">
                        <p><strong>@b_libelle</strong></p>
                        <img src="@b_photo" alt=" " style="max-height:150px"></img>
                        <p align="justify">@b_description</p>
                        <div align="center">
                            <a class="button" href="@b_lien" target="_blank">
                                Découvrir
                            </a>
                        </div>
                    </div>
                   """
    )
    
    plot.add_tools(b_hover)
    plot.toolbar.logo = None

    return plot