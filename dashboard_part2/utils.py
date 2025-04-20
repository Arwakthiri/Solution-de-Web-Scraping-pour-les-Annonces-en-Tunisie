import sqlite3
import pandas as pd
import plotly.express as px

def load_data():
    conn = sqlite3.connect("../annonces.db")
    df = pd.read_sql_query("SELECT * FROM annonces", conn)
    conn.close()

    # Nettoyage
    df["prix_clean"] = df["prix"].str.replace(r"[^\d]", "", regex=True)
    df["prix_clean"] = pd.to_numeric(df["prix_clean"], errors='coerce')

    df["superficie_clean"] = df["superficie"].str.replace(r"[^\d]", "", regex=True)
    df["superficie_clean"] = pd.to_numeric(df["superficie_clean"], errors='coerce')

    df["modifie"] = pd.to_datetime(df["modifie"], format="%d/%m/%Y", errors='coerce')
    return df

def get_stats(df_filtered):
    prix_moyen = round(df_filtered["prix_clean"].mean(), 2)
    superficie_moyenne = round(df_filtered["superficie_clean"].mean(), 2)
    return prix_moyen, superficie_moyenne
