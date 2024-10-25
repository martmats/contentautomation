import streamlit as st
import openai
import requests

# Configuración de la API de OpenAI y parámetros iniciales
st.title("Automatización de Contenido Basado en IA")
st.subheader("Crea contenido personalizado para redes sociales con ayuda de IA")

# Input de API Key de OpenAI
openai_api_key = st.text_input("Introduce tu clave de API de OpenAI", type="password")

# Selección de red social
network = st.selectbox("Selecciona la red social", ["Instagram", "Facebook", "Twitter", "LinkedIn"])

# Petición de API Key de la red social si es necesario
network_api_key = st.text_input(f"Introduce la clave de API para {network}", type="password")

# Inputs para conocer el tipo de contenido y producto
content_type = st.selectbox("Selecciona el tipo de contenido que quieres crear", ["Publicación", "Anuncio", "Historia", "Reel"])
product_type = st.text_input("Describe brevemente el producto o servicio que promocionarás")

# Pregunta si quiere segmentar y cómo
audience_segment = st.text_input("Describe el segmento de clientes al que va dirigido (edad, intereses, etc.)")

if st.button("Generar Contenido"):
    if openai_api_key and network_api_key:
        # Ejemplo de extracción de contenido reciente para analizar tono
        social_api_url = f"https://api.{network.lower()}.com/user/content"  # URL simulada para demostración
        headers = {"Authorization": f"Bearer {network_api_key}"}
        
        response = requests.get(social_api_url, headers=headers)
        
        if response.status_code == 200:
            recent_content = response.json()  # Asumiendo que el contenido está en JSON
            
            # Análisis de tono con OpenAI
            openai.api_key = openai_api_key
            tone_analysis = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Analiza el siguiente contenido para capturar el tono: {recent_content}",
                max_tokens=50
            )
            
            # Generación de contenido adaptado
            content_prompt = f"""
                Crea un {content_type} para {network} sobre un producto de tipo {product_type}. 
                El contenido debe estar adaptado al tono detectado y dirigido a un público {audience_segment}.
            """
            generated_content = openai.Completion.create(
                engine="text-davinci-003",
                prompt=content_prompt,
                max_tokens=150
            )

            # Mostrar el contenido generado
            st.subheader("Contenido Generado")
            st.write(generated_content.choices[0].text.strip())
        else:
            st.error(f"Error al acceder al contenido de {network}. Verifica la API Key.")
    else:
        st.error("Introduce ambas claves de API para continuar.")
