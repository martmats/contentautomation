import streamlit as st
import pandas as pd
import openai

# Título y configuración de la API de OpenAI
st.title("Herramienta de Análisis de Sentimiento con OpenAI")
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
