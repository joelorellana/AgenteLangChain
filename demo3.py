from configparser import MAX_INTERPOLATION_DEPTH
import os
from urllib import response
import requests
from datetime import datetime
from typing import Dict, Any, Optional
import json 
from urllib.parse import quote_plus
import re

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI

GOOGLE_API_KEY = "AIzaSyCcY5G63Icu74LA6VivSzA7d5BBGVoe6qI"
WEATHER_API_KEY = "d045be970d974bbdb57221118252409"  # WeatherAPI configurada 
NEWS_API_KEY = "2dc2cb20fff140f1a12d7a09c09d55c6"        # NewsAPI configurada
    
# URLs base
WEATHER_BASE_URL = "http://api.weatherapi.com/v1"
NEWS_BASE_URL = "https://newsapi.org/v2"


class HerramientaClima:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = WEATHER_BASE_URL
    
    def obtener_clima_actual(self, ciudad:str) -> str:

        try:
            url = f"{self.base_url}/current.json"
            params = {
                "key": self.api_key,
                "q": ciudad,
                "lang": "es"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            # obtener info
            location = data["location"]
            current = data["current"]
            clima_info = f"""
            Clima en {location['name']}, {location["country"]}
            Temperatura: {current["temp_c"]}°C (se siente como {current["feelslike_c"]}°C)
            Condicion: {current["condition"]["text"]}
            Viento: {current["wind_kph"]} km/h
            Humedad: {current["humidity"]}%
            Visibilidad: {current["vis_km"]} km
            Ultima actualizacion: {current["last_updated"]}
            """.strip()
            return clima_info
        except Exception as e:
            return f"Error al obtener el clima: {str(e)}"


class HerramientaNoticias:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = NEWS_BASE_URL
    
    def obtener_noticias_por_tema(self, tema: str, cantidad: int = 3) -> str:
        try:
            url = f"{self.base_url}/everything"
            params = {
                "apiKey": self.api_key,
                "q": tema,
                "language": "es",
                "sortBy": "publishedAt",
                "pageSize": cantidad
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data["totalResults"] == 0:
                return f"No se encontraron noticias para el tema '{tema}'."
            
            noticias_texto = f"Ultimas noticias sobre el tema '{tema}':\n\n"

            for i, noticia in enumerate(data["articles"], 1):
                titulo = noticia["title"] or "Sin titulo"
                descripcion = noticia["description"] or "Sin descripcion"
                fuente = noticia["source"]["name"] or "Fuente desconocida"
                fecha = noticia["publishedAt"][:10] if noticia["publishedAt"] else "Fecha desconocida"

                noticias_texto += f"{i}. {titulo}\n"
                noticias_texto += f"Descripcion: {descripcion}\n"
                noticias_texto += f"Fuente: {fuente}\n"
                noticias_texto += f"Fecha: {fecha}\n\n"

                return noticias_texto.strip()
        except Exception as e:
            return f"Error al obtener las noticias: {str(e)}"

    def obtener_noticias_principales(self, pais: str = "sv", cantidad: int = 3) -> str:
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                "apiKey": self.api_key,
                "country": pais,
                "pageSize": cantidad
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data["totalResults"] == 0:
                return f"No se encontraron noticias para el pais '{pais}'."
            
            noticias_texto = f"Ultimas noticias principales para el pais '{pais.upper()}':\n\n"
            for i, noticia in enumerate(data["articles"], 1):
                titulo = noticia["title"] or "Sin titulo"
                descripcion = noticia["description"] or "Sin descripcion"
                fuente = noticia["source"]["name"] or "Fuente desconocida"
                fecha = noticia["publishedAt"]["publishedAt"][:10] if noticia["publishedAt"] else "Fecha desconocida"
                
                noticias_texto += f"{i}. {titulo}\n"
                noticias_texto += f"Descripcion: {descripcion}\n"
                noticias_texto += f"Fuente: {fuente}\n"
                noticias_texto += f"Fecha: {fecha}\n\n"
                
                return noticias_texto.strip()
        except Exception as e:
            return f"Error al obtener las noticias: {str(e)}"


class HerramientaBusquedaWeb:
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
    
    def buscar_web(self, consulta:str, cantidad:int = 3) -> str:
        try:
            params = {
                "q": consulta,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }

            response = requests.get(
                self.base_url, params=params, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            resultados_texto = f"Resultados de busqueda para '{consulta}':\n\n"

            if data.get("Answer"):
                resultados_texto += f"Respuesta directa: {data['Answer']}\n\n"
            
            if data.get("AbstractText"):
                resultados_texto += f"Resumen: {data['AbstractText']}\n\n"
                if data.get("AbstractSource"):
                    resultados_texto += f"Fuente: {data['AbstractSource']}\n\n"

            if data.get("RelatedTopics"):
                resultados_texto += "Temas relacionados:\n\n"
                for i, tema in enumerate(data["RelatedTopics"][:cantidad], 1):
                    if isinstance(tema, dict) and tema.get("Text"):
                        texto = tema["Text"][:200] + "..." if len(tema["Text"]) > 200 else tema["Text"]
                        resultados_texto += f"{i}. {texto}\n\n"
                resultados_texto += "\n"
            
            if data.get("Definition"):
                resultados_texto += f"Definicion: {data['Definition']}\n\n"
                if data.get("DefinitionSource"):
                    resultados_texto += f"Fuente: {data['DefinitionSource']}\n\n"
            
            if not any([data.get("Answer"), data.get("AbstractText"), data.get("RelatedTopics"), data.get("Definition")]):
                return self._busqueda_alternativa(consulta)

            return resultados_texto.strip()

        except Exception as e:
            return f"Error al buscar en la web: {str(e)}"
    
    def _busqueda_alternativa(self, consulta:str) -> str:
        try:
            url = "https://duckduckgo.com/html/"
            params = {
                "q": consulta
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text

                import re
                titles = re.findall(r'<a[^>]*class="result__a"[^>]*>([^<]+)</a>', content)

                if titles:
                    resultado = f"Resultados de busqueda para '{consulta}':\n\n"
                    for i, title in enumerate(titles[:3], 1):
                        resultado += f"{i}. {title}\n\n"
                    
                    return resultado.strip()

            return f"Busqueda realizada para '{consulta}'. No se encontraron resultados."
                

        except Exception as e:
            return f"Error al buscar en la web: {str(e)}"



class AgenteMultiAPI:

    def __init__(self):
        self.nombre = "Asistente Bootcamp"
        
        self.herramienta_clima = HerramientaClima(WEATHER_API_KEY)
        self.herramienta_noticias = HerramientaNoticias(NEWS_API_KEY)
        self.herramienta_busqueda = HerramientaBusquedaWeb()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key = GOOGLE_API_KEY,
            temperature=0.7

        )

        self.memoria = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.herramientas = self._crear_herramientas_langchain()

        self.agente = initialize_agent(
            tools=self.herramientas,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memoria,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=4
        )

        print(f"Agente inicializado: {self.nombre}")
        print(f"Herramientas disponibles: {self.herramientas}")
        print(f"LLM a usar: {self.llm}")

    
    def _crear_herramientas_langchain(self) -> list:
        herramientas = [
            Tool(
                name="ConsultarClima",
                func= self.herramienta_clima.obtener_clima_actual,
                description="""
                Util para obtener informacion del clima actual de cualquier ciudad.
                Input: nombre de la ciudad (ej: "Soyapango", "Managua", "New York")
                Output: informacion detallada del clima incluyendo temperatura, condiciones, viento, humedad.
                """
            ),
            Tool(
                name="BuscarNoticias",
                func= self.herramienta_noticias.obtener_noticias_por_tema,
                description="""
                Util para buscar noticias sbre un tema especifico.
                Input: tema o palabra clave (ej: "tecnologia", "politica", "deportes")
                Output: Ultimas noticias relacionadas con el tema
                """
            ),
            Tool(
                name="NoticiasPrincipales",
                func=lambda pais="sv": self.herramienta_noticias.obtener_noticias_principales(pais),
                description="""
                Util para obtener las noticias principales/destacadas de un país.
                Input: código del país (ej: "sv" para El Salvador, "us" para Estados Unidos, "mx" para Mexico)
                Output: Noticias principales/destacadas del país especificado.
                """

            ),
            Tool(
                name="BuscarWeb",
                func=self.herramienta_busqueda.buscar_web,
                description="""
                Util para buscar informacion en la web.
                Input: término o pregunta de búsqueda (ej: "Que es Machine learning?")
                Output: Resultadosd de busqueda con informacion relevante de la web.
                """
            )
        ]
        return herramientas 

    def procesar_consulta(self, consulta:str) -> str:
        
        try:
            print(f"Procesando consulta: {consulta}")
            print("========"*10)
            respuesta = self.agente.invoke(consulta)
            return respuesta
        
        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"
    
    def mostrar_capacidades_del_agente(self):
        print("Capacidades del agente:")
        print("-"*20)
        for herramienta in self.herramientas:
            print(f"Nombre: {herramienta.name}")
            print(f"Descripcion: {herramienta.description}")
            print("-"*20)
    
    def conversar(self):
        print(f"Hola!, soy {self.nombre}. ¿En que puedo ayudarte?")
        print(f"Entre mis capacidades puedo ayudarte con:")
        self.mostrar_capacidades_del_agente()
        print("\n")
        print("Comandos especiales: ")
        print("Escribe 'capacidades' para ver mis capacidades")
        print("Escribe 'salir' para terminar la conversacion")
        print("\n")
        print("="*50)

        while True:
            try:
                consulta = input("Tú: ")
                if consulta.lower() in ["exit","bye", "salir"]:
                    print("Adios, gracias por usar el asistente.")
                    break
                
                elif consulta.lower() == "capacidades":
                    self.mostrar_capacidades_del_agente()
                    continue

                elif not consulta.strip():
                    print("Por favor, escribe algo.")
                    continue

                respuesta = self.procesar_consulta(consulta)
                print(f"{self.nombre}: {respuesta}")
                print("="*50)
            
            except KeyboardInterrupt:
                print("\nAdios, gracias por usar el asistente.")
                break
            except Exception as e:
                print(f"Error: {str(e)}")


if __name__ == "__main__":
    try:
        agente = AgenteMultiAPI()
        agente.conversar()
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
                    

       