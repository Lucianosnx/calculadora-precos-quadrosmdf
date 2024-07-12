import streamlit as st

def calcular_preco(largura_cm, altura_cm, fator_complexidade, margem_lucro, quantidade, recorrencia):
    area = largura_cm * altura_cm
    area_referencia = 35 * 31
    preco_base = (area * 8) / area_referencia
    preco_base *= fator_complexidade

    st.markdown(f"**Preço após markup: R$ {preco_base:.2f}**")
    preco_final = preco_base * margem_lucro
    preco_total = preco_final * quantidade * recorrencia
    return preco_total

st.title('Calculadora de Preços para Quadros em MDF')

largura_cm = st.number_input('Largura do quadro (em centímetros):', min_value=0.0, format="%.2f")
altura_cm = st.number_input('Altura do quadro (em centímetros):', min_value=0.0, format="%.2f")

# Calcula e mostra o preço base quando as dimensões são fornecidas
if largura_cm and altura_cm:
    area = largura_cm * altura_cm
    area_referencia = 35 * 31
    preco_base = (area * 8) / area_referencia
    st.write(f"Preço base: R$ {preco_base:.2f}")

opcoes_complexidade = {1: 1.05, 2: 1.10, 3: 1.15, 4: 1.20}
fator_complexidade = st.selectbox('Complexidade do design (1 a 4):', options=list(opcoes_complexidade.keys()), format_func=lambda x: f"{x} - {opcoes_complexidade[x]*100-100:.0f}%")

opcoes_lucro = {1: 1.05, 2: 1.10, 3: 1.20, 4: 1.30}
margem_lucro = st.selectbox('Margem de lucro:', options=list(opcoes_lucro.keys()), format_func=lambda x: f"{x} - {opcoes_lucro[x]*100-100:.0f}%")

tipo = st.selectbox('Tipo:', ('Produto', 'Serviço'))

quantidade = 1
recorrencia = 1
if tipo == 'Serviço':
    quantidade = st.number_input('Quantidade:', min_value=1)
    recorrencia = st.number_input('Recorrência:', min_value=1)

# Atualização dinâmica do preço ao modificar qualquer entrada
if largura_cm and altura_cm:
    resultado = calcular_preco(largura_cm, altura_cm, opcoes_complexidade[fator_complexidade], opcoes_lucro[margem_lucro], quantidade, recorrencia)
    st.markdown(f"**Preço final: R$ {resultado:.2f}**")
