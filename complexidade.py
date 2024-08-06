from svgpathtools import svg2paths

def calculate_cut_time_and_complexity(svg_file_path, laser_speed):
    # Carregar os caminhos do arquivo SVG
    paths, attributes = svg2paths(svg_file_path)
    
    # Calcular o comprimento total dos caminhos
    total_length = sum(path.length() for path in paths)
    
    # Calcular o tempo de corte em segundos
    cut_time_seconds = total_length / laser_speed
    
    # Calcular o número de segmentos e trocas de direção
    num_segments = sum(len(path) for path in paths)
    num_changes_in_direction = sum(len(path) for path in paths)
    
    # Definir pesos para cada fator de complexidade
    weight_length = 0.5
    weight_segments = 0.3
    weight_direction_changes = 0.2
    
    # Normalizar os valores para uma escala de 0 a 1
    max_length = 1000  # Assumindo um comprimento máximo arbitrário para normalização
    max_segments = 1000  # Assumindo um número máximo de segmentos arbitrário para normalização
    max_direction_changes = 1000  # Assumindo um número máximo de trocas de direção arbitrário para normalização
    
    norm_length = min(total_length / max_length, 1.0)
    norm_segments = min(num_segments / max_segments, 1.0)
    norm_direction_changes = min(num_changes_in_direction / max_direction_changes, 1.0)
    
    # Calcular a complexidade
    complexity = (
        norm_length * weight_length +
        norm_segments * weight_segments +
        norm_direction_changes * weight_direction_changes
    ) * 100
    
    # Converter tempo de corte para minutos
    cut_time_minutes = cut_time_seconds / 60
    
    return cut_time_minutes, complexity
