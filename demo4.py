"""
Demo4: Agente mínimo importando tools de demo3
"""

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from herramientas_db import HerramientaSQL, HerramientaFecha
from prompts import get_system_prompt, get_conversation_prompt
from demo3 import HerramientaClima, HerramientaNoticias, HerramientaBusquedaWeb, GOOGLE_API_KEY, WEATHER_API_KEY, NEWS_API_KEY

class AgenteMinimo:
    """Agente completo con todas las herramientas"""
    
    def __init__(self):
        self.nombre = "Asistente Demo4"
        
        # LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3
        )
        
        # Memoria conversacional
        self.memoria = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Herramientas
        self.sql_tool = HerramientaSQL()
        self.fecha_tool = HerramientaFecha()
        self.clima_tool = HerramientaClima(WEATHER_API_KEY)
        self.noticias_tool = HerramientaNoticias(NEWS_API_KEY)
        self.busqueda_tool = HerramientaBusquedaWeb()
        
        # Tools para LangChain
        tools = [
            Tool(
                name="ConectarDB",
                func=self.sql_tool.conectar_base_datos_publica,
                description="Conecta a base de datos Chinook (música)"
            ),
            Tool(
                name="EjecutarSQL",
                func=self.sql_tool.ejecutar_sql_directo,
                description="Ejecuta consulta SQL directa en la base de datos"
            ),
            Tool(
                name="ObtenerFecha",
                func=self.fecha_tool.obtener_fecha_actual,
                description="Obtiene fecha y hora actual"
            ),
            Tool(
                name="ConsultarClima",
                func=self.clima_tool.obtener_clima_actual,
                description="Obtiene clima actual de cualquier ciudad"
            ),
            Tool(
                name="BuscarNoticias",
                func=self.noticias_tool.obtener_noticias_por_tema,
                description="Busca noticias sobre un tema específico"
            ),
            Tool(
                name="BuscarWeb",
                func=self.busqueda_tool.buscar_web,
                description="Busca información en la web"
            )
        ]
        
        # Agente con memoria y prompts personalizados
        self.agente = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memoria,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors="Check your output and make sure it conforms to the expected format!",
            early_stopping_method="generate",
            agent_kwargs={
                "system_message": get_system_prompt().format(nombre=self.nombre)
            }
        )
    
    
    def chat(self):
        """Chat completo con todas las herramientas"""
        print(f"🤖 {self.nombre} - Agente Multi-API")
        print("Puedo ayudarte con: clima, noticias, búsquedas web, consultas SQL, fechas")
        print("Comandos especiales: 'sql [pregunta]', 'salir'")
        print("-" * 50)
        
        while True:
            try:
                entrada = input("Tú: ").strip()
                
                if entrada.lower() == 'salir':
                    print("¡Hasta luego!")
                    break
                elif entrada.lower().startswith('sql '):
                    # Consulta SQL directa
                    pregunta = entrada[4:]
                    resultado = self.sql_tool.consulta_inteligente(pregunta, self.llm)
                    print(f"{self.nombre}: {resultado}")
                else:
                    # Usar agente completo con todas las herramientas
                    respuesta = self.agente.invoke(entrada)
                    print(f"{self.nombre}: {respuesta['output']}")
                    
                print("-" * 50)
                    
            except KeyboardInterrupt:
                print("\n¡Hasta luego!")
                break
            except EOFError:
                print("\nSesión terminada. ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import os
    agente = AgenteMinimo()
    agente.chat()
