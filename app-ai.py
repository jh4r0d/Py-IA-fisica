import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import io
import random

st.set_page_config(
    page_title="AIrtin - Tu Profe de Física 1",
    page_icon="🍎",
    layout="centered"
)

if "prev_modo" not in st.session_state:
    st.session_state.prev_modo = "🎓 Modo Universitario (Prepárate para la PC)"
if "pastel_colors" not in st.session_state:
    st.session_state.pastel_colors = ["#FDFDFD", "#FFE3E3", "#E8F5E9", "#FFF9E6"]

st.sidebar.header("⚙️ Configuración de la Clase")
modo_explicacion = st.sidebar.selectbox(
    "¿En qué tono quieres la clase?",
    ["👶 Modo Niño (Para que tu sobrinito entienda)", 
     "🎓 Modo Universitario (Prepárate para la PC)",
     "🧪 Modo Experimento (Para vagos, digo, dinámicos)"]
)

if modo_explicacion != st.session_state.prev_modo:
    if modo_explicacion == "👶 Modo Niño (Para que tu sobrinito entienda)":
        lista_colores = ["#FFB6C1", "#ADD8E6", "#98FB98", "#F0E68C", "#E6E6FA", "#FFD700", "#FFA07A", "#20B2AA", "#87CEFA", "#FF69B4"]
        elegidos = random.sample(lista_colores, 3)
        st.session_state.pastel_colors = ["#FDFDFD", elegidos[0], elegidos[1], elegidos[2]]
    st.session_state.prev_modo = modo_explicacion

