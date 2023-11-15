"""
Launches a dashboard to visualizes academic world dataset. 

Requires 3 databases configured according to MP1. Containing AcademicWorld dataset. 

Michael Miller and Michael Inoue for University of Illinois CS 411
4/17/2023
"""

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import mongodb_utils
import neo_utils
import mysql_utils
import plotly.express as px

# MongoDB Init
mongodb_utils.init_mongodb()

# Common strings for UI 
CONFIG_CARD_TITLE = 'Configure Widget'

# Dash config 
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Using example app layout here for inspiration: https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/

# data for cluster widget
cluster_data = neo_utils.get_largest_clusters()
cluster_labels = [{'name': 'Cluster', 'id': 0}, {'name': 'Keyword Count', 'id': 1}]

# data for keyword similarity widget
cluster_similarity_data = neo_utils.get_similar_clusters('deep learning')
cluster_similarity_labels = [{'name': 'Keyword/Cluster', 'id': 0}, {'name': 'Shared Publications', 'id': 1}]

# data for keyword audit widget
keyword_audit_data = mysql_utils.get_recently_rated()
keyword_audit_labels = [{'name': 'Keyword', 'id': 'name'}, {'name': 'Rating', 'id': 'rating'}]



keyword_audit_widget = dbc.Card([dbc.CardBody([
    html.H4('Rate a keyword', className="card-title"),
    dbc.Input(id='audit-keyword', type='text', placeholder='Keyword'),
    dbc.Input(id='audit-rating', type='number', placeholder='Rating (0-5)'),
    dbc.Button(id='keyword-audit-button', n_clicks=0, children='Rate')
    ])])

keyword_popularity_widget = dbc.Card([dbc.CardBody([
    html.H4(CONFIG_CARD_TITLE, className="card-title"),
    dbc.Input(id='keyword', type='text', placeholder='Keyword'),
    dbc.InputGroup([
        dbc.InputGroupText("From Year:"),
        dbc.Input(id='start-year-keyword-popularity', type='number', placeholder='Start Year'),
        dbc.InputGroupText("To Year:"),
        dbc.Input(id='end-year-keyword-popularity', type='number', placeholder='End Year')
        ]),
    dbc.Button(id='keyword-popularity-button', n_clicks=0, children='Search')
    ])])

university_research_widget = dbc.Card([dbc.CardBody([
    html.H4(CONFIG_CARD_TITLE, className="card-title"),
    dbc.Input(id='research-interests-keyword', type='text', placeholder='Keyword'),
    dcc.Dropdown(
        id="research-interests-university",
        options=[
            {"label": col, "value": col} for col in mongodb_utils.mongo_db.faculty.distinct("affiliation.name")
        ],
        placeholder="University"
    ),
    dbc.InputGroup([
        dbc.InputGroupText("From Year:"),
        dbc.Input(id='start-year-research-interests', type='number', placeholder='Start Year'),
        dbc.InputGroupText("To Year:"),
        dbc.Input(id='end-year-research-interests', type='number', placeholder='End Year')
        ]),
    dbc.Button(id='research-interests-button', n_clicks=0, children='Search')
    ])])

research_publication_count_widget = dbc.Card([dbc.CardBody([
    html.H4(CONFIG_CARD_TITLE, className="card-title"),
    dbc.Input(id='researcher-publication-keyword', type='text', placeholder='Keyword'),
    dcc.Dropdown(
        id="researcher",
        options=[
            {"label": col, "value": col} for col in mongodb_utils.mongo_db.faculty.distinct("name")
        ],
        placeholder="Researcher",
    ),
    dbc.InputGroup([
        dbc.InputGroupText("From Year:"),
        dbc.Input(id='start-year-researcher-publication-count', type='number', placeholder='Start Year'),
        dbc.InputGroupText("To Year:"),
        dbc.Input(id='end-year-researcher-publication-count', type='number', placeholder='End Year')
        ]),
    dbc.Button(id='researcher-publication-count-button', n_clicks=0, children='Search')
    ])])

create_cluster_widget = dbc.Card([dbc.CardBody([
    html.H4('Create a Cluster', className="card-title"),
    dbc.Input(id='cluster-input', type='text', placeholder='Keywords to cluster'),
    dbc.Button(id='create-cluster-button', n_clicks=0, children='Create')
    ])])

cluster_compare_widget = dbc.Card([dbc.CardBody([
    html.H4(CONFIG_CARD_TITLE, className="card-title"),
    dbc.Input(id='cluster-compare-input', type='text', placeholder='Keyword to compare'),
    dbc.Button(id='cluster-compare-button', n_clicks=0, children='Search')
    ])])


