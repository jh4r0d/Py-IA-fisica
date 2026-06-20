import streamlit as st
from google import genai
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Profesor de Física IA",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Tu Profesor Artificial de Física 1")
st.write("¡Bienvenido al chat! Puedes escribirme tus dudas de Caída Libre o Movimiento Parabólico, o subir una imagen con tu problema.")

# --- CONFIGURACIÓN DE LA IA ---
API_KEY = "AQ.Ab8RN6JvCsVZXOqrtj1qfrR1o0z0GYW5gzfR5iArhc6tihqO6Q"
client = genai.Client(api_key=API_KEY)

# Instrucciones del sistema para el comportamiento del profesor
system_instruction = """
Eres un profesor experto en física mecánica especializado en Caída Libre y Movimiento Parabólico.
Responde de forma interactiva y amigable a través de este chat. Si te dan un problema:
1. Enumera los datos explícitos e implícitos.
2. Muestra las fórmulas antes de operar.
3. Muestra el desarrollo matemático paso a paso de forma clara.
4. Destaca el resultado final con sus unidades en el Sistema Internacional.
"""

# --- HISTORIAL DEL CHAT (Session State) ---
# Si es la primera vez que se abre la app, inicializamos el historial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu tutor de física. ¿Qué problema o concepto quieres resolver hoy?"}
    ]

# Mostrar los mensajes anteriores del historial en la pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], caption="Imagen analizada", use_container_width=True)

# --- ENTRADAS MULTIMODALES EN LA BARRA LATERAL ---
st.sidebar.header("📁 Archivos Adjuntos")
imagen_subida = st.sidebar.file_uploader(
    "Sube una foto del problema o diagrama:", 
    type=["png", "jpg", "jpeg"]
)

# --- CASILLA DE TEXTO DEL CHAT ---
if prompt := st.chat_input("Escribe tu duda o problema aquí..."):
    
    # 1. Mostrar el mensaje del usuario en la pantalla y guardarlo en el historial
    with st.chat_message("user"):
        st.markdown(prompt)
    
    nuevo_mensaje_usuario = {"role": "user", "content": prompt}
    
    # Si el usuario subió una imagen, la procesamos y la guardamos junto al mensaje
    imagen_pil = None
    if imagen_subida:
        imagen_pil = Image.open(imagen_subida)
        with st.chat_message("user"):
            st.image(imagen_pil, caption="Imagen adjunta", use_container_width=True)
        nuevo_mensaje_usuario["image"] = imagen_pil
        
    st.session_state.messages.append(nuevo_mensaje_usuario)

    # 2. Generar la respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando como físico... 🧠"):
            try:
                # Armamos la solicitud para la API de Gemini
                contenido_solicitud = [prompt]
                if imagen_pil:
                    contenido_solicitud.append(imagen_pil)
                
                # Llamada al modelo Gemini 2.5 Flash
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contenido_solicitud,
                    config={"system_instruction": system_instruction, "temperature": 0.2}
                )
                
                respuesta_texto = response.text
                st.markdown(respuesta_texto)
                
                # Guardar la respuesta del asistente en el historial
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                
            except Exception as e:
                # Intento de respaldo si falla el modelo principal
                try:
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=contenido_solicitud,
                        config={"system_instruction": system_instruction, "temperature": 0.2}
                    )
                    respuesta_texto = response.text
                    st.markdown(respuesta_texto)
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                except Exception as e_backup:
                    st.error(f"Error al conectar con la IA: {e_backup}")