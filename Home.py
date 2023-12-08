import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import json
from urllib.request import urlopen


st.set_page_config(page_title="Input", page_icon="🏠️", layout="centered", initial_sidebar_state="auto", menu_items=None)

with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
    countries = json.load(response)

for index, value in enumerate(countries['features']):
        countries['features'][index]['id'] = countries['features'][index]['properties']['code']

type = st.radio(
    "",
    ["Émissions annuelles moyennes de GES des trajets domicile-travail selon le département de résidence en 2019", 
     "Distance domicile-travail moyenne selon le département de résidence en 2019", 
     "Émissions annuelles moyennes de GES des voitures par adulte selon le département en 2019"])

def importer_data(path):
      return 

if type == "Émissions annuelles moyennes de GES des trajets domicile-travail selon le département de résidence en 2019":
    df = pd.read_excel("co2_deplacements.ods", engine="odf", sheet_name="Figure_1", header=3)
elif type == "Distance domicile-travail moyenne selon le département de résidence en 2019":
    df = pd.read_excel("co2_deplacements.ods", engine="odf", sheet_name="Figure_1b_web", header=3)
else:
    df = pd.read_excel("co2_deplacements.ods", engine="odf", sheet_name="Fig_encadré_", header=3)

df = df[["Numéro de département", "Nom de département", df.columns[2]]]

fig = go.Figure(go.Choroplethmapbox(geojson=countries,locations=df['Numéro de département'], z=df[df.columns[2]],
                                    colorscale="Viridis", zmin=min(df[df.columns[2]]), zmax=max(df[df.columns[2]]),
                                    marker_opacity=0.5, marker_line_width=0 ))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=4.5, mapbox_center = {"lat": 46.8566, "lon": 2.3522})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)