import speech_recognition as sr
import webbrowser
import pyttsx3
import time  # Para agregar pausas

recognizer = sr.Recognizer()  # Creamos el objeto de reconocimiento de voz
engine = pyttsx3.init()  # Inicializamos el motor de texto a voz

def talk():
    try:
        mic = sr.Microphone()  # Usamos el micrófono como entrada de audio
        with mic as source:
            audio = recognizer.listen(source)  # Escuchamos lo que dice el usuario
        text = recognizer.recognize_google(audio, language='es-ES')  # Convertimos el audio en texto
        print(f'Te he entendido, has dicho: {text}')
        return text.lower()
    except sr.UnknownValueError:
        print("No te he entendido, repítelo, por favor")
        engine.say("No te he entendido, repítelo, por favor")
        engine.runAndWait()
        
        return ""  # Regresamos a la función talk
    except sr.RequestError as e:
        print(f"Ha fallado el reconocimiento de voz: {e}")
        engine.say("Falló el reconocimiento de voz, por favor, inténtalo de nuevo")
        engine.runAndWait()
         
        return ""

def ask_to_continue():
    engine.say("¿Deseas continuar buscando o cerrar el programa? Di continuar o cerrar.")
    engine.runAndWait()
    response = talk()  # Capturamos la respuesta del usuario
    if 'cerrar' in response:
        engine.say("Cerrando el programa. ¡Hasta pronto!")
        engine.runAndWait()
        return False  # Indicamos que queremos salir
    elif 'continuar' in response:
        return True  # Indicamos que queremos seguir buscando
    else:
        engine.say("No entendí tu respuesta, por favor di continuar o cerrar.")
        engine.runAndWait()
        return ask_to_continue()  # Si no se entiende la respuesta, volvemos a preguntar

try:
    while True:
        # Solo preguntamos qué plataforma usar al principio
        engine.say("Dime donde quieres buscar: amazon, google o youtube. Te estoy escuchando...")
        engine.runAndWait()
        
        text = talk()  # Llamamos a talk para obtener el texto reconocido

        # Si el usuario dice "amazon"
        if 'amazon' in text:
            engine.say('¿En qué te quieres gastar el dinero en amazon?')
            engine.runAndWait()
             
            search = talk()
            if search:
                webbrowser.open(f'https://www.amazon.es/s?k={search}')
            else:
                engine.say("No hemos encontrado nada, eso que te ahorras")
                engine.runAndWait()
        
        # Si el usuario dice "google"
        elif 'google' in text:
            engine.say('¿Qué quieres buscar en google?')
            engine.runAndWait()
             
            search = talk()
            if search:
                webbrowser.open(f'https://www.google.com/search?q={search}')
            else:
                engine.say("No hemos encontrado nada")
                engine.runAndWait()
        
        # Si el usuario dice "youtube"
        elif 'youtube' in text:
            engine.say('¿Qué quieres buscar en youtube?')
            engine.runAndWait()
           
            search = talk()
            if search:
                webbrowser.open(f'https://www.youtube.com/results?search_query={search}')
            else:
                engine.say("No hemos encontrado nada en youtube")
                engine.runAndWait()
        
        # Si el usuario no dijo nada válido
        else:
            print("No dijiste ninguna opción, inténtalo otra vez.")
            engine.say("No dijiste ninguna opción, inténtalo otra vez.")
            engine.runAndWait()
            time.sleep(2)  # Pausa de 2 segundos antes de volver a pedir la opción
        
        # Preguntamos al usuario si desea continuar o cerrar el programa
        if not ask_to_continue():
            break  # Si el usuario dice "cerrar", terminamos el bucle y el programa
except Exception as e:
    print(f"Tenemos un error inesperado: {e}")
    engine.say("Tenemos un error inesperado")
    engine.runAndWait()
