import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Élec Lemba", layout="wide")

# 2. Titre et Sidebar
st.title("⚡ Analyseur Électrique - Lemba")
st.sidebar.header("Paramètres")

fichier = st.sidebar.file_uploader("Charger le fichier Excel", type=["xlsx"])

# 3. Logique principale
if fichier:
    try:
        # Lecture des données
        df = pd.read_excel(fichier)
        
        # Nettoyage automatique des noms de colonnes (enlève les espaces en trop)
        df.columns = [str(c).strip() for c in df.columns]

        # Vérification des colonnes nécessaires
        colonnes_requises = ["Date", "Secteur", "Consommation(kWh)"]
        if all(col in df.columns for col in colonnes_requises):
            
            # Filtre par secteur
            secteurs = df["Secteur"].unique()
            choix = st.sidebar.multiselect("Choisir les secteurs", secteurs, default=secteurs)
            df_filtre = df[df["Secteur"].isin(choix)]

            # Affichage des indicateurs
            col1, col2 = st.columns([1, 2])
            
            with col1:
                total = df_filtre["Consommation(kWh)"].sum()
                st.metric("Consommation Totale", f"{total:,.2f} kWh")
                st.write("### Résumé par Secteur")
                st.dataframe(df_filtre.groupby("Secteur")["Consommation(kWh)"].sum(), width=None)

            with col2:
                st.write("### Évolution de la Consommation")
                fig = px.line(df_filtre, x="Date", y="Consommation(kWh)", color="Secteur")
                # Utilisation de width='stretch' pour occuper tout l'espace (Standard 2026)
                st.plotly_chart(fig, width="stretch")
        else:
            st.error(f"Le fichier doit contenir : {', '.join(colonnes_requises)}")
            
    except Exception as e:
        st.error(f"Erreur lors de la lecture : {e}")
else:
    st.info("👋 Bienvenue ! Veuillez charger un fichier Excel pour commencer l'analyse.")