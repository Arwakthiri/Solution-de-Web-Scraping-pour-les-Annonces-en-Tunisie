from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
from utils import load_data, get_stats
import plotly.express as px


df = load_data()
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Tableau de bord immobilier", style={"textAlign": "center"}),

    html.Div([
        html.Label("Filtrer par région :"),
        dcc.Dropdown(
            options=[{"label": r, "value": r} for r in sorted(df["region"].dropna().unique())],
            value=None,
            id="region-filter",
            placeholder="Choisir une région"
        ),

        html.Label("Filtrer par type de bien :"),
        dcc.Dropdown(
            options=[{"label": t, "value": t} for t in sorted(df["type"].dropna().unique())],
            value=None,
            id="type-filter",
            placeholder="Choisir un type de bien"
        ),
    ], style={"width": "50%", "margin": "auto"}),

    html.Br(),

    html.Div(id="statistiques", style={"textAlign": "center", "fontSize": "18px"}),

    html.Br(),

    dcc.Graph(id="graph-types"),
    dcc.Graph(id="graph-regions"),
    dcc.Graph(id="graph-prix"),
    dcc.Graph(id="graph-prix-par-region"),
    dcc.Graph(id="graph-nature"),


    html.H3("Tableau des annonces", style={"textAlign": "center"}),
    dash_table.DataTable(
    id="annonce-table",
    columns=[{"name": col, "id": col} for col in df.columns],
    data=df.to_dict("records"),
    page_size=10,
    filter_action="native",
    sort_action="native",
    style_table={"overflowX": "auto"},
    style_header={
        "backgroundColor": "#0d6efd",
        "color": "white",
        "fontWeight": "bold",
        "textAlign": "center"
    },
    style_cell={
        "backgroundColor": "#f8f9fa",  
        "color": "#212529",
        "padding": "10px",
        "textAlign": "left",
        "fontFamily": "Arial",
        "fontSize": "14px",
    },
    style_data={
        "whiteSpace": "normal",
        "height": "auto",
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#e9ecef",  
        }
    ]
)

])

@app.callback(
    Output("graph-types", "figure"),
    Output("graph-regions", "figure"),
    Output("graph-prix", "figure"),
    Output("graph-prix-par-region", "figure"),
    Output("graph-nature", "figure"),
    Output("statistiques", "children"),
    Output("annonce-table", "data"),
    Input("region-filter", "value"),
    Input("type-filter", "value")
)
def update_dashboard(region, type_bien):
    dff = df.copy()
    if region:
        dff = dff[dff["region"] == region]
    if type_bien:
        dff = dff[dff["type"] == type_bien]

    fig_types = px.pie(dff, names="type", title="Répartition des types de biens")
    fig_regions = px.bar(dff["region"].value_counts().head(10), title="Top 10 régions",color_discrete_sequence=["#a3a1ff"])
    fig_prix = px.histogram(dff, x="prix_clean", nbins=20, title="Distribution des prix")
    fig_prix_region = px.bar(
    dff.groupby("region")["prix_clean"].mean().sort_values(ascending=False).head(10),
    title="Prix moyen par région",
    labels={"value": "Prix moyen (DT)", "region": "Région"},
    color_discrete_sequence=["#007BFF", "#6610f2", "#20c997", "#FFC107", "#dc3545"]

)
    fig_nature = px.bar(
    dff.groupby(["type", "nature"]).size().reset_index(name="Nombre d'annonces"),
    x="type",
    y="Nombre d'annonces",
    color="nature",
    barmode="group",
    title="Répartition des annonces par type et nature"
)
    
    prix_moy, sup_moy = get_stats(dff)
    stats = f" Prix moyen : {prix_moy} DT |  Surface moyenne : {sup_moy} m²"

    return fig_types, fig_regions, fig_prix,fig_prix_region,fig_nature, stats, dff.to_dict("records")
    
if __name__ == "__main__":
    app.run(debug=True)
