import speech_recognition as sr ### para convertit audio en texto
import webbrowser ### para abrir el navegador
import pyttsx3 ### para converir texto en voz

recognizer = sr.Recognizer()  ### creamos un objeto para procesar el audio y convertirlo en texto
engine = pyttsx3.init()  ### empezamos el motor de texto a voz

def talk():  ### con está función capturamos el audio del micrófono, lo procesamos y lo retormamos en texto
    try:
         ### capturamos el audio  ### 
        mic = sr.Microphone()  ### usamos el  microfono como entrada de audio
        with mic as source:  ### abrimos el microfono
            print("Dime donde quieres buscar:\n amazon\n google\n youtube?\n Te estoy escuchando...") 
            audio = recognizer.listen(source) ### escucha lo que hablamos por el microfono, lo captura en audio 
            ### source es el objeto fuente de audio, que permite que la biblioteca speech_recognition obtenga audio desde el micrófono configurado. 
        text = recognizer.recognize_google(audio, language='es-ES')  # Creamos text, que es el audio transformado en texto usando un servicio de google, en español.
        print(f'Te he entendido, has dicho: {text}') ### la f: Permite insertar expresiones o valores de variables directamente dentro de una cadena de texto usando llaves {}.
        return text.lower() ### el texto lo ponemos en minusculas
    except sr.UnknownValueError:  ### se activa si el reconocedor de voz no entiende lo que decimos
        print("No te he entendido, vocaliza") 
        engine.say("No te he entendido, vocaliza")  ### genera un audio con el texto que le facilitemos
        engine.runAndWait() ### asegura de que esta notificación sea reproducida completamente antes de pasar a la siguiente iteración del bucle. Asegura que se escuche. se reproduzca antes de continuar
        return ""  ### si tenemos este error, nos devuelve a la función talk, es decir, volvemos a empezar y se añade a la cola del motor
    except sr.RequestError as e: ### se activa si eun error con el servicio: no tenemos conexión, servicio caído
        print(f"Ha fallado el reconocimiento de voz: {e}")
        engine.say("Falló el reconocimiento de voz, por favor, inténtalo de nuevo")
        engine.runAndWait()
        return "" ### si tenemos este error, nos devuelve a la función talk, es decir, volvemos a empezar

try:
    while True: ### empezamos  un bucle infinito que repite la escucha y procesamiento hasta que se encuentre una opción válida o haya un error
        text = talk() ### el texto será el que ha reconocido en la función anterior, talk
        if 'amazon' in text: ### se ejecuta si hemos dicho amazon en la pregunta inicial
            engine.say('¿En qué te quieres gastar el dinero en amazon?')
            engine.runAndWait()  # Corrected method name
            search = talk() ### volvemos a ejecutar tal, pero ahora lo guardamos en la variable search
            if search:
                webbrowser.open(f'https://www.amazon.es/s?k={search}')  # si es correcto se abre el nave
            else:
                engine.say("No hemos encontrado nada, eso que te ahorras")
                engine.runAndWait()  # Corrected method name
            break
        elif 'google' in text:
            engine.say('¿Qué quieres buscar en google?')
            engine.runAndWait()  # Corrected method name
            search = talk()
            if search:
                webbrowser.open(f'https://www.google.com/search?q={search}')  # Corrected URL format
            else:
                engine.say("No hemos encontrado nada, eso que te ahorras")
                engine.runAndWait()  # Corrected method name
            break
        elif 'youtube' in text:
            engine.say('¿Qué quieres buscar en youtube?')
            engine.runAndWait()  # Corrected method name
            search = talk()
            if search:
                webbrowser.open(f'https://www.youtube.com/results?search_query={search}')  # Corrected URL format
            else:
                engine.say("No hemos encontrado nada en youtube")
                engine.runAndWait()  # Corrected method name
            break
        else:
            print("No dijiste ninguna opción, inténtalo otra vez.")
            engine.say("No dijiste ninguna opción, inténtalo otra vez.")
            engine.runAndWait()  # Corrected method name
except Exception as e:
    print(f"Tenemos un error inesperado: {e}")
    engine.say("Tenemos un error inesperado")
    engine.runAndWait()  # Corrected method name