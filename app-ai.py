import streamlit as st
from google import genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import io

st.set_page_config(
    page_title="AIrtin - Tu Profe de Física 1",
    page_icon="🍎",
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    h1 { color: #38bdf8 !important; text-align: center; font-family: 'Arial', sans-serif; font-weight: bold; }
    .stButton>button { background-color: #ec4899 !important; color: white !important; border-radius: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("👨‍🏫 AIrtin: Tu Profesor de Física 1")
st.write("¡A ver, entren, entren! Saquen una hoja... mentira. Pregúntame lo que quieras de física, teoría o problemas. Puedes hablarme, escribirme o subir la foto de ese ejercicio que no te sale.")

API_KEY = "AQ.Ab8RN6JvCsVZXOqrtj1qfrR1o0z0GYW5gzfR5iArhc6tihqO6Q"
client = genai.Client(api_key=API_KEY)

st.sidebar.header("⚙️ Configuración de la Clase")
modo_explicacion = st.sidebar.selectbox(
    "¿En qué tono quieres la clase?",
    ["👶 Modo Niño (Para que tu sobrinito entienda)", 
     "🎓 Modo Universitario (Prepárate para la PC)",
     "🧪 Modo Experimento (Para vagos, digo, dinámicos)"]
)

st.sidebar.markdown("---")
st.sidebar.header("📁 Adjuntar Ejercicio")
imagen_subida = st.sidebar.file_uploader("Sube la foto del problema:", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Buenas noches con todos! Soy AIrtin, tu clon virtual de Física 1. A ver, ¿quién va a ser el valiente que va a lanzar la primera duda hoy? No muerdo, solo jalo en los exámenes si no repasan. 🚀"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

st.write("---")
st.write("🎙️ **¿Te da flojera escribir? Habla por el micrófono:**")
audio_grabado = mic_recorder(
    start_prompt="🔴 Hablar con Martín",
    stop_prompt="⏹️ Enviar audio",
    key='extractor_mic',
    just_once=True
)

prompt = st.chat_input("Escribe tu duda aquí...")
audio_bytes = None

if audio_grabado and 'bytes' in audio_grabado:
    audio_bytes = audio_grabado['bytes']
    prompt = "Contesta a la nota de audio adjunta"

if prompt:
    with st.chat_message("user"):
        if audio_bytes:
            st.markdown("🎤 *Mensaje de voz enviado*")
            st.audio(audio_bytes, format="audio/wav")
        else:
            st.markdown(prompt)
            
    st.session_state.messages.append({"role": "user", "content": prompt if not audio_bytes else "🎤 Mensaje de voz"})

    perfil_instrucciones = f"Estás dictando clase en {modo_explicacion}. "
    system_instruction = perfil_instrucciones + """
    Eres AIrtin, un profesor de física 1 universitario llamado Martín. Tienes un humor muy característico de docente: 
    eres carismático, lanzas bromas típicas de salón, usas frases como '¡A ver, presten atención atrás!', '¡Esto viene en la Práctica Calificada (PC)!', 
    'No se duerman', o ironías amigables sobre los que se copian o dejan todo para el final.
    Respondes CUALQUIER duda de física. Si te dan un problema, resuélvelo con rigurosidad matemática paso a paso:
    1. Datos explícitos e implícitos (haz un chiste si se olvidan de la gravedad).
    2. Fórmulas completas.
    3. Desarrollo matemático claro.
    4. Resultado final bien marcado.
    Mantén siempre el personaje de Martín ingenioso y dinámico.
    """

    contenido_solicitud = []
    
    if audio_bytes:
        contenido_solicitud.append({"mime_type": "audio/wav", "data": audio_bytes})
    else:
        contenido_solicitud.append(prompt)
        
    if imagen_subida:
        imagen_pil = Image.open(imagen_subida)
        contenido_solicitud.append(imagen_pil)

    with st.chat_message("assistant"):
        with st.spinner("Buscando las tizas y borrando la pizarra... 👨‍🏫"):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contenido_solicitud,
                    config={"system_instruction": system_instruction, "temperature": 0.5}
                )
                
                respuesta_texto = response.text
                st.markdown(respuesta_texto)
                
                audio_response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Lee en voz alta de forma natural, imitando el tono de un profesor de universidad hablando con sus alumnos, sin leer asteriscos ni símbolos: {respuesta_texto}",
                    config={"response_mime_type": "audio/mp3"}
                )
                
                if hasattr(audio_response, 'inline_data') or (audio_response.text and "audio" in str(audio_response)):
                    st.audio(audio_response.text, format="audio/mp3")
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto, "audio": audio_response.text})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                    
            except Exception as e:
                st.error(f"¡Un lapsus! Se nos cayó la tiza del servidor: {e}")
