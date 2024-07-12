import streamlit as st

# Função para calcular o preço dos quadros em MDF
def calculate_price(width_cm, height_cm, markup_multiplier, profit_margin, quantity, recurrence, multiplier):
    # Calcula a área em centímetros quadrados
    area = width_cm * height_cm
    # Define a área de referência
    reference_area = 35 * 31
    # Calcula o preço base usando regra de três
    base_price = (area * 8) / reference_area
    # Aplica o markup selecionado
    base_price *= markup_multiplier
    # Mostra o preço após markup
    st.write(f"Preço após markup: R$ {base_price:.2f}")
    # Calcula o preço final aplicando a margem de lucro
    final_price = base_price * profit_margin
    # Calcula o total considerando quantidade e recorrência
    total_price = final_price * quantity * recurrence * multiplier
    return total_price

st.title('Calculadora de Preços para Quadros em MDF')

# Inputs para largura e altura do quadro
width_cm = st.number_input('Largura do quadro (em centímetros):', min_value=0.0, format="%.2f")
height_cm = st.number_input('Altura do quadro (em centímetros):', min_value=0.0, format="%.2f")

# Calcula e mostra o preço base quando as dimensões são fornecidas
if width_cm and height_cm:
    area = width_cm * height_cm
    reference_area = 35 * 31
    base_price = (area * 8) / reference_area
    st.write(f"Preço base: R$ {base_price:.2f}")

# Seleção do markup pela complexidade
markup_choices = {1: 1.05, 2: 1.10, 3: 1.15, 4: 1.20}
markup = st.selectbox('Complexidade do design (1 a 4):', options=list(markup_choices.keys()), format_func=lambda x: f"{x} - {markup_choices[x]*100-100:.0f}%")

# Seleção da margem de lucro
profit_margin_choices = {1: 1.05, 2: 1.10, 3: 1.20, 4: 1.30}
profit_margin = st.selectbox('Margem de lucro:', options=list(profit_margin_choices.keys()), format_func=lambda x: f"{x} - {profit_margin_choices[x]*100-100:.0f}%")

# Seleção de produto ou serviço
product_or_service = st.selectbox('Tipo:', ('Produto', 'Serviço'))

# Configurações de quantidade e recorrência para serviços
quantity = 1
recurrence = 1
if product_or_service == 'Serviço':
    quantity = st.number_input('Quantidade:', min_value=1)
    recurrence = st.number_input('Recorrência:', min_value=1)

# Seleção do multiplicador para o preço final
multiplier = st.selectbox('Multiplicador do preço final:', options=(1, 2, 3, 4))

# Botão para calcular o preço final
if st.button('Calcular Preço'):
    result = calculate_price(width_cm, height_cm, markup_choices[markup], profit_margin_choices[profit_margin], quantity, recurrence, multiplier)
    st.write(f"Preço final: R$ {result:.2f}")
