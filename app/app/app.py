# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_dangerously_set_inner_html
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import json
import numpy as np
import os
from scipy import stats

import pprint
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from functools import lru_cache
from wb_nlp import dir_manager

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server


# @lru_cache(maxsize=None)
def get_country_popularity_fig():
    df = pd.read_csv(dir_manager.get_data_dir(
        'preprocessed', 'country_popularity.csv'))

    return px.choropleth(
        df, locations='iso_alpha', locationmode='ISO-3',
        color='popularity', animation_frame='year',
        color_continuous_scale='Blues')


# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
nav = dbc.NavbarSimple(
    [
        dbc.NavItem(dbc.NavLink("HOME", href="#")),
        dbc.NavItem(dbc.NavLink("SEARCH", href="#")),
        dbc.NavItem(dbc.NavLink("EXPLORE", active=True, href="#")),
        dbc.NavItem(dbc.NavLink("ANALYZE", href="#")),
        dbc.NavItem(dbc.NavLink("METHODS & TOOLS", href="#")),
        dbc.NavItem(dbc.NavLink("API", href="#")),
        dbc.NavItem(dbc.NavLink("ABOUT", href="#")),
    ],
    light=True,
    # color="red",
    # color="primary",
    # dark=True,
    # , horizontal='end'
)

nav_link_style = {"padding-top": "5px", "padding-bottom": "5px"}

sidebar_items = [
    dict(
        link_children=["INTRODUCTION"],
        href="/intro",
        id="intro",
        style=nav_link_style,
    ),
    dict(
        link_children=["INTRODUCTION"],
        href="/intro",
        id="intro",
        style=nav_link_style,
    ),
]

sub_apps = dict(
    word_embeddings=dcc.Markdown("""# Word embeddings""")
)

CONTENT = dict(
    topic_composition=dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                <iframe src="https://agoldst.github.io/dfr-browser/demo/" frameborder="0" height="800px" width="100%" >Header</h1>
            '''),
    corpus__sources_and_volume=dcc.Markdown("""# Corpus - Metadata and API

Description of metadata collected and augmented;

Access to CSV and API (MongoDB)"""),
    corpus__geographic_coverage=dcc.Markdown(
        """# Corpus - Geographic coverage"""),
    corpus__test_corpus=dcc.Markdown("""# Corpus - Test corpus

Provide a test corpus of ~50,000 WB docs with related metadata, source and clean txt files

Purpose: training

Collection of selected scripts for modeling, analysis"""),
    word_embeddings=sub_apps.get("word_embeddings"),
)

vertical_nav_items = [dbc.NavItem(
    dbc.NavLink(
        children=item["link_children"],
        href=item["href"],
        id=item["id"],
        style=item["style"],
    )
) for item in sidebar_items]

vertical_nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("INTRODUCTION", active=True,
                                href="/intro", id='intro', style=nav_link_style)),
        dbc.NavItem(children=[
            dbc.NavLink(children=[
                "CORPUS"
            ], href="/corpus", id='corpus', style=nav_link_style),
            dbc.Collapse(
                dbc.NavItem([
                    dbc.NavLink(children=[
                        "Sources and volume"
                    ], href="/corpus/sources-and-volume", id="corpus__sources_and_volume"),
                    dbc.NavLink(children=[
                        "Geographic coverage"
                    ], href="/corpus/geographic-coverage", id="corpus__geographic_coverage"),
                    dbc.NavLink(children=[
                        "Metadata and API"
                    ], href="/corpus/metadata-and-api", id="corpus__metadata_and_api"),
                    dbc.NavLink(children=[
                        "Test corpus"
                    ], href="/corpus/test-corpus", id="corpus__test_corpus")
                ], style=dict(float="right")),
                id="collapse",
            )
        ]),
        dbc.NavItem(dbc.NavLink("TOPIC COMPOSITION",
                                href="/topic-composition", id='topic-composition', style=nav_link_style)),
        dbc.NavItem(dbc.NavLink("TOPIC PROFILES",
                                href="/topic-profiles", id='topic-profiles', style=nav_link_style)),
        dbc.NavItem(dbc.NavLink("TOPIC TAXONOMY",
                                href="/topic-taxonomy", id='topic-taxonomy', style=nav_link_style)),
        dbc.NavItem(dbc.NavLink("TOPIC RELATIONSHIPS",
                                href="/topic-relationships", id='topic-relationships', style=nav_link_style)),
        dbc.NavItem(dbc.NavLink("WORD EMBEDDINGS",
                                href="/word-embeddings", id='word-embeddings', style=nav_link_style)),
        dbc.NavItem(dbc.NavLink("SIMILARITY",
                                href="/similarity", id='similarity', style=nav_link_style)),
        dbc.NavItem(dbc.NavLink("MONITORING SYSTEM",
                                href="/monitory-system", id='monitory-system', style=nav_link_style)),
    ],
    pills=True,
    vertical=True,
)

# app.layout = html.Div(children=[
#     html.Div(children=[
#         html.Br(),
#         nav
#     ]),
#     dbc.Container(children=[
#         html.Br(),
#         html.Br(),
#         html.Br(),
#         html.Br(),
#         dbc.Row(children=[
#             dbc.Col(children=[
#                 vertical_nav
#             ], width=2),
#             dbc.Col(children=[
#             ], width=1),
#             dbc.Col(children=[
#             ], id='content-panel', width=9)
#         ])
#     ], fluid=True)
# ])

app.layout = html.Div(children=[
    dcc.Location(id="url"),
    dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(children=[
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                vertical_nav
            ], width=2.5),
            dbc.Col(children=[
            ], width=1),
            dbc.Col(children=[
                html.Div(children=[
                    html.Br(),
                    nav
                ]),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div(children=[
                ], id="content-panel"),
                dcc.Graph(id="content-graph")
            ], width=8),
            dbc.Col(children=[
            ], width=0.5),
        ])
    ], fluid=True)
])


nav_ids = [
    "intro",
    "corpus",
    "topic-composition",
    "topic-profiles",
    "topic-taxonomy",
    "topic-relationships",
    "word-embeddings",
    "similarity",
    "monitory-system",
]


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on


# @app.callback(
#     [Output(f"{i}", "active") for i in nav_ids],
#     [Input("url", "pathname")],
# )
# def toggle_active_links(pathname):
#     print(pathname)
#     if pathname == "/":
#         # Treat page 1 as the homepage / index
#         home = [True] + [False] * (len(nav_ids) - 1)
#         return home

#     print(pathname)

#     return [pathname == f"/{i}" for i in nav_ids]


# Nav callbacks
@ app.callback(
    [
        Output("content-panel", "children"),
        Output("content-graph", "figure"),
        Output("collapse", "is_open")
    ] + [Output(f"{i}", "active") for i in nav_ids],
    [Input("url", "pathname")],
    # [State("collapse", "is_open")],
)
def intro_content(
        *args, **kwargs
):
    element = ""
    # https://dash.plotly.com/advanced-callbacks
    ctx = dash.callback_context
    pathname = ctx.inputs['url.pathname']
    if pathname is None:
        pathname = '/'

    # try:
    #     nav_id = ctx.triggered[0]['prop_id'].split('.')[0]
    # except IndexError:
    #     nav_id = 'intro'

    # ctx_msg = json.dumps({
    #     'states': ctx.states,
    #     'triggered': ctx.triggered,
    #     'inputs': ctx.inputs,
    # }, indent=2)

    # print(ctx_msg)

    default_element = dcc.Markdown("""# Introduction

Explain purpose and main components of the “EXPLORE” section of the site.

- Corpus describes the collection of documents (sources, scope, coverage, updates)
- Topic composition based on LDA model; describes the distribution of topics in the corpus or sub-corpus for different LDA models
- Topic profiles; select one topic, and see how it has evolved over time, by region, source, type, etc.
- Classification model: taxonomy tagging
- Word embeddings: semantic closeness using word2vec
- Similarity: select or load a document, find closest based on different measures of similarity

All code (except scrapers) in GitHub. See Methods and Tools.""")

    content_id = pathname.lstrip("/").replace("/", "__").replace("-", "_")
    print(content_id)

    element = CONTENT.get(content_id, default_element)

    # if pathname == "/topic-composition":
    #     # element = html.Iframe(
    #     #     src="https://agoldst.github.io/dfr-browser/demo/#", height="800px", width="100%")
    #     element = dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
    #             <iframe src="https://agoldst.github.io/dfr-browser/demo/" frameborder="0" height="800px" width="100%" >Header</h1>
    #         ''')
    # elif pathname == "/corpus":
    #     element = dcc.Markdown("# This is a corpus page...")
    # else:
    #     content.

    is_corpus_open = pathname.startswith("/corpus")
    content_figure = None

    if content_id == 'corpus__geographic_coverage':
        content_figure = get_country_popularity_fig()

    outputs = [element, content_figure, is_corpus_open] + \
        [pathname == f"/{i}" for i in nav_ids]

    return outputs

