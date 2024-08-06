import xml.etree.ElementTree as ET

def calcular_complexidade(svg_file_path):
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    
    velocidade_laser = 7  # Velocidade do laser em unidades de comprimento por minuto
    
    comprimento_total = 0
    for element in root.iter('{http://www.w3.org/2000/svg}path'):
        d = element.attrib.get('d')
        if d:
            comprimento_total += 100  # Substituir pelo cálculo real
    
    tempo_corte = comprimento_total / velocidade_laser  # Tempo de corte em minutos
    
    if tempo_corte < 10:
        complexidade = 1.05
    elif tempo_corte < 20:
        complexidade = 1.10
    elif tempo_corte < 30:
        complexidade = 1.15
    else:
        complexidade = 1.20
    
    return complexidade, tempo_corte
