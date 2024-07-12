import streamlit as st

def calculate_price(width_cm, height_cm, markup, profit_margin, quantity, recurrence):
    # Convertendo dimensões para metros
    width = width_cm / 100.0
    height = height_cm / 100.0
    
    # Cálculo da área em metros quadrados
    area = width * height
    
    # Cálculo da área de referência para o preço base
    base_area = (35 / 100.0) * (31 / 100.0)
    
    # Preço base proporcional à área do quadro
    base_price = (area / base_area) * 8
    
    # Adicionando a porcentagem de acordo com o markup
    if markup == 1:
        base_price *= 1.05
    elif markup == 2:
        base_price *= 1.10
    elif markup == 3:
        base_price *= 1.15
    elif markup == 4:
        base_price *= 1.20
    
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

