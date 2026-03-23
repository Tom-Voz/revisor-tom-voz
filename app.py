import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Manual oficial
MANUAL = """
Voz: Simples, resolutiva, respeitosa.
Tom: Varia conforme contexto (informativo, empático, motivador, direto).
Regras:
- Use "você" para se dirigir ao leitor
- Frases curtas e diretas
- Evite termos técnicos e burocráticos
- Seja claro e objetivo
"""

# Configurar Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.success("✅ Conectado ao Gemini")
except Exception as e:
    st.error(f"Erro: {e}")
    st.stop()

opcao = st.radio("Funcionalidade:", ["✏️ Revisar texto", "✨ Criar texto"], horizontal=True)

if opcao == "✏️ Revisar texto":
    st.subheader("Revisão de Conteúdo")
    texto = st.text_area("Texto para revisar:", height=150)
    
    if st.button("Revisar", type="primary"):
        if texto:
            with st.spinner("Revisando com IA..."):
                prompt = f"""
                Você é um revisor do Governo de São Paulo.
                
                MANUAL:
                {MANUAL}
                
                TEXTO ORIGINAL:
                {texto}
                
                TAREFA: Revise o texto seguindo o manual.
                Mantenha o sentido original, apenas melhore a linguagem.
                Responda APENAS com o texto revisado, sem explicações.
                """
                resposta = model.generate_content(prompt)
                st.markdown("### ✅ Texto revisado")
                st.success(resposta.text)
        else:
            st.warning("Digite um texto")

else:
    st.subheader("Criação de Conteúdo")
    
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: Prazo do IPTU")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    publico = st.text_input("Público-alvo:", placeholder="Ex: Contribuintes")
    
    if st.button("Criar", type="primary"):
        if assunto:
            with st.spinner("Criando com IA..."):
                prompt = f"""
                Você é um redator do Governo de São Paulo.
                
                MANUAL:
                {MANUAL}
                
                Crie um texto sobre: {assunto}
                Tom: {tom}
                Público: {publico if publico else "Cidadãos"}
                
                O texto deve ser natural, como se um humano escrevesse.
                Responda APENAS com o texto criado.
                """
                resposta = model.generate_content(prompt)
                st.markdown("### ✨ Texto criado")
                st.success(resposta.text)
        else:
            st.warning("Digite o assunto")
