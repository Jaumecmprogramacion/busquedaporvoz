### primera versión reconocimiento voz amazon###
import sys
import speech_recognition as sr
import pyttsx3
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class VoiceThread(QThread):
    textChanged = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, recognizer, microphone):
        super().__init__()
        self.recognizer = recognizer
        self.microphone = microphone

    def run(self):
        try:
            with self.microphone as source:
                self.textChanged.emit("Te estoy escuchando...")
                audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio, language='es-ES')
            self.textChanged.emit(f'Te he entendido, has dicho: {text}')
            self.finished.emit(text.lower())
        except sr.UnknownValueError:
            self.textChanged.emit("No te he entendido, prueba otra vez")
            self.finished.emit("")
        except sr.RequestError as e:
            self.textChanged.emit(f"Ha fallado el reconocimiento de voz: {e}")
            self.finished.emit("")

class VoiceAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()

    def initUI(self):
        self.setWindowTitle('Asistente de Voz')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)

        self.listenButton = QPushButton('Escuchar')
        self.listenButton.clicked.connect(self.start_listening)
        layout.addWidget(self.listenButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_listening(self):
        self.listenButton.setEnabled(False)
        self.thread = VoiceThread(self.recognizer, self.microphone)
        self.thread.textChanged.connect(self.update_text)
        self.thread.finished.connect(self.process_voice)
        self.thread.start()

    def update_text(self, text):
        self.textEdit.append(text)

    def process_voice(self, text):
        self.listenButton.setEnabled(True)
        if 'amazon' in text:
            self.engine.say('¿En qué te quieres gastar el dinero?')
            self.engine.runAndWait()
            self.start_listening()
        elif text:
            webbrowser.open(f'https://www.amazon.es/s?k={text}')
            self.engine.say(f"Buscando {text} en Amazon")
            self.engine.runAndWait()
        else:
            self.engine.say("No hemos encontrado nada, eso que te ahorras")
            self.engine.runAndWait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceAssistant()
    ex.show()
    sys.exit(app.exec_())

