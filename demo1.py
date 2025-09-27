# AGENTES
# 1. Recibe una pregunta
# 2. La procesa con un LLM (Gemini)
# 3. Devuelve una respuesta

import google.generativeai as genai 
import os

# CONFIGURAR el cerebro del agente (el modelo de Gemini)

def configurar_genai():
    API_KEY = "AIzaSyCFb8L1KC_Nya_PlLKYj65hO-JMOfGravw"
    genai.configure(api_key=API_KEY)

    MODEL_NAME = "gemini-2.5-flash"

    modelo = genai.GenerativeModel(MODEL_NAME)

    return modelo


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
        self.personalidad = """
        Eres un asistente educativo, amigable y util.
        Tu trabajo es ayudar a programadores a aprender otro lenguaje de programación.
        Siempre responde de manera clara y educativa.
        """
    
    def pensar(self, pregunta):
        try:
            prompt = f"""{self.personalidad}
            Pregunta del usuario: {pregunta}"""

            respuesta = self.modelo.generate_content(prompt)

            return respuesta.text
        
        except Exception as e:
            return f"Error: {str(e)}"

    def conversar(self):
        print(f"Hola, soy {self.nombre}")
        print("Soy un Asistente que puede ayudarte con tus preguntas.")
        print("Puedes preguntarme lo que quieras.")
        print("Para salir, escribe 'adios'.")

        while True:
            pregunta = input("\nTú: ")
            
            if pregunta.lower() == "adios":
                print("Adios, gracias por usar el asistente.")
                break
            
            print(f"{self.nombre}: ", end="")
            respuesta = self.pensar(pregunta)
            # guardar respuesta en un .txt
            with open("respuesta.txt", "w") as f:
                f.write(respuesta)
            print(respuesta)
            print("=="*50)


def main():
    print("MI PRIMER AGENTE.")
    print("=="*50)

    modelo = configurar_genai()
    agente = Agent(modelo)
    agente.conversar()

if __name__ == "__main__":
    main()
            
        

