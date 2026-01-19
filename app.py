import streamlit as st
import sqlite3
import pandas as pd
import requests

# Configuración de la página (Esto debe ir primero)
st.set_page_config(page_title="Predictor Premier League", page_icon="⚽")

# --- CLASE DEL SISTEMA (Tu lógica original) ---
class SistemaPrediccionFutbol:
    def __init__(self, db_name='predicciones_futbol.db'):
        self.db_name = db_name
        self.inicializar_db()

    def inicializar_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS equipos (id_equipo INTEGER PRIMARY KEY, nombre TEXT, elo_actual REAL)')
        conn.commit()
        conn.close()

# --- INTERFAZ DE STREAMLIT ---
st.title("⚽ Análisis de Bajas y Marcador Exacto")
st.write("Bienvenido al sistema de predicción basado en SofaScore y ClubElo.")

sistema = SistemaPrediccionFutbol()

# Simulación de visualización de bajas
st.header("Próximo Partido: Man City vs Liverpool")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Bajas Local (Man City)")
    st.error("❌ Kevin De Bruyne (Motor) - Impacto: -15% goles")

with col2:
    st.subheader("Bajas Visitante (Liverpool)")
    st.error("❌ Virgil van Dijk (Muro) - Impacto: +20% vulnerabilidad")

# Botón para ejecutar el modelo
if st.button('Calcular Marcador Exacto'):
    st.success("Predicción sugerida: 1 - 1 o 2 - 1")
    st.info("Valor detectado en el Empate: 7.2%")