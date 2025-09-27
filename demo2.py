# AGENTES
# 1. Recibe una pregunta
# 2. La procesa con un LLM (Gemini)
# 3. Devuelve una respuesta

from asyncio import ensure_future
import google.generativeai as genai 
import os
from datetime import datetime


# CONFIGURAR el cerebro del agente (el modelo de Gemini)

def configurar_genai():
    API_KEY = "AIzaSyCFb8L1KC_Nya_PlLKYj65hO-JMOfGravw"
    genai.configure(api_key=API_KEY)

    MODEL_NAME = "gemini-2.5-flash"

    modelo = genai.GenerativeModel(MODEL_NAME)

    return modelo


class MemoriaConversacion:
    
    def __init__(self):
        self.historial = []
        self.inicio_conversacion = datetime.now()

    def agregar_mensaje(self, rol, contenido):
        mensaje = {
            "rol": rol,
            "contenido": contenido,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.historial.append(mensaje)


    def obtener_contexto(self, ultimos_n=10):
        if not self.historial:
            return "Esto es la primera vez que conversamos."

        mensajes_recientes = self.historial[-ultimos_n:]

        contexto = "HISTORIAL DE CONVERSACION:\n"
        for msg in mensajes_recientes:
            rol_emoji = "👨‍💻" if msg["rol"] == "usuario" else "🤖"
            contexto += f"{rol_emoji} {msg['rol'].title()}: {msg['contenido']}\n"
        
        return contexto

    def obtener_estadisticas(self):
        total_mensajes = len(self.historial)
        mensajes_usuario = len([msg for msg in self.historial if msg['rol'] == 'usuario'])
        mensajes_agente = len([msg for msg in self.historial if msg['rol'] == 'agente'])
        
        return {
            'total': total_mensajes,
            'mensajes_usuario': mensajes_usuario,
            'mensajes_agente': mensajes_agente,
            'duracion': datetime.now() - self.inicio_conversacion
        }

class Agent:
    """Agente basico. 
    QUE HACE? 
    1. Recibe preguntas.
    2. Procesa con Gemini.
    3. Devuelve respuesta.
    """

    def __init__(self, modelo):

        self.modelo = modelo
        self.nombre = "Asistente de Gemini"
        self.memoria = MemoriaConversacion()
        self.personalidad = """
        Eres un asistente educativo, amigable y util.
        Tu trabajo es ayudar a programadores a aprender otro lenguaje de programación.
        Siempre responde de manera clara y educativa.
        """
    
    def pensar(self, pregunta):
        try:
            self.memoria.agregar_mensaje("usuario", pregunta)

            contexto = self.memoria.obtener_contexto()
            

            prompt = f"""{self.personalidad}
            {contexto}
            Pregunta del usuario: {pregunta}
            Responde considerando todo el contexto de la conversación."""

            respuesta = self.modelo.generate_content(prompt)

            respuesta_texto = respuesta.text

            self.memoria.agregar_mensaje("agente", respuesta_texto)

            return respuesta_texto
        
        except Exception as e:
            error_msg = f"Error al procesar: {str(e)}"
            self.memoria.agregar_mensaje("agente", error_msg)
            return error_msg

    


    def conversar(self):
        print(f"Hola, soy {self.nombre}")
        print("Soy un Asistente que puede ayudarte con tus preguntas.")
        print("Puedes preguntarme lo que quieras.")
        print("Tengo memoria! Asi que recuerdo todo.")
        print("Para salir, escribe 'adios'.")

        while True:
            pregunta = input("\nTú: ")
            
            if pregunta.lower() == "adios":
                self.obtener_estadisticas()

                print("Adios, gracias por usar el asistente.")
                break
            elif pregunta.lower() == "stats":
                self.obtener_estadisticas()
                continue

            elif pregunta.lower() == "guardar":
                self.guardar_conversacion()
                continue

            print(f"{self.nombre}: ", end="")
            respuesta = self.pensar(pregunta)
            print(respuesta)
            print("=="*50)
    
    def obtener_estadisticas(self):
        stats = self.memoria.obtener_estadisticas()
        print("\nESTADISTICAS DE LA CONVERSACIÓN:")
        print(f"Total de mensajes: {stats['total']}")
        print(f"Mensajes del usuario: {stats['mensajes_usuario']}")
        print(f"Mensajes del agente: {stats['mensajes_agente']}")
        print(f"Duración: {stats['duracion']}")
    
    def guardar_conversacion(self, archivo="conversacion.json"):
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(self.memoria.historial, f, ensure_ascii=False, indent=4)
            print(f"Conversación guardada en {archivo}")
        except Exception as e:
            print(f"Error al guardar la conversación: {str(e)}")

        


def main():
    print("MI PRIMER AGENTE.")
    print("=="*50)

    modelo = configurar_genai()
    agente = Agent(modelo)
    agente.conversar()

if __name__ == "__main__":
    main()
            
        