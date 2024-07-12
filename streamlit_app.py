import streamlit as st

def calculate_price(width_cm, height_cm, markup, profit_margin, quantity, recurrence):
    # Cálculo da área em centímetros quadrados
    area = width_cm * height_cm
    
    # Área do quadro de referência
    reference_area = 35 * 31
    
    # Preço base usando regra de três
    base_price = (area * 8) / reference_area
    
    # Adicionando a porcentagem de acordo com o markup
    markup_multiplier = 1 + markup / 100.0 * 5  # Calculando o multiplicador do markup
    base_price *= markup_multiplier
    
    # Calculando o preço final com margem de lucro
    final_price = base_price * (1 + profit_margin)
    
    # Considerando a quantidade e a recorrência se for serviço
    total_price = final_price * quantity * recurrence
    
    return total_price

# Inputs do usuário
st.title('Calculadora de Preços para Quadros em MDF')

# Dimensões do quadro
width_cm = st.number_input('Largura do quadro (em centímetros):', min_value=0.0, format="%.2f")
height_cm = st.number_input('Altura do quadro (em centímetros):', min_value=0.0, format="%.2f")

# Markup pela complexidade
markup = st.selectbox('Complexidade do design (1 a 4):', (1, 2, 3, 4))

# Margem de lucro
profit_margin = st.selectbox('Margem de lucro:', (0.05, 0.10, 0.20, 0.30))

# Produto ou Serviço
product_or_service = st.selectbox('Tipo:', ('Produto', 'Serviço'))

quantity = 1
recurrence = 1

if product_or_service == 'Serviço':
    quantity = st.number_input('Quantidade:', min_value=1)
    recurrence = st.number_input('Recorrência:', min_value=1)

# Botão para calcular
if st.button('Calcular Preço'):
    result = calculate_price(width_cm, height_cm, markup, profit_margin, quantity, recurrence)
    st.write(f'O preço final é: R$ {result:.2f}')

