def calcular_complexidade(svg_file_path):
    import xml.etree.ElementTree as ET
    
    # Lê o arquivo SVG
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    
    # Simulação de cálculo de tempo de corte com base em algumas propriedades do SVG
    # No exemplo, consideramos o número de elementos, comprimento de paths, etc.
    tempo_corte = 0
    
    # Exemplo de cálculo baseado no número de elementos
    for elem in root.iter():
        if elem.tag.endswith('path'):
            # Supondo que cada path leve um tempo proporcional ao seu comprimento
            path_length = len(elem.attrib.get('d', ''))
            tempo_corte += path_length * 0.01  # Ajustar o fator conforme necessário
        elif elem.tag.endswith('rect'):
            tempo_corte += 2  # Tempo fixo para retângulos, ajustar conforme necessário
        elif elem.tag.endswith('circle'):
            tempo_corte += 3  # Tempo fixo para círculos, ajustar conforme necessário
        # Adicionar outras formas conforme necessário
    
    # Tempo de corte simulado (em minutos)
    tempo_corte = tempo_corte / 60  # Converte para minutos

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
