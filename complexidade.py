import xml.etree.ElementTree as ET

def calcular_complexidade(svg_file_path):
    # Carregar o arquivo SVG
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    
    # Velocidade do laser
    velocidade_laser = 7
    
    # Calcular o comprimento total dos caminhos no SVG
    comprimento_total = 0
    for element in root.iter('{http://www.w3.org/2000/svg}path'):
        d = element.attrib.get('d')
        if d:
            # Aqui você deve implementar o cálculo do comprimento do caminho 'd'
            # Para simplificação, vamos supor que cada caminho tenha um comprimento fixo
            comprimento_total += 100  # Substituir pelo cálculo real
    
    # Calcular o tempo de corte
    tempo_corte = comprimento_total / velocidade_laser
    
    # Definir a complexidade com base no tempo de corte
    if tempo_corte < 10:
        complexidade = 1.05
    elif tempo_corte < 20:
        complexidade = 1.10
    elif tempo_corte < 30:
        complexidade = 1.15
    else:
        complexidade = 1.20
    
    return complexidade
