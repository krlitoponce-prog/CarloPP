import sqlite3
import requests
import pandas as pd
from datetime import datetime

class SistemaPrediccionFutbol:
    def __init__(self, db_name='predicciones_futbol.db'):
        self.db_name = db_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.inicializar_db()

    def inicializar_db(self):
        """Crea las tablas necesarias para el modelo avanzado."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabla de Equipos
        cursor.execute('''CREATE TABLE IF NOT EXISTS equipos 
            (id_equipo INTEGER PRIMARY KEY, nombre TEXT, ciudad TEXT, elo_actual REAL)''')

        # Tabla de Jugadores con Atributos Técnicos
        cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores (
            id_jugador INTEGER PRIMARY KEY,
            nombre TEXT,
            posicion TEXT,
            score_aereo REAL DEFAULT 5.0,
            score_pies REAL DEFAULT 5.0,
            importancia_estrella REAL DEFAULT 1.0
        )''')

        # Tabla de Partidos e Indicadores de Rendimiento
        cursor.execute('''CREATE TABLE IF NOT EXISTS partidos (
            id_partido INTEGER PRIMARY KEY,
            fecha DATE,
            local_id INTEGER,
            visitante_id INTEGER,
            goles_local INTEGER,
            goles_visitante INTEGER,
            elo_local REAL,
            elo_visitante REAL,
            cuota_local REAL,
            cuota_visitante REAL,
            descanso_local_dias INTEGER,
            descanso_visitante_dias INTEGER,
            ausencias_estrella_local INTEGER, -- Conteo de bajas clave
            ausencias_estrella_visitante INTEGER,
            FOREIGN KEY(local_id) REFERENCES equipos(id_equipo),
            FOREIGN KEY(visitante_id) REFERENCES equipos(id_equipo)
        )''')
        
        conn.commit()
        conn.close()
        print("✅ Base de Datos y Tablas preparadas.")

    def calcular_fatiga(self, equipo_id, fecha_actual):
        """Calcula los días de descanso desde el último partido en la DB."""
        conn = sqlite3.connect(self.db_name)
        query = f"""SELECT fecha FROM partidos 
                    WHERE local_id = {equipo_id} OR visitante_id = {equipo_id} 
                    ORDER BY fecha DESC LIMIT 1"""
        last_match = pd.read_sql(query, conn)
        conn.close()
        
        if not last_match.empty:
            delta = datetime.strptime(fecha_actual, '%Y-%m-%d') - datetime.strptime(last_match['fecha'][0], '%Y-%m-%d')
            return delta.days
        return 7  # Por defecto si no hay registro anterior

    def obtener_elo_historico(self, equipo_nombre, fecha):
        """Conecta con ClubElo para obtener el poder del equipo en una fecha dada."""
        # Nota: ClubElo API devuelve el Elo actual, para histórico se requiere scraping de su CSV
        url = f"http://api.clubelo.com/{equipo_nombre}"
        # Lógica simplificada para el ejemplo
        return 1500.0 

    def analizar_impacto_bajas(self, alineacion_actual, id_equipo):
        """
        Compara la alineación contra el 'Core' histórico.
        Si falta un jugador con importancia_estrella > 1.5, penaliza el rendimiento.
        """
        # Aquí iría la lógica de comparación de IDs de jugadores
        pass

# --- INSTANCIACIÓN Y PRUEBA ---
sistema = SistemaPrediccionFutbol()