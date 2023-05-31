from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
import anvil.server
import random
import anvil.tz
from datetime import datetime
from anvil.tables import app_tables
import anvil.media
from datetime import datetime
from collections import deque

# colecciones para almacenar los datos de las gráficas
soundLevel = deque()
timestamps = deque()


class Form1(Form1Template):
    def init(self, **properties):
        # Establecer propiedades del formulario y enlaces de datos.
        self.init_components(**properties)
        self.timer_1.interval = 1000  # Configurar el temporizador para que se ejecute cada segundo
        self.timer_1.enabled = True  # Habilitar el temporizador

    # Codigo para el boton Save Sound
    def button_1_click(self, **event_args):
        a = anvil.server.call('calculate_sound_level')
        self.label_5.text = (a)
        time = datetime.now()
        app_tables.sounddatabase.add_row(timeStamp=time, SoundLevel=a)
        self.plot_data()

    # Codigo para el boton Show Danger Level
    def button_3_click(self, **event_args):
        # El boton activa el medidor de riesgo de sonido
        x = anvil.server.call('picodangerLevel')
        self.label_4.text = x  # Mostrar el mensaje en el cuadro de texto
        # Guardar en base de datos el mensaje y su hora
        time = datetime.now()
        app_tables.dangerlevel.add_row(timeStamp=time, mensaje=x)

    def button_2_click(self, **event_args):
        anvil.server.call('useLED')

    def timer_1_tick(self, **event_args):
        global soundLevel
        global timestamps
        timestamp = datetime.now()
        sound = anvil.server.call_s('calculate_sound_level')
        soundLevel.append(sound)
        timestamps.append(timestamp)

        self.plot_1.data = go.Scatter(x=list(timestamps), y=list(soundLevel))
        self.plot_1.layout.title = "Sound Level" 