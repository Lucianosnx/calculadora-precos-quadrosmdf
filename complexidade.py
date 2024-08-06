import svgpathtools

def calcular_complexidade(svg_file_path, velocidade_laser):
    # Carregar o arquivo SVG usando svgpathtools
    paths, _ = svgpathtools.svg2paths(svg_file_path)
    
    # Calcular o comprimento total dos caminhos
    comprimento_total = sum(path.length() for path in paths)
    
    # Calcular o tempo de corte baseado na velocidade do laser
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
    
    return complexidade, tempo_corte
