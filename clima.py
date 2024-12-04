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

# Carregando os dados do CSV ou JSON
def carregar_dados(arquivo: str) -> pd.DataFrame:
    """Função para carregar os dados de um arquivo CSV ou JSON"""
    try:
        if arquivo.endswith('.csv'):
            return pd.read_csv(arquivo)
        elif arquivo.endswith('.json'):
            with open(arquivo, "r") as f:
                dados_json = [json.loads(linha.strip()) for linha in f]
            return pd.DataFrame(dados_json)
        else:
            raise ValueError("Arquivo deve ser CSV ou JSON.")
    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo} não foi encontrado.")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo {arquivo}.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Erro inesperado ao carregar os dados: {e}")
        return pd.DataFrame()

# Limpar e preparar os dados
def limpar_dados(dados: pd.DataFrame) -> None:
    """Função para limpar e preparar os dados"""
    if dados.empty:
        print("Erro: Dados vazios.")
        return
    
    try:
        # Renomeando as colunas
        dados.rename(columns={
            'date': 'data',
            'precipitation': 'precipitação',
            'temp_max': 'temperatura_maxima',
            'temp_min': 'temperatura_minima',
            'wind': 'vento',
            'weather': 'clima'
        }, inplace=True)

        # Traduzindo a coluna 'clima'
        clima_traducao = {
            'sun': 'sol',
            'rain': 'chuva',
            'drizzle': 'chuvisco',
            'snow': 'neve',
            'fog': 'nevoeiro',
            'cloudy': 'nublado'
        }

        dados['clima'] = dados['clima'].map(clima_traducao)
        dados['data'] = pd.to_datetime(dados['data'], errors='coerce')
        dados['mes'] = dados['data'].dt.month
        dados['dia_ano'] = dados['data'].dt.dayofyear
        dados['baixo_radiacao'] = dados['clima'].apply(lambda x: 1 if x in ['chuva', 'neve', 'chuvisco', 'nevoeiro'] else 0)
    except Exception as e:
        print(f"Erro ao limpar os dados: {e}")

# Função para treinar o modelo de aprendizado de máquina
def aprendizado_maquina(dados: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """Função para treinar o modelo de aprendizado de máquina"""
    if dados.empty:
        print("Erro: Dados vazios.")
        return pd.Series(), pd.Series()

    try:
        x = dados[['temperatura_maxima', 'temperatura_minima', 'precipitação', 'vento', 'clima', 'mes', 'dia_ano']]
        y = dados['baixo_radiacao']
        encoder = LabelEncoder()
        x['clima'] = encoder.fit_transform(x['clima'])

        # Dividindo os dados em treino e teste
        x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.3, random_state=42)

        # Normalizando os dados
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_treino)
        x_test_scaled = scaler.transform(x_teste)

        # Treinando o modelo Random Forest
        model = RandomForestClassifier(n_estimators=100, random_state=11231)
        model.fit(x_train_scaled, y_treino)

        # Fazendo previsões
        y_prev = model.predict(x_test_scaled)

        # Avaliando o modelo
        print(f"Acurácia do modelo: {accuracy_score(y_teste, y_prev) * 100:.2f}%")
        print("Relatório de Classificação:\n", classification_report(y_teste, y_prev))

        return y_teste, y_prev
    except Exception as e:
        print(f"Erro ao treinar o modelo de aprendizado de máquina: {e}")
        return pd.Series(), pd.Series()

# Função para prever os próximos 7 dias e calcular a radiação
def prever_proximos_7_dias(dados: pd.DataFrame, cidade: str) -> pd.DataFrame:
    """Função para prever os próximos 7 dias de clima com base em dados históricos"""
    import random

    try:
        # Gerar previsões de temperatura de forma simulada (diferente para cada cidade)
        previsao = []

        for i in range(7):
            if cidade == 'seattle':
                temperatura_maxima = random.uniform(5, 15)  # Temperatura média mais baixa
                temperatura_minima = random.uniform(-1, 5)
            elif cidade == 'curitiba':
                temperatura_maxima = random.uniform(18, 25)  # Temperatura média mais alta
                temperatura_minima = random.uniform(10, 18)

            precipitação = random.uniform(0, 10)  # Simulando precipitação
            vento = random.uniform(0, 15)  # Simulando velocidade do vento
            clima = random.choice(['sol', 'chuva', 'nublado', 'neve', 'chuvisco'])  # Clima aleatório

            # Classificar o nível de radiação com base na temperatura
            if clima == 'sol':
                if temperatura_maxima > 25:
                    nivel_radiacao = 'Bom'
                elif temperatura_maxima > 15:
                    nivel_radiacao = 'Moderado'
                else:
                    nivel_radiacao = 'Ruim'
            else:
                nivel_radiacao = 'Ruim'

            # Adicionar a previsão para o dia
            previsao.append({
                'data': f'2024-11-{i + 21}',  # Exemplo de datas (pode ser ajustado conforme necessário)
                'temperatura_maxima': temperatura_maxima,
                'temperatura_minima': temperatura_minima,
                'precipitação': precipitação,
                'vento': vento,
                'clima': clima,
                'nivel_radiacao': nivel_radiacao
            })

        # Retornar as previsões em formato DataFrame
        return pd.DataFrame(previsao)
    except Exception as e:
        print(f"Erro ao prever os próximos 7 dias: {e}")
        return pd.DataFrame()

