import streamlit as st
import openai
import requests

# Configuración de la Sidebar
st.sidebar.title("Configuración de APIs")
st.sidebar.markdown("Por favor, introduce tus claves de API para conectarte con las redes sociales y OpenAI.")

# Campos para las claves de API
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
twitter_api_key = st.sidebar.text_input("Twitter API Key", type="password")
instagram_api_key = st.sidebar.text_input("Instagram API Key", type="password")
facebook_api_key = st.sidebar.text_input("Facebook API Key", type="password")
extra_api_key = st.sidebar.text_input("Otra API Key (opcional)", type="password")

# Selección de la red social
social_platform = st.sidebar.selectbox(
    "Selecciona la red social",
    ["Twitter", "Instagram", "Facebook", "Otra"]
)

# Pregunta al usuario si desea hacer cambios en el contenido generado
modify_content = st.sidebar.checkbox("¿Quieres realizar cambios en el contenido generado?")

# Configuración de OpenAI
if openai_api_key:
    openai.api_key = openai_api_key

# Función para analizar el tono de una publicación
def analyse_tone(content):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Analiza el tono del siguiente texto: {content}",
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error("Error al conectar con la API de OpenAI. Verifica tu clave.")
        return None

# Función para extraer contenido de la red social seleccionada
def get_social_content(api_key, platform):
    # Lógica placeholder para autenticación y extracción de contenido
    if platform == "Twitter":
        st.write("Conectando con Twitter...")
        # Aquí añadirías la lógica para conectarte a Twitter
        return "Contenido de ejemplo de Twitter"
    elif platform == "Instagram":
        st.write("Conectando con Instagram...")
        # Aquí añadirías la lógica para conectarte a Instagram
        return "Contenido de ejemplo de Instagram"
    elif platform == "Facebook":
        st.write("Conectando con Facebook...")
        # Aquí añadirías la lógica para conectarte a Facebook
        return "Contenido de ejemplo de Facebook"
    else:
        st.write("Conectando con API personalizada...")
        return "Contenido de ejemplo de una API personalizada"

# Interfaz de la app principal
st.title("Generador Inteligente de Contenido para Redes Sociales")
st.write("Esta aplicación genera contenido optimizado para tu red social basándose en el análisis de tono.")

if st.button("Analizar tono y generar contenido"):
    if not openai_api_key:
        st.error("Por favor, ingresa tu clave de API de OpenAI.")
    else:
        # Obtener contenido de la red social seleccionada
        content = get_social_content(
            api_key=twitter_api_key if social_platform == "Twitter" else 
                    instagram_api_key if social_platform == "Instagram" else 
                    facebook_api_key if social_platform == "Facebook" else 
                    extra_api_key,
            platform=social_platform
        )

        # Analizar el tono del contenido
        tone = analyse_tone(content)
        if tone:
            st.write(f"Tono detectado: {tone}")

            # Generar nuevo contenido
            prompt = f"Genera una publicación en tono {tone} sobre el tema que elija el usuario."
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=150
            )
            generated_content = response.choices[0].text.strip()
            st.write("Contenido generado:")
            st.write(generated_content)

            # Permitir modificaciones si el usuario lo seleccionó
            if modify_content:
                user_modifications = st.text_area("Modifica el contenido generado si lo deseas:", generated_content)
                st.write("Contenido final:")
                st.write(user_modifications)
        else:
            st.error("No se pudo analizar el tono. Verifica las configuraciones.")

