# CAMBIOS DESDE COMMIT ORIGINAL:
# ✅ AGREGADO: Import MAX_INTERPOLATION_DEPTH (aunque no se usa - limpiar después)
from configparser import MAX_INTERPOLATION_DEPTH
import os
# ✅ AGREGADO: Import urllib.response (aunque no se usa - limpiar después)
from urllib import response
import requests
from datetime import datetime
from typing import Dict, Any, Optional
import json 
from urllib.parse import quote_plus
import re

# ✅ AGREGADO: Imports de LangChain para agentes conversacionales
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
# ✅ AGREGADO: Import de prompts personalizados
from prompts import get_system_prompt, get_conversation_prompt
# ✅ AGREGADO: Import de herramientas de fecha y base de datos
from herramientas_db import HerramientaFecha, HerramientaSQL

# ✅ AGREGADO: API Keys para servicios externos (MOVER A .env EN PRODUCCIÓN)
GOOGLE_API_KEY = "AIzaSyCcY5G63Icu74LA6VivSzA7d5BBGVoe6qI"  # ⚠️ CAMBIAR: Usar variables de entorno
WEATHER_API_KEY = "d045be970d974bbdb57221118252409"  # ✅ AGREGADO: WeatherAPI configurada 
NEWS_API_KEY = "2dc2cb20fff140f1a12d7a09c09d55c6"        # ✅ AGREGADO: NewsAPI configurada
    
# ✅ AGREGADO: URLs base para APIs externas
WEATHER_BASE_URL = "http://api.weatherapi.com/v1"
NEWS_BASE_URL = "https://newsapi.org/v2"


