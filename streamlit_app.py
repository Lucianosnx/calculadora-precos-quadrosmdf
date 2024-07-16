import streamlit as st
import pandas as pd

def calcular_preco(largura_cm, altura_cm, multiplicador, mackup, margem_lucro, quantidade, recorrencia, tipo, tipo_usuario):
    area = largura_cm * altura_cm
    area_referencia = 35 * 31
    custo_materia_prima = (area * 8) / area_referencia
    
    detalhes_precos = []

    detalhes_precos.append(('Custo Matéria Prima', f"{custo_materia_prima:.2f}"))

    preco_multiplicado = custo_materia_prima * multiplicador
    diferenca_multiplicador = preco_multiplicado - custo_materia_prima
    detalhes_precos.append(('Multiplicador', f"+ {diferenca_multiplicador:.2f}  (R$ {preco_multiplicado:.2f})"))

    preco_mackup = preco_multiplicado * mackup
    diferenca_mackup = preco_mackup - preco_multiplicado
    detalhes_precos.append(('Mackup', f"+ {diferenca_mackup:.2f}  (R$ {preco_mackup:.2f})"))

    preco_final = preco_mackup * margem_lucro
    diferenca_lucro = preco_final - preco_mackup
    detalhes_precos.append(('Margem de Lucro', f"+ {diferenca_lucro:.2f}  (R$ {preco_final:.2f})"))

    taxa_erro = 1.03
    preco_erro = preco_final * taxa_erro
    diferenca_erro = preco_erro - preco_final
    detalhes_precos.append(('Taxa de Erro (3%)', f"+ {diferenca_erro:.2f}  (R$ {preco_erro:.2f})"))
    
    custo_aquisicao = 1.17
    preco_aquisicao = preco_erro * custo_aquisicao
    diferenca_aquisicao = preco_aquisicao - preco_erro
    detalhes_precos.append(('Custo de Aquisição (17%)', f"+ {diferenca_aquisicao:.2f}  (R$ {preco_aquisicao:.2f})"))

    desconto_texto = "0%"  # Inicialização padrão

    if tipo == 'Serviço':
        preco_anterior = preco_aquisicao
        preco_aquisicao *= 2  # Aplicar taxa de serviço
        diferenca_servico = preco_aquisicao - preco_anterior
        detalhes_precos.append(('Taxa de Serviço', f"+ {diferenca_servico:.2f}  (R$ {preco_aquisicao:.2f})"))

        preco_recorrencia = preco_aquisicao
        if recorrencia > 0:
            desconto_recorrencia = 1 - (recorrencia * 0.05) if tipo_usuario == 'Consumidor' else 1 - (recorrencia * 0.1)
            preco_recorrencia = preco_aquisicao * desconto_recorrencia
            diferenca_recorrencia = preco_recorrencia - preco_aquisicao
            detalhes_precos.append(('Desconto de Recorrência', f"- {abs(diferenca_recorrencia):.2f}  (R$ {preco_recorrencia:.2f})"))
        preco_final = preco_recorrencia

    else:
        preco_final = preco_aquisicao

    preco_total = preco_final
    if quantidade >= 1:
        if quantidade > 1 and quantidade < 10:
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
        
        preco_total_com_desconto = preco_total * desconto_qtd
        diferenca_quantidade = preco_total_com_desconto - preco_total
        detalhes_precos.append(('Desconto de Quantidade', f"- {abs(diferenca_quantidade):.2f}  (R$ {preco_total_com_desconto:.2f})"))
        preco_total = preco_total_com_desconto

    return detalhes_precos, desconto_texto, preco_total

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
    
    if quantidade >= 1 and quantidade < 10:
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
    detalhes_precos, desconto_texto, preco_total = calcular_preco(largura_cm, altura_cm, multiplicadores[multiplicador], opcoes_mackup[mackup], opcoes_lucro[margem_lucro], quantidade, recorrencia, tipo, tipo_usuario)
    
    df_precos = pd.DataFrame(detalhes_precos, columns=['Descrição', 'Preço (R$)'])
    st.table(df_precos)
    st.write(f"Preço Total: R$ {preco_total:.2f}")
