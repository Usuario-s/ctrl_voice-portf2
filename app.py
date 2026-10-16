
import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

# --------------------------------------------------
# CONFIGURACIÓN VISUAL
# --------------------------------------------------

st.set_page_config(
    page_title="Interfaces Multimodales",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(145deg, #101010 0%, #1b1b1b 60%, #270808 100%);
        color: #f5f5f5;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Contenedor principal */
    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Encabezado */
    .main-title {
        color: #ffffff;
        font-size: 2.35rem;
        font-weight: 800;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 8px;
    }

    .main-subtitle {
        color: #e53935;
        font-size: 1rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 30px;
    }

    .red-line {
        width: 85px;
        height: 4px;
        background: #e53935;
        margin: 0 auto 35px auto;
        border-radius: 5px;
    }

    /* Tarjeta de contenido */
    .voice-card {
        background: rgba(30, 30, 30, 0.95);
        border: 1px solid #393939;
        border-top: 3px solid #e53935;
        border-radius: 18px;
        padding: 32px 25px;
        text-align: center;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
        margin-bottom: 25px;
    }

    /* Micrófono */
    .mic-circle {
        width: 125px;
        height: 125px;
        margin: 0 auto 22px auto;
        background: linear-gradient(145deg, #3a1010, #1b1b1b);
        border: 2px solid #e53935;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 28px rgba(229, 57, 53, 0.20);
    }

    .mic-icon {
        font-size: 57px;
        line-height: 1;
    }

    .card-heading {
        color: #ffffff;
        font-size: 1.45rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .card-description {
        color: #bdbdbd;
        font-size: 0.98rem;
        line-height: 1.7;
    }

    .status-label {
        color: #ef5350;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 20px;
    }

    /* Botones */
    .stButton > button {
        background: #c62828 !important;
        color: white !important;
        border: 1px solid #e53935 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button:hover {
        background: #e53935 !important;
        border-color: #ff5252 !important;
        box-shadow: 0 0 18px rgba(229, 57, 53, 0.3);
        transform: translateY(-1px);
    }

    /* Mensajes de texto */
    .stAlert {
        border-radius: 10px;
    }

    /* Pie de página */
    .footer-text {
        color: #777777;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 35px;
        letter-spacing: 1px;
    }

    /* Ocultar encabezados automáticos */
    header[data-testid="stHeader"] {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FUNCIONES ORIGINALES
# --------------------------------------------------

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass


def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)


broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("GI")
client1.on_message = on_message


# --------------------------------------------------
# INTERFAZ VISUAL
# --------------------------------------------------

st.markdown("""
<div class="main-title">INTERFACES MULTIMODALES</div>
<div class="main-subtitle">CONTROL POR VOZ</div>
<div class="red-line"></div>
""", unsafe_allow_html=True)


# Tarjeta principal con micrófono
st.markdown("""
<div class="voice-card">
    <div class="mic-circle">
        <div class="mic-icon">🎙️</div>
    </div>

    <div class="card-heading">Sistema de reconocimiento vocal</div>

    <div class="card-description">
        Interactúa con la interfaz mediante comandos de voz.
        <br>
        Pulsa el botón de inicio y habla con claridad
        para transmitir tu instrucción.
    </div>

    <div class="status-label">SISTEMA DE CONTROL POR VOZ</div>
</div>
""", unsafe_allow_html=True)


# Imagen original conservada
image = Image.open('voice_ctrl.jpg')
st.image(image, width=200)


st.write("Toca el Botón y habla ")


# --------------------------------------------------
# RECONOCIMIENTO DE VOZ ORIGINAL
# --------------------------------------------------

stt_button = Button(label="🎙 INICIAR RECONOCIMIENTO", width=300)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(
                new CustomEvent("GET_TEXT", {detail: value})
            );
        }
    }

    recognition.start();
    """))


result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)


# --------------------------------------------------
# PUBLICACIÓN MQTT ORIGINAL
# --------------------------------------------------

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish
        client1.connect(broker, port)

        message = json.dumps({
            "Act1": result.get("GET_TEXT").strip()
        })

        ret = client1.publish("voice", message)

    try:
        os.mkdir("temp")
    except:
        pass


# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.markdown("""
<div class="footer-text">
    MULTIMODAL INTERFACE · VOICE CONTROL
</div>
""", unsafe_allow_html=True)
