# coding: utf-8

__author__ = 'Lrakotoson'
__maintainer__ = 'Loïc Rakotoson'
__email__ = 'contact@loicrakotoson.com'
__status__ = 'planning'
__all__ = [
    'header', 'footer', 'blank',
    'textInit', 'textTitle', 'style'
]


from bokeh.models import Div

def header():
    """
    En-tête en html
    :return: bokeh Model
    """

    div = Div(
        text = """
        <style>
            .text_header {
                display: inline-block;
                margin: 0;
            }

            .text_zone {
                display: inline-block;
                margin-left: 1.5%;
            }

            .title_header, .text_header {
                margin: 0;
                display: block;
            }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Viga&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <img src="https://www.lecollectifdesfestivals.org/annuaire/wp-content/uploads/cache/images/2020/04/Ville-de-Rennes/Ville-de-Rennes-353263439.png"
        alt="Rennes" style="filter: invert(5); width: 15%;">
        <div class = "text_zone">
            <h1 class = "title_header">Budget Participatif</h1>
            <p class = "text_header">Tableau de bord de suivi des campagnes de budget participatif dans la ville de Rennes</p>
        </div>
        """,
        style = {
            'top': 0,
            'left': 0,
            'width': '100%',
            'padding': '1%',
            'background-image': 'url(https://www.la-loi-pinel.com/wp-content/uploads/2018/08/cover-rennes-1920x800.jpg)',
            'background-attachment': 'fixed',
            'box-shadow': 'inset 2000px 0 0 0 rgba(39, 174, 96,0.6)',
            'font-family': '"Viga", Helvetica, sans-serif',
            'color': 'white',
            'text-shadow': '1px 2px 3px rgb(0, 148, 50)'
        },
        sizing_mode = "stretch_width"
    )

    return div


def footer():
    """
    Pied de page en html
    :return: bokeh Model
    """

    div = Div(
        text = """
        <style>
            .fa {
                color: white !important;
                font-size: x-large !important;
                padding: 0 2% !important;
            }
            p.foot {
                padding: 0 !important;
                margin: 0 !important;
            }
        </style>
        <center>
            <a href="https://github.com/Lrakotoson" target="_blank"><i class="fa fa-github"></i></a>
            <a href="https://loicrakotoson.com/" target="_blank"><i class="fa fa-globe"></i></a>
            <a href="https://www.linkedin.com/in/loicrakotoson" target="_blank"><i class="fa fa-linkedin"></i></a>
            <p class="foot"><strong>Loïc Rakotoson</strong></p>
            <p class="foot">Master 1 - MAS - Rennes 2</p>
            <p class="foot">Avril 2020</p>
        </center>
        """,
        style = {
            'bottom': '0',
            'left': '0',
            'width': '100%',
            'padding': '1%',
            'background-image': 'url(https://www.la-loi-pinel.com/wp-content/uploads/2018/08/cover-rennes-1920x800.jpg)',
            'box-shadow': 'inset 2000px 0 0 0 rgba(127, 140, 141, 0.5)',
            'background-attachment': 'fixed',
            'font-family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            'color': 'white',
            'filter': 'grayscale(100%)',
            'text-shadow': '1px 2px 3px rgb(87, 101, 116)'
        },
        sizing_mode = "stretch_width"
    )

    return div


def blank():
    """
    Colonne vide
    :return: bokeh Model
    """

    div = Div(
        text = " ",
        style = {
            'width': '10px',
            'height': '100%'
        }
    )
    return div


def textInit():
    """
    Texte d'introduction aux filtres
    :return: bokeh Model
    """
    div = Div(
        text = """
        <h2 style="border:2px solid #dcdde1; color: white; background-color:#718093">Filtres</h2>
        <p>Les différents filtres permettent de sélectionner les enregistrements
            et mettent à jour les 3 graphiques, à savoir la répartition géographique,
            le nombre de projets par quartier, le statut et le nombre de projets pour
            chaque campagne.
        </p>
        """,
        style = {
            'text-align': 'center',
            'font-family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        },
        sizing_mode = "stretch_width"
    )
    return div


def textTitle(element):
    """
    Titre de chaque filtre
    :element: str, titre
    :return: bokeh Model
    """
    div = Div(
        text = "<h3>{}</h3>".format(element),
        style = {
            'display': 'block',
            'text-align': 'center',
            'font-family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        },
        sizing_mode = "stretch_width"
    )
    return div


def style():
    """
    Style CSS global
    :return: bokeh Model
    """
    div = Div(
        text = """
        <style>

            body {
                margin: 0 !important;
                padding: 0 !important;
                overflow-x: hidden !important;
            }

            div.bk:has(> div.bk-clearfix) {
                left: 0 !important;
            }

            div.bk-input-group {
                padding: 2px !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            div.bk-input-group label span{
                display: inline-block !important;
                background-color: rgba(255, 255, 255, .9) !important;
                border: 3px solid rgba(139, 139, 139, .3) !important;
                color: black;
                border-radius: 25px !important;
                white-space: nowrap !important;
                margin: 3px 0px !important;
                -webkit-touch-callout: none !important;
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
                user-select: none !important;
                -webkit-tap-highlight-color: transparent !important;
                transition: all .2s !important;
                padding: 8px 12px !important;
                cursor: pointer !important;
            }
            
            div.bk-input-group label span::before {
                display: inline-block !important;
                font-style: normal !important;
                font-variant: normal !important;
                text-rendering: auto !important;
                -webkit-font-smoothing: antialiased !important;
                font-family: "FontAwesome" !important;
                font-weight: 900 !important;
                font-size: 12px !important;
                padding: 2px 6px 2px 2px !important;
                content: "\\f067" !important;
                transition: transform .3s ease-in-out !important;
            }
            
            div.bk-input-group label input[type="checkbox"]:checked + span::before {
                content: "\\f00c" !important;
                transform: rotate(-360deg) !important;
                transition: transform .3s ease-in-out !important;
            }
            
            div.bk-input-group label input[type="checkbox"]:checked + span {
                border: 2px solid #2ecc71 !important;
                background-color: #27ae60 !important;
                color: #f5f6fa !important;
                transition: all .2s !important;
            }
            
            div.bk-input-group label input[type="checkbox"] {
                display: absolute !important;
                position: absolute !important;
                opacity: 0 !important;
            }
            
            div.bk-input-group label input[type="checkbox"]:focus + span {
                border: 2px solid #e9a1ff !important;
            }  
        </style>
        """,
        style = {'display': 'none'}
    )
    return div


    """
    Titre de chaque filtre
    :element: str, titre
    :return: bokeh Model
    """
    div = Div(
        text = "<h3>{}</h3>".format(element),
        style = {
            'text-align': 'center',
            'font-family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        },
        sizing_mode = "stretch_width"
    )
    return div