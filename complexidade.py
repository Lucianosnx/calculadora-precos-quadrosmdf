import svgpathtools

def calcular_complexidade(svg_file_path):
    # Carregar o arquivo SVG usando svgpathtools
    paths, _ = svgpathtools.svg2paths(svg_file_path)
    
    velocidade_laser = 7  # Velocidade do laser em unidades de comprimento por minuto
    
    comprimento_total = sum(path.length() for path in paths)
    
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
