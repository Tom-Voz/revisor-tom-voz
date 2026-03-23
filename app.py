import streamlit as st
import requests

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Manual de tom e voz
MANUAL = """
Você é um especialista em comunicação do Governo de São Paulo.

Nossa voz:
- Simples: linguagem clara, frases curtas, só o necessário
- Prestativa: proativa, resolve problemas, acolhedora
- Confiável: informações corretas, sem ambiguidades

Regras:
- Use "você" em vez de "o cidadão"
- Use "pagar" em vez de "efetuar pagamento"
- Use "pelo" em vez de "através de"
- Use "todo mês" em vez de "mensalmente"
- Frases curtas e diretas
- Seja acolhedor quando apropriado
"""

# Pegar chave do Groq
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("Configure a chave API GROQ_API_KEY em Settings → Secrets")
    st.stop()

# URL da API Groq (OpenAI-compatible)
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def chamar_groq(prompt):
    """Chama a API do Groq"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": MANUAL},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            resultado = response.json()
            return resultado["choices"][0]["message"]["content"]
        else:
            st.error(f"Erro {response.status_code}: {response.text[:200]}")
            return None
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# Teste rápido
with st.spinner("Verificando conexão..."):
    teste = chamar_groq("Diga apenas: OK")
    if teste:
        st.success("✅ Conectado ao Groq (Llama 3.3 70B)!")
    else:
        st.error("❌ Falha na conexão. Verifique sua chave.")

st.divider()

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto = st.text_area("Texto para revisar:", height=150)
    
    if st.button("Revisar", type="primary"):
        if texto:
            with st.spinner("Revisando com IA..."):
                prompt = f"Revise este texto seguindo as regras. Mantenha o sentido original. Responda APENAS com o texto revisado.\n\nTEXTO: {texto}"
                resultado = chamar_groq(prompt)
                if resultado:
                    st.markdown("**Original**")
                    st.info(texto)
                    st.markdown("**Revisado**")
                    st.success(resultado)
        else:
            st.warning("Digite um texto")

with aba2:
    assunto = st.text_input("Assunto:")
    tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    if st.button("Criar", type="primary"):
        if assunto:
            with st.spinner("Criando com IA..."):
                prompt = f"Crie um texto sobre: {assunto}. Tom: {tom}. Público: Cidadãos de São Paulo. Responda APENAS com o texto criado."
                resultado = chamar_groq(prompt)
                if resultado:
                    st.markdown("**Texto criado**")
                    st.success(resultado)
        else:
            st.warning("Digite o assunto")

st.divider()
st.caption("📌 IA: Groq (Llama 3.3 70B) | Gratuito | 1.000 requisições/dia")
