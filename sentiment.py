import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Configuración de la API de OpenAI
st.title("Herramienta de Análisis de Sentimiento Avanzado")
openai_api_key = st.text_input("Introduce tu API Key de OpenAI", type="password")

if openai_api_key:
    openai.api_key = openai_api_key

    # Carga de la base de datos
    uploaded_file = st.file_uploader("Sube tu base de datos en formato CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(df.head())

        # Selección de columnas
        text_column = st.selectbox("Selecciona la columna de texto para el análisis de sentimiento", df.columns)
        date_column = st.selectbox("Selecciona la columna de fecha (opcional)", df.columns.insert(0, "Ninguna"))

        # Filtros de fecha
        if date_column != "Ninguna":
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            start_date = st.date_input("Fecha de inicio", min_value=df[date_column].min(), max_value=df[date_column].max())
            end_date = st.date_input("Fecha de fin", min_value=df[date_column].min(), max_value=df[date_column].max())
            df = df[(df[date_column] >= pd.Timestamp(start_date)) & (df[date_column] <= pd.Timestamp(end_date))]

        # Función para analizar el sentimiento
        def analyze_sentiment(text):
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Analiza el sentimiento del siguiente texto: '{text}'",
                    max_tokens=10
                )
                return response.choices[0].text.strip()
            except Exception as e:
                st.error("Error en la API de OpenAI")
                return "Error"

        # Aplicación del análisis de sentimiento
        df["Sentimiento"] = df[text_column].apply(analyze_sentiment)
        st.write("Análisis completado:")
        st.dataframe(df[[text_column, "Sentimiento"]])

        # Visualización de resultados
        st.subheader("Visualización de Resultados de Sentimiento")
        
        # Conteo de sentimientos
        sentiment_counts = df["Sentimiento"].value_counts()
        plt.figure(figsize=(10, 5))
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
        plt.title("Distribución de Sentimientos")
        plt.xlabel("Sentimiento")
        plt.ylabel("Frecuencia")
        st.pyplot(plt)

        # Nube de palabras
        st.subheader("Nube de Palabras de Sentimientos")
        from wordcloud import WordCloud
        positive_words = ' '.join(df[df["Sentimiento"] == "Positivo"][text_column])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_words)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Exportar resultados
        st.subheader("Descargar Resultados")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV con análisis de sentimiento",
            data=csv,
            file_name="sentimiento_analisis.csv",
            mime="text/csv",
        )
else:
    st.warning("Introduce tu API Key para continuar.")
