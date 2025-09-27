"""
Herramientas para consultas SQL y manejo de fechas
"""

import sqlite3
import requests
import os
from datetime import datetime, date
from typing import Optional, Dict, Any
import tempfile

class HerramientaFecha:
    """Herramienta para obtener fecha y hora actual"""
    
    def obtener_fecha_actual(self, formato: str = "completo") -> str:
        """
        Obtiene la fecha actual en diferentes formatos
        
        Args:
            formato: 'completo', 'fecha', 'hora', 'iso'
        """
        ahora = datetime.now()
        
        formatos = {
            'completo': ahora.strftime("%A, %d de %B de %Y a las %H:%M:%S"),
            'fecha': ahora.strftime("%d/%m/%Y"),
            'hora': ahora.strftime("%H:%M:%S"),
            'iso': ahora.isoformat(),
            'simple': ahora.strftime("%Y-%m-%d %H:%M")
        }
        
        return formatos.get(formato, formatos['completo'])

class HerramientaSQL:
    """Herramienta para consultas SQL en bases de datos públicas"""
    
    def __init__(self):
        self.db_path = None
        self.schema_info = {}
        self.current_db = None
        
    def conectar_base_datos_publica(self, nombre_db: str = "chinook") -> str:
        """
        Conecta a la base de datos pública Chinook (música)
        
        Base disponible:
        - chinook: Base de datos de música (artistas, álbumes, canciones, clientes)
        """
        try:
            if nombre_db.lower() == "chinook":
                return self._conectar_chinook()
            else:
                return f"Solo está disponible la base de datos 'chinook' (música)"
                
        except Exception as e:
            return f"Error conectando a la base de datos: {str(e)}"
    
    def _conectar_chinook(self) -> str:
        """Conecta a la base de datos Chinook (música)"""
        try:
            # Descargar Chinook DB si no existe
            db_url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
            self.db_path = os.path.join(tempfile.gettempdir(), "chinook.db")
            
            if not os.path.exists(self.db_path):
                response = requests.get(db_url)
                with open(self.db_path, 'wb') as f:
                    f.write(response.content)
            
            self.current_db = "chinook"
            self.schema_info = {
                "descripcion": "Base de datos de una tienda de música digital",
                "tablas": {
                    "Artist": "Artistas musicales (ArtistId, Name)",
                    "Album": "Álbumes (AlbumId, Title, ArtistId)",
                    "Track": "Canciones (TrackId, Name, AlbumId, GenreId, Composer, UnitPrice)",
                    "Genre": "Géneros musicales (GenreId, Name)",
                    "Customer": "Clientes (CustomerId, FirstName, LastName, Email, Country)",
                    "Invoice": "Facturas (InvoiceId, CustomerId, InvoiceDate, Total)",
                    "InvoiceLine": "Líneas de factura (InvoiceLineId, InvoiceId, TrackId, Quantity)"
                },
                "relaciones": [
                    "Artist -> Album (ArtistId)",
                    "Album -> Track (AlbumId)", 
                    "Customer -> Invoice (CustomerId)",
                    "Invoice -> InvoiceLine (InvoiceId)",
                    "Track -> InvoiceLine (TrackId)"
                ]
            }
            
            return f"✅ Conectado a Chinook DB - {self.schema_info['descripcion']}\n\nTablas disponibles:\n" + \
                   "\n".join([f"- {tabla}: {desc}" for tabla, desc in self.schema_info['tablas'].items()])
                   
        except Exception as e:
            return f"Error conectando a Chinook: {str(e)}"
    
    
    def obtener_schema_actual(self) -> str:
        """Obtiene información del schema de la base actual"""
        if not self.current_db:
            return "❌ No hay base de datos conectada. Usa 'conectar_base_datos_publica' primero."
        
        info = f"📊 Schema de {self.current_db.upper()}:\n\n"
        info += f"Descripción: {self.schema_info['descripcion']}\n\n"
        info += "Tablas:\n"
        
        for tabla, desc in self.schema_info['tablas'].items():
            info += f"• {tabla}: {desc}\n"
        
        if 'relaciones' in self.schema_info:
            info += f"\nRelaciones:\n"
            for rel in self.schema_info['relaciones']:
                info += f"• {rel}\n"
        
        return info
    
    def ejecutar_consulta_sql(self, consulta_natural: str) -> str:
        """
        Traduce una consulta en lenguaje natural a SQL y la ejecuta
        
        Args:
            consulta_natural: Pregunta en lenguaje natural sobre los datos
        """
        if not self.current_db:
            return "❌ No hay base de datos conectada. Usa 'conectar_base_datos_publica' primero."
        
        try:
            # Traducir consulta natural a SQL
            sql_query = self._traducir_a_sql(consulta_natural)
            
            if sql_query.startswith("ERROR"):
                return sql_query
            
            # Ejecutar consulta
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql_query)
            
            # Obtener resultados
            resultados = cursor.fetchall()
            columnas = [description[0] for description in cursor.description]
            conn.close()
            
            # Formatear respuesta
            respuesta = f"🔍 Consulta: {consulta_natural}\n"
            respuesta += f"📝 SQL generado: {sql_query}\n\n"
            respuesta += f"📊 Resultados ({len(resultados)} filas):\n"
            
            if resultados:
                # Mostrar encabezados
                respuesta += " | ".join(columnas) + "\n"
                respuesta += "-" * (len(" | ".join(columnas))) + "\n"
                
                # Mostrar hasta 10 resultados
                for i, fila in enumerate(resultados[:10]):
                    respuesta += " | ".join([str(valor) for valor in fila]) + "\n"
                
                if len(resultados) > 10:
                    respuesta += f"\n... y {len(resultados) - 10} filas más"
            else:
                respuesta += "No se encontraron resultados."
            
            return respuesta
            
        except Exception as e:
            return f"❌ Error ejecutando consulta: {str(e)}"
    
    def _traducir_a_sql(self, consulta_natural: str) -> str:
        """Traduce consulta natural a SQL para Chinook"""
        consulta = consulta_natural.lower()
        
        if self.current_db == "chinook":
            return self._traducir_chinook(consulta)
        else:
            return "ERROR: Solo se soporta la base de datos Chinook"
    
    def _traducir_chinook(self, consulta: str) -> str:
        """Traduce consultas para Chinook DB"""
        
        # Patrones comunes para Chinook
        if any(word in consulta for word in ['artista', 'artist', 'banda']):
            if any(word in consulta for word in ['cuantos', 'cantidad', 'numero']):
                return "SELECT COUNT(*) as total_artistas FROM Artist"
            else:
                return "SELECT Name FROM Artist LIMIT 10"
        
        elif any(word in consulta for word in ['album', 'disco']):
            if any(word in consulta for word in ['cuantos', 'cantidad']):
                return "SELECT COUNT(*) as total_albums FROM Album"
            else:
                return "SELECT a.Title, ar.Name as Artista FROM Album a JOIN Artist ar ON a.ArtistId = ar.ArtistId LIMIT 10"
        
        elif any(word in consulta for word in ['cancion', 'track', 'tema']):
            if 'precio' in consulta or 'caro' in consulta:
                return "SELECT Name, UnitPrice FROM Track ORDER BY UnitPrice DESC LIMIT 10"
            else:
                return "SELECT Name FROM Track LIMIT 10"
        
        elif any(word in consulta for word in ['cliente', 'customer']):
            if 'pais' in consulta or 'country' in consulta:
                return "SELECT Country, COUNT(*) as clientes FROM Customer GROUP BY Country ORDER BY clientes DESC"
            else:
                return "SELECT FirstName, LastName, Email FROM Customer LIMIT 10"
        
        elif any(word in consulta for word in ['venta', 'factura', 'invoice']):
            return "SELECT InvoiceDate, Total FROM Invoice ORDER BY Total DESC LIMIT 10"
        
        else:
            return "SELECT 'Consulta no reconocida. Intenta preguntar sobre: artistas, álbumes, canciones, clientes o ventas' as mensaje"
    
