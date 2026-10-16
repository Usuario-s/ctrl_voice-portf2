

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
# CONFIGURACIÓN DE STREAMLIT
# --------------------------------------------------

st.set_page_config(
    page_title="Interfaces Multimodales",
    page_icon="🎙️",
    layout="centered"
)


# --------------------------------------------------
# DISEÑO GENERAL
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(
            145deg,
            #0b0b0b 0%,
            #151515 60%,
            #250707 100%
        );
        color: #ffffff;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    p {
        color: #d0d0d0;
    }

    .red-line {
        width: 85px;
        height: 4px;
        background: #e53935;
        margin: 0 auto 35px auto;
        border-radius: 5px;
    }

    .mic-container {
        text-align: center;
        margin: 10px 0 15px 0;
    }

    .mic-circle {
        width: 125px;
        height: 125px;
        margin: 0 auto;
        background: linear-gradient(
            145deg,
            #351010,
            #151515
        );
        border: 2px solid #e53935;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(229, 57, 53, 0.2);
    }

    .mic-icon {
        font-size: 55px;
    }

    .status-text {
        text-align: center;
        color: #e53935;
        font-size: 0.8rem;
        font-weight: bold;
        letter-spacing: 3px;
        margin-top: 15px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(25, 25, 25, 0.95);
        border: 1px solid #3a3a3a;
        border-top: 3px solid #e53935;
        border-radius: 18px;
    }

    /* Botones nativos de Streamlit */
    .stButton > button {
        background-color: #c62828 !important;
        color: white !important;
        border: 1px solid #e53935 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }

    .stButton > button:hover {
        background-color: #e53935 !important;
        box-shadow: 0 0 18px rgba(229, 57, 53, 0.35);
    }

    /* Botón de Bokeh */
    .voice-mic-button {
        background-color: #c62828 !important;
        color: #ffffff !important;
        border: 1px solid #e53935 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        box-shadow: 0 0 12px rgba(229, 57, 53, 0.2);
    }

    .footer-text {
        text-align: center;
        color: #666666;
        font-size: 12px;
        letter-spacing: 2px;
        margin-top: 35px;
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

    message_received = str(
        message.payload.decode("utf-8")
    )

    st.write(message_received)


# --------------------------------------------------
# CONFIGURACIÓN MQTT
# --------------------------------------------------

broker = "broker.mqttdashboard.com"
port = 1883

client1 = paho.Client("GI")
client1.on_message = on_message


# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.markdown(
    "<h1 style='text-align:center; color:white; "
    "letter-spacing:3px;'>"
    "INTERFACES MULTIMODALES"
    "</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:#e53935; "
    "font-weight:bold; letter-spacing:5px;'>"
    "CONTROL POR VOZ"
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='red-line'></div>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# TARJETA PRINCIPAL
# --------------------------------------------------

with st.container(border=True):

    st.markdown("""
        <div class="mic-container">
            <div class="mic-circle">
                <span class="mic-icon">🎙️</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<h3 style='text-align:center; color:white;'>"
        "Sistema de reconocimiento vocal"
        "</h3>",
        unsafe_allow_html=True
    )

    st.write(
        "Interactúa con la interfaz mediante comandos de voz. "
        "Pulsa el botón de inicio y habla con claridad "
        "para transmitir tu instrucción."
    )

    st.markdown(
        "<p class='status-text'>"
        "SISTEMA DE CONTROL POR VOZ"
        "</p>",
        unsafe_allow_html=True
    )


# --------------------------------------------------
# IMAGEN ORIGINAL
# --------------------------------------------------

image = Image.open("voice_ctrl.jpg")
st.image(image, width=200)


# --------------------------------------------------
# INSTRUCCIONES
# --------------------------------------------------

st.markdown(
    "<p style='text-align:center;'>"
    "Pulsa el botón para activar el micrófono y hablar."
    "</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# BOTÓN DE RECONOCIMIENTO DE VOZ
# --------------------------------------------------

stt_button = Button(
    label="🎙 INICIAR RECONOCIMIENTO",
    width=300,
    height=48,
    button_type="danger",
    css_classes=["voice-mic-button"]
)


# --------------------------------------------------
# RECONOCIMIENTO DE VOZ CON JAVASCRIPT
# --------------------------------------------------

stt_button.js_on_event(
    "button_click",
    CustomJS(code="""
        var SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            alert(
                "Tu navegador no admite reconocimiento de voz. "
                + "Prueba con Google Chrome."
            );
            return;
        }

        var recognition = new SpeechRecognition();

        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "es-CO";

        recognition.onresult = function (e) {
            var value = "";

            for (
                var i = e.resultIndex;
                i < e.results.length;
                ++i
            ) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }

            if (value.trim() !== "") {
                document.dispatchEvent(
                    new CustomEvent(
                        "GET_TEXT",
                        {detail: value.trim()}
                    )
                );
            }
        };

        recognition.onerror = function (e) {
            console.error(
                "Error de reconocimiento:",
                e.error
            );
        };

        recognition.start();
    """)
)


# --------------------------------------------------
# MOSTRAR BOTÓN Y RECIBIR EVENTOS
# --------------------------------------------------

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)


# --------------------------------------------------
# PROCESAR RESULTADO Y PUBLICAR POR MQTT
# --------------------------------------------------

if result:
    if "GET_TEXT" in result:

        texto_reconocido = result.get("GET_TEXT")

        st.markdown("### Texto reconocido")
        st.write(texto_reconocido)

        client1.on_publish = on_publish

        client1.connect(broker, port)

        message = json.dumps({
            "Act1": texto_reconocido.strip()
        })

        ret = client1.publish(
            "voice",
            message
        )

    # Crear carpeta temporal si no existe
    try:
        os.mkdir("temp")
    except FileExistsError:
        pass


# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.markdown("""
    <p class="footer-text">
        MULTIMODAL INTERFACE · VOICE CONTROL
    </p>
""", unsafe_allow_html=True)

