import streamlit as st
import requests
import json

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Verificar se a chave existe
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    st.success("✅ Chave API encontrada")
except:
    st.error("❌ Configure a chave API em Settings → Secrets")
    st.stop()

# Usar o endpoint correto da API
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def chamar_gemini(prompt):
    """Chama a API do Gemini"""
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            resultado = response.json()
            return resultado["candidates"][0]["content"]["parts"][0]["text"]
        else:
            st.error(f"Erro {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

# Interface
st.markdown("### 📖 Revisor e Criador de Conteúdo")

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto = st.text_area("Texto para revisar:", height=150, 
                         placeholder="Ex: Acesse o portal Poupatempo e digite Consulta de matrícula na barra de busca e siga as orientações")
    
    if st.button("Revisar", type="primary"):
        if texto:
            with st.spinner("Revisando com IA..."):
                prompt = f"""
                Você é um revisor de conteúdo do Governo de São Paulo.
                
                Siga estas regras:
                - Use linguagem simples e direta
                - Substitua "o cidadão" por "você"
                - Use "pagar" em vez de "efetuar pagamento"
                - Use "pelo" em vez de "através de"
                - Use "todo mês" em vez de "mensalmente"
                - Frases curtas e objetivas
                - Mantenha emojis se forem apropriados
                
                Texto original: {texto}
                
                Responda APENAS com o texto revisado.
                """
                resultado = chamar_gemini(prompt)
                if resultado:
                    st.markdown("**📄 Original**")
                    st.info(texto)
                    st.markdown("**✅ Revisado**")
                    st.success(resultado)
        else:
            st.warning("Digite um texto para revisar")

with aba2:
    assunto = st.text_input("Assunto:", placeholder="Ex: Consulta de matrícula Poupatempo")
    tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    if st.button("Criar", type="primary"):
        if assunto:
            with st.spinner("Criando com IA..."):
                prompt = f"""
                Você é um redator do Governo de São Paulo.
                
                Crie um texto sobre: {assunto}
                Tom: {tom}
                
                Regras:
                - Use linguagem simples e direta
                - Use "você" para se dirigir ao leitor
                - Seja claro e objetivo
                - Frases curtas
                
                Responda APENAS com o texto criado.
                """
                resultado = chamar_gemini(prompt)
                if resultado:
                    st.markdown("**✨ Texto criado**")
                    st.success(resultado)
        else:
            st.warning("Digite o assunto")

st.divider()
st.caption("📌 Manual oficial: cms.sp.gov.br/cms/tomevoz")
