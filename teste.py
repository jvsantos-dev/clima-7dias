import streamlit as st
import requests
import matplotlib.pyplot as plt
import plotly.express as px

# Função para carregar os dados da API da cidade
@st.cache_data
def carregar_dados(cidade: str):
    api_key = "91cac1b28f06467fcf5687839e0cdc69"
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br"
    api = requests.get(link)
    api_dic = api.json()

    if api_dic.get('cod') == 200:
        latitude = api_dic['coord']['lat']
        longitude = api_dic['coord']['lon']
        return latitude, longitude, api_dic
    else:
        return None, None, None

# Formatação dos dados climáticos
def formatar_dados_climaticos(api_dic: dict) -> dict:
    temp_atual = api_dic['main']['temp'] - 273.15
    temp_max = api_dic['main']['temp_max'] - 273.15
    temp_min = api_dic['main']['temp_min'] - 273.15
    sensacao = api_dic['main']['feels_like'] - 273.15
    umidade = api_dic['main']['humidity']
    vento_speed = api_dic['wind']['speed']
    clima = api_dic['weather'][0]['description'].capitalize()

    return {
        'Temperatura Atual (°C)': temp_atual,
        'Temperatura Máxima (°C)': temp_max,
        'Temperatura Mínima (°C)': temp_min,
        'Sensação Térmica (°C)': sensacao,
        'Umidade (%)': umidade,
        'Velocidade do Vento (m/s)': vento_speed,
        'Clima': clima,
    }

# Função para criar gráficos
def criar_graficos(dados: dict):
    # Gráfico de barras com Plotly
    fig = px.bar(
        x=['Temperatura Atual', 'Temperatura Máxima', 'Temperatura Mínima'],
        y=[dados['Temperatura Atual (°C)'], dados['Temperatura Máxima (°C)'], dados['Temperatura Mínima (°C)']],
        labels={'x': 'Tipo', 'y': 'Temperatura (°C)'},
        title='Temperaturas',
        color=['Temperatura Atual', 'Temperatura Máxima', 'Temperatura Mínima']
    )
    st.plotly_chart(fig, use_container_width=True)

# Layout do Streamlit
st.title("🌤️ Aplicativo de Clima")
st.write("Confira as condições climáticas de qualquer cidade do mundo!")

cidade = st.text_input("Digite o nome de uma cidade:", "São Paulo")

if cidade:
    latitude, longitude, api_dic = carregar_dados(cidade)

    if latitude is not None:
        dados_climaticos = formatar_dados_climaticos(api_dic)

        # Dividir em duas colunas
        col1, col2 = st.columns(2)

        with col1:
            st.header(f"📍 {cidade.capitalize()}")
            for chave, valor in dados_climaticos.items():
                st.write(f"**{chave}:** {valor}")

        with col2:
            st.header("📊 Gráficos")
            criar_graficos(dados_climaticos)
    else:
        st.error("Cidade não encontrada. Verifique o nome e tente novamente.")
