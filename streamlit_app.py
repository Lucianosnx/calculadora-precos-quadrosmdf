import streamlit as st
import pandas as pd

def calcular_preco(largura_cm, altura_cm, multiplicador, mackup, margem_lucro, quantidade, recorrencia, tipo, tipo_usuario):
    area = largura_cm * altura_cm
    area_referencia = 35 * 31
    custo_materia_prima = (area * 8) / area_referencia
    
    detalhes_precos = []

    detalhes_precos.append(('Custo Matéria Prima', custo_materia_prima))

    preco_multiplicado = custo_materia_prima * multiplicador
    preco_mackup = preco_multiplicado * mackup

    detalhes_precos.append(('Preço após Multiplicador', preco_multiplicado))
    detalhes_precos.append(('Preço após Mackup', preco_mackup))

    preco_final = preco_mackup * margem_lucro
    detalhes_precos.append(('Preço após Margem de Lucro', preco_final))

    taxa_erro = 1.03
    preco_erro = preco_final * taxa_erro
    detalhes_precos.append(('Preço após Taxa de Erro (3%)', preco_erro))
    
    custo_aquisicao = 1.17
    preco_aquisicao = preco_erro * custo_aquisicao
    detalhes_precos.append(('Preço após Custo de Aquisição (17%)', preco_aquisicao))

    if tipo == 'Serviço':
        preco_aquisicao *= 2  # Aplicar taxa de serviço
        detalhes_precos.append(('Preço após Taxa de Serviço', preco_aquisicao))

        if quantidade == 1:
            desconto_qtd = 1
            desconto_texto = "0%"
        elif quantidade > 1 and quantidade < 10:
            desconto_qtd = 1
            desconto_texto = "0%"
        elif quantidade >= 10 and quantidade < 50:
            desconto_qtd = 0.95 if tipo_usuario == 'Consumidor' else 0.9
            desconto_texto = "5%" if tipo_usuario == 'Consumidor' else "10%"
        elif quantidade >= 50 and quantidade < 100:
            desconto_qtd = 0.9 if tipo_usuario == 'Consumidor' else 0.8
            desconto_texto = "10%" if tipo_usuario == 'Consumidor' else "20%"
        elif quantidade >= 100:
            desconto_qtd = 0.85 if tipo_usuario == 'Consumidor' else 0.7
            desconto_texto = "15%" if tipo_usuario == 'Consumidor' else "30%"
        
        preco_quantidade = preco_aquisicao * desconto_qtd
        detalhes_precos.append(('Preço após Desconto de Quantidade', preco_quantidade))
        
        preco_recorrencia = preco_quantidade
        if recorrencia > 0:
            desconto_recorrencia = 1 - (recorrencia * 0.05) if tipo_usuario == 'Consumidor' else 1 - (recorrencia * 0.1)
            preco_recorrencia = preco_quantidade * desconto_recorrencia
            detalhes_precos.append(('Preço após Desconto de Recorrência', preco_recorrencia))
        
        preco_final = preco_recorrencia if recorrencia > 0 else preco_quantidade
    else:
        preco_final = preco_aquisicao

    preco_total = preco_final * (quantidade if tipo == 'Serviço' else 1)
    if quantidade > 1 and tipo == 'Serviço':
        detalhes_precos.append(('Preço Unitário', preco_final))
        detalhes_precos.append(('Preço Final Total', preco_total))
    else:
        detalhes_precos.append(('Preço Final', preco_total))

    return detalhes_precos, desconto_texto

st.title('Calculadora de Preços QuadrosMDF')

largura_cm = st.number_input('Largura do quadro (em centímetros):', min_value=0.0, format="%.2f")
altura_cm = st.number_input('Altura do quadro (em centímetros):', min_value=0.0, format="%.2f")

multiplicadores = {1: 1, 2: 2, 3: 3, 4: 4}
multiplicador = st.selectbox('Multiplicador do preço base:', options=list(multiplicadores.keys()))

opcoes_mackup = {1: 1.05, 2: 1.10, 3: 1.15, 4: 1.20}
mackup = st.selectbox('Mackup do design (1 a 4):', options=list(opcoes_mackup.keys()), format_func=lambda x: f"{x} - {opcoes_mackup[x]*100-100:.0f}%")

opcoes_lucro = {1: 1.05, 2: 1.10, 3: 1.20, 4: 1.30}
margem_lucro = st.selectbox('Margem de lucro:', options=list(opcoes_lucro.keys()), format_func=lambda x: f"{x} - {opcoes_lucro[x]*100-100:.0f}%")

tipo = st.selectbox('Tipo:', ('Produto', 'Serviço'))

tipo_usuario = 'Empresa'
quantidade = 1
recorrencia = 0

if tipo == 'Serviço':
    tipo_usuario = st.radio('Tipo de usuário:', ('Consumidor', 'Empresa'))
    
    quantidade = st.number_input('Quantidade:', min_value=1, format="%d")
    
    if quantidade == 1:
        desconto_texto = "0%"
    elif quantidade > 1 and quantidade < 10:
        desconto_texto = "0%"
    elif quantidade >= 10 and quantidade < 50:
        desconto_texto = "5%" if tipo_usuario == 'Consumidor' else "10%"
    elif quantidade >= 50 and quantidade < 100:
        desconto_texto = "10%" if tipo_usuario == 'Consumidor' else "20%"
    elif quantidade >= 100:
        desconto_texto = "15%" if tipo_usuario == 'Consumidor' else "30%"
    
    st.write(f'Desconto aplicado para a quantidade escolhida: {desconto_texto}')
    
    descontos_recorrencia_display = {i: f"{(i * 5 if tipo_usuario == 'Consumidor' else i * 10)}%" for i in range(6)}
    recorrencia = st.selectbox('Recorrência:', options=list(descontos_recorrencia_display.keys()), format_func=lambda x: f"{x} ({descontos_recorrencia_display[x]})")

if largura_cm and altura_cm:
    detalhes_precos, desconto_texto = calcular_preco(largura_cm, altura_cm, multiplicadores[multiplicador], opcoes_mackup[mackup], opcoes_lucro[margem_lucro], quantidade, recorrencia, tipo, tipo_usuario)
    
    df_precos = pd.DataFrame(detalhes_precos, columns=['Descrição', 'Preço (R$)'])
    st.table(df_precos)