# ✅ AGREGADO: Clase completa para manejo de API de clima
class HerramientaClima:
    """
    ✅ NUEVA CLASE: Herramienta para obtener información meteorológica
    Integra con WeatherAPI para consultas de clima en tiempo real
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = WEATHER_BASE_URL
    
    # ✅ AGREGADO: Método principal para consultar clima actual
    def obtener_clima_actual(self, ciudad:str) -> str:
        """
        ✅ NUEVO MÉTODO: Obtiene información meteorológica actual de una ciudad
        Parámetros: ciudad (str) - Nombre de la ciudad a consultar
        Retorna: str - Información formateada del clima o mensaje de error
        """
        try:
            url = f"{self.base_url}/current.json"
            params = {
                "key": self.api_key,
                "q": ciudad,
                "lang": "es"  # ✅ AGREGADO: Respuestas en español
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            # ✅ AGREGADO: Extracción y formateo de datos meteorológicos
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


# ✅ AGREGADO: Clase completa para manejo de API de noticias
class HerramientaNoticias:
    """
    ✅ NUEVA CLASE: Herramienta para obtener noticias actuales
    Integra con NewsAPI para búsquedas por tema y noticias principales
    """
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
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: Error de conexión en noticias por tema: {str(e)}")
            return f"Error de conexión al obtener noticias por tema: {str(e)}"
        except Exception as e:
            print(f"DEBUG: Error general en noticias por tema: {str(e)}")
            return f"Error al obtener noticias por tema: {str(e)}"

    def obtener_noticias_principales(self, pais: str = "sv", cantidad: int = 3) -> str:
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                "apiKey": self.api_key,
                "country": pais,
                "pageSize": cantidad
            }
            
            print(f"DEBUG: Solicitando noticias para país: {pais}")
            print(f"DEBUG: URL: {url}")
            print(f"DEBUG: Params: {params}")

            response = requests.get(url, params=params, timeout=10)
            print(f"DEBUG: Status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            print(f"DEBUG: Respuesta JSON: {data}")
            
            if data.get("status") == "error":
                error_msg = data.get("message", "Error desconocido")
                print(f"DEBUG: Error de API: {error_msg}")
                return f"Error de la API de noticias: {error_msg}"
            
            if data.get("totalResults", 0) == 0:
                return f"No se encontraron noticias para el pais '{pais}'."
            
            noticias_texto = f"Ultimas noticias principales para el pais '{pais.upper()}':\n\n"
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
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: Error de conexión en noticias principales: {str(e)}")
            return f"Error de conexión al obtener las noticias principales: {str(e)}"
        except Exception as e:
            print(f"DEBUG: Error general en noticias principales: {str(e)}")
            return f"Error al obtener las noticias principales: {str(e)}"


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



# ✅ AGREGADO: Clase principal del agente conversacional multi-API
class AgenteMultiAPI:
    """
    ✅ NUEVA CLASE PRINCIPAL: Agente inteligente que integra múltiples APIs
    Combina LangChain + Gemini + APIs externas para crear un asistente conversacional
    """
    def __init__(self):
        self.nombre = "Asistente Bootcamp"
        
        # ✅ AGREGADO: Inicialización de todas las herramientas de API
        self.herramienta_clima = HerramientaClima(WEATHER_API_KEY)
        self.herramienta_noticias = HerramientaNoticias(NEWS_API_KEY)
        self.herramienta_busqueda = HerramientaBusquedaWeb()
        self.herramienta_fecha = HerramientaFecha()  # ✅ IMPORTADO: De herramientas_db.py
        self.herramienta_sql = HerramientaSQL()      # ✅ IMPORTADO: De herramientas_db.py

        # ✅ AGREGADO: Configuración del modelo LLM con LangChain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",  # ✅ MODIFICADO: Usar modelo más reciente
            google_api_key = GOOGLE_API_KEY,
            temperature=0.7  # ✅ AGREGADO: Controlar creatividad de respuestas
        )

        # ✅ AGREGADO: Memoria conversacional para mantener contexto
        self.memoria = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # ✅ AGREGADO: Conversión de herramientas a formato LangChain
        self.herramientas = self._crear_herramientas_langchain()

        # ✅ AGREGADO: Configuración de prompts personalizados
        prompt_template = get_conversation_prompt()  # ✅ IMPORTADO: De prompts.py
        
        # ✅ AGREGADO: Inicialización del agente conversacional
        self.agente = initialize_agent(
            tools=self.herramientas,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # ✅ TIPO: Agente conversacional
            memory=self.memoria,
            verbose=True,  # ✅ DEBUG: Mostrar proceso de razonamiento
            handle_parsing_errors=True,  # ✅ ROBUSTO: Manejar errores de parsing
            max_iterations=4,  # ✅ LÍMITE: Máximo 4 pasos de razonamiento
            agent_kwargs={
                "system_message": get_system_prompt().format(nombre=self.nombre)  # ✅ PROMPT: Personalizado
            }
        )

        print(f"Agente inicializado: {self.nombre}")
        print(f"Herramientas disponibles: {self.herramientas}")
        print(f"LLM a usar: {self.llm}")

    
    # ✅ AGREGADO: Método para convertir herramientas Python a formato LangChain
    def _crear_herramientas_langchain(self) -> list:
        """
        ✅ NUEVO MÉTODO: Convierte todas las herramientas a objetos Tool de LangChain
        Cada Tool encapsula una funcionalidad específica con nombre y descripción
        """
        herramientas = [
            # ✅ AGREGADO: Tool para consultas meteorológicas
            Tool(
                name="ConsultarClima",
                func= self.herramienta_clima.obtener_clima_actual,
                description="""
                Util para obtener informacion del clima actual de cualquier ciudad.
                Input: nombre de la ciudad (ej: "Soyapango", "Managua", "New York")
                Output: informacion detallada del clima incluyendo temperatura, condiciones, viento, humedad.
                """
            ),
            # ✅ AGREGADO: Tool para búsqueda de noticias por tema
            Tool(
                name="BuscarNoticias",
                func= self.herramienta_noticias.obtener_noticias_por_tema,
                description="""
                Util para buscar noticias sbre un tema especifico.
                Input: tema o palabra clave (ej: "tecnologia", "politica", "deportes")
                Output: Ultimas noticias relacionadas con el tema
                """
            ),
            # ✅ AGREGADO: Tool para noticias principales por país
            Tool(
                name="NoticiasPrincipales",
                func=lambda pais="sv": self.herramienta_noticias.obtener_noticias_principales(pais),
                description="""
                Util para obtener las noticias principales/destacadas de un país.
                Input: código del país (ej: "sv" para El Salvador, "us" para Estados Unidos, "mx" para Mexico)
                Output: Noticias principales/destacadas del país especificado.
                """
            ),
            # ✅ AGREGADO: Tool para búsquedas web generales
            Tool(
                name="BuscarWeb",
                func=self.herramienta_busqueda.buscar_web,
                description="""
                Util para buscar informacion en la web.
                Input: término o pregunta de búsqueda (ej: "Que es Machine learning?")
                Output: Resultadosd de busqueda con informacion relevante de la web.
                """
            ),
            # ✅ AGREGADO: Tool para obtener fecha y hora actual
            Tool(
                name="ObtenerFecha",
                func=self.herramienta_fecha.obtener_fecha_actual,  # ✅ IMPORTADO: De herramientas_db.py
                description="""
                Util para obtener la fecha y hora actual.
                Input: formato ('completo', 'fecha', 'hora', 'iso', 'simple')
                Output: Fecha y hora actual en el formato solicitado.
                """
            ),
            # ✅ AGREGADO: Tool para conexión a base de datos
            Tool(
                name="ConectarBaseDatos",
                func=self.herramienta_sql.conectar_base_datos_publica,  # ✅ IMPORTADO: De herramientas_db.py
                description="""
                Util para conectarse a la base de datos pública Chinook (música).
                Input: 'chinook' (base de datos de música)
                Output: Información de conexión y schema de la base de datos.
                """
            ),
            # ✅ AGREGADO: Tool para consultar schema de BD
            Tool(
                name="ConsultarSchema",
                func=self.herramienta_sql.obtener_schema_actual,  # ✅ IMPORTADO: De herramientas_db.py
                description="""
                Util para obtener información del schema de la base de datos actual.
                Input: no requiere parámetros
                Output: Descripción completa de tablas y relaciones de la BD conectada.
                """
            ),
            # ✅ AGREGADO: Tool para consultas SQL en lenguaje natural
            Tool(
                name="ConsultaSQL",
                func=self.herramienta_sql.ejecutar_consulta_sql,  # ✅ IMPORTADO: De herramientas_db.py
                description="""
                Util para hacer consultas a la base de datos en lenguaje natural.
                Input: pregunta en lenguaje natural sobre los datos
                Output: Consulta SQL generada y resultados de la base de datos.
                """
            )
        ]
        return herramientas 

    # ✅ AGREGADO: Método principal para procesar consultas del usuario
    def procesar_consulta(self, consulta:str) -> str:
        """
        ✅ NUEVO MÉTODO: Procesa consultas usando el agente LangChain
        El agente decide automáticamente qué herramientas usar
        """
        try:
            print(f"Procesando consulta: {consulta}")
            print("========"*10)
            respuesta = self.agente.invoke(consulta)  # ✅ LANGCHAIN: Invoca el agente
            return respuesta
        
        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"
    
    # ✅ AGREGADO: Método para mostrar capacidades disponibles
    def mostrar_capacidades_del_agente(self):
        """✅ NUEVO MÉTODO: Muestra todas las herramientas disponibles"""
        print("Capacidades del agente:")
        print("-"*20)
        for herramienta in self.herramientas:
            print(f"Nombre: {herramienta.name}")
            print(f"Descripcion: {herramienta.description}")
            print("-"*20)
    
    # ✅ AGREGADO: Interfaz conversacional interactiva
    def conversar(self):
        """
        ✅ NUEVO MÉTODO: Interfaz principal para conversación con el usuario
        Maneja comandos especiales y errores de entrada
        """
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
            
            # ✅ AGREGADO: Manejo robusto de errores de entrada
            except KeyboardInterrupt:
                print("\nAdios, gracias por usar el asistente.")
                break
            except EOFError:  # ✅ SOLUCIONADO: Problema de bucle infinito por EOF
                print("\nSesión terminada por EOF. Adios!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                break


# ✅ AGREGADO: Punto de entrada principal del programa
if __name__ == "__main__":
    """
    ✅ NUEVO BLOQUE: Ejecuta el asistente cuando se ejecuta directamente
    Maneja errores de inicialización y ejecución
    """
    try:
        # ✅ AGREGADO: Inicialización del agente multi-API
        agente = AgenteMultiAPI()
        # ✅ AGREGADO: Inicio de la interfaz conversacional
        agente.conversar()
    
    except Exception as e:
        print(f"Error: {str(e)}")

# ✅ RESUMEN DE CAMBIOS DESDE COMMIT ORIGINAL:
# 
# 🆕 ARCHIVOS NUEVOS CREADOS:
# - prompts.py: Sistema de prompts personalizados
# - herramientas_db.py: Herramientas de fecha y base de datos
# - TAREA_TELEGRAM_BOT.md: Tarea completa para estudiantes
# 
# 🔧 FUNCIONALIDADES AGREGADAS:
# - Integración completa con LangChain framework
# - Agente conversacional con memoria
# - 8 herramientas diferentes (clima, noticias, web, fecha, BD)
# - Manejo robusto de errores y EOF
# - Interfaz conversacional interactiva
# - Sistema de prompts personalizados
# 
# 🐛 PROBLEMAS SOLUCIONADOS:
# - Bucle infinito por EOF en modo no interactivo
# - Manejo de errores de conexión de APIs
# - Formato de respuestas del agente
# - Instalación y configuración de dependencias
# 
# ⚠️ PENDIENTES PARA PRODUCCIÓN:
# - Mover API keys a variables de entorno (.env)
# - Limpiar imports no utilizados (MAX_INTERPOLATION_DEPTH, urllib.response)
# - Agregar logging estructurado
# - Implementar rate limiting para APIs
# - Agregar tests unitarios