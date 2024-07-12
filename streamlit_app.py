import streamlit as st

def calcular_preco(largura_cm, altura_cm, multiplicador, fator_complexidade, margem_lucro, quantidade, recorrencia):
    area = largura_cm * altura_cm
    area_referencia = 35 * 31
    preco_base = (area * 8) / area_referencia
    preco_base *= fator_complexidade

    st.markdown(f"**Preço após markup: R$ {preco_base:.2f}**")
    preco_final = preco_base * margem_lucro
    preco_total = preco_final * quantidade * recorrencia * multiplicador
    return preco_total

st.title('Calculadora de Preços para Quadros em MDF')

largura_cm = st.number_input('Largura do quadro (em centímetros):', min_value=0.0, format="%.2f")
altura_cm = st.number_input('Altura do quadro (em centímetros):', min_value=0.0, format="%.2f")

multiplicadores = {1: 1, 2: 2, 3: 3, 4: 4}
multiplicador = st.selectbox('Multiplicador do preço final:', options=list(multiplicadores.keys()))

fatores_complexidade = {1: 1.05, 2: 1.10, 3: 1.15, 4: 1.20}
fator_complexidade = st.selectbox('Complexidade do design (1 a 4):', options=list(fatores_complexidade.keys()))

margens_lucro = {1: 1.05, 2: 1.10, 3: 1.20, 4: 1.30}
margem_lucro = st.selectbox('Margem de lucro:', options=list(margens_lucro.keys()))

tipo = st.selectbox('Tipo:', ('Produto', 'Serviço'))

quantidade = 1
recorrencia = 1
if tipo == 'Serviço':
    quantidade = st.number_input('Quantidade:', min_value=1)
    recorrencia = st.number_input('Recorrência:', min_value=1)

# Atualização dinâmica do preço ao modificar qualquer entrada
if largura_cm and altura_cm:
    resultado = calcular_preco(largura_cm, altura_cm, multiplicadores[multiplicador], fatores_complexidade[fator_complexidade], margens_lucro[margem_lucro], quantidade, recorrencia)
    st.markdown(f"**Preço final: R$ {resultado:.2f}**")
