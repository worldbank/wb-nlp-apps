# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
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
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

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

vertical_nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("INTRODUCTION", active=True,
                                href="/intro", id='intro')),
        dbc.NavItem(children=[
            dbc.NavLink(children=[
                "CORPUS",
            ], href="/corpus", id='corpus'),
            dbc.NavItem([
                dbc.NavLink(children=[
                    "Sources and volume"
                ], href="/corpus/sources-and-volume"),
                dbc.NavLink(children=[
                    "Geographic coverage"
                ], href="/corpus/geographic-coverage"),
                dbc.NavLink(children=[
                    "Metadata and API"
                ], href="/corpus/metadata-and-api"),
                dbc.NavLink(children=[
                    "Test corpus"
                ], href="/corpus/test-corpus")
            ], style=dict(float="right"))
        ]),
        dbc.NavItem(dbc.NavLink("TOPIC COMPOSITION",
                                href="/topic-composition", id='topic-composition')),
        dbc.NavItem(dbc.NavLink("TOPIC PROFILES",
                                href="/topic-profiles", id='topic-profiles')),
        dbc.NavItem(dbc.NavLink("TOPIC TAXONOMY",
                                href="/topic-taxonomy", id='topic-taxonomy')),
        dbc.NavItem(dbc.NavLink("TOPIC RELATIONSHIPS",
                                href="/topic-relationships", id='topic-relationships')),
        dbc.NavItem(dbc.NavLink("WORD EMBEDDINGS",
                                href="/word-embeddings", id='word-embeddings')),
        dbc.NavItem(dbc.NavLink("SIMILARITY",
                                href="/similarity", id='similarity')),
        dbc.NavItem(dbc.NavLink("MONITORING SYSTEM",
                                href="/monitory-system", id='monitory-system')),
    ], pills=True,
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

                ], id="content-panel")
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
@app.callback(
    [Output(f"{i}", "active") for i in nav_ids],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    print(pathname)
    if pathname == "/":
        # Treat page 1 as the homepage / index
        home = [True] + [False] * (len(nav_ids) - 1)
        return home

    print(pathname)

    return [pathname == f"/{i}" for i in nav_ids]


# Nav callbacks
@ app.callback(
    Output("content-panel", "children"),
    [Input("intro", "n_clicks"),
     Input("corpus", "n_clicks"),
     Input("topic-composition", "n_clicks"),
     Input("topic-profiles", "n_clicks"),
     Input("topic-taxonomy", "n_clicks"),
     Input("topic-relationships", "n_clicks"),
     Input("word-embeddings", "n_clicks"),
     Input("similarity", "n_clicks"),
     Input("monitory-system", "n_clicks")],
)
def intro_content(
        n_clicks1,
        n_clicks2,
        n_clicks3,
        n_clicks4,
        n_clicks5,
        n_clicks6,
        n_clicks7,
        n_clicks8,
        n_clicks9,
):
    element = ""
    # https://dash.plotly.com/advanced-callbacks
    ctx = dash.callback_context
    nav_id = ctx.triggered[0]['prop_id'].split('.')[0]
    # print(ctx)

    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs,
        # 'ctx': ctx
    }, indent=2)
    print(ctx_msg)

    if nav_id == "topic-composition":
        element = html.Iframe(
            src=f'https://mahalla.avsolatorio.com', height="800px", width="100%")
    else:
        element = dcc.Markdown(f"""# Introduction

Explain purpose and main components of the “EXPLORE” section of the site.

- Corpus describes the collection of documents (sources, scope, coverage, updates)
- Topic composition based on LDA model; describes the distribution of topics in the corpus or sub-corpus for different LDA models
- Topic profiles; select one topic, and see how it has evolved over time, by region, source, type, etc.
- Classification model: taxonomy tagging
- Word embeddings: semantic closeness using word2vec
- Similarity: select or load a document, find closest based on different measures of similarity

All code (except scrapers) in GitHub. See Methods and Tools.""")

    return element


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
    app.run_server(host='0.0.0.0', port=8000, debug=True,
                   threaded=False, processes=1)

    # app.run_server(host='0.0.0.0', port=8000, debug=True)
