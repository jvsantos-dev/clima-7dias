import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from typing import Dict, List, Tuple

# Carregando a api
def carregar_dados(cidade: str) -> pd.DataFrame:
    """Função para carregar os dados da api"""
    api_key = "91cac1b28f06467fcf5687839e0cdc69"
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br"
    api = requests.get(link)
    api_dic = api.json()
    return api_dic

def coletar_dados(api_dic: pd.DataFrame) -> None:
    temp_media = api_dic['temp']['temp_max'] - ['temp']['temp_min'] - 273.15
    clima = api_dic['weather']['main']





def main():
    main