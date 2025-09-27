# 🤖 Asistente Multi-API - Bootcamp KODIGO

Un asistente inteligente desarrollado con LangChain y Google Gemini que integra múltiples APIs para proporcionar información sobre clima, noticias y búsquedas web.

## 🌟 Características

- **🌤️ Consultas de Clima**: Obtén información meteorológica actual de cualquier ciudad
- **📰 Noticias por Tema**: Busca las últimas noticias sobre temas específicos
- **📺 Noticias Principales**: Consulta los titulares principales por país
- **🔍 Búsqueda Web**: Realiza búsquedas generales en internet
- **💬 Conversación Natural**: Interactúa con el asistente usando lenguaje natural
- **🧠 Memoria Conversacional**: El asistente recuerda el contexto de la conversación

## 🛠️ Tecnologías Utilizadas

- **LangChain**: Framework para aplicaciones con LLM
- **Google Gemini**: Modelo de lenguaje avanzado
- **WeatherAPI**: API para datos meteorológicos
- **NewsAPI**: API para noticias
- **DuckDuckGo**: Motor de búsqueda web
- **Python 3.11+**: Lenguaje de programación

## 📦 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd Assistants
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura las API Keys** (ya incluidas en el código para demostración):
   - Google Gemini API Key
   - WeatherAPI Key  
   - NewsAPI Key

## 🚀 Uso

### Opción 1: Interfaz Interactiva (Recomendada)
```bash
python asistente_interactivo.py
```

Esta opción te permite:
- Seleccionar funcionalidades específicas desde un menú
- Probar cada herramienta individualmente
- Conversar libremente con el asistente
- Ejecutar demos automáticos

### Opción 2: Demo Automático
```bash
python demo_test.py
```

Ejecuta pruebas automáticas de todas las funcionalidades.

### Opción 3: Conversación Directa
```bash
python demo3.py
```

Inicia una conversación directa con el asistente (modo clásico).

## 📋 Ejemplos de Uso

### Consultas de Clima
```
"¿Cómo está el clima en San Salvador?"
"Temperatura actual en Madrid"
"Clima en New York"
```

### Búsqueda de Noticias
```
"Noticias sobre tecnología"
"Últimas noticias de deportes"
"Noticias principales de El Salvador"
```

### Búsquedas Web
```
"¿Qué es la inteligencia artificial?"
"Información sobre Python programming"
"Historia de El Salvador"
```

### Conversación Natural
```
"Hola, ¿cómo estás?"
"¿Puedes ayudarme con información del clima y noticias?"
"Explícame qué puedes hacer"
```

## 📁 Estructura del Proyecto

```
Assistants/
├── demo3.py                    # Asistente principal con todas las clases
├── asistente_interactivo.py    # Interfaz interactiva mejorada
├── demo_test.py               # Script de pruebas automáticas
├── demo1.py                   # Versión básica (histórica)
├── demo2.py                   # Versión intermedia (histórica)
├── requirements.txt           # Dependencias del proyecto
├── .gitignore                # Archivos ignorados por Git
├── respuesta.txt             # Archivo de respuestas (histórico)
└── README.md                 # Este archivo
```

## 🔧 Componentes Principales

### `AgenteMultiAPI`
Clase principal que coordina todas las herramientas y el modelo de lenguaje.

### `HerramientaClima`
Integración con WeatherAPI para consultas meteorológicas.

### `HerramientaNoticias`
Integración con NewsAPI para búsqueda de noticias por tema y país.

### `HerramientaBusquedaWeb`
Integración con DuckDuckGo para búsquedas web generales.

## 🎯 Funcionalidades Destacadas

- **Procesamiento de Lenguaje Natural**: Comprende consultas en español
- **Múltiples Fuentes de Datos**: Integra APIs especializadas
- **Manejo de Errores**: Gestión robusta de errores de conexión y API
- **Interfaz Amigable**: Múltiples formas de interactuar con el asistente
- **Logging y Debug**: Información detallada para desarrollo

## 🔍 Comandos Especiales

En el modo conversación, puedes usar:
- `capacidades`: Muestra las herramientas disponibles
- `salir`, `exit`, `bye`: Termina la conversación
- `volver`, `menu`: Regresa al menú principal (en modo interactivo)

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "API Key not found"
Verifica que las API keys estén configuradas correctamente en `demo3.py`.

### Error: "Connection timeout"
Verifica tu conexión a internet y que las APIs estén disponibles.

## 📊 Estado del Proyecto

✅ **Completado**:
- Integración con múltiples APIs
- Procesamiento de lenguaje natural
- Interfaz interactiva
- Manejo de errores
- Documentación

🔄 **En Desarrollo**:
- Mejoras en la precisión de respuestas
- Nuevas fuentes de datos
- Interfaz web (futuro)

## 👨‍💻 Desarrollado para

**Bootcamp KODIGO** - Proyecto de demostración de integración de APIs con LangChain y modelos de lenguaje.

## 📝 Notas

- Las API keys incluidas son para demostración y pueden tener límites de uso
- El proyecto está optimizado para uso educativo y de demostración
- Se recomienda usar Python 3.11 o superior

---

¡Disfruta explorando las capacidades del Asistente Multi-API! 🚀
