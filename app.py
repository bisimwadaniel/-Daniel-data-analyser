import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Configuration de la page
st.set_page_config(
    page_title="Analyseur de Données Pro",
    page_icon="📊",
    layout="wide"
)

# Style CSS personnalisé pour épurer l'interface
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stMetric {background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .stHeader {color: #1f77b4; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 2. Titre de l'application
st.title("📊 Application d'Analyse de Données Interactive")
st.subheader("Importez votre fichier pour explorer, filtrer et visualiser vos données instantanément.")
st.write("---")

# 3. Sidebar - Importation du fichier
st.sidebar.header("📁 Chargement des données")
uploaded_file = st.sidebar.file_uploader(
    "Choisissez un fichier (CSV ou Excel)", 
    type=["csv", "xlsx"]
)

# Fonction pour charger les données avec mise en cache pour optimiser les performances
@st.cache_data
def load_data(file):
    """Charge les données depuis un fichier CSV ou Excel"""
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
        return None

def create_chart(df, chart_type, x_axis, y_axis=None, color_axis=None):
    """
    Crée un graphique Plotly selon le type sélectionné
    
    Args:
        df: DataFrame pandas
        chart_type: Type de graphique à créer
        x_axis: Colonne pour l'axe X
        y_axis: Colonne pour l'axe Y (optionnel pour histogramme)
        color_axis: Colonne pour la coloration (optionnel)
    
    Returns:
        Figure Plotly ou None si erreur
    """
    chart_mapping = {
        "Nuage de points (Scatter)": px.scatter,
        "Ligne (Line)": px.line,
        "Barres (Bar)": px.bar,
        "Boîte à moustaches (Boxplot)": px.box,
        "Histogramme": px.histogram,
    }
    
    chart_func = chart_mapping.get(chart_type)
    if not chart_func:
        return None
    
    kwargs = {"template": "plotly_white"}
    kwargs["x"] = x_axis
    if y_axis and chart_type != "Histogramme":
        kwargs["y"] = y_axis
    if color_axis:
        kwargs["color"] = color_axis
    
    try:
        return chart_func(df, **kwargs)
    except Exception as e:
        st.error(f"Erreur lors de la génération du graphique : {e}")
        return None

# 4. Corps principal de l'application
if uploaded_file is not None:
    # Chargement du DataFrame
    df = load_data(uploaded_file)
    
    if df is not None:
        # --- SECTION 0 : INFORMATIONS SUR LES COLONNES ---
        st.sidebar.write("---")
        st.sidebar.write("### 📋 Types de colonnes détectées")
        col_types = df.dtypes
        for col, dtype in col_types.items():
            st.sidebar.write(f"- **{col}**: {dtype}")
        
        # --- SECTION 1 : APPERÇU ET KPI ---
        st.header("🔍 Aperçu des Données")
        
        # Affichage des indicateurs clés (KPI)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Lignes", df.shape[0])
        col2.metric("Colonnes", df.shape[1])
        col3.metric("Valeurs Manquantes", df.isna().sum().sum())
        col4.metric("Mémoire (MB)", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}")
        
        st.write("### Extrait de la table (10 premières lignes)")
        st.dataframe(df.head(10), use_container_width=True)
        
        # --- SECTION 1.5 : FILTRER LES DONNÉES ---
        st.write("---")
        st.header("🔎 Filtrer les Données")
        
        col_filter_left, col_filter_right = st.columns([2, 1])
        
        with col_filter_left:
            filter_col = st.selectbox("Colonne à filtrer", df.columns)
            
        with col_filter_right:
            filter_value = st.text_input("Valeur à rechercher")
        
        if filter_value:
            try:
                df_filtered = df[df[filter_col].astype(str).str.contains(filter_value, case=False, na=False)]
                st.success(f"✅ {len(df_filtered)} lignes correspondantes trouvées")
                st.dataframe(df_filtered, use_container_width=True)
            except Exception as e:
                st.error(f"Erreur lors du filtrage : {e}")
                df_filtered = df
        else:
            df_filtered = df
        
        # Bouton de téléchargement des données filtrées
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les données (CSV)",
            data=csv,
            file_name="donnees_filtrees.csv",
            mime="text/csv"
        )
        
        # --- SECTION 2 : STATISTIQUES ET FILTRES ---
        st.write("---")
        st.header("📈 Statistiques Descriptives")
        
        tab1, tab2, tab3 = st.tabs(["🔢 Variables Numériques", "🔤 Variables Catégorielles", "📊 Groupement"])
        
        # Détection des colonnes numériques et catégorielles
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        with tab1:
            if num_cols:
                st.write(df[num_cols].describe())
                
                # Option d'exporter les statistiques
                stats_csv = df[num_cols].describe().to_csv()
                st.download_button(
                    label="📥 Télécharger les statistiques (CSV)",
                    data=stats_csv,
                    file_name="statistiques_numeriques.csv",
                    mime="text/csv"
                )
            else:
                st.info("ℹ️ Aucune colonne numérique détectée.")
                
        with tab2:
            if cat_cols:
                st.write(df[cat_cols].describe())
            else:
                st.info("ℹ️ Aucune colonne catégorielle détectée.")
        
        with tab3:
            if cat_cols and num_cols:
                st.write("### Groupement par catégorie")
                group_col = st.selectbox("Grouper par", cat_cols, key="group_col")
                numeric_col = st.selectbox("Colonne à agréger", num_cols, key="agg_col")
                
                grouped = df.groupby(group_col)[numeric_col].agg(['mean', 'sum', 'count', 'min', 'max'])
                st.dataframe(grouped, use_container_width=True)
                
                # Visualiser le groupement
                fig_group = px.bar(
                    df.groupby(group_col)[numeric_col].mean().reset_index(),
                    x=group_col,
                    y=numeric_col,
                    title=f"Moyenne de {numeric_col} par {group_col}",
                    template="plotly_white"
                )
                st.plotly_chart(fig_group, use_container_width=True)
            else:
                st.info("ℹ️ Besoin de colonnes numériques et catégorielles pour le groupement.")

        # --- SECTION 3 : VISUALISATION DYNAMIQUE ---
        st.write("---")
        st.header("📊 Visualisation Graphique")
        
        if len(df.columns) >= 2:
            col_left, col_right = st.columns([1, 3])
            
            with col_left:
                st.write("### Configuration")
                # Choix du type de graphique
                chart_type = st.selectbox(
                    "Type de graphique",
                    ["Nuage de points (Scatter)", "Ligne (Line)", "Barres (Bar)", "Boîte à moustaches (Boxplot)", "Histogramme"]
                )
                
                # Sélection des axes
                x_axis = st.selectbox("Axe X (Horizontal)", df.columns, key="x_axis")
                
                if chart_type != "Histogramme":
                    y_axis = st.selectbox("Axe Y (Vertical)", num_cols if num_cols else df.columns, key="y_axis")
                else:
                    y_axis = None
                
                # Option de coloration optionnelle
                color_axis = st.selectbox("Colorer par (Optionnel)", [None] + df.columns.tolist(), key="color_axis")
            
            with col_right:
                st.write(f"### Graphique : {chart_type}")
                
                # Génération du graphique
                fig = create_chart(df, chart_type, x_axis, y_axis, color_axis)
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("❌ Impossible de générer le graphique avec ces variables.")
        else:
            st.warning("⚠️ Le jeu de données doit contenir au moins 2 colonnes pour la visualisation.")
            
else:
    # Message d'accueil si aucun fichier n'est chargé
    st.info("💡 En attente d'un fichier. Veuillez importer un fichier CSV ou Excel depuis la barre latérale pour commencer l'analyse.")
    
    # Simulation d'un petit exemple visuel pour l'utilisateur
    st.write("### Exemple de structure attendue :")
    example_data = pd.DataFrame({
        'Date': pd.date_range(start='2026-01-01', periods=5),
        'Ventes (€)': [1200, 1500, 1100, 1700, 2100],
        'Catégorie': ['Électronique', 'Mode', 'Électronique', 'Mode', 'Jardin']
    })
    st.table(example_data)