# nav_id = ctx.triggered[0]['prop_id'].split('.')[0]


# @ app.callback(
#     Output("content-panel", "children"),
#     [Input("corpus", "children")],
# )
# def corpus_content(children):
#     return dcc.Markdown(children)


# @ app.callback(
#     Output("content-panel", "children"),
#     [Input("topic-composition", "children")],
# )
# def topic_composition_content(children):
#     return dcc.Markdown(children)


# @ app.callback(
#     Output("content-panel", "children"),
#     [Input("topic-profiles", "children")],
# )
# def topic_profiles_content(children):
#     return dcc.Markdown(children)


# @ app.callback(
#     Output("content-panel", "children"),
#     [Input("topic-taxonomy", "children")],
# )
# def topic_taxonomy_content(children):
#     return dcc.Markdown(children)


# @ app.callback(
#     Output("content-panel", "children"),
#     [Input("topic-relationships", "children")],
# )
# def topic_relationships_content(children):
#     return dcc.Markdown(children)


# @ app.callback(
#     Output("content-panel", "children"),
#     [Input("word-embeddings", "children")],
# )
# def word_embeddings_content(children):
#     return dcc.Markdown(children)


# @ app.callback(
#     Output("content-panel", "children"),
#     [Input("similarity", "children")],
# )
# def similarity_content(children):
#     return dcc.Markdown(children)


# @ app.callback(
#     Output("content-panel", "children"),
#     [Input("monitory-system", "children")],
# )
# def monitory_system_content(children):
#     return dcc.Markdown(children)


if __name__ == '__main__':
    # https://community.plotly.com/t/dash-callbacks-are-not-async-handling-multiple-requests-and-callbacks-in-parallel/5848/3
    # gunicorn -b :8000 -w 2 --worker-class gevent --threads 8 app:server
    # app.run_server(host='0.0.0.0', port=8000, debug=True,
    #                threaded=False, processes=1)

    app.run_server(host='0.0.0.0', port=8000, debug=True,
                   threaded=True, processes=1)

    # app.run_server(host='0.0.0.0', port=8000, debug=True)
