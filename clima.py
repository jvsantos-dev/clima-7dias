import json
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple

# Função para carregar os dados da API da cidade
def carregar_dados(cidade: str) -> Tuple[float, float]:
    """Função para carregar os dados da API OpenWeather para obter a latitude e longitude da cidade"""
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
        print(f"Cidade não encontrada ou erro na requisição: {api_dic.get('message')}")
        return None, None, None

# Função para formatar os dados da previsão atual
def formatar_dados_climaticos(api_dic: dict) -> dict:
    """Extrai e formata os dados climáticos atuais"""
    try:
        temp_atual = api_dic['main']['temp'] - 273.15  # Temperatura em Celsius
        temp_max = api_dic['main']['temp_max'] - 273.15  # Temperatura máxima em Celsius
        temp_min = api_dic['main']['temp_min'] - 273.15  # Temperatura mínima em Celsius
        sensacao = api_dic['main']['feels_like'] - 273.15  # Sensação térmica em Celsius
        umidade = api_dic['main']['humidity']  # Umidade
        vento_speed = api_dic['wind']['speed']  # Velocidade do vento
        vento_deg = api_dic['wind']['deg']  # Direção do vento
        clima = api_dic['weather'][0]['main']  # Condição climática

        # Formatação dos dados em um dicionário
        dados_climaticos = {
            'temperatura_atual': temp_atual,
            'temperatura_maxima': temp_max,
            'temperatura_minima': temp_min,
            'sensacao_termica': sensacao,
            'umidade': umidade,
            'vento_speed': vento_speed,
            'vento_direcao': vento_deg,
            'clima': clima,
        }

        return dados_climaticos
    except KeyError as e:
        print(f"Erro ao acessar a chave: {e}")
        return {}

# Função para criar gráficos com os dados climáticos
def graficos(dados: dict) -> None:
    """Cria gráficos com os dados climáticos atuais"""
    try:
        # Gráfico de temperaturas
        plt.figure(figsize=(10, 6))
        plt.bar(['Temperatura Atual', 'Temperatura Máxima', 'Temperatura Mínima'],
                [dados['temperatura_atual'], dados['temperatura_maxima'], dados['temperatura_minima']],
                color=['red', 'orange', 'blue'])
        plt.title('Temperaturas Atual, Máxima e Mínima')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True)
        plt.show()

        # Gráfico de umidade e vento
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        ax1.bar(['Umidade'], [dados['umidade']], color='green')
        ax1.set_title('Umidade')
        ax1.set_ylabel('Umidade (%)')

        ax2.bar(['Vento'], [dados['vento_speed']], color='orange')
        ax2.set_title('Velocidade do Vento')
        ax2.set_ylabel('Velocidade (m/s)')

        plt.show()

    except Exception as e:
        print(f"Erro ao gerar gráficos: {e}")

# Função principal para executar o programa
def main():
    cidade = input("Digite a cidade: ")
    
    latitude, longitude, api_dic = carregar_dados(cidade)
    
    if latitude is not None and longitude is not None:
        dados_climaticos = formatar_dados_climaticos(api_dic)

        if dados_climaticos:
            print(f"Clima atual em {cidade}:")
            for chave, valor in dados_climaticos.items():
                print(f"{chave.replace('_', ' ').capitalize()}: {valor}")

            # Exibir gráficos com as previsões
            graficos(dados_climaticos)
        else:
            print("Erro ao processar os dados climáticos.")
    else:
        print("Cidade não encontrada ou erro na requisição.")

# Chamada principal para rodar o programa
if __name__ == "__main__":
    main()
