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
    """Herramienta SQL mínima"""
    
    def __init__(self):
        self.db_path = None
        self.current_db = None
        
    def conectar_base_datos_publica(self) -> str:
        """Conecta a Chinook DB"""
        try:
            db_url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
            self.db_path = os.path.join(tempfile.gettempdir(), "chinook.db")
            
            if not os.path.exists(self.db_path):
                response = requests.get(db_url, timeout=30)
                with open(self.db_path, 'wb') as f:
                    f.write(response.content)
            
            self.current_db = "chinook"
            return "✅ Conectado a Chinook DB"
                   
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def ejecutar_sql_directo(self, sql: str) -> str:
        """Ejecuta SQL directamente"""
        try:
            if not self.db_path:
                return "❌ Conecta primero"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            conn.close()
            
            if resultados:
                respuesta = f"Columnas: {', '.join(columnas)}\n\n"
                for i, fila in enumerate(resultados[:10], 1):
                    respuesta += f"{i}. {' | '.join(map(str, fila))}\n"
                return respuesta
            else:
                return "Sin resultados"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def generar_sql_con_gemini(self, pregunta: str, llm) -> str:
        """Genera SQL con Gemini"""
        prompt = f"""Convierte a SQL para base Chinook:

Tablas: Artist(ArtistId,Name), Album(AlbumId,Title,ArtistId), Track(TrackId,Name,AlbumId,UnitPrice), Customer(CustomerId,FirstName,LastName,Country)

Pregunta: {pregunta}

SQL (solo la consulta, LIMIT 10):"""
        
        try:
            response = llm.invoke(prompt)
            sql = response.content.strip().replace('```sql', '').replace('```', '').strip()
            return sql
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def consulta_inteligente(self, pregunta: str, llm) -> str:
        """Consulta que genera SQL automáticamente"""
        try:
            # 1. Conectar si no está conectado
            if not self.current_db:
                self.conectar_base_datos_publica()
            
            # 2. Generar SQL
            sql = self.generar_sql_con_gemini(pregunta, llm)
            print(f"🤖 SQL generado: {sql}")
            
            # 3. Ejecutar
            resultado = self.ejecutar_sql_directo(sql)
            return resultado
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
