import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor de Tom e Voz")
st.caption("Manual do Governo de SP")

# Manual resumido
MANUAL = """
Regras:
- Use linguagem simples e clara
- Use "você" para se dirigir ao leitor
- Seja direto e resolutivo
- Trate com respeito (mas sem formalidade excessiva)
"""

st.write("### ✅ Status da conexão")

try:
    # Pegar chave
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Tentar modelo
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        test = model.generate_content("Diga OK")
        st.success("✅ Conectado com gemini-1.5-flash")
    except:
        try:
            model = genai.GenerativeModel('gemini-pro')
            test = model.generate_content("Diga OK")
            st.success("✅ Conectado com gemini-pro")
        except:
            st.error("❌ Nenhum modelo disponível")
            st.stop()
            
except Exception as e:
    st.error(f"Erro: {e}")
    st.stop()

st.divider()

# Interface simples
opcao = st.radio("Escolha:", ["Revisar texto", "Criar texto"])

if opcao == "Revisar texto":
    texto = st.text_area("Texto original:", height=150)
    if st.button("Revisar"):
        if texto:
            with st.spinner("Revisando..."):
                prompt = f"{MANUAL}\n\nRevise este texto seguindo as regras acima:\n{texto}"
                resposta = model.generate_content(prompt)
                st.write("### Texto revisado:")
                st.write(resposta.text)

else:
    assunto = st.text_input("Assunto do texto:")
    if st.button("Criar"):
        if assunto:
            with st.spinner("Criando..."):
                prompt = f"{MANUAL}\n\nCrie um texto sobre: {assunto}"
                resposta = model.generate_content(prompt)
                st.write("### Texto criado:")
                st.write(resposta.text)
