import streamlit as st

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Validador de Convergência",
    layout="centered"
)

def extrair_ativos(texto):
    """
    Limpa o texto colado (remove espaços, vírgulas, quebras de linha)
    e retorna um conjunto de ativos únicos.
    """
    if not texto:
        return set()
    
    # Substitui vírgulas e quebras de linha por espaços
    limpo = texto.replace(",", " ").replace("\n", " ")
    # Divide e limpa cada item
    lista = [ativo.strip().upper() for ativo in limpo.split(" ") if ativo.strip()]
    return set(lista)

def executar():
    st.title("🎯 Validador de Convergência")
    st.write("Identifique quais ativos estão presentes em dois scanners ao mesmo tempo.")

    # Área de entrada
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Lista Scanner 1")
        txt_1 = st.text_area("Cole os ativos do Setup A:", height=200, placeholder="Ex: PETR4, VALE3, ITUB4")

    with col2:
        st.subheader("Lista Scanner 2")
        txt_2 = st.text_area("Cole os ativos do Setup B:", height=200, placeholder="Ex: PETR4, ABEV3, VALE3")

    st.divider()

    # Botão de processamento
    if st.button("🔥 Comparar Listas", use_container_width=True):
        set_1 = extrair_ativos(txt_1)
        set_2 = extrair_ativos(txt_2)

        # Intersecção: o que existe em ambos
        comuns = sorted(list(set_1.intersection(set_2)))

        if comuns:
            st.success(f"✅ Encontrado(s) **{len(comuns)}** ativo(s) em comum!")
            
            # Exibe os ativos em 'cards' visuais
            cols = st.columns(5)
            for idx, ativo in enumerate(comuns):
                cols[idx % 5].info(f"**{ativo}**")
            
            st.write("---")
            st.subheader("📋 Lista para Copiar:")
            st.code(", ".join(comuns))
        else:
            if not txt_1 or not txt_2:
                st.info("Aguardando a colagem das duas listas para comparar...")
            else:
                st.warning("⚠️ Nenhum ativo em comum foi encontrado entre as duas listas.")

if __name__ == "__main__":
    executar()
