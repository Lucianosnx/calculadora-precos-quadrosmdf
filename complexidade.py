# complexidade.py
from svgpathtools import svg2paths

def calculate_cut_time_and_complexity(svg_file, laser_speed=7.0):
    # Carregar os caminhos do conteúdo SVG
    paths, attributes = svg2paths(svg_file)
    
    # Calcular o comprimento total dos caminhos
    total_length = sum(path.length() for path in paths)
    
    # Calcular o tempo de corte
    cut_time_seconds = total_length / laser_speed
    cut_time_minutes = cut_time_seconds / 60  # Convertendo para minutos
    
    # Calcular a complexidade com base no tempo de corte
    if cut_time_minutes < 10:
        complexity = 1.05  # 5% de acréscimo
    elif cut_time_minutes < 20:
        complexity = 1.10  # 10% de acréscimo
    elif cut_time_minutes < 30:
        complexity = 1.15  # 15% de acréscimo
    elif cut_time_minutes < 40:
        complexity = 1.20  # 20% de acréscimo
    else:
        complexity = 1.25  # 25% de acréscimo

    return cut_time_minutes, complexity
