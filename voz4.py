# Importamos las librerías necesarias
import sys  # Para interactuar con el sistema operativo (por ejemplo, salir del programa)
import speech_recognition as sr  # Para capturar y reconocer voz
import pyttsx3  # Para convertir texto en audio (síntesis de voz)
import webbrowser  # Para abrir páginas web en el navegador predeterminado

# Librerías de PyQt5 para crear la interfaz gráfica
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal  # QThread para hilos; pyqtSignal para señales

# ========================
# Clase VoiceThread
# ========================
class VoiceThread(QThread):
    # Señales que esta clase emitirá para comunicar eventos
    textChanged = pyqtSignal(str)  # Señal para enviar actualizaciones de texto
    finished = pyqtSignal(str)  # Señal cuando se termine el reconocimiento de voz

    def __init__(self, recognizer, microphone):
        super().__init__()  # Inicializamos el hilo (QThread)
        self.recognizer = recognizer  # Asignamos el objeto Recognizer
        self.microphone = microphone  # Asignamos el objeto Microphone

    def run(self):
        """
        Este método se ejecuta cuando se inicia el hilo.
        Aquí capturamos la voz, la reconocemos y enviamos las señales correspondientes.
        """
        try:
            # Activamos el micrófono y escuchamos al usuario
            with self.microphone as source:
                self.textChanged.emit("Te estoy escuchando...")  # Actualizamos el texto en la interfaz
                audio = self.recognizer.listen(source)  # Capturamos el audio del usuario

            # Intentamos convertir el audio en texto (usando Google Speech Recognition)
            text = self.recognizer.recognize_google(audio, language='es-ES')  # Reconocemos en español
            self.textChanged.emit(f'Te he entendido, has dicho: {text}')  # Mostramos el texto reconocido
            self.finished.emit(text.lower())  # Enviamos el texto reconocido en minúsculas

        # Si no se entiende lo dicho, emitimos una señal indicando que no se reconoció
        except sr.UnknownValueError:
            self.textChanged.emit("No te he entendido, vocaliza")
            self.finished.emit("")

        # Si hay un problema con el servicio de reconocimiento, emitimos un error
        except sr.RequestError as e:
            self.textChanged.emit(f"Ha fallado el reconocimiento de voz: {e}")
            self.finished.emit("")

# ========================
# Clase VoiceAssistant
# ========================
class VoiceAssistant(QMainWindow):
    def __init__(self):
        super().__init__()  # Inicializamos la ventana principal
        self.initUI()  # Configuramos la interfaz
        self.recognizer = sr.Recognizer()  # Creamos el objeto para reconocer voz
        self.microphone = sr.Microphone()  # Creamos el objeto para usar el micrófono
        self.engine = pyttsx3.init()  # Iniciamos el motor de síntesis de voz

    # Configuración de la interfaz gráfica
    def initUI(self):
        self.setWindowTitle('Asistente de Voz')  # Título de la ventana
        self.setGeometry(100, 100, 400, 300)  # Tamaño y posición de la ventana

        layout = QVBoxLayout()  # Diseño vertical para los elementos

        # Cuadro de texto para mostrar mensajes del asistente
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)  # Hacemos que el cuadro sea solo de lectura
        layout.addWidget(self.textEdit)

        # Botón para iniciar el reconocimiento de voz
        self.listenButton = QPushButton('Escuchar')
        self.listenButton.clicked.connect(self.start_listening)  # Conecta el clic a la función start_listening
        layout.addWidget(self.listenButton)

        # Contenedor para los widgets y asignación a la ventana principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Inicia el hilo de reconocimiento de voz
    def start_listening(self):
        self.listenButton.setEnabled(False)  # Deshabilitamos el botón mientras escuchamos
        self.thread = VoiceThread(self.recognizer, self.microphone)  # Creamos un hilo para el reconocimiento
        self.thread.textChanged.connect(self.update_text)  # Conectamos la señal de texto
        self.thread.finished.connect(self.process_voice)  # Conectamos la señal de finalización
        self.thread.start()  # Iniciamos el hilo

    # Muestra el texto recibido en el cuadro de texto
    def update_text(self, text):
        self.textEdit.append(text)

    # Procesa el texto reconocido y realiza las acciones correspondientes
    def process_voice(self, text):
        self.listenButton.setEnabled(True)  # Volvemos a habilitar el botón
        if 'amazon' in text:  # Si se menciona "amazon"
            self.engine.say('¿En qué te quieres gastar el dinero?')  # Mensaje de voz
            self.engine.runAndWait()
            self.start_listening()  # Continuamos escuchando
        elif text:  # Si se reconoce texto, realizamos una búsqueda en Amazon
            webbrowser.open(f'https://www.amazon.es/s?k={text}')  # Abrimos la búsqueda en Amazon España
            self.engine.say(f"Buscando {text} en Amazon")  # Avisamos al usuario
            self.engine.runAndWait()
        else:  # Si no se reconoció nada
            self.engine.say("No hemos encontrado nada, eso que te ahorras")
            self.engine.runAndWait()

# ========================
# Bloque principal
# ========================
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Creamos la aplicación
    ex = VoiceAssistant()  # Instanciamos el asistente
    ex.show()  # Mostramos la ventana
    sys.exit(app.exec_())  # Iniciamos el bucle de eventos de PyQt
