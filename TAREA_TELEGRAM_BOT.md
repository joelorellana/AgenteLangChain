# 🤖 TAREA: Bot de Telegram con Gemini AI

**Bootcamp KODIGO - Despliegue de un proyecto de IA**

---

## 📋 **INFORMACIÓN GENERAL**

- **Duración**: 1 semana (7 días)
- **Fecha límite**: Próximo sábado
- **Modalidad**: Individual o parejas (máximo 2 personas)
- **Calificación**: Base 100 puntos
- **Defensa**: Sábado en clase

---

## 🎯 **OBJETIVO**

Crear un bot de Telegram que integre **Google Gemini AI** para responder preguntas de manera inteligente, incluyendo información de clima y funcionalidades adicionales. El enfoque está en el **desarrollo funcional** y **demostración en vivo**.

---

## 📦 **ENTREGABLES**

1. **Repositorio de GitHub** con código completo y documentación
2. **Bot de Telegram funcionando** (enlace @tu_bot)
3. **README.md** con instrucciones de instalación y uso
4. **Video demo** (2-3 minutos) mostrando funcionalidades

---

## ⭐ **FUNCIONALIDADES MÍNIMAS (OBLIGATORIAS)**

### **Nivel Básico - 70 puntos**

1. **Bot funcional en Telegram** (15 pts)
   - Responde a mensajes básicos
   - Comando `/start` con mensaje de bienvenida
   - Comando `/help` con lista de funcionalidades

2. **Integración con LangChain + Gemini AI** (25 pts)
   - **OBLIGATORIO**: Usar LangChain framework
   - Integración con ChatGoogleGenerativeAI
   - Configuración correcta de API keys
   - Manejo de conversaciones naturales

3. **Funcionalidades básicas** (20 pts)
   - Comando `/fecha` - Fecha y hora actual
   - Comando `/clima [ciudad]` - Información meteorológica
   - Al menos 1 comando personalizado adicional

4. **Bot funcionando localmente** (10 pts)
   - Bot ejecutándose correctamente en desarrollo
   - Variables de entorno configuradas
   - Todas las funcionalidades operativas

### **Nivel Intermedio - 85 puntos**

5. **LangChain Tools** (15 pts adicionales)
   - **OBLIGATORIO**: Crear AL MENOS 2 LangChain Tools personalizadas
   - Usar `Tool` class de LangChain para encapsular funcionalidades
   - Ejemplos: WeatherTool, DatabaseTool, NewsTool, CalculatorTool
   - **Creatividad**: Pueden crear tools originales

### **Nivel Avanzado - 100 puntos**

6. **LangChain Agents** (15 pts adicionales)
   - **OBLIGATORIO**: Implementar un agente LangChain
   - Usar `initialize_agent` o crear agente personalizado
   - El agente debe decidir automáticamente qué tool usar
   - Memoria conversacional opcional
   - **Creatividad**: Agentes especializados (ej: MusicAgent, WeatherAgent)

### **Funcionalidades Opcionales (Puntos Extra)**

7. **Deployment en la nube** (+10 pts bonus)
   - Bot funcionando 24/7 en Render o similar
   - Variables de entorno en producción
   - **OPCIONAL** - Solo para estudiantes que quieran destacar

---

## 🛠️ **TECNOLOGÍAS A UTILIZAR**

### **Obligatorias:**
- **Python 3.9+**
- **python-telegram-bot** library
- **LangChain** framework (OBLIGATORIO)
- **langchain-google-genai** para Gemini
- **Google Gemini API** (gratuita)
- **Git/GitHub**

### **Opcionales:**
- **SQLite** para base de datos
- **Requests** para APIs externas
- **python-dotenv** para variables de entorno
- **Render/Railway** para deployment (bonus)

---

## 📚 **RECURSOS DE ESTUDIO**

### **📖 Tutoriales Obligatorios:**

