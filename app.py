import streamlit as st
import requests
import json

# Configurar a página
st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Manual de tom e voz
MANUAL = """
Voz do Governo de SP:
- Simples: usar linguagem clara, sem termos técnicos desnecessários
- Resolutiva: focar em resolver problemas e dar respostas práticas
- Respeitosa: tratar todas as pessoas com educação, sem informalidade excessiva

Tom (varia conforme situação):
- Informativo: objetivo, com dados claros
- Empático: acolhedor, especialmente em situações difíceis
- Motivador: para engajar em eventos ou programas

Regras práticas:
- Use "você" para se dirigir ao leitor
- Prefira frases curtas
- Evite siglas sem explicação
"""

# Pegar a chave API
API_KEY = st.secrets["GEMINI_API_KEY"]
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

def chamar_gemini(prompt):
    """Função para chamar a API do Gemini"""
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        resultado = response.json()
        return resultado["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Erro: {response.status_code} - {response.text}"

# Abas
aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    st.subheader("Revisão de Conteúdo")
    texto_original = st.text_area("Texto para revisar:", height=200)
    
    if st.button("Revisar Texto", type="primary"):
        if texto_original:
            with st.spinner("Revisando..."):
                prompt = f"""
                Você é um revisor do Governo de SP.
                
                MANUAL:
                {MANUAL}
                
                Revise este texto seguindo as regras acima. 
                Deixe mais simples, use "você", e seja direto.
                
                TEXTO: {texto_original}
                
                Responda apenas com o texto revisado.
                """
                resultado = chamar_gemini(prompt)
                st.markdown("### 📄 Texto Revisado")
                st.write(resultado)
        else:
            st.warning("Digite um texto.")

with aba2:
    st.subheader("Criação de Conteúdo")
    
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador"])
    
    if st.button("Criar Conteúdo", type="primary"):
        if assunto:
            with st.spinner("Criando..."):
                prompt = f"""
                Você é um redator do Governo de SP.
                
                MANUAL: {MANUAL}
                
                Crie um conteúdo sobre: {assunto}
                Tom: {tom}
                Use linguagem simples e direta.
                
                Responda apenas com o texto criado.
                """
                resultado = chamar_gemini(prompt)
                st.markdown("### ✨ Conteúdo Criado")
                st.write(resultado)
        else:
            st.warning("Digite o assunto.")
