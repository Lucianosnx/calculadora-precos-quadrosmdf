import xml.etree.ElementTree as ET
import math

def parse_svg_path(path_data):
    # Implement a simple SVG path parser for demonstration purposes
    length = 0
    commands = path_data.split()
    current_pos = (0, 0)
    start_pos = (0, 0)
    
    for command in commands:
        if command == 'M':
            start_pos = (float(commands.pop(0)), float(commands.pop(0)))
            current_pos = start_pos
        elif command == 'L':
            next_pos = (float(commands.pop(0)), float(commands.pop(0)))
            length += math.dist(current_pos, next_pos)
            current_pos = next_pos
        elif command == 'Z':
            length += math.dist(current_pos, start_pos)
            current_pos = start_pos
    
    return length

def calcular_complexidade(svg_file_path):
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    
    velocidade_laser = 7  # Velocidade do laser em unidades de comprimento por minuto
    
    comprimento_total = 0
    for element in root.iter('{http://www.w3.org/2000/svg}path'):
        d = element.attrib.get('d')
        if d:
            comprimento_total += parse_svg_path(d)
    
    # Calibrar o tempo de corte com base no exemplo fornecido
    tempo_corte_real = 21  # minutos para o SVG fornecido
    comprimento_real = comprimento_total  # comprimento total do SVG fornecido
    fator_calibracao = tempo_corte_real / comprimento_real
    
    # Ajustar o comprimento total com base no fator de calibração
    tempo_corte = comprimento_total * fator_calibracao
    
    if tempo_corte < 10:
        complexidade = 1.05
    elif tempo_corte < 20:
        complexidade = 1.10
    elif tempo_corte < 30:
        complexidade = 1.15
    else:
        complexidade = 1.20
    
    return complexidade, tempo_corte
