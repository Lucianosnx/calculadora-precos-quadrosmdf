import streamlit as st

def calculate_price(width_cm, height_cm, markup_multiplier, profit_margin, quantity, recurrence):
    area = width_cm * height_cm
    reference_area = 35 * 31
    base_price = (area * 8) / reference_area
    
    base_price *= markup_multiplier
    if width_cm and height_cm:
        st.write(f"Preço após markup: R$ {base_price:.2f}")
    
    final_price = base_price * 2 * (1 + profit_margin)
    total_price = final_price * quantity * recurrence
    return total_price

st.title('Calculadora de Preços para Quadros em MDF')

width_cm = st.number_input('Largura do quadro (em centímetros):', min_value=0.0, format="%.2f")
height_cm = st.number_input('Altura do quadro (em centímetros):', min_value=0.0, format="%.2f")

if width_cm and height_cm:
    area = width_cm * height_cm
    reference_area = 35 * 31
    base_price = (area * 8) / reference_area
    st.write(f"Preço base: R$ {base_price:.2f}")

markup_choices = {1: 1.05, 2: 1.10, 3: 1.15, 4: 1.20}
markup = st.selectbox('Complexidade do design (1 a 4):', options=list(markup_choices.keys()), format_func=lambda x: f"{x} - {markup_choices[x]*100-100:.0f}%")

profit_margin_choices = {1: 1.05, 2: 1.10, 3: 1.20, 4: 1.30}
profit_margin = st.selectbox('Margem de lucro:', options=list(profit_margin_choices.keys()), format_func=lambda x: f"{x} - {profit_margin_choices[x]*100-100:.0f}%")


product_or_service = st.selectbox('Tipo:', ('Produto', 'Serviço'))

quantity = 1
recurrence = 1

if product_or_service == 'Serviço':
    quantity = st.number_input('Quantidade:', min_value=1)
    recurrence = st.number_input('Recorrência:', min_value=1)

if st.button('Calcular Preço'):
    result = calculate_price(width_cm, height_cm, markup_choices[markup], profit_margin, quantity, recurrence)
    st.write(f"Preço final: R$ {result:.2f}")
