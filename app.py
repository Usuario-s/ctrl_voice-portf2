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
# DISEÑO
# --------------------------------------------------

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background: linear-gradient(
            145deg,
            #0b0b0b 0%,
            #151515 60%,
            #250707 100%
        );
        color: #ffffff;
    }

    /* Ocultar menú y footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Encabezado */
    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Título */
    h1 {
        color: #ffffff !important;
    }

    /* Subtítulos */
    h2, h3 {
        color: #ffffff !important;
    }

    /* Texto */
    p {
        color: #d0d0d0;
    }

    /* Línea roja */
    .red-line {
        width: 85px;
        height: 4px;
        background: #e53935;
        margin: 0 auto 35px auto;
        border-radius: 5px;
    }

    /* Contenedor del micrófono */
    .mic-container {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    /* Círculo del micrófono */
    .mic-circle {
        width: 125px;
        height: 125px;

        margin-left: auto;
        margin-right: auto;

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

        box-shadow:
            0 0 25px rgba(229, 57, 53, 0.20),
            inset 0 0 20px rgba(0, 0, 0, 0.5);
    }

    .mic-icon {
        font-size: 55px;
    }

    /* Texto pequeño */
    .status-text {
        text-align: center;
        color: #e53935;
        font-size: 0.8rem;
        font-weight: bold;
        letter-spacing: 3px;
        margin-top: 15px;
    }

    /* Botón */
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

    /* Contenedores */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(25, 25, 25, 0.95);
        border: 1px solid #3a3a3a;
        border-top: 3px solid #e53935;
        border-radius: 18px;
    }

    /* Caption */
    .stCaption {
        color: #e53935 !important;
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
# MQTT
# --------------------------------------------------

broker = "broker.mqttdashboard.com"
port = 1883

client1 = paho.Client("GI")

client1.on_message = on_message


# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.markdown(
    "<h1 style='text-align:center; letter-spacing:3px;'>"
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

    # Micrófono
    st.markdown("""
        <div class="mic-container">
            <div class="mic-circle">
                <span class="mic-icon">🎙️</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Título
    st.markdown(
        "<h3 style='text-align:center;'>"
        "Sistema de reconocimiento vocal"
        "</h3>",
        unsafe_allow_html=True
    )

    # Descripción
    st.write(
        "Interactúa con la interfaz mediante comandos de voz. "
        "Pulsa el botón de inicio y habla con claridad "
        "para transmitir tu instrucción."
    )

    # Estado
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

st.image(
    image,
    width=200
)


# --------------------------------------------------
# INSTRUCCIÓN
# --------------------------------------------------

st.markdown(
    "<p style='text-align:center; color:#bdbdbd;'>"
    "Toca el botón y habla"
    "</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# BOTÓN DE RECONOCIMIENTO DE VOZ
# --------------------------------------------------

stt_button = Button(
    label="🎙  INICIAR RECONOCIMIENTO",
    width=300
)


stt_button.js_on_event(
    "button_click",
    CustomJS(code="""

        var recognition = new webkitSpeechRecognition();

        recognition.continuous = true;
        recognition.interimResults = true;

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

            if (value != "") {

                document.dispatchEvent(
                    new CustomEvent(
                        "GET_TEXT",
                        {
                            detail: value
                        }
                    )
                );

            }

        }

        recognition.start();

    """)
)


# --------------------------------------------------
# EVENTO DE STREAMLIT BOKEH
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
# RESULTADO DEL RECONOCIMIENTO
# --------------------------------------------------

if result:

    if "GET_TEXT" in result:

        st.write(
            result.get("GET_TEXT")
        )

        # Callback MQTT
        client1.on_publish = on_publish

        # Conexión
        client1.connect(
            broker,
            port
        )

        # Crear mensaje
        message = json.dumps(
            {
                "Act1": result.get(
                    "GET_TEXT"
                ).strip()
            }
        )

        # Publicar mensaje
        ret = client1.publish(
            "voice",
            message
        )


    # --------------------------------------------------
    # CREAR CARPETA TEMP
    # --------------------------------------------------

    try:

        os.mkdir("temp")

    except:

        pass


# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.markdown(
    "<p style='text-align:center; "
    "color:#555555; "
    "font-size:12px; "
    "letter-spacing:2px; "
    "margin-top:35px;'>"
    "MULTIMODAL INTERFACE · VOICE CONTROL"
    "</p>",
    unsafe_allow_html=True
)
