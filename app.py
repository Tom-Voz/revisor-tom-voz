import streamlit as st
import requests
import json

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Manual resumido
MANUAL = """
Voz: Simples, resolutiva, respeitosa.
Regras:
- Use "você" em vez de "o cidadão"
- Use "pagar" em vez de "efetuar pagamento"
- Use "pelo" em vez de "através de"
- Use "todo mês" em vez de "mensalmente"
- Frases curtas e diretas
- Seja acolhedor quando necessário
"""

# Pegar chave dos secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Configure a chave API em Settings → Secrets")
    st.stop()

# URL correta da API
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

def chamar_gemini(prompt):
    """Chama a API do Gemini"""
    headers = {"Content-Type": "application/json"}
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
        return None

st.info("✅ Sistema pronto. Digite um texto para revisar ou criar.")

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto = st.text_area("Texto para revisar:", height=150)
    
    if st.button("Revisar", type="primary"):
        if texto:
            with st.spinner("Revisando com IA..."):
                prompt = f"""
                Você é um revisor do Governo de São Paulo.
                
                Siga estas regras:
                {MANUAL}
                
                Texto original: {texto}
                
                TAREFA: Revise o texto seguindo as regras. 
                Mantenha o sentido original.
                Responda APENAS com o texto revisado.
                """
                resultado = chamar_gemini(prompt)
                
                if resultado:
                    st.markdown("**Original**")
                    st.info(texto)
                    st.markdown("**Revisado**")
                    st.success(resultado)
                else:
                    st.error("Erro na API. Verifique sua chave.")
        else:
            st.warning("Digite um texto")

with aba2:
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    if st.button("Criar", type="primary"):
        if assunto:
            with st.spinner("Criando com IA..."):
                prompt = f"""
                Você é um redator do Governo de São Paulo.
                
                Regras: {MANUAL}
                
                Crie um texto sobre: {assunto}
                Tom: {tom}
                Público: Cidadãos de São Paulo
                
                Responda APENAS com o texto criado.
                """
                resultado = chamar_gemini(prompt)
                
                if resultado:
                    st.markdown("**Texto criado**")
                    st.success(resultado)
                else:
                    st.error("Erro na API. Verifique sua chave.")
        else:
            st.warning("Digite o assunto")
