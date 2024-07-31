import streamlit as st
import pandas as pd

def calcular_preco(largura_cm, altura_cm, multiplicador, mackup, margem_lucro, quantidade, recorrencia, tipo, tipo_usuario):
    area = largura_cm * altura_cm
    area_referencia = 35 * 31
    custo_materia_prima = round((area * 8) / area_referencia, 2)
    
    detalhes_precos = []

    detalhes_precos.append(('Custo Matéria Prima', f"{custo_materia_prima:.2f}"))

    preco_mackup = round(custo_materia_prima * mackup, 2)
    diferenca_mackup = round(preco_mackup - custo_materia_prima, 2)
    detalhes_precos.append(('Mackup', f"+ {diferenca_mackup:.2f}"))

    preco_final = round(preco_mackup * margem_lucro, 2)
    diferenca_lucro = round(preco_final - preco_mackup, 2)
    detalhes_precos.append(('Margem de Lucro', f"+ {diferenca_lucro:.2f}"))

    taxa_erro = 1.03
    preco_erro = round(preco_final * taxa_erro, 2)
    diferenca_erro = round(preco_erro - preco_final, 2)
    detalhes_precos.append(('Taxa de Erro (3%)', f"+ {diferenca_erro:.2f}"))
    
    custo_aquisicao = 1.17
    preco_aquisicao = round(preco_erro * custo_aquisicao, 2)
    diferenca_aquisicao = round(preco_aquisicao - preco_erro, 2)
    detalhes_precos.append(('Custo de Aquisição (17%)', f"+ {diferenca_aquisicao:.2f}"))

    desconto_texto = "0%"

    if tipo == 'Serviço':
        preco_anterior = preco_aquisicao
        preco_aquisicao = round(preco_aquisicao * 2, 2)  #taxa de serviço
        diferenca_servico = round(preco_aquisicao - preco_anterior, 2)
        detalhes_precos.append(('Taxa de Serviço (+100%)', f"+ {diferenca_servico:.2f}"))

        preco_anterior = preco_aquisicao
        taxa_nota_fiscal = 1.04
        preco_aquisicao = round(preco_aquisicao * taxa_nota_fiscal, 2)  #taxa de nota fiscal
        diferenca_nota_fiscal = round(preco_aquisicao - preco_anterior, 2)
        detalhes_precos.append(('Taxa da Nota Fiscal (4%)', f"+ {diferenca_nota_fiscal:.2f}"))

        preco_recorrencia = preco_aquisicao
        if recorrencia > 0:
            desconto_recorrencia = 1 - (recorrencia * 0.05) if tipo_usuario == 'Consumidor' else 1 - (recorrencia * 0.1)
            preco_recorrencia = round(preco_aquisicao * desconto_recorrencia, 2)
            diferenca_recorrencia = round(preco_recorrencia - preco_aquisicao, 2)
            detalhes_precos.append(('Desconto de Recorrência', f"- {abs(diferenca_recorrencia):.2f}"))
        preco_final = preco_recorrencia

    else:
        preco_final = preco_aquisicao

    if tipo == 'Produto' and preco_final < 70:
        diferenca_ajuste = 7
        preco_final += diferenca_ajuste
        detalhes_precos.append(('Ajuste de Preço (Abaixo de R$70)', f"+ {diferenca_ajuste:.2f}"))

    preco_final = round(preco_final * multiplicador, 2)
    diferenca_multiplicador = round(preco_final - preco_aquisicao, 2)
    detalhes_precos.append(('Quantidade', f"+ {diferenca_multiplicador:.2f}"))

    preco_total = preco_final
    desconto_qtd = 1
    if quantidade > 1:
        if quantidade >= 10 and quantidade < 50:
            desconto_qtd = 0.95 if tipo_usuario == 'Consumidor' else 0.9
            desconto_texto = "5%" if tipo_usuario == 'Consumidor' else "10%"
        elif quantidade >= 50 and quantidade < 100:
            desconto_qtd = 0.9 if tipo_usuario == 'Consumidor' else 0.8
            desconto_texto = "10%" if tipo_usuario == 'Consumidor' else "20%"
        elif quantidade >= 100:
            desconto_qtd = 0.85 if tipo_usuario == 'Consumidor' else 0.7
            desconto_texto = "15%" if tipo_usuario == 'Consumidor' else "30%"
        
        preco_unitario_com_desconto = round(preco_total * desconto_qtd, 2)
        diferenca_quantidade = round(preco_unitario_com_desconto - preco_total, 2)
        detalhes_precos.append(('Desconto de Quantidade', f"- {abs(diferenca_quantidade):.2f}"))
        preco_total = round(preco_unitario_com_desconto * quantidade, 2)
        detalhes_precos.append(('Preço Unitário', f"{preco_unitario_com_desconto:.2f}"))
        detalhes_precos.append((f'Quantidade', f"{quantidade}"))
    
    detalhes_precos.append(('Preço Total', f"{preco_total:.2f}"))

    return detalhes_precos, desconto_texto

st.title('Calculadora de Preços QuadrosMDF')

largura_cm = st.number_input('Largura do quadro (em centímetros):', min_value=0.0, format="%.2f")
altura_cm = st.number_input('Altura do quadro (em centímetros):', min_value=0.0, format="%.2f")

multiplicadores = {1: 1, 2: 2, 3: 3, 4: 4}
multiplicador = st.selectbox('Quantidade:', options=list(multiplicadores.keys()))

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
    
    if quantidade >= 1 and quantidade < 10:
        desconto_texto = "0%"
    elif quantidade >= 10 and quantidade < 50:
        desconto_texto = "5%" if tipo_usuario == 'Consumidor' else "10%"
    elif quantidade >= 50 e quantidade < 100:
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
