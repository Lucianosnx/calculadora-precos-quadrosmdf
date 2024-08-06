from svgpathtools import svg2paths

def calculate_cut_time_and_complexity(svg_file_path):
    # Carregar os caminhos do arquivo SVG
    paths, attributes = svg2paths(svg_file_path)
    
    # Definir a velocidade do laser em unidades de comprimento por segundo
    laser_speed = 19.12
    
    # Calcular o comprimento total dos caminhos
    total_length = sum(path.length() for path in paths)
    
    # Calcular o tempo de corte em segundos e converter para minutos
    cut_time_minutes = (total_length / laser_speed) / 60
    
    # Calcular a complexidade com base no tempo de corte
    if cut_time_minutes < 10:
        complexity = 1.05
    elif cut_time_minutes < 20:
        complexity = 1.10
    elif cut_time_minutes < 30:
        complexity = 1.15
    else:
        complexity = 1.20
    
    return cut_time_minutes, complexity
