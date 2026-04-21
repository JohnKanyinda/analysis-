import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Élec Lemba", layout="wide")
st.title("⚡ Analyseur Électrique - Lemba")

fichier = st.sidebar.file_uploader("Charger le fichier Excel", type=["xlsx", "csv"])

if fichier:
    try:
        # Lecture (on supporte Excel et CSV au cas où)
        if fichier.name.endswith('.csv'):
            df = pd.read_csv(fichier)
        else:
            df = pd.read_excel(fichier)
        
        # --- NETTOYAGE MAGIQUE DES COLONNES ---
        # 1. On enlève les espaces avant/après
        # 2. On met tout en minuscules pour ne plus avoir de soucis de majuscules
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # On définit ce qu'on cherche en minuscules
        col_date = "date"
        col_secteur = "secteur"
        col_conso = "consommation(kwh)"

        if col_date in df.columns and col_secteur in df.columns and col_conso in df.columns:
            
            # Filtre
            secteurs = df[col_secteur].unique()
            choix = st.sidebar.multiselect("Choisir les secteurs", secteurs, default=secteurs)
            df_filtre = df[df[col_secteur].isin(choix)]

            # Affichage
            col1, col2 = st.columns([1, 2])
            with col1:
                total = df_filtre[col_conso].sum()
                st.metric("Consommation Totale", f"{total:,.2f} kWh")
                st.write("### Résumé par Secteur")
                st.dataframe(df_filtre.groupby(col_secteur)[col_conso].sum())

            with col2:
                st.write("### Évolution de la Consommation")
                # On s'assure que la date est au bon format pour le graphique
                df_filtre[col_date] = pd.to_datetime(df_filtre[col_date])
                fig = px.line(df_filtre, x=col_date, y=col_conso, color=col_secteur)
                st.plotly_chart(fig, width="stretch")
        else:
            # Message d'aide si ça ne marche toujours pas
            st.error("⚠️ Colonnes non détectées !")
            st.write("Voici les colonnes que j'ai trouvées dans votre fichier :", list(df.columns))
            st.info("Assurez-vous que votre fichier a bien des colonnes nommées : Date, Secteur, et Consommation(kWh)")
            
    except Exception as e:
        st.error(f"Erreur : {e}")
else:
    st.info("👋 Chargez votre fichier 'Classeur1.xlsx' pour voir l'analyse.")
