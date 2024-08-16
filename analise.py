
import pandas as pd
import folium
import webbrowser


variaveis_mark=[]
# Substitua o caminho do arquivo conforme necessário.
caminho_arquivo = 'base_de_dados/base_favelas.xlsx'

# Abre o arquivo Excel.
xls = pd.ExcelFile(caminho_arquivo)

# Inicializa um mapa centrado em uma localização de sua escolha.
mapa = folium.Map(location=[-22.714048, -43.317890], zoom_start=15)  # Exemplo: Rio de Janeiro


header_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Justiça Hídrica nas Favelas</title>
    <!-- Adicione aqui os links para seus arquivos CSS -->
    <link rel="stylesheet" href="css/botao_favelas.css">
</head>
<body>
</body>


"""

mapa.get_root().html.add_child(folium.Element(header_html))

# Lista de coordenadas para as quais você deseja criar botões.
outras_coordenadas = [
    {"nome": "Jacarezinho", "latitude": -22.8876379, "longitude": -43.2673894},
    {"nome": "Dique de Vila Alzira", "latitude": -22.714048, "longitude": -43.317890},
    {"nome": "Providencia", "latitude": -22.9013608, "longitude": -43.2055232},
    {"nome": "PPG", "latitude": -22.9799448, "longitude": -43.2052896},
    {"nome": "Pedreira", "latitude": -22.8229438, "longitude": -43.3648037},
    {"nome": "Morro dos Macacos", "latitude": -22.9138396, "longitude": -43.2598692},
    {"nome": "CDD", "latitude": -22.9138396, "longitude": -43.2598692},
    {"nome": "Cosmorama", "latitude": -22.795701, "longitude": -43.4218074},
    {"nome": "Coréia", "latitude": -22.7742436, "longitude": -43.4429788},
    {"nome": "Complexo da Penha", "latitude": -22.8490874, "longitude": -43.2815215},
    {"nome": "Éden", "latitude": -22.7967909, "longitude": -43.4041497},
    {"nome": "Engenho", "latitude": -22.864299, "longitude": -43.783698},
    {"nome": "Itacolomi", "latitude": -22.802973, "longitude": -43.2027552},
    {"nome": "Jagutinga", "latitude": -22.7704826, "longitude": -43.4150145}
]


# Divisão da tela em duas colunas usando HTML e CSS.
html = f"""
<div style="display: flex; width: 100%;">
    <div style="width: 70%; float: left;">
        <div id="map" style="width: 100%; height: 100%;"></div>
    </div>
    <div style="width: 30%; float: left; padding-left: 10px;">
        <h2>Selecione as opções:</h2>
        <form>
            <label><input onclick="VerPreto()" type="checkbox" name="Preto">Preto</label><br>
            <label><input type="checkbox" name="option2"> Branco</label><br>
            <label><input type="checkbox" name="option3"> Pardo</label><br>
            <label><input type="checkbox" name="option4"> Indígena</label><br>
            <label><input type="checkbox" name="option5">Outros</label><br>
            <!-- Adicione mais checkboxes conforme necessário -->
        </form>
    </div>
</div>
"""

# Adicione o elemento HTML à página do mapa.
mapa.get_root().html.add_child(folium.Element(html))


# O restante do seu código para criar botões e marcadores permanece o mesmo.

# Adicione um contêiner div para os botões com a classe "button-container".
botao_container_html = """
<div class="button-container">
"""

# Itera sobre as coordenadas e cria botões para cada uma delas.
for coordenada in outras_coordenadas:
    nome = coordenada["nome"]
    latitude = coordenada["latitude"]
    longitude = coordenada["longitude"]
    
    # Cria um botão HTML com um evento onclick para centralizar o mapa.
    botao_html = f'''<button  class="button" onclick="{mapa.get_name()}.setView([{latitude}, {longitude}], 15)">{nome}
  <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
    <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm4.28 10.28a.75.75 0 000-1.06l-3-3a.75.75 0 10-1.06 1.06l1.72 1.72H8.25a.75.75 0 000 1.5h5.69l-1.72 1.72a.75.75 0 101.06 1.06l3-3z" clip-rule="evenodd"></path>
  </svg>
</button>'''
    
    # Adicione o botão HTML ao contêiner.
    botao_container_html += botao_html

# Feche o contêiner div.
botao_container_html += """
</div>
"""

# Adicione o contêiner de botões à página.
mapa.get_root().html.add_child(folium.Element(botao_container_html))

# Itera sobre as abas no arquivo Excel.
for nome_aba in xls.sheet_names:
    # Lê a planilha na aba específica.
    planilha = pd.read_excel(caminho_arquivo, sheet_name=nome_aba)

    # Itera sobre as linhas da planilha e adiciona marcadores para cada pessoa com coordenadas válidas.
    for indice, linha in planilha.iterrows():
        latitude = linha.iloc[5]  # Latitude da coluna 5 (índice 5)
        longitude = linha.iloc[6]  # Longitude da coluna 6 (índice 6)
        print(latitude)
        print(longitude)

        # Verifica se as coordenadas são válidas (não nulas ou em branco).
        if not pd.isna(latitude) and not pd.isna(longitude):
            print(linha['Qual a categoria de raça/cor que você se identifica?'])
            if 'Preto' in str(linha['Qual a categoria de raça/cor que você se identifica?']):
                cor='SaddleBrown'
            elif 'Pardo' in str(linha['Qual a categoria de raça/cor que você se identifica?']):
                cor='Peru'
            elif 'Branco' in str(linha['Qual a categoria de raça/cor que você se identifica?']):
                cor='Wheat'
            elif 'Indigena' in str(linha['Qual a categoria de raça/cor que você se identifica?']):
                cor='DarkOrange'
            else:
                cor = 'black'
            hover=f"""
                    cor/Etnia:\t{linha['Qual a categoria de raça/cor que você se identifica?']}<br>
                    Gênero:\t{linha['Qual o gênero da pessoa entrevistada?']}<br>
                    Idade:\t{linha['Qual sua idade?']}<br>
                    Falta de Água:\t{linha['Com que frequência falta água na sua casa?']}<br>
                    Vazamento de água próximo:{linha['Nas ruas da comunidade, é comum ver canos com água vazando?']}<br>
                    Banho de até 10 Minutos:{linha['Tomo banho em menos de 10 min']}<br>
                    Possui Energia eletrica: {linha['Sua casa possui energia elétrica?']}<br>
                    Tipo de Lampadas:{linha['Qual tipo de lâmpada você mais usa?']}<br>
                    Quantidade de Chuveiro Elétrico:{linha['Chuveiro Elétrico:']}<br>

             """
            # Cria um marcador com uma bolinha marrom.
            folium.CircleMarker(
                location=[latitude, longitude],
                radius=5,
                color=cor,
                fill=True,
                fill_color=cor,
                fill_opacity=1.0,
                tooltip=hover  # Exibe o nome da pessoa ao passar o mouse sobre o marcador.
            ).add_to(mapa)
            variaveis_mark.append(folium.CircleMarker().get_name())
            print(folium.CircleMarker().get_name())

#Quando o botão VerPreto() For acionado deve percorrer a lista de variaveis_mark  e ver qual color é SaddleBrown passe o stick para falsee assim conseguira desativar todos os outros que nao sao pretos

# Salva o mapa como um arquivo HTML.
mapa.save('mapa_pessoas.html')

# Abre o mapa no navegador padrão.
webbrowser.open('mapa_pessoas.html')

