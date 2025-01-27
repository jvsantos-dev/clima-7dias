import json
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple

# Função para carregar os dados da API da cidade
@st.cache_data
def carregar_dados(cidade: str) -> Tuple[float, float, dict]:
    """Carrega os dados da API OpenWeather para obter a latitude, longitude e outros detalhes da cidade."""
    api_key = "91cac1b28f06467fcf5687839e0cdc69"  # Substitua pela sua chave de API
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br"
    api = requests.get(link)
    api_dic = api.json()

    # Verificando se a cidade foi encontrada e extraindo a latitude e longitude
    if api_dic.get('cod') == 200:
        latitude = api_dic['coord']['lat']
        longitude = api_dic['coord']['lon']
        return latitude, longitude, api_dic  # Retorna também os dados completos
    else:
        st.error(f"Cidade não encontrada ou erro na requisição: {api_dic.get('message')}")
        return None, None, None

# Função para formatar os dados da previsão atual
def formatar_dados_climaticos(api_dic: dict) -> dict:
    """Extrai e formata os dados climáticos atuais."""
    try:
        temp_atual = api_dic['main']['temp'] - 273.15  # Temperatura em Celsius
        temp_max = api_dic['main']['temp_max'] - 273.15  # Temperatura máxima em Celsius
        temp_min = api_dic['main']['temp_min'] - 273.15  # Temperatura mínima em Celsius
        sensacao = api_dic['main']['feels_like'] - 273.15  # Sensação térmica em Celsius
        umidade = api_dic['main']['humidity']  # Umidade
        vento_speed = api_dic['wind']['speed']  # Velocidade do vento
        vento_deg = api_dic['wind']['deg']  # Direção do vento
        clima = api_dic['weather'][0]['description']  # Condição climática

        # Formatação dos dados em um dicionário
        dados_climaticos = {
            'Temperatura Atual (°C)': round(temp_atual, 2),
            'Temperatura Máxima (°C)': round(temp_max, 2),
            'Temperatura Mínima (°C)': round(temp_min, 2),
            'Sensação Térmica (°C)': round(sensacao, 2),
            'Umidade (%)': umidade,
            'Velocidade do Vento (m/s)': vento_speed,
            'Direção do Vento (°)': vento_deg,
            'Condição Climática': clima.capitalize(),
        }

        return dados_climaticos
    except KeyError as e:
        st.error(f"Erro ao acessar os dados: {e}")
        return {}

# Função para criar gráficos com os dados climáticos
def graficos(dados: dict) -> None:
    """Cria gráficos com os dados climáticos atuais."""
    try:
        # Gráfico de temperaturas
        fig_temp, ax_temp = plt.subplots()
        ax_temp.bar(['Atual', 'Máxima', 'Mínima'],
                    [dados['Temperatura Atual (°C)'], dados['Temperatura Máxima (°C)'], dados['Temperatura Mínima (°C)']],
                    color=['red', 'orange', 'blue'])
        ax_temp.set_title('Temperaturas (°C)')
        ax_temp.set_ylabel('Temperatura')
        ax_temp.grid(True)
        st.pyplot(fig_temp)

        # Gráficos de umidade e vento
        fig_uv, (ax_umid, ax_vento) = plt.subplots(1, 2, figsize=(10, 4))

        ax_umid.bar(['Umidade'], [dados['Umidade (%)']], color='green')
        ax_umid.set_title('Umidade (%)')
        ax_umid.set_ylabel('Porcentagem')

        ax_vento.bar(['Velocidade do Vento'], [dados['Velocidade do Vento (m/s)']], color='orange')
        ax_vento.set_title('Velocidade do Vento (m/s)')
        ax_vento.set_ylabel('Velocidade')

        st.pyplot(fig_uv)

    except Exception as e:
        st.error(f"Erro ao gerar gráficos: {e}")

# Interface do Streamlit
st.title("Consulta Climática em Tempo Real")
st.markdown("Insira o nome de uma cidade para visualizar os dados climáticos atuais.")

# Entrada do usuário para a cidade
cidade = st.text_input("Digite o nome da cidade:")

if cidade:
    latitude, longitude, api_dic = carregar_dados(cidade)

    if latitude is not None and longitude is not None:
        dados_climaticos = formatar_dados_climaticos(api_dic)

        if dados_climaticos:
            st.subheader(f"Clima atual em {cidade.capitalize()}:")
            for chave, valor in dados_climaticos.items():
                st.write(f"**{chave}**: {valor}")

            # Exibir gráficos
            st.subheader("Gráficos Climáticos")
            graficos(dados_climaticos)
        else:
            st.error("Erro ao processar os dados climáticos.")
    else:
        st.error("Cidade não encontrada ou erro na requisição.")