if modo_explicacion == "👶 Modo Niño (Para que tu sobrinito entienda)":
    bg_chat = st.session_state.pastel_colors[0]
    bg_entorno = st.session_state.pastel_colors[1]
    bg_zonas_rojas = st.session_state.pastel_colors[2]
    btn_color = st.session_state.pastel_colors[3]
    
    st.markdown(f"""
        <style>
        .stApp, [data-testid="stHeader"], [data-testid="stSidebarCollapsedControl"] {{
            background-color: {bg_entorno} !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {bg_zonas_rojas} !important;
            border-right: 3px dashed {btn_color} !important;
        }}
        [data-testid="stBottomBlockContainer"] {{
            background-color: {bg_zonas_rojas} !important;
            border-top: 3px dashed {btn_color} !important;
        }}
        [data-testid="stChatInputContainer"] {{
            background-color: transparent !important;
            border: none !important;
        }}
        .stChatMessage, [data-testid="stChatMessage"] {{
            background-color: {bg_chat} !important;
            border-radius: 15px !important;
            border: 3px solid {btn_color} !important;
            padding: 15px !important;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.06) !important;
        }}
        .stChatInputContainer textarea, [data-testid="stChatInput"] {{
            background-color: {bg_chat} !important;
            color: #1c1c1c !important;
            border: 3px solid {btn_color} !important;
            border-radius: 15px !important;
        }}
        h1 {{ 
            color: #2c3e50 !important; 
            text-align: center; 
            font-family: 'Comic Sans MS', sans-serif; 
            font-weight: bold; 
        }}
        .stButton>button {{ 
            background-color: {btn_color} !important; 
            color: #1c1c1c !important; 
            border-radius: 20px; 
            font-weight: bold; 
            border: 2px solid #2c3e50 !important;
        }}
        p, span, label, li, .stMarkdown {{ 
            color: #2c3e50 !important; 
            font-family: 'Comic Sans MS', sans-serif; 
            font-weight: bold !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 0; overflow: hidden;">
            <div class="teleport-item" style="position: absolute; top: 10%; left: 2%; animation: teleportLeft 14s infinite linear;"><img src="https://cdn-icons-png.flaticon.com/512/3020/3020473.png" width="100" style="opacity: 0.20;"></div>
            <div class="teleport-item" style="position: absolute; top: 40%; left: 4%; animation: teleportLeft2 18s infinite linear 2s;"><img src="https://cdn-icons-png.flaticon.com/512/2510/2510001.png" width="110" style="opacity: 0.20;"></div>
            <div class="teleport-item" style="position: absolute; bottom: 25%; left: 1%; animation: teleportLeft3 22s infinite linear 4s;"><img src="https://cdn-icons-png.flaticon.com/512/3655/3655581.png" width="95" style="opacity: 0.20;"></div>
            
            <div class="teleport-item" style="position: absolute; top: 12%; right: 2%; animation: teleportRight 16s infinite linear 1s;"><img src="https://cdn-icons-png.flaticon.com/512/2940/2940176.png" width="105" style="opacity: 0.20;"></div>
            <div class="teleport-item" style="position: absolute; top: 45%; right: 3%; animation: teleportRight2 20s infinite linear 3s;"><img src="https://cdn-icons-png.flaticon.com/512/1048/1048943.png" width="100" style="opacity: 0.20;"></div>
            <div class="teleport-item" style="position: absolute; bottom: 22%; right: 1%; animation: teleportRight3 24s infinite linear 5s;"><img src="https://cdn-icons-png.flaticon.com/512/911/911174.png" width="90" style="opacity: 0.20;"></div>
        </div>
        <style>
        @keyframes teleportLeft {
            0% { opacity: 0; transform: translate(0px, 0px) rotate(0deg); }
            5% { opacity: 0.4; }
            30% { transform: translate(30px, -60px) rotate(45deg); opacity: 0.4; }
            35% { opacity: 0; transform: translate(30px, -60px) rotate(45deg); }
            40% { transform: translate(-10px, 200px) rotate(-20deg); opacity: 0; }
            45% { opacity: 0.4; }
            70% { transform: translate(40px, 120px) rotate(60deg); opacity: 0.4; }
            95% { opacity: 0; }
            100% { opacity: 0; transform: translate(0px, 0px) rotate(0deg); }
        }
        @keyframes teleportLeft2 {
            0% { opacity: 0; transform: translate(0px, 0px) rotate(0deg); }
            10% { opacity: 0.4; }
            40% { transform: translate(25px, 80px) rotate(-30deg); opacity: 0.4; }
            45% { opacity: 0; transform: translate(25px, 80px) rotate(-30deg); }
            50% { transform: translate(5px, -150px) rotate(15deg); opacity: 0; }
            55% { opacity: 0.4; }
            90% { transform: translate(35px, -70px) rotate(-45deg); opacity: 0.4; }
            100% { opacity: 0; transform: translate(0px, 0px) rotate(0deg); }
        }
        @keyframes teleportLeft3 {
            0% { opacity: 0; transform: translate(0px, 0px); }
            8% { opacity: 0.4; }
            35% { transform: translate(20px, -100px); opacity: 0.4; }
            40% { opacity: 0; }
            45% { transform: translate(40px, -250px); opacity: 0; }
            50% { opacity: 0.4; }
            92% { transform: translate(-5px, -180px); opacity: 0.4; }
            100% { opacity: 0; }
        }
        @keyframes teleportRight {
            0% { opacity: 0; transform: translate(0px, 0px) rotate(0deg); }
            5% { opacity: 0.4; }
            30% { transform: translate(-25px, -70px) rotate(-40deg); opacity: 0.4; }
            35% { opacity: 0; transform: translate(-25px, -70px) rotate(-40deg); }
            40% { transform: translate(15px, 180px) rotate(30deg); opacity: 0; }
            45% { opacity: 0.4; }
            70% { transform: translate(-35px, 100px) rotate(-70deg); opacity: 0.4; }
            95% { opacity: 0; }
            100% { opacity: 0; transform: translate(0px, 0px) rotate(0deg); }
        }
        @keyframes teleportRight2 {
            0% { opacity: 0; transform: translate(0px, 0px) rotate(0deg); }
            10% { opacity: 0.4; }
            40% { transform: translate(-30px, 60px) rotate(25deg); opacity: 0.4; }
            45% { opacity: 0; transform: translate(-30px, 60px) rotate(25deg); }
            50% { transform: translate(-10px, -120px) rotate(-15deg); opacity: 0; }
            55% { opacity: 0.4; }
            90% { transform: translate(-40px, -50px) rotate(50deg); opacity: 0.4; }
            100% { opacity: 0; transform: translate(0px, 0px) rotate(0deg); }
        }
        @keyframes teleportRight3 {
            0% { opacity: 0; transform: translate(0px, 0px); }
            8% { opacity: 0.4; }
            35% { transform: translate(-15px, -90px); opacity: 0.4; }
            40% { opacity: 0; }
            45% { transform: translate(-35px, -220px); opacity: 0; }
            50% { opacity: 0.4; }
            92% { transform: translate(10px, -140px); opacity: 0.4; }
            100% { opacity: 0; }
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stBottomBlockContainer"] { background-color: #0f172a !important; }
        [data-testid="stChatInputContainer"] { background-color: #0f172a !important; }
        h1 { color: #38bdf8 !important; text-align: center; font-family: 'Arial', sans-serif; font-weight: bold; }
        .stButton>button { background-color: #ec4899 !important; color: white !important; border-radius: 20px; }
        </style>
    """, unsafe_allow_html=True)

st.title("👨‍🏫 AIrtin: Tu Profesor de Física 1")
st.write("¡A ver, entren, entren! Saquen una hoja... mentira. Pregúntame lo que quieras de física, teoría o problemas. Puedes hablarme, escribirme o subir la foto de ese ejercicio que no te sale.")

API_KEY = "AQ.Ab8RN6JvCsVZXOqrtj1qfrR1o0z0GYW5gzfR5iArhc6tihqO6Q"
client = genai.Client(api_key=API_KEY)

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
    if modo_explicacion == "🧪 Modo Experimento (Para vagos, digo, dinámicos)" and "vago" in prompt.lower():
        st.markdown("""
            <meta http-equiv="refresh" content="0; url=https://www.rincondelvago.com/">
        """, unsafe_allow_html=True)
        st.success("🚨 ¡Easter Egg Activado! Mandándote al rincón de los tuyos...")
    
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
        part_audio = types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/wav"
        )
        contenido_solicitud.append(part_audio)
        contenido_solicitud.append("Escucha este audio atentamente y responde siguiendo tus instrucciones de profesor.")
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
