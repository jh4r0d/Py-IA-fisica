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
    st.session_state.pastel_colors = ["#FAFAFA", "#FFE3E3", "#E8F5E9", "#FFF9E6"]

if "messages_nino" not in st.session_state:
    st.session_state.messages_nino = [
        {"role": "assistant", "content": "¡Hola, pequeño gran explorador del universo! ✨ Soy AIrtin, tu compañero de aventuras científicas. ¿Qué misterio de la naturaleza o curiosidad te gustaría descubrir juntos hoy? ¡Pregúntame con toda confianza! 🌟"}
    ]
if "messages_uni" not in st.session_state:
    st.session_state.messages_uni = [
        {"role": "assistant", "content": "¡Buenas noches con todos! Soy AIrtin, tu clon virtual de Física 1. A ver, ¿quién va a ser el valiente que va a lanzar la primera duda hoy? No muerdo, solo jalo en los exámenes si no repasan. 🚀"}
    ]
if "messages_exp" not in st.session_state:
    st.session_state.messages_exp = [
        {"role": "assistant", "content": "¡Buenas! Bienvenidos al laboratorio de experimentos prácticos. Aquí venimos a aprender física rompiendo cosas en casa (de manera segura, claro). ¿Qué quieren probar hoy? No se queden como vagos. 🧪"}
    ]

st.sidebar.header("⚙️ Configuración de la Clase")
modo_explicacion = st.sidebar.selectbox(
    "¿En qué tono quieres la clase?",
    ["👶 Modo Niño (Para que tu sobrinito entienda)", 
     "🎓 Modo Universitario (Prepárate para la PC)",
     "🧪 Modo Experimento (Para vagos, digo, dinámicos)"]
)

if modo_explicacion == "👶 Modo Niño (Para que tu sobrinito entienda)":
    chat_actual = st.session_state.messages_nino
elif modo_explicacion == "🎓 Modo Universitario (Prepárate para la PC)":
    chat_actual = st.session_state.messages_uni
else:
    chat_actual = st.session_state.messages_exp