# Função para classificar a radiação solar
def classificar_solar(linha: pd.Series, limite: Dict[str, int]) -> str:
    """Classifica o nível de radiação solar"""
    try:
        if linha['clima'] == 'sol':
            if linha['temperatura_maxima'] > limite['alta']:
                return 'Alta'
            elif linha['temperatura_maxima'] > limite['moderada']:
                return 'Moderada'
            else:
                return 'Baixa'
        elif linha['clima'] in ['chuva', 'neve', 'nevoeiro']:
            return 'Baixa'
        else:
            return 'Moderada'
    except KeyError as e:
        print(f"Erro ao classificar a radiação solar. Limite ausente: {e}")
        return 'Desconhecido'
    except Exception as e:
        print(f"Erro inesperado ao classificar a radiação solar: {e}")
        return 'Desconhecido'

# Função para aplicar a classificação de radiação solar em um DataFrame
def aplicar_solar(dados: pd.DataFrame, limite: Dict[str, int] = None) -> pd.DataFrame:
    """Aplica a classificação de radiação solar no DataFrame"""
    if limite is None:
        limite = {'alta': 25, 'moderada': 15}  # Limites padrão

    try:
        for idx, linha in dados.iterrows():
            dados.loc[idx, 'nivel_radiacao'] = classificar_solar(linha, limite)
        return dados
    except Exception as e:
        print(f"Erro ao aplicar a classificação solar: {e}")
        return dados

# Função para gerar gráficos
def graficos(dados: pd.DataFrame, escolher: int) -> None:
    """Exibe gráficos com base na escolha do usuário"""
    try:
        dados = aplicar_solar(dados)  # Aplica a classificação de radiação solar
        if escolher == 1:
            clima_freq = dados['clima'].value_counts()
            sns.barplot(x=clima_freq.index, y=clima_freq.values)
            plt.title('Frequência dos Tipos de Clima')
            plt.xlabel('Clima')
            plt.ylabel('Dias')
            plt.show()
        elif escolher == 2:
            plt.figure(figsize=(10, 6))
            plt.plot(dados['data'], dados['temperatura_maxima'], label='Temperatura Máxima', color='red')
            plt.plot(dados['data'], dados['temperatura_minima'], label='Temperatura Mínima', color='blue')
            plt.title('Variação de Temperatura ao Longo do Tempo')
            plt.xlabel('Data')
            plt.ylabel('Temperatura (°C)')
            plt.legend()
            plt.grid()
            plt.show()
        else:
            print("Opção inválida de gráfico.")
    except Exception as e:
        print(f"Erro ao gerar gráficos: {e}")

# Função de menu 
def menu():
    """Menu principal do sistema"""
    try:
        dados_seattle = carregar_dados('./seattle-weather.csv')
        dados_curitiba = carregar_dados('curitiba-weather.json')

        # Limpando e preparando os dados
        limpar_dados(dados_seattle)
        limpar_dados(dados_curitiba)
        aprendizado_maquina(dados_seattle)
        aprendizado_maquina(dados_curitiba)

        while True:
            print("\nMenu de Opções:")
            print("1 - Seattle")
            print("2 - Curitiba")
            print("3 - Sair")

            escolha = input("Escolha uma opção (1-3): ")

            if escolha == '1':
                while True:
                    print("\nEscolha uma opção para Seattle:")
                    print("1 - Previsão de 7 dias")
                    print("2 - Exibir gráfico de frequência dos tipos de clima")
                    print("3 - Exibir gráfico de variação de temperatura")
                    print("4 - Voltar")

                    escolha_seattle = input("Escolha uma opção (1-4): ")

                    if escolha_seattle == '1':
                        previsao_seattle = prever_proximos_7_dias(dados_seattle, 'seattle')
                        print(previsao_seattle)
                    elif escolha_seattle == '2':
                        graficos(dados_seattle, 1)
                    elif escolha_seattle == '3':
                        graficos(dados_seattle, 2)
                    elif escolha_seattle == '4':
                        break
                    else:
                        print("Opção inválida, por favor, escolha novamente.")
            elif escolha == '2':
                while True:
                    print("\nEscolha uma opção para Curitiba:")
                    print("1 - Previsão de 7 dias")
                    print("2 - Exibir gráfico de frequência dos tipos de clima")
                    print("3 - Exibir gráfico de variação de temperatura")
                    print("4 - Voltar")

                    escolha_curitiba = input("Escolha uma opção (1-4): ")

                    if escolha_curitiba == '1':
                        previsao_curitiba = prever_proximos_7_dias(dados_curitiba, 'curitiba')
                        print(previsao_curitiba)
                    elif escolha_curitiba == '2':
                        graficos(dados_curitiba, 1)
                    elif escolha_curitiba == '3':
                        graficos(dados_curitiba, 2)
                    elif escolha_curitiba == '4':
                        break
                    else:
                        print("Opção inválida, por favor, escolha novamente.")
            elif escolha == '3':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida, por favor, escolha novamente.")
    except Exception as e:
        print(f"Erro inesperado no menu: {e}")

if __name__ == "__main__":
    menu()
