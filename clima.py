import json
import base64
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple

@st.cache_data
def pegar_img(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8')

# Carregar a imagem
img = pegar_img("background.jpg")

# Aplicar a imagem de fundo e letras brancas no Streamlit
bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64, {img}");
    background-size: cover;
    color: white;
}}
[data-testid="stSidebar"]{{
background-color: blue;
}}
header {{
    visibility: hidden;
}}
.css-1d391kg {{
    visibility: hidden;
}}
.css-1kxg7xu {{
    visibility: hidden;
}}
body{{
    color: white;
}}
.stTextInput input {{
            color: black;
            background-color: transparent;
            border: 1px solid white;
        }}
        .stTextInput input:focus {{
            border-color: lightblue;
        }}
</style>
"""
st.markdown(bg_img, unsafe_allow_html=True)

# Função para carregar os dados da API da cidade
@st.cache_data
def carregar_dados(cidade: str) -> Tuple[float, float, str, dict]:
    api_key = "91cac1b28f06467fcf5687839e0cdc69"  # Substitua pela sua chave de API
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br"
    api = requests.get(link)
    api_dic = api.json()

    if api_dic.get('cod') == 200:
        latitude = api_dic['coord']['lat']
        longitude = api_dic['coord']['lon']
        pais = api_dic['sys']['country']
        return latitude, longitude, pais, api_dic
    else:
        st.error(f"Cidade não encontrada ou erro na requisição: {api_dic.get('message')}")
        return None, None, None, None

# Função para formatar os dados climáticos
def formatar_dados_climaticos(api_dic: dict) -> dict:
    try:
        temp_atual = api_dic['main']['temp'] - 273.15
        temp_max = api_dic['main']['temp_max'] - 273.15
        temp_min = api_dic['main']['temp_min'] - 273.15
        sensacao = api_dic['main']['feels_like'] - 273.15
        umidade = api_dic['main']['humidity']
        vento_speed = api_dic['wind']['speed']
        vento_deg = api_dic['wind']['deg']
        clima = api_dic['weather'][0]['description']

        dados_climaticos = {
            'Temperatura Atual (°C)': int(temp_atual),
            'Umidade (%)': umidade,
            'Condição Climática': clima.capitalize(),
            'Sensação Térmica (°C)': int(sensacao),
            'Temperatura Máxima (°C)': int(temp_max),
            'Temperatura Mínima (°C)': int(temp_min),
            'Velocidade do Vento (m/s)': vento_speed,
            'Direção do Vento (°)': vento_deg,
        }

        return dados_climaticos
    except KeyError as e:
        st.error(f"Erro ao acessar os dados: {e}")
        return {}

# Função para criar gráficos com fundo transparente
def graficos(dados: dict) -> None:
    try:
        # Contar as ocorrências de cada condição climática
        condicoes_freq = dados['Condição Climática'].value_counts().sort_index()
        
        # Plotar gráfico de barras empilhadas
        fig, ax = plt.subplots(figsize=(8, 6))
        condicoes_freq.plot(kind='bar', stacked=True, color=['#FF5733', '#33A1FF', '#FF8D1A', '#2F4F4F'], ax=ax)
        ax.set_title('Distribuição das Condições Climáticas', fontsize=14, color='white')
        ax.set_ylabel('Quantidade', fontsize=12, color='white')
        ax.set_xlabel('Condições Climáticas', fontsize=12, color='white')
        
        # Exibir o gráfico
        fig.patch.set_alpha(0)  # Torna o fundo invisível
        ax.set_facecolor('none')
        
        # Criando o gráfico de linhas
        fig_clima, ax_clima = plt.subplots(figsize=(8, 4))

        # Plotando a temperatura e umidade
        ax_clima.plot(['Agora'], [dados['Temperatura Atual (°C)']], label='Temperatura (°C)', color='#FF5733', marker='o')
        ax_clima.plot(['Agora'], [dados['Umidade (%)']], label='Umidade (%)', color='#33A1FF', marker='o')

        # Títulos e rótulos
        ax_clima.set_title('Temperatura e Umidade Atual', color='white')
        ax_clima.set_xlabel('Hora', color='white')
        ax_clima.set_ylabel('Valor', color='white')
        ax_clima.tick_params(colors='white')

        # Exibindo a legenda
        ax_clima.legend()

        # Desligando o grid
        ax_clima.grid(True)

        # Removendo fundo e configurando transparência
        fig_clima.patch.set_alpha(0)
        ax_clima.set_facecolor('none')
        
        # Gráfico de pizza
        dados_pizza = [
            max(dados['Temperatura Atual (°C)'], 0),
            max(dados['Sensação Térmica (°C)'], 0),
            max(dados['Velocidade do Vento (m/s)'], 0),
            max(dados['Umidade (%)'], 0)
        ]
        fig_pizza, ax_pizza = plt.subplots(figsize=(6, 6))
        labels = ['Temperatura', 'Sensação Térmica', 'Velocidade do Vento', 'Umidade']
        ax_pizza.pie(dados_pizza, labels=labels, autopct='%1.1f%%', startangle=90,
                    colors=['#184ED6', '#1076EB', '#0D90D6', '#25D6FA'], textprops={'color': 'white'})
        fig_pizza.patch.set_alpha(0)  # Torna o fundo invisível

        col1, col2 = st.columns(2)

        with col1:
            st.pyplot(fig)

        with col2:
            st.pyplot(fig_pizza)

    except Exception as e:
        st.error(f"Erro ao gerar gráficos: {e}")

# Interface do Streamlit
st.title("Consulta Climática em Tempo Real")
st.markdown("Insira o nome de uma cidade para visualizar os dados climáticos atuais.")

# Entrada do usuário
cidade = st.text_input("", placeholder="Digite a cidade")

if cidade:
    latitude, longitude, pais, api_dic = carregar_dados(cidade)

    if latitude is not None and longitude is not None:
        dados_climaticos = formatar_dados_climaticos(api_dic)

        if dados_climaticos:
            st.subheader(f"Clima atual em {cidade.capitalize()}, {pais}:")
            # Informações lado a lado
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Dados Principais")
                for chave, valor in list(dados_climaticos.items())[:4]:
                    st.write(f"**{chave}**: {valor}")

            with col2:
                st.write("### Dados Adicionais")
                for chave, valor in list(dados_climaticos.items())[4:]:
                    st.write(f"**{chave}**: {valor}")

            # Gráficos
            st.subheader("Gráficos Climáticos")
            graficos(dados_climaticos)
        else:
            st.error("Erro ao processar os dados climáticos.")
    else:
        st.error("Cidade não encontrada ou erro na requisição.")
else:
    st.error("Por favor, digite o nome de uma cidade.")