app.layout = dbc.Container([
    html.H1(children='Research Time - Exploring Research Trends over Time', style={'textAlign': 'center', 'margin': 20}),
    dbc.ListGroup([
        dbc.ListGroupItem([
            html.H2(children='Popularity of Keywords in Publications Over Time'),
            dbc.Row([
                dbc.Col(keyword_popularity_widget, md=4),
                dbc.Col(dcc.Graph(id='keyword-popularity-graph'), md=8)
                ], align="center"),
            ]),
        dbc.ListGroupItem([
            html.H2(children='Popularity of Research Interests at Universities Over Time'),
            dbc.Row([
                dbc.Col(dcc.Graph(id='research-interests-graph'), md=8),
                dbc.Col(university_research_widget, md=4)
                ], align="center"),
            ]),
        dbc.ListGroupItem([
            html.H2(children='Researcher Publication Count Over Time'),
            dbc.Row([
                dbc.Col(research_publication_count_widget, md=4),
                dbc.Col(dcc.Graph(id='researcher-publication-count-graph'), md=8)
                ], align="center"),
            ]),
        dbc.ListGroupItem([
            html.H2('Keyword Clustering'),
            dbc.Row([
                dbc.Col([
                    html.H3('Clustered Keywords', style={'textAlign': 'center'}),
                    dbc.Row([
                        dbc.Col(create_cluster_widget, md=4), 
                        dbc.Col(dash_table.DataTable(data=cluster_data, columns=cluster_labels, id='cluster-table'), md=8)
                        ], align='center')
                    ], md=6),
                dbc.Col([
                    html.H3('Top Cluster/Keyword Similarity for "deep learning"', style={'textAlign': 'center'}, id='cluster-compare-title'),
                    dbc.Row([
                        dbc.Col(cluster_compare_widget, md=4), 
                        dbc.Col(dash_table.DataTable(data=cluster_similarity_data, columns=cluster_similarity_labels, id='cluster-compare-table'), md=8)
                        ], align='center')
                    ], md=6)
                ], align="center"),
            
            ]),
        dbc.ListGroupItem([
            html.H2(children='Keyword Audit'),
            dbc.Row([
                dbc.Col(keyword_audit_widget, md=3), 
                dbc.Col([
                    html.H3('Recent ratings', style={'textAlign': 'center'}),
                    dash_table.DataTable(data=keyword_audit_data, columns=keyword_audit_labels, id='keyword-audit-table')
                    ], md=3)
                ], align="center"),
            ]),
        ]),
    
    ], fluid=True)


# called whenever keyword is rated
@app.callback(Output('keyword-audit-table', 'data'),
              Input('keyword-audit-button', 'n_clicks'),
              State('audit-keyword', 'value'), 
              State('audit-rating', 'value'))
def rate_keyword(n_clicks, keyword, rating):
    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    # rating will be None if non-numeric
    if keyword and rating is not None:
        mysql_utils.rate_keyword(keyword, rating) 
        
    return mysql_utils.get_recently_rated()


# called whenever create cluster widget is refreshed 
@app.callback(Output('cluster-table', 'data'), [
                  Input('create-cluster-button', 'n_clicks'),
                  State('cluster-input', 'value')],)
def update_clusters(n_clicks, keyword_string):
    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    if keyword_string is not None:        
        neo_utils.cluster_keywords(keyword_string)
        
    return neo_utils.get_largest_clusters()

# called when new query is entered for keyword similarity
@app.callback(Output('cluster-compare-table', 'data'),
              Output('cluster-compare-title', 'children'),
              Input('cluster-compare-button', 'n_clicks'),
              State('cluster-compare-input', 'value'))
def similar_keyword_query(n_clicks, keyword):
    if keyword is not None:
        out_vals = neo_utils.get_similar_clusters(keyword)
        if len(out_vals) > 0:
            
            out_str = 'Top Cluster/Keyword Similarity for "{}"'.format(keyword)
            return out_vals, out_str
    
    return dash.no_update

@app.callback(Output('keyword-popularity-graph', 'figure'),
              [
                  Input('keyword-popularity-button', 'n_clicks'),
                  Input('keyword', 'value'),
                  Input('start-year-keyword-popularity', 'value'),
                  Input('end-year-keyword-popularity', 'value'),
              ],
              )
def update_keyword_popularity_graph(n_clicks, keyword, start_year, end_year):
    if n_clicks > 0 and keyword is not None:
        results = list(
            mongodb_utils.get_keyword_popularity_over_time(keyword_name=keyword, year1=start_year, year2=end_year))
        if results == []:
            return {}
        fig = px.bar(results, x='year', y='keyword score', title=f'Popularity of "{keyword}" Over Time')
        return fig
    else:
        return {}


@app.callback(Output('research-interests-graph', 'figure'),
              [
                  Input('research-interests-button', 'n_clicks'),
                  Input('research-interests-university', 'value'),
                  Input('research-interests-keyword', 'value'),
                  Input('start-year-research-interests', 'value'),
                  Input('end-year-research-interests', 'value'),
              ],
              )
def update_research_interests_graph(n_clicks, university, keyword, start_year, end_year):
    if n_clicks > 0 and keyword is not None:
        results = list(
            mongodb_utils.get_school_topic_popularity_over_time(keyword_name=keyword,
                                                                university_name=university,
                                                                year1=start_year,
                                                                year2=end_year))
        if results == []:
            return {}
        fig = px.bar(results, x='year', y='keyword score', color_discrete_sequence=['orange'], title=f'Popularity of "{keyword}" Over Time')
        return fig
    else:
        return {}

@app.callback(Output('researcher-publication-count-graph', 'figure'),
              [
                  Input('researcher-publication-count-button', 'n_clicks'),
                  Input('researcher-publication-keyword', 'value'),
                  Input('researcher', 'value'),
                  Input('start-year-researcher-publication-count', 'value'),
                  Input('end-year-researcher-publication-count', 'value'),
              ],
              )
def update_researcher_publication_count_graph(n_clicks, keyword, researcher, start_year, end_year):
    if n_clicks > 0 and keyword is not None:
        results = list(
            mongodb_utils.get_researcher_publication_count(researcher=researcher,
                                                           keyword_name=keyword,
                                                           year1=start_year,
                                                           year2=end_year))
        if results == []:
            return {}

        fig = px.bar(results, x='year', y='publication count', color_discrete_sequence=['red'], title=f'{researcher}\'s Publication Count of "{keyword}" Over Time')
        fig.update_layout(
            xaxis=dict(
                tickmode='linear',
                dtick=1
            )
        )
        fig.update_traces(width=1)
        return fig
    else:
        return {}

# SCRIPT BODY 
if __name__ == '__main__':
    app.run_server()
