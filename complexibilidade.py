from svgpathtools import svg2paths2

def calcular_complexidade(svg_content):
    # Lê os caminhos (paths) do conteúdo SVG
    paths, _ = svg2paths2(svg_content)
    
    # Simulação de cálculo de tempo de corte com base no comprimento dos caminhos
    tempo_corte = 0
    
    for path in paths:
        tempo_corte += path.length()
    
    # Convertendo o comprimento total para minutos (ajustar fator conforme necessário)
    tempo_corte = tempo_corte / 100  # Ajustar o fator conforme necessário para minutos
    
    # Definindo a complexidade com base no tempo de corte
    if tempo_corte < 10:
        return 1.05, tempo_corte
    elif 10 <= tempo_corte < 20:
        return 1.10, tempo_corte
    elif 20 <= tempo_corte < 30:
        return 1.15, tempo_corte
    elif 30 <= tempo_corte < 40:
        return 1.20, tempo_corte
    else:
        return 1.25, tempo_corte
