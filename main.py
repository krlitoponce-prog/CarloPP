import sqlite3
import pandas as pd
import requests
from datetime import datetime
import time

# --- CONFIGURACIÓN Y BASE DE DATOS ---
class SistemaPrediccionFutbol:
    def __init__(self, db_name='predicciones_futbol.db'):
        self.db_name = db_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.inicializar_db()

    def inicializar_db(self):
        """Inicializa las tablas. Nota: sqlite3 no requiere instalación por pip."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabla de Equipos
        cursor.execute('CREATE TABLE IF NOT EXISTS equipos (id_equipo INTEGER PRIMARY KEY, nombre TEXT, elo_actual REAL)')

        # Tabla de Jugadores Estrella y Atributos
        cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores (
            id_jugador INTEGER PRIMARY KEY,
            nombre TEXT,
            posicion TEXT,
            score_aereo REAL,
            score_pies REAL,
            importancia_estrella REAL
        )''')

        # Tabla de Partidos con Variables de Control (Fatiga, Bajas, Cuotas)
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
            bajas_clave_local INTEGER, 
            bajas_clave_visitante INTEGER
        )''')
        
        conn.commit()
        conn.close()
        print("✅ Sistema listo: Base de Datos configurada.")

    # --- MÓDULO DE BAJAS Y LESIONES ---
    def obtener_bajas_sofascore(self, match_id):
        """
        Simula la extracción de bajas desde la API de SofaScore.
        Busca jugadores con estado 'missing' o 'doubtful'.
        """
        # En una implementación real, aquí haríamos el request a /event/{match_id}/lineups
        # Por ahora, definimos la lógica de impacto:
        print(f"🔍 Analizando bajas para el partido ID: {match_id}...")
        
        # Ejemplo de retorno de datos procesados
        bajas_detectadas = {
            'local': [{'nombre': 'Kevin De Bruyne', 'rol': 'Motor', 'impacto': 0.85}],
            'visitante': [{'nombre': 'Virgil van Dijk', 'rol': 'Muro', 'impacto': 1.20}]
        }
        return bajas_detectadas

    # --- MÓDULO DE CÁLCULO DE VALOR (VALUE BETTING) ---
    def calcular_probabilidad_ajustada(self, prob_base, bajas):
        """
        Ajusta la probabilidad de victoria según las bajas detectadas.
        """
        ajuste = 1.0
        for baja in bajas['local']:
            ajuste *= baja['impacto'] # Si es mediocentro creativo, baja la prob. de anotar
        
        return round(prob_base * ajuste, 2)

    def detectar_valor(self, prob_nuestra, cuota_casa):
        """Fórmula de Value Betting: (Prob * Cuota) - 1"""
        valor = (prob_nuestra * cuota_casa) - 1
        return round(valor * 100, 2)

    # --- MOTOR DE INGESTA (3 TEMPORADAS) ---
    def ejecutar_scraper_historico(self):
        print("🚀 Iniciando descarga de las últimas 3 temporadas de la Premier League...")
        # Aquí se integraría el loop de las temporadas 23/24, 24/25 y 25/26
        time.sleep(1)
        print("📊 Procesando 1,140 partidos potenciales...")

# --- EJECUCIÓN DEL PROTOTIPO ---
if __name__ == "__main__":
    sistema = SistemaPrediccionFutbol()
    
    # Prueba de concepto con un partido
    bajas = sistema.obtener_bajas_sofascore(match_id=12345)
    
    # Si nuestra probabilidad base era 60% (0.60)
    prob_final = sistema.calcular_probabilidad_ajustada(0.60, bajas)
    
    # Si la casa paga 1.90
    valor = sistema.detectar_valor(prob_final, 1.90)
    
    print(f"\n--- REPORTE DE PREDICCIÓN ---")
    print(f"Probabilidad Ajustada por Bajas: {prob_final * 100}%")
    print(f"Valor Estimado en la Apuesta: {valor}%")
    if valor > 0:
        print("✅ Recomendación: Apostar (Valor positivo)")
    else:
        print("❌ Recomendación: No apostar (Sin ventaja)")