1. **Crear Bot de Telegram:**
   - [FreeCodeCamp - Telegram Bot Python](https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/)
   - [Documentación oficial python-telegram-bot](https://docs.python-telegram-bot.org/)

2. **Google Gemini API:**
   - [Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/quickstart)
   - [LangChain + Gemini Integration](https://python.langchain.com/docs/integrations/chat/google_generative_ai/)

3. **Deployment (OPCIONAL):**
   - [Render Deployment Guide](https://render.com/docs/deploy-python-app) (GRATIS)
   - [PythonAnywhere Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/) (GRATIS)
   - [Heroku Python Deploy](https://devcenter.heroku.com/articles/getting-started-with-python) (GRATIS con limitaciones)

### **🎥 Videos Recomendados:**
- Buscar en YouTube: "Python Telegram Bot Tutorial 2024"
- "Google Gemini API Python Integration"
- "Deploy Python Bot Railway"

### **📋 Documentación Oficial:**
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather Commands](https://core.telegram.org/bots#botfather)
- [Railway Documentation](https://docs.railway.com/)

---

## 🚀 **GUÍA PASO A PASO DETALLADA**

### **Día 1: Setup y Configuración Inicial**

#### **🤖 1. Crear el bot en Telegram (30 min):**
   **Pasos detallados:**
   1. Abrir Telegram y buscar `@BotFather`
   2. Iniciar conversación con `/start`
   3. Enviar `/newbot` y seguir el diálogo:
      - Elegir nombre del bot (ej: "Mi Bot Inteligente")
      - Elegir username único (debe terminar en 'bot', ej: `mibot_kodigo_bot`)
   4. **IMPORTANTE**: Copiar y guardar el TOKEN inmediatamente
   5. **Opcional**: Configurar descripción con `/setdescription`
   6. **Opcional**: Agregar foto con `/setuserpic`

#### **💻 2. Configurar entorno de desarrollo (45 min):**
   **Estructura recomendada:**
   ```bash
   mkdir telegram_bot_proyecto
   cd telegram_bot_proyecto
   
   # Crear entorno virtual
   python -m venv bot_env
   source bot_env/bin/activate  # Linux/Mac
   # bot_env\Scripts\activate   # Windows
   
   # Instalar dependencias básicas
   pip install python-telegram-bot==20.7
   pip install google-generativeai
   pip install python-dotenv
   pip install requests  # Para APIs externas
   ```

   **Crear estructura de archivos:**
   ```
   telegram_bot_proyecto/
   ├── .env                 # Variables secretas (NO subir a GitHub)
   ├── .gitignore          # Ignorar archivos sensibles
   ├── bot.py              # Archivo principal
   ├── config.py           # Configuraciones
   ├── handlers/           # Carpeta para manejadores
   │   ├── __init__.py
   │   ├── commands.py     # Comandos del bot
   │   └── messages.py     # Manejo de mensajes
   ├── utils/              # Utilidades
   │   ├── __init__.py
   │   └── gemini_client.py # Cliente de Gemini
   ├── requirements.txt    # Lista de dependencias
   └── README.md          # Documentación
   ```

#### **🔑 3. Obtener y configurar API Keys (30 min):**
   **Gemini API:**
   1. Ir a [Google AI Studio](https://ai.google.dev/)
   2. Hacer clic en "Get API Key"
   3. Crear nuevo proyecto o usar existente
   4. Generar API Key y copiarla
   5. **NUNCA** compartir esta key públicamente

   **Crear archivo .env:**
   ```env
   TELEGRAM_BOT_TOKEN=tu_token_aqui
   GEMINI_API_KEY=tu_gemini_key_aqui
   WEATHER_API_KEY=tu_weather_key_aqui  # Opcional
   ```

   **Crear .gitignore:**
   ```gitignore
   .env
   __pycache__/
   *.pyc
   bot_env/
   .DS_Store
   ```

### **Día 2: Primer Bot Funcional**

#### **🔧 4. Crear bot básico (2 horas):**
   **Conceptos clave a entender:**
   - **Handlers**: Funciones que manejan diferentes tipos de mensajes
   - **Update**: Objeto que contiene información del mensaje recibido
   - **Context**: Información adicional y herramientas del bot
   - **Filters**: Para filtrar tipos específicos de mensajes

   **Pasos para el primer bot:**
   1. **Crear config.py** para centralizar configuraciones
   2. **Crear bot.py** con estructura básica
   3. **Implementar comando /start** (mensaje de bienvenida)
   4. **Implementar manejo básico de mensajes** (eco simple)
   5. **Probar localmente** antes de continuar

   **Estructura de un handler típico:**
   ```python
   async def mi_comando(update: Update, context):
       # 1. Obtener información del usuario/mensaje
       # 2. Procesar la información
       # 3. Generar respuesta
       # 4. Enviar respuesta al usuario
   ```

#### **🧪 5. Pruebas iniciales (30 min):**
   **Checklist de pruebas:**
   - [ ] Bot responde al comando `/start`
   - [ ] Bot responde a mensajes de texto
   - [ ] No hay errores en la consola
   - [ ] Variables de entorno se cargan correctamente
   - [ ] Bot aparece "online" en Telegram

### **Día 3: Integración con Gemini AI**

#### **🤖 6. Integrar LangChain + Gemini (2 horas):**
   **Pasos detallados:**
   1. **Instalar LangChain**: `pip install langchain langchain-google-genai`
   2. **Crear ChatGoogleGenerativeAI** instance
   3. **Configurar modelo Gemini** con LangChain
   4. **Implementar conversación básica** usando LangChain
   5. **Manejar errores** de API y límites

   **Código base sugerido:**
   ```python
   from langchain_google_genai import ChatGoogleGenerativeAI
   
   llm = ChatGoogleGenerativeAI(
       model="gemini-pro",
       google_api_key=GEMINI_API_KEY
   )
   ```

   **Consideraciones importantes:**
   - LangChain maneja automáticamente muchos errores
   - Usar `invoke()` method para consultas
   - Preparar para agregar Tools después

#### **💬 7. Mejorar conversaciones (1 hora):**
   **Funcionalidades a implementar:**
   - **Indicador de "escribiendo"** mientras procesa
   - **Manejo de mensajes largos** (dividir respuestas)
   - **Comandos de ayuda** (/help con lista de funciones)
   - **Mensajes de error amigables** cuando algo falla

### **Día 4: Comandos Específicos**

#### **📅 8. Comando /fecha (45 min):**
   **Requerimientos:**
   - Mostrar fecha y hora actual
   - Formato legible en español
   - Incluir zona horaria
   - Opcional: diferentes formatos (/fecha corta, /fecha completa)

   **Pistas de implementación:**
   - Usar módulo `datetime` de Python
   - Considerar zona horaria del usuario
   - Formatear respuesta de manera atractiva

#### **🌤️ 9. Comando /clima (1.5 horas):**
   **Requerimientos:**
   - Obtener clima de cualquier ciudad
   - Mostrar temperatura, descripción, humedad
   - Manejar ciudades no encontradas
   - Formato: `/clima San Salvador`

   **APIs recomendadas (gratuitas):**
   - OpenWeatherMap (5 días gratis)
   - WeatherAPI (1M requests/mes gratis)
   - AccuWeather (50 calls/día gratis)

   **Pasos de implementación:**
   1. Registrarse en la API elegida
   2. Crear función para hacer requests
   3. Parsear respuesta JSON
   4. Formatear información para el usuario
   5. Manejar errores (ciudad no encontrada, API caída)

#### **🛠️ 10. Crear LangChain Tools (Nivel Intermedio - 2 horas):**
   **Requerimientos:**
   - **Crear AL MENOS 2 Tools personalizadas**
   - Usar `Tool` class de LangChain
   - Encapsular funcionalidades en tools reutilizables
   - **Ser creativos** - No copiar las de clase

   **Ejemplos de Tools creativas:**
   ```python
   from langchain.tools import Tool
   
   def weather_function(city: str) -> str:
       # Tu lógica de clima aquí
       return f"Clima de {city}: ..."
   
   weather_tool = Tool(
       name="WeatherTool",
       description="Obtiene clima de una ciudad",
       func=weather_function
   )
   ```

   **Ideas de Tools originales:**
   - CalculatorTool, TranslatorTool, JokeTool
   - DatabaseTool, QRCodeTool, PasswordTool
   - CurrencyTool, RandomFactTool, etc.

### **Día 5: LangChain Agents (Nivel Avanzado)**

#### **🤖 11. Implementar LangChain Agent (2.5 horas):**
   **Requerimientos:**
   - **Crear un agente** que use las Tools automáticamente
   - El usuario NO especifica qué tool usar
   - El agente **decide inteligentemente** basándose en la consulta
   - Usar `initialize_agent` o crear agente personalizado

   **Código base sugerido:**
   ```python
   from langchain.agents import initialize_agent, AgentType
   
   agent = initialize_agent(
       tools=[weather_tool, calculator_tool, ...],
       llm=llm,
       agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
       verbose=True
   )
   ```

   **Ejemplos de funcionamiento:**
   - Usuario: "¿Qué temperatura hace en Madrid?"
   - Agente: Decide usar WeatherTool automáticamente
   - Usuario: "¿Cuánto es 25 * 8?"
   - Agente: Decide usar CalculatorTool automáticamente

#### **🧠 12. Memoria Conversacional (1 hora) - OPCIONAL:**
   **Conceptos:**
   - El agente recuerda conversaciones anteriores
   - Usar `ConversationBufferMemory`
   - Contexto persistente por usuario

### **Día 6: Finalización y Documentación**

#### **🚀 14. Preparar para presentación (2 horas):**
   **Checklist final:**
   - [ ] Crear `requirements.txt` completo
   - [ ] Probar todas las funcionalidades localmente
   - [ ] Implementar manejo robusto de errores
   - [ ] Verificar que el bot funciona sin problemas
   - [ ] Preparar datos de prueba para la demo

   **Archivo requirements.txt sugerido:**
   ```txt
   python-telegram-bot==20.7
   google-generativeai>=0.3.0
   python-dotenv>=1.0.0
   requests>=2.28.0
   sqlite3  # Si usas base de datos
   ```

#### **☁️ 15. Deployment (OPCIONAL - Puntos Bonus):**
   **Solo para estudiantes que quieran evitar la ultima tarea:**
   1. **Crear cuenta en Render.com** (gratis)
   2. **Conectar repositorio GitHub** 
   3. **Configurar Web Service:**
      - Build Command: `pip install -r requirements.txt`
      - Start Command: `python bot.py`
   4. **Configurar variables de entorno** en el dashboard
   5. **Hacer deploy** y verificar funcionamiento 24/7

   **Nota**: El deployment NO es obligatorio para aprobar

#### **📋 16. Documentación completa (1.5 horas):**
   **README.md debe incluir:**
   - Descripción del proyecto
   - Lista de funcionalidades
   - Instrucciones de instalación local
   - Comandos disponibles con ejemplos
   - Screenshots del bot funcionando
   - Información sobre APIs utilizadas
   - Créditos y contacto

### **Día 7: Preparación para Defensa/Exposición**

#### **🧪 17. Testing exhaustivo (1.5 horas):**
   **Checklist de pruebas para la exposición:**
   - [ ] Todos los comandos funcionan correctamente
   - [ ] Manejo de errores es robusto
   - [ ] Bot responde en tiempo razonable
   - [ ] Variables de entorno están configuradas
   - [ ] Documentación está actualizada
   - [ ] **CRÍTICO**: Bot funciona en tu laptop para la demo

#### **🎥 18. Crear video demo (1 hora):**
   **Contenido sugerido (2-3 minutos):**
   - Mostrar bot funcionando en Telegram
   - Demostrar cada comando principal
   - Explicar brevemente la arquitectura
   - Mostrar código más interesante
   - Mencionar desafíos superados

#### **🎯 19. Preparar defensa/exposición (1 hora):**
   **La defensa será EN VIVO con pruebas reales:**
   
   **Formato de la exposición:**
   - **5 minutos**: Explicación del proyecto y arquitectura
   - **5 minutos**: **DEMO EN VIVO** - Probar bot funcionando
   - **2 minutos**: Preguntas del profesor
   
   **Checklist para la defensa:**
   - [ ] Laptop con bot funcionando localmente
   - [ ] Telegram abierto y bot activo
   - [ ] Comandos de prueba preparados
   - [ ] Código abierto para mostrar
   - [ ] Explicación clara de funcionalidades
   
   **Comandos de prueba sugeridos:**
   ```
   /start
   /help
   /fecha
   /clima San Salvador
   Hola, ¿cómo estás? (conversación con Gemini)
   /musica cuántos artistas hay (si implementaste BD)
   ```
   
   **⚠️ IMPORTANTE**: El bot DEBE funcionar durante la exposición

---

## 📊 **CRITERIOS DE EVALUACIÓN**

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| **Funcionalidad Básica** | 30 | Bot responde, comandos básicos funcionan |
| **Integración Gemini** | 25 | IA responde correctamente, maneja conversaciones |
| **Código y Estructura** | 20 | Código limpio, comentado, bien organizado |
| **Demo en Vivo** | 15 | Bot funciona correctamente durante la exposición |
| **Documentación** | 10 | README claro, instrucciones completas |
| **Funcionalidades Extra** | +15 | Base de datos, comandos avanzados, creatividad |
| **Deployment (Bonus)** | +10 | Bot funcionando en la nube 24/7 |

---

## 🎯 **EJEMPLOS DE INTERACCIÓN**

```
Usuario: /start
Bot: ¡Hola! Soy tu asistente con IA. Puedo ayudarte con:
- Conversaciones inteligentes
- Información del clima
- Consultas de música
- Y mucho más. Escribe /help para ver todos los comandos.

Usuario: ¿Qué tiempo hace en San Salvador?
Bot: 🌤️ El clima en San Salvador es:
Temperatura: 28°C (se siente como 31°C)
Condición: Parcialmente nublado
Viento: 15 km/h
Humedad: 65%

Usuario: /musica cuántos artistas hay
Bot: 🎵 Consultando base de datos...
Hay 275 artistas en total en la base de datos de música.

Usuario: Explícame qué es la inteligencia artificial
Bot: 🤖 La inteligencia artificial (IA) es una rama de la informática...
[Respuesta detallada de Gemini]
```

---

## 🚨 **CONSIDERACIONES IMPORTANTES**

### **⚠️ Seguridad:**
- **NUNCA** subir API keys al repositorio
- Usar variables de entorno (.env)
- Agregar `.env` al `.gitignore`

### **💰 Costos:**
- **Gemini API**: Gratis hasta 15 requests/min
- **Render**: 750 horas gratis/mes (permanente)
- **WeatherAPI**: 1M requests gratis/mes
- **⚠️ Railway**: Solo $5 trial por 30 días, luego pago

### **🐛 Debugging:**
- Probar localmente antes de desplegar
- Usar logs para identificar errores
- Telegram tiene límites de rate (30 msg/segundo)

---

## 🏆 **IDEAS PARA DESTACAR**

### **🛠️ LangChain Tools Creativas:**
- **🧮 CalculatorTool**: Operaciones matemáticas complejas
- **🌍 TranslatorTool**: Traducir texto entre idiomas
- **🎲 RandomTool**: Dados, números aleatorios, decisiones
- **💱 CurrencyTool**: Conversión de monedas en tiempo real
- **🔐 PasswordTool**: Generar contraseñas seguras
- **📊 StatsTool**: Estadísticas de uso del bot
- **🎭 JokeTool**: Chistes y humor
- **📝 SummaryTool**: Resumir textos largos
- **🔍 SearchTool**: Búsquedas específicas
- **⏰ ReminderTool**: Recordatorios y alarmas

### **🤖 Agentes Especializados:**
- **WeatherAgent**: Especializado en clima y meteorología
- **MathAgent**: Resuelve problemas matemáticos complejos
- **NewsAgent**: Analiza y resume noticias
- **TravelAgent**: Información de viajes y turismo
- **StudyAgent**: Ayuda con tareas educativas

### **🎯 Funcionalidades Técnicas Avanzadas:**
- Memoria conversacional persistente
- Manejo de múltiples usuarios simultáneos
- Logs estructurados con timestamps
- Rate limiting personalizado
- Respuestas con formato Markdown
- Botones interactivos de Telegram

---

## 📞 **SOPORTE Y AYUDA**

### **Recursos de Ayuda:**
- **Documentación oficial** de cada tecnología
- **Stack Overflow** para problemas específicos
- **GitHub Issues** de las librerías
- **Discord/Telegram** de desarrolladores

### **🔧 Troubleshooting Detallado:**

#### **Bot no responde:**
- **Síntoma**: Bot aparece offline o no contesta mensajes
- **Posibles causas**:
  - Token incorrecto o mal configurado
  - Bot no está ejecutándose
  - Errores en el código que causan crash
- **Soluciones**:
  1. Verificar token con @BotFather (`/token`)
  2. Revisar logs de consola para errores
  3. Probar con bot mínimo primero
  4. Verificar que variables de entorno se cargan

#### **Gemini API no funciona:**
- **Síntoma**: Errores al generar respuestas con IA
- **Posibles causas**:
  - API key inválida o expirada
  - Límites de rate exceeded (15 req/min)
  - Mensajes muy largos
- **Soluciones**:
  1. Verificar API key en Google AI Studio
  2. Implementar retry con backoff
  3. Limitar longitud de mensajes
  4. Agregar manejo de excepciones específicas

#### **Deploy falla en Render:**
- **Síntoma**: Build fails o servicio no inicia
- **Posibles causas**:
  - requirements.txt incompleto
  - Variables de entorno faltantes
  - Comando de inicio incorrecto
- **Soluciones**:
  1. Verificar que requirements.txt incluye todas las dependencias
  2. Configurar variables de entorno en dashboard
  3. Usar `python bot.py` como start command
  4. Revisar build logs para errores específicos

#### **Errores de permisos/importación:**
- **Síntoma**: ModuleNotFoundError o ImportError
- **Posibles causas**:
  - Entorno virtual no activado
  - Dependencias no instaladas
  - Rutas de archivos incorrectas
- **Soluciones**:
  1. Activar entorno virtual antes de ejecutar
  2. Reinstalar dependencias: `pip install -r requirements.txt`
  3. Verificar estructura de carpetas
  4. Usar imports relativos correctamente

#### **Bot responde lento:**
- **Síntoma**: Demora excesiva en respuestas
- **Posibles causas**:
  - APIs externas lentas
  - Consultas SQL complejas
  - Falta de indicadores de "typing"
- **Soluciones**:
  1. Agregar `await context.bot.send_chat_action(chat_id, "typing")`
  2. Implementar timeouts en requests
  3. Optimizar consultas de base de datos
  4. Usar async/await correctamente

---

## 📅 **CRONOGRAMA SUGERIDO**

| Día | Actividades |
|-----|-------------|
| **Lunes** | Setup inicial, crear bot, configurar entorno |
| **Martes** | Integración básica con Gemini, comandos simples |
| **Miércoles** | Funcionalidades adicionales (clima, fecha) |
| **Jueves** | Base de datos y consultas avanzadas |
| **Viernes** | Funcionalidades avanzadas y testing |
| **Sábado** | Documentación, video demo, preparar exposición |

---

## 🎓 **DEFENSA/EXPOSICIÓN DE LA TAREA**

### **📅 Fecha**: Próximo sábado en clase
### **⏰ Formato**: 12 minutos por estudiante/equipo

### **🎯 Estructura de la Exposición:**

#### **Parte 1: Explicación (5 minutos)**
- **Descripción del proyecto** y funcionalidades implementadas
- **Arquitectura técnica** y decisiones de diseño
- **APIs utilizadas** y su integración
- **Desafíos superados** durante el desarrollo

#### **Parte 2: DEMO EN VIVO (5 minutos) - OBLIGATORIO**
- **⚠️ CRÍTICO**: El bot DEBE funcionar durante la presentación
- **Ejecutar bot localmente** en tu laptop
- **Demostrar comandos** en tiempo real:
  - `/start` y `/help`
  - `/fecha` 
  - `/clima [ciudad]`
  - Conversación con Gemini
  - Funcionalidades adicionales implementadas
- **Mostrar código** de las partes más importantes

#### **Parte 3: Preguntas (2 minutos)**
- Preguntas técnicas del profesor
- Explicación de decisiones de implementación
- Posibles mejoras futuras

### **📋 Checklist para la Exposición:**
- [ ] **Laptop con bot funcionando** (fundamental)
- [ ] **Telegram abierto** y bot activo
- [ ] **Variables de entorno** configuradas
- [ ] **Código fuente** accesible para mostrar
- [ ] **README.md** completo en GitHub
- [ ] **Video demo** subido (como respaldo)
- [ ] **Comandos de prueba** preparados y probados

### **⚠️ ADVERTENCIAS IMPORTANTES:**
- **Si el bot no funciona durante la exposición, la calificación será significativamente menor**
- **Probar TODO antes de la presentación**
- **Tener plan B**: Video demo como respaldo
- **Internet estable**: Verificar conexión antes de presentar

### **🏆 Aspectos a Evaluar:**
- **Funcionamiento en vivo** (15 pts) - El más importante
- **Comprensión técnica** demostrada
- **Calidad del código** mostrado
- **Creatividad** en las funcionalidades
- **Capacidad de explicación** clara

---

## 🌟 **¡ÉXITO EN TU PROYECTO!**

Recuerda que esta tarea te permitirá:
- ✅ Integrar múltiples APIs reales
- ✅ Trabajar con IA de última generación
- ✅ Desplegar aplicaciones en la nube
- ✅ Crear un proyecto para tu portafolio
- ✅ Aprender tecnologías demandadas en la industria

**¡Diviértete programando y crea algo increíble!** 🚀

---

*Bootcamp KODIGO - Formando desarrolladores del futuro* 💻
