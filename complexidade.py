import xml.etree.ElementTree as ET
import re  # Adicionando a importação do módulo re

def calculate_svg_complexity(svg_file_path, w, h):
    try:
        tree = ET.parse(svg_file_path)
        root = tree.getroot()

        # Iniciando variáveis para cálculos
        num_elements = 0
        element_types = set()
        attribute_complexity = 0
        max_depth = 0
        width = 0
        height = 0
        total_path_length = 0
        num_groups = 0
        num_transforms = 0
        num_styles = 0

        # Função para calcular profundidade de aninhamento
        def calculate_depth(element, depth=0):
            nonlocal max_depth
            if depth > max_depth:
                max_depth = depth
            for child in element:
                calculate_depth(child, depth + 1)

        # Função para calcular complexidade de atributos
        def calculate_attribute_complexity(attributes):
            complexity = 0
            for attr, value in attributes.items():
                complexity += len(value)  # Usar comprimento do valor como proxy para complexidade
                if attr == 'd':  # Contabilizar comprimento total dos paths
                    complexity += len(value)
            return complexity

        # Função para calcular comprimento dos paths
        def calculate_path_length(d_value):
            return len(d_value)

        def extract_number(value):
            match = re.match(r'(\d+)', value)
            return int(match.group(1)) if match else 0

        # Obtendo largura e altura do SVG
        width = extract_number(root.attrib.get('width', w))
        height = extract_number(root.attrib.get('height', h))

        # Percorrendo todos os elementos SVG
        for elem in root.iter():
            num_elements += 1
            element_types.add(elem.tag)
            attribute_complexity += calculate_attribute_complexity(elem.attrib)
            calculate_depth(elem)

            if elem.tag == 'path':
                total_path_length += calculate_path_length(elem.attrib.get('d', ''))
            if elem.tag == 'g':
                num_groups += 1
            if 'transform' in elem.attrib:
                num_transforms += 1
            if 'style' in elem.attrib:
                num_styles += 1

        # Peso dos fatores de complexidade
        weights = {
            'num_elements': 0.2,
            'element_types': 0.1,
            'attribute_complexity': 0.2,
            'max_depth': 0.1,
            'dimensions': 0.1,
            'total_path_length': 0.1,
            'num_groups': 0.1,
            'num_transforms': 0.05,
            'num_styles': 0.05
        }

        # Normalizando valores para a escala 0-1
        num_elements_score = min(num_elements / 1000, 1)
        element_types_score = min(len(element_types) / 10, 1)
        attribute_complexity_score = min(attribute_complexity / 1000, 1)
        max_depth_score = min(max_depth / 10, 1)
        dimensions_score = min((width * height) / (1000 * 1000), 1)
        total_path_length_score = min(total_path_length / 10000, 1)
        num_groups_score = min(num_groups / 100, 1)
        num_transforms_score = min(num_transforms / 100, 1)
        num_styles_score = min(num_styles / 100, 1)

        # Calculando complexidade com base nos pesos
        complexity = (
            num_elements_score * weights['num_elements'] +
            element_types_score * weights['element_types'] +
            attribute_complexity_score * weights['attribute_complexity'] +
            max_depth_score * weights['max_depth'] +
            dimensions_score * weights['dimensions'] +
            total_path_length_score * weights['total_path_length'] +
            num_groups_score * weights['num_groups'] +
            num_transforms_score * weights['num_transforms'] +
            num_styles_score * weights['num_styles']
        )

        # Escalando a complexidade para 5-100
        complexity = complexity * 95 + 5

        return round(complexity)

    except Exception as e:
        print(f"Erro ao calcular a complexidade do SVG: {e}")
        return None


#Exemplo de uso
#svg_file_path = './arquivo.svg'
#complexity_score = calculate_svg_complexity(svg_file_path, '100', '100')
#print(f"A complexidade do arquivo SVG é: {complexity_score}")
