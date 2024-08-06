# complexidade.py
from svgpathtools import svg2paths2
import io

# Defina o comprimento total do caminho do SVG de referência que levou 21 minutos para ser cortado
LENGTH_REFERENCE_SVG = 21  # Este valor deve ser o comprimento total do caminho do SVG de referência em unidades apropriadas

def calculate_cut_time_and_complexity(svg_content, laser_speed=7.0):
    # Carregar os caminhos do conteúdo SVG a partir de uma string
    paths, attributes, svg_attributes = svg2paths2(io.StringIO(svg_content))
    
    # Calcular o comprimento total dos caminhos
    total_length = sum(path.length(error=1e-2) for path in paths)
    
    # Calcular o tempo de corte
    # Assumindo que o SVG de referência levou 21 minutos para ser cortado
    cut_time_minutes = (total_length / LENGTH_REFERENCE_SVG) * 21
    
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
