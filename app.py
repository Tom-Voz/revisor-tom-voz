import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

MANUAL = """
Voz do Governo de SP:
- Simples: linguagem clara, sem termos técnicos
- Resolutiva: foco em resolver problemas
- Respeitosa: tratar todos com educação

Regras:
- Use "você"
- Frases curtas
- Evite siglas
"""

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Listar modelos disponíveis para descobrir qual funciona
    modelos = genai.list_models()
    modelo_usado = None
    
    for m in modelos:
        if 'generateContent' in m.supported_generation_methods:
            modelo_usado = m.name
            break
    
    if modelo_usado:
        st.success(f"✅ Usando modelo: {modelo_usado}")
        model = genai.GenerativeModel(modelo_usado)
    else:
        st.error("Nenhum modelo disponível")
        st.stop()
        
except Exception as e:
    st.error(f"Erro: {e}")
    st.info("Verifique sua chave API em Settings → Secrets")
    st.stop()

aba1, aba2 = st.tabs(["✏️ Revisar", "✨ Criar"])

with aba1:
    texto = st.text_area("Texto para revisar:", height=150)
    if st.button("Revisar"):
        if texto:
            with st.spinner("Revisando..."):
                prompt = f"Siga estas regras: {MANUAL}\n\nRevise este texto: {texto}\n\nResponda apenas com o texto revisado."
                resposta = model.generate_content(prompt)
                st.write(resposta.text)

with aba2:
    assunto = st.text_input("Assunto:")
    tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador"])
    if st.button("Criar"):
        if assunto:
            with st.spinner("Criando..."):
                prompt = f"Regras: {MANUAL}\nTom: {tom}\n\nCrie um texto sobre: {assunto}"
                resposta = model.generate_content(prompt)
                st.write(resposta.text)
