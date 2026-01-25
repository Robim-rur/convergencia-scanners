import streamlit as st
import pandas as pd

def processar_compras(listas_dict):
    """
    Analisa as listas focando em convergência de compra e volume.
    """
    # Filtra apenas listas que possuem conteúdo
    listas_ativas = {k: set(v) for k, v in listas_dict.items() if v}
    
    if len(listas_ativas) < 2:
        return None, None, len(listas_ativas)

    sets = list(listas_ativas.values())
    nomes = list(listas_ativas.keys())

    # 1. Interseção Total (O que comprar de todos os fornecedores/listas)
    intersecao_total = set.intersection(*sets)

    # 2. Análise de Frequência (Para identificar volume de compra)
    todos_itens = set().union(*sets)
    contagem = []
    for item in todos_itens:
        frequencia = sum(1 for s in sets if item in s)
        if frequencia >= 2:
            # Identifica em quais listas o item aparece
            onde_aparece = [nome for nome, conteudo in listas_ativas.items() if item in conteudo]
            contagem.append({
                "Item": item, 
                "Frequência": frequencia,
                "Origens": ", ".join(onde_aparece)
            })
    
    df_frequencia = pd.DataFrame(contagem).sort_values(by="Frequência", ascending=False)
    
    return intersecao_total, df_frequencia, len(listas_ativas)

# --- INTERFACE ---
st.set_page_config(page_title="Comparador Buy Side 6x", layout="wide")

st.title("🛒 Comparador de Suprimentos (Até 6 Listas)")
st.subheader("Focado em identificação de volume e convergência")

# Organização das entradas em 2 linhas e 3 colunas
col_config = [st.columns(3), st.columns(3)]
listas_input = {}

contador = 1
for linha in col_config:
    for col in linha:
        with col:
            nome_lista = st.text_input(f"Identificador da Lista {contador}", f"Fornecedor/Lista {contador}")
            conteudo = st.text_area(f"Itens (um por linha)", height=150, key=f"area_{contador}")
            # Limpeza dos dados
            listas_input[nome_lista] = [line.strip().upper() for line in conteudo.split('\n') if line.strip()]
            contador += 1

st.divider()

if st.button("📊 ANALISAR LISTAS DE COMPRA"):
    comuns, df_freq, total_ativas = processar_compras(listas_input)
    
    if total_ativas < 2:
        st.error("⚠️ Insira pelo menos 2 listas para realizar a comparação.")
    else:
        tab1, tab2 = st.tabs(["🎯 Itens em Comum (Todas)", "📈 Análise de Volume (2 ou +)"])
        
        with tab1:
            if comuns:
                st.success(f"Encontrados {len(comuns)} itens presentes em TODAS as {total_ativas} listas.")
                st.write(list(comuns))
            else:
                st.info("Não há itens comuns a todas as listas simultaneamente.")
                
        with tab2:
            if not df_freq.empty:
                st.write("Itens recorrentes encontrados em múltiplas origens:")
                st.dataframe(df_freq, use_container_width=True, hide_index=True)
                
                # Botão de exportação focado em relatório de compra
                csv = df_freq.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Baixar Relatório de Oportunidade de Volume", csv, "compras_recorrentes.csv", "text/csv")
            else:
                st.warning("Nenhum item se repete entre as listas analisadas.")
