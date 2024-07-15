import streamlit as st
import pandas as pd

def calcular_preco(largura_cm, altura_cm, multiplicador, fator_complexidade, margem_lucro, quantidade, recorrencia, tipo, tipo_usuario):
    area = largura_cm * altura_cm
    area_referencia = 35 * 31
    preco_base = (area * 8) / area_referencia
    
    detalhes_precos = []

    detalhes_precos.append(('Preço Base', preco_base))

    preco_multiplicado = preco_base * multiplicador
    preco_complexidade = preco_multiplicado * fator_complexidade

    detalhes_precos.append(('Preço após Multiplicador', preco_multiplicado))
    detalhes_precos.append(('Preço após Complexidade', preco_complexidade))

    preco_final = preco_complexidade * margem_lucro
    detalhes_precos.append(('Preço após Margem de Lucro', preco_final))

    if tipo == 'Serviço':
        descontos_quantidade = {1: 2, 10: 0.9, 50: 0.8, 100: 0.7}
        if tipo_usuario == 'Consumidor':
            descontos_quantidade = {1: 2, 10: 0.95, 50: 0.9, 100: 0.85}
        
        desconto_qtd = descontos_quantidade[quantidade]
        
        preco_quantidade = preco_final * desconto_qtd
        detalhes_precos.append(('Preço após Desconto de Quantidade', preco_quantidade))
        
        preco_recorrencia = preco_quantidade
        if recorrencia > 0:
            desconto_recorrencia = 1 - (recorrencia * 0.1)
            if tipo_usuario == 'Consumidor':
                desconto_recorrencia = 1 - (recorrencia * 0.05)
            
            preco_recorrencia = preco_quantidade * desconto_recorrencia
            detalhes_precos.append(('Preço após Desconto de Recorrência', preco_recorrencia))
        
        preco_final = preco_recorrencia if recorrencia > 0 else preco_quantidade
    else:
        preco_final = preco_complexidade * margem_lucro

    taxa_erro = 1.03
    preco_erro = preco_final * taxa_erro
    detalhes_precos.append(('Preço após Taxa de Erro (3%)', preco_erro))
    
    custo_aquisicao = 1.17
    preco_aquisicao = preco_erro * custo_aquisicao
    detalhes_precos.append(('Preço após Custo de Aquisição (17%)', preco_aquisicao))
    
    preco_total = preco_aquisicao * (quantidade if tipo == 'Serviço' else 1)
    if quantidade > 1 and tipo == 'Serviço':
        detalhes_precos.append(('Preço Unitário', preco_aquisicao))
        detalhes_precos.append(('Preço Final Total', preco_total))
    else:
        detalhes_precos.append(('Preço Final', preco_total))

    return detalhes_precos

st.title('Calculadora de Preços QuadrosMDF')

largura_cm = st.number_input('Largura do quadro (em centímetros):', min_value=0.0, format="%.2f")
altura_cm = st.number_input('Altura do quadro (em centímetros):', min_value=0.0, format="%.2f")

if largura_cm and altura_cm:
    area = largura_cm * altura_cm
    area_referencia = 35 * 31
    preco_base = (area * 8) / area_referencia
    st.write(f"**Preço base: R$ {preco_base:.2f}**")

multiplicadores = {1: 1, 2: 2, 3: 3, 4: 4}
multiplicador = st.selectbox('Multiplicador do preço base:', options=list(multiplicadores.keys()))

opcoes_complexidade = {1: 1.05, 2: 1.10, 3: 1.15, 4: 1.20}
fator_complexidade = st.selectbox('Complexidade do design (1 a 4):', options=list(opcoes_complexidade.keys()), format_func=lambda x: f"{x} - {opcoes_complexidade[x]*100-100:.0f}%")

opcoes_lucro = {1: 1.05, 2: 1.10, 3: 1.20, 4: 1.30}
margem_lucro = st.selectbox('Margem de lucro:', options=list(opcoes_lucro.keys()), format_func=lambda x: f"{x} - {opcoes_lucro[x]*100-100:.0f}%")

tipo = st.selectbox('Tipo:', ('Produto', 'Serviço'))

tipo_usuario = 'Empresa'
quantidade = 1
recorrencia = 0

if tipo == 'Serviço':
    tipo_usuario = st.radio('Tipo de usuário:', ('Consumidor', 'Empresa'))
    
    descontos_quantidade_display = {1: '0%', 10: '5%' if tipo_usuario == 'Consumidor' else '10%', 50: '10%' if tipo_usuario == 'Consumidor' else '20%', 100: '15%' if tipo_usuario == 'Consumidor' else '30%'}
    descontos_recorrencia_display = {i: f"{(i * 5 if tipo_usuario == 'Consumidor' else i * 10)}%" for i in range(6)}

    quantidade = st.selectbox('Quantidade:', options=[1, 10, 50, 100], format_func=lambda x: f"{x} ({descontos_quantidade_display[x]})")
    recorrencia = st.selectbox('Recorrência:', options=list(descontos_recorrencia_display.keys()), format_func=lambda x: f"{x} ({descontos_recorrencia_display[x]})")

if largura_cm and altura_cm:
    detalhes_precos = calcular_preco(largura_cm, altura_cm, multiplicadores[multiplicador], opcoes_complexidade[fator_complexidade], opcoes_lucro[margem_lucro], quantidade, recorrencia, tipo, tipo_usuario)
    
    df_precos = pd.DataFrame(detalhes_precos, columns=['Descrição', 'Preço (R$)'])
    st.table(df_precos)
