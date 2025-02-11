# Consulta Climática em Tempo Real

Este projeto é uma aplicação interativa desenvolvida com o **Streamlit**, permitindo consultar dados climáticos em tempo real de qualquer cidade. Ao fornecer o nome da cidade, o sistema retorna informações detalhadas sobre a temperatura, umidade, sensação térmica, vento e mais. Além disso, a aplicação exibe gráficos interativos de comparação entre a temperatura atual e a sensação térmica, assim como um gráfico de pizza com dados adicionais sobre o clima.

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

### 📋 Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- **Python**: versão 3.8 ou superior.
  
### 🛠️ Bibliotecas Utilizadas

Este projeto utiliza as seguintes bibliotecas:

- **Streamlit**: Biblioteca para criar interfaces web interativas de forma simples.
- **requests**: Para fazer requisições HTTP à API de clima.
- **matplotlib**: Biblioteca para geração de gráficos estáticos.
- **pandas**: Biblioteca para manipulação e análise de dados.
- **base64**: Para codificação e manipulação de imagens base64.
- **numpy**: Para cálculos e manipulações numéricas.

## 🔧 Instalação

Siga estas etapas para configurar o ambiente:

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu_usuario/cilma-7dias.git

    Acesse o diretório do projeto:

cd consulta-climatica

Crie um ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

Execute a aplicação:

    streamlit run clima.py

    Abra o navegador e acesse http://127.0.0.1:8501 para visualizar a aplicação.

📈 Funcionalidades

    Consulta de Clima: Insira o nome de uma cidade e veja os dados climáticos em tempo real, incluindo:
        Temperatura
        Sensação térmica
        Umidade
        Direção e velocidade do vento
    Gráficos Interativos:
        Gráfico de barras comparando a temperatura atual com a sensação térmica.
        Gráfico de pizza com a distribuição percentual de temperatura, sensação térmica, umidade e velocidade do vento.

🎨 Personalizações

    Imagem de Fundo: A aplicação inclui uma imagem de fundo personalizada (em formato JPEG), que pode ser trocada facilmente para mudar a aparência.
    Estilos de Interface: A interface do Streamlit foi customizada com cores e fontes para melhorar a estética e a experiência do usuário.

📸 Exemplos Visuais

Abaixo estão exemplos dos gráficos gerados pela aplicação:

    Gráfico de Comparação (Temperatura Atual vs Sensação Térmica): Um gráfico de barras comparando os dados.
    Gráfico de Pizza: Mostra a distribuição percentual de temperatura, sensação térmica, umidade e velocidade do vento.

📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