if modo_explicacion != st.session_state.prev_modo:
    if modo_explicacion == "👶 Modo Niño (Para que tu sobrinito entienda)":
        lista_colores = ["#FFB6C1", "#ADD8E6", "#98FB98", "#F0E68C", "#E6E6FA", "#FFD700", "#FFA07A", "#20B2AA", "#87CEFA", "#FF69B4"]
        elegidos = random.sample(lista_colores, 3)
        st.session_state.pastel_colors = ["#FAFAFA", elegidos[0], elegidos[1], elegidos[2]]
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
        }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {{
            color: #FFFFFF !important;
        }}
        [data-testid="stBottomBlockContainer"] {{
            background-color: {bg_zonas_rojas} !important;
        }}
        .stChatMessage, [data-testid="stChatMessage"] {{
            background-color: {bg_chat} !important;
            border-radius: 15px !important;
            border: 3px solid {btn_color} !important;
            padding: 15px !important;
        }}
        .stChatMessage * {{
            color: #2c3e50 !important;
        }}
        [data-testid="stChatInputContainer"] {{
            background-color: transparent !important;
            border: none !important;
        }}
        [data-testid="stChatInput"] {{
            background-color: {bg_chat} !important;
            border: 3px solid {btn_color} !important;
            border-radius: 15px !important;
        }}
        [data-testid="stChatInput"] textarea {{
            background-color: transparent !important;
            color: #1c1c1c !important;
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
        .stAlert p {{
            color: #1c1c1c !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 0; overflow: hidden;">
            <div style="position: absolute; top: 10%; left: 2%; animation: moveOne 14s infinite linear;"><img src="https://cdn-icons-png.flaticon.com/512/3020/3020473.png" width="90" style="opacity: 0.25;"></div>
            <div style="position: absolute; top: 45%; left: 3%; animation: moveTwo 18s infinite linear;"><img src="https://cdn-icons-png.flaticon.com/512/2510/2510001.png" width="100" style="opacity: 0.25;"></div>
            <div style="position: absolute; bottom: 20%; left: 1%; animation: moveThree 22s infinite linear;"><img src="https://cdn-icons-png.flaticon.com/512/3655/3655581.png" width="85" style="opacity: 0.25;"></div>
            <div style="position: absolute; top: 15%; right: 2%; animation: moveFour 16s infinite linear;"><img src="https://cdn-icons-png.flaticon.com/512/2940/2940176.png" width="95" style="opacity: 0.25;"></div>
            <div style="position: absolute; top: 50%; right: 3%; animation: moveFive 20s infinite linear;"><img src="https://cdn-icons-png.flaticon.com/512/1048/1048943.png" width="90" style="opacity: 0.25;"></div>
            <div style="position: absolute; bottom: 25%; right: 1%; animation: moveSix 24s infinite linear;"><img src="https://cdn-icons-png.flaticon.com/512/911/911174.png" width="80" style="opacity: 0.25;"></div>
        </div>
        <style>
        @keyframes moveOne {
            0% { opacity: 0; transform: translate(0px, 0px) scale(0.8); }
            10% { opacity: 0.4; }
            45% { transform: translate(40px, -40px) scale(1); opacity: 0.4; }
            50% { opacity: 0; transform: translate(40px, -40px) scale(0.8); }
            55% { transform: translate(10px, 150px) scale(0.8); opacity: 0; }
            60% { opacity: 0.4; }
            90% { transform: translate(-20px, 80px) scale(1); opacity: 0.4; }
            100% { opacity: 0; transform: translate(0px, 0px) scale(0.8); }
        }
        @keyframes moveTwo {
            0% { opacity: 0; transform: translate(0px, 0px); }
            15% { opacity: 0.4; }
            40% { transform: translate(30px, 60px); opacity: 0.4; }
            45% { opacity: 0; transform: translate(30px, 60px); }
            50% { transform: translate(-10px, -100px); opacity: 0; }
            55% { opacity: 0.4; }
            95% { transform: translate(20px, -40px); opacity: 0.4; }
            100% { opacity: 0; transform: translate(0px, 0px); }
        }
        @keyframes moveThree {
            0% { opacity: 0; transform: translate(0px, 0px); }
            10% { opacity: 0.4; }
            50% { transform: translate(20px, -80px); opacity: 0.4; }
            55% { opacity: 0; }
            60% { transform: translate(35px, -180px); opacity: 0; }
            65% { opacity: 0.4; }
            95% { transform: translate(0px, -120px); opacity: 0.4; }
            100% { opacity: 0; }
        }
        @keyframes moveFour {
            0% { opacity: 0; transform: translate(0px, 0px); }
            12% { opacity: 0.4; }
            40% { transform: translate(-30px, -50px); opacity: 0.4; }
            45% { opacity: 0; transform: translate(-30px, -50px); }
            50% { transform: translate(20px, 120px); opacity: 0; }
            55% { opacity: 0.4; }
            92% { transform: translate(-15px, 60px); opacity: 0.4; }
            100% { opacity: 0; transform: translate(0px, 0px); }
        }
        @keyframes moveFive {
            0% { opacity: 0; transform: translate(0px, 0px); }
            8% { opacity: 0.4; }
            48% { transform: translate(-25px, 70px); opacity: 0.4; }
            53% { opacity: 0; transform: translate(-25px, 70px); }
            58% { transform: translate(15px, -90px); opacity: 0; }
            63% { opacity: 0.4; }
            95% { transform: translate(-10px, -45px); opacity: 0.4; }
            100% { opacity: 0; transform: translate(0px, 0px); }
        }
        @keyframes moveSix {
            0% { opacity: 0; transform: translate(0px, 0px); }
            15% { opacity: 0.4; }
            45% { transform: translate(-20px, -70px); opacity: 0.4; }
            50% { opacity: 0; }
            55% { transform: translate(-30px, -160px); opacity: 0; }
            60% { opacity: 0.4; }
            90% { transform: translate(15px, -110px); opacity: 0.4; }
            100% { opacity: 0; }
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stBottomBlockContainer"] { background-color: #0f172a !important; }
        [data-testid="stChatInputContainer"] { background-color: #0f172a !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
            color: #FFFFFF !important;
        }
        h1 { color: #38bdf8 !important; text-align: center; font-family: 'Arial', sans-serif; font-weight: bold; }
        .stButton { text-align: center !important; }
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

for message in chat_actual:
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
    vago_activado = False
    if modo_explicacion == "🧪 Modo Experimento (Para vagos, digo, dinámicos)" and "vago" in prompt.lower():
        vago_activado = True
    
    with st.chat_message("user"):
        if audio_bytes:
            st.markdown("🎤 *Mensaje de voz enviado*")
            st.audio(audio_bytes, format="audio/wav")
        else:
            st.markdown(prompt)
            
    chat_actual.append({"role": "user", "content": prompt if not audio_bytes else "🎤 Mensaje de voz"})

    perfil_instrucciones = f"Estás dictando clase en {modo_explicacion}. "
    
    if modo_explicacion == "👶 Modo Niño (Para que tu sobrinito entienda)":
        system_instruction = perfil_instrucciones + """
        Eres AIrtin, pero en esta ocasión te estás comunicando con niños pequeños. Modifica tu comportamiento por completo: 
        sé extremadamente educado, gentil, cariñoso y paciente. No uses bromas de jalar exámenes, prácticas calificadas, amanecidas o copiar. 
        Explica los conceptos de física con mucha ternura, usando analogías muy fáciles basadas en superhéroes, caramelos, magia, cuentos o animales. 
        Mantén un tono de maestro de primaria muy alegre, motivador, que los felicite por su curiosidad y use muchos emojis bonitos.
        """
    else:
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
                
                if vago_activado:
                    st.markdown("### 🦥 ¡ALERTA DE VAGO DETECTADA!")
                    st.link_button("👉 CLICK AQUÍ PARA IR AL RINCÓN DEL VAGO", "https://www.rincondelvago.com/")
                
                audio_html = ""
                if modo_explicacion == "👶 Modo Niño (Para que tu sobrinito entienda)":
                    texto_limpio = respuesta_texto.replace('"', '&quot;').replace('\n', ' ')
                    audio_html = f"""
                    <div style="margin-top:10px;">
                        <p style="font-size:13px; color:#555;">🔊 <i>Leyendo para ti:</i></p>
                        <audio autoplay controls src="https://translate.google.com/translate_tts?ie=UTF-8&tl=es&client=tw-ob&q={texto_limpio[:200]}"></audio>
                    </div>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
                
                chat_actual.append({"role": "assistant", "content": respuesta_texto if not audio_html else respuesta_texto + audio_html})
                    
            except Exception as e:
                st.error(f"¡Un lapsus! Se nos cayó la tiza del servidor: {e}")
