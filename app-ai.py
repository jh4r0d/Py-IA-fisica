import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import io
import random
import re

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

# --- INYECCIÓN DE ESTILOS CON CONTRASTE ALTO SEGÚN EL ENTORNO ---
if modo_explicacion == "👶 Modo Niño (Para que tu sobrinito entienda)":
    bg_chat = st.session_state.pastel_colors[0]
    bg_entorno = st.session_state.pastel_colors[1]
    bg_zonas_rojas = st.session_state.pastel_colors[2]
    btn_color = st.session_state.pastel_colors[3]
    
    st.markdown(f"""
        <style>
        /* CONTRASTE MODO CLARO / PASTEL NIÑOS: Todo el texto base debe ser Oscuro (#2c3e50) */
        .stApp, [data-testid="stHeader"], [data-testid="stSidebarCollapsedControl"] {{
            background-color: {bg_entorno} !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {bg_zonas_rojas} !important;
        }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] li {{
            color: #FFFFFF !important;
        }}
        [data-testid="stBottomBlockContainer"] {{
            background-color: {bg_zonas_rojas} !important;
        }}
        
        /* Modificadores globales de texto en el cuerpo principal */
        .stApp p, .stApp span, .stApp label, .stApp li, .stApp div, .stApp h1, .stApp h2, .stApp h3 {{
            color: #2c3e50 !important;
            font-family: 'Comic Sans MS', sans-serif;
        }}
        
        /* Bloques de chat */
        .stChatMessage, [data-testid="stChatMessage"] {{
            background-color: {bg_chat} !important;
            border-radius: 15px !important;
            border: 3px solid {btn_color} !important;
            padding: 15px !important;
        }}
        .stChatMessage p, .stChatMessage span, .stChatMessage li, .stChatMessage div {{
            color: #2c3e50 !important;
        }}
        
        /* Entrada de texto del chat */
        [data-testid="stChatInputContainer"] {{
            background-color: transparent !important;
            border: none !important;
        }}
        [data-testid="stChatInput"] {{
            background-color: #FFFFFF !important;
            border: 3px solid {btn_color} !important;
            border-radius: 15px !important;
        }}
        [data-testid="stChatInput"] textarea {{
            background-color: transparent !important;
            color: #2c3e50 !important;
            -webkit-text-fill-color: #2c3e50 !important;
        }}
        [data-testid="stChatInput"] textarea::placeholder {{
            color: #7f8c8d !important;
            -webkit-text-fill-color: #7f8c8d !important;
        }}

        /* Componente de subida de archivos */
        [data-testid="stFileUploader"] section {{
            background-color: #FAFAFA !important;
            border: 2px dashed #2c3e50 !important;
        }}
        [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small {{
            color: #2c3e50 !important;
        }}
        [data-testid="stFileUploader"] button {{
            background-color: #2c3e50 !important;
            color: #FFFFFF !important;
            border: none !important;
        }}
        
        /* Botones generales */
        .stButton>button {{ 
            background-color: {btn_color} !important; 
            color: #1c1c1c !important; 
            border-radius: 20px; 
            font-weight: bold; 
            border: 2px solid #2c3e50 !important;
        }}
        .stAlert p {{
            color: #1c1c1c !important;
        }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        /* CONTRASTE MODO OSCURO (UNI/EXP): Todo el texto base debe ser Blanco Puro (#FFFFFF) o Celeste (#38bdf8) */
        .stApp, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stBottomBlockContainer"] { 
            background-color: #0f172a !important; 
        }
        
        /* Forzar texto blanco en toda la aplicación principal para que resalte sobre el azul oscuro */
        .stApp p, .stApp span, .stApp label, .stApp li, .stApp div, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] li {
            color: #FFFFFF !important;
            font-family: 'Arial', sans-serif;
        }
        
        /* Títulos */
        h1, h2, h3 { 
            color: #38bdf8 !important; 
            font-family: 'Arial', sans-serif; 
            font-weight: bold; 
        }
        
        /* Cajas de mensajes dentro del chat */
        .stChatMessage, [data-testid="stChatMessage"] {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
        }
        .stChatMessage p, .stChatMessage span, .stChatMessage li, .stChatMessage div {
            color: #FFFFFF !important;
        }
        
        /* Entrada de texto de chat (Fondo intermedio, letras blancas nítidas) */
        [data-testid="stChatInputContainer"] { background-color: #0f172a !important; }
        [data-testid="stChatInput"] {
            background-color: #1e293b !important;
            border: 2px solid #38bdf8 !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #94a3b8 !important;
            -webkit-text-fill-color: #94a3b8 !important;
        }

        /* Subida de archivos */
        [data-testid="stFileUploader"] section {
            background-color: #1e293b !important;
            border: 1px dashed #38bdf8 !important;
        }
        [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small {
            color: #FFFFFF !important;
        }
        [data-testid="stFileUploader"] button {
            background-color: #38bdf8 !important;
            color: #0f172a !important;
            font-weight: bold !important;
        }

        /* Botones decorativos */
        .stButton { text-align: center !important; }
        .stButton>button { 
            background-color: #ec4899 !important; 
            color: white !important; 
            border-radius: 20px; 
            font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("👨‍🏫 AIrtin: Tu Profesor de Física 1")
st.write("¡A ver, entren, entren! Saquen una hoja... mentira. Pregúntame lo que quieras de física, teoría o problemas. Puedes hablarme, escribirme o subir la foto de ese ejercicio que no te sale.")

# --- LISTA DE CLAVES DISPONIBLES ---
POOL_KEYS = [
    "AQ.Ab8RN6JvCsVZXOqrtj1qfrR1o0z0GYW5gzfR5iArhc6tihqO6Q",
    "AIzaSyB7tGeuVKL_1Wz85UZdqCeL60Eh8YHD_6w",
    "AIzaSyDBAG8oax2hRyuIzuSIWPp5-H-dvUNP_VE"
]

st.sidebar.markdown("---")
st.sidebar.header("📁 Adjuntar Ejercicio")
imagen_subida = st.sidebar.file_uploader("Sube la foto del problema:", type=["png", "jpg", "jpeg"])

for message in chat_actual:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
            
            response = None
            ultimo_error = ""
            random.shuffle(POOL_KEYS)
            
            for key in POOL_KEYS:
                try:
                    client = genai.Client(api_key=key.strip())
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contenido_solicitud,
                        config={"system_instruction": system_instruction, "temperature": 0.5}
                    )
                    if response:
                        break
                except Exception as e:
                    ultimo_error = str(e)
                    continue

            if response:
                try:
                    respuesta_texto = response.text
                    st.markdown(respuesta_texto)
                    
                    if vago_activado:
                        st.markdown("### 🦥 ¡ALERTA DE VAGO DETECTADA!")
                        st.link_button("👉 CLICK AQUÍ PARA IR AL RINCÓN DEL VAGO", "https://www.rincondelvago.com/")
                    
                    chat_actual.append({"role": "assistant", "content": respuesta_texto})
                except Exception as e:
                    st.error("🎒 **¡Un pequeño tropiezo en el salón de clases!** No pudimos procesar tu mensaje. Por favor, espera unos segundos e inténtalo de nuevo.")
            else:
                if "429" in ultimo_error or "quota" in ultimo_error.lower() or "limit" in ultimo_error.lower():
                    segundos_espera = "10"
                    match = re.search(r'retry in ([\d\.]+)', ultimo_error)
                    if match:
                        segundos_espera = str(int(float(match.group(1))) + 1)
                    st.warning(f"⏳ **¡Uy, un segundo!** Como este es un chatbot educativo gratuito, tenemos que tomar turnos para usar la pizarra. Por favor, **espera {segundos_espera} segundos** y vuelve a enviar tu pregunta. ¡Muchas gracias por tu paciencia! 🎒")
                else:
                    st.error("🎒 **¡Un pequeño tropiezo en el salón de clases!** No pudimos conectar con ninguna clave. Por favor, espera unos segundos e inténtalo de nuevo.")
                    st.caption(f"🔧 *Nota técnica del error:* `{ultimo_error}`")